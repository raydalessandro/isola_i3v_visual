"""
flux_image_gen.py — Modulo standalone per generazione immagini via Flux (fal.ai).

Provider disponibili:
    flux-schnell        $0.015/img  ~2s   bozze veloci (no reference image)
    flux-pro            $0.04/img   ~5s   produzione (no reference image)
    flux-kontext-pro    $0.04/img   ~5s   character consistency nativa
    flux-kontext-max    $0.08/img   ~8s   massima qualità + consistency

Flux Kontext è il tier raccomandato per libri illustrati:
mantiene coerenza dei personaggi tra tavole senza trucchi prompt.

Env vars richieste:
    FAL_KEY — chiave API fal.ai (https://fal.ai)

Uso minimo:
    from flux_image_gen import generate_image
    generate_image("a watercolor fox in the forest", output_path="fox.png")
"""

from __future__ import annotations

import base64
import json
import os
import time
from pathlib import Path
from typing import Optional, Union


# ---------------------------------------------------------------------------
# Modelli fal.ai
# ---------------------------------------------------------------------------

_FAL_MODELS: dict[str, str] = {
    "flux-schnell":      "fal-ai/flux/schnell",
    "flux-pro":          "fal-ai/flux-pro/v1.1",
    "flux-kontext-pro":  "fal-ai/flux-pro/kontext",
    "flux-kontext-max":  "fal-ai/flux-pro/kontext/max",
}

_COSTS_USD: dict[str, float] = {
    "flux-schnell":      0.015,
    "flux-pro":          0.040,
    "flux-kontext-pro":  0.040,
    "flux-kontext-max":  0.080,
}

_SUPPORTS_REFERENCE: set[str] = {"flux-kontext-pro", "flux-kontext-max"}

DEFAULT_TIER = "flux-kontext-pro"


# ---------------------------------------------------------------------------
# Risultato
# ---------------------------------------------------------------------------

class GenerationResult:
    """Contiene i bytes dell'immagine generata e metadata."""

    def __init__(
        self,
        image_bytes: bytes,
        provider: str,
        model: str,
        cost_usd: float,
        seed: Optional[int] = None,
    ):
        self.image_bytes = image_bytes
        self.provider = provider
        self.model = model
        self.cost_usd = cost_usd
        self.seed = seed

    def save(self, path: Union[str, Path]) -> Path:
        """Salva l'immagine su disco e ritorna il path."""
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(self.image_bytes)
        return out

    def __repr__(self) -> str:
        return (
            f"GenerationResult(model={self.model!r}, "
            f"cost=${self.cost_usd:.3f}, "
            f"size={len(self.image_bytes)//1024}KB)"
        )


# ---------------------------------------------------------------------------
# Helpers interni
# ---------------------------------------------------------------------------

def _get_api_key() -> str:
    key = os.getenv("FAL_KEY")
    if not key:
        raise RuntimeError(
            "FAL_KEY non trovata. Setta la variabile d'ambiente "
            "o crea un file .env con FAL_KEY=<tua_chiave>."
        )
    return key


def _parse_size(size: str) -> dict:
    """Converte '1024x1536' → {image_size: {width, height}}."""
    parts = size.split("x")
    if len(parts) == 2:
        try:
            return {"image_size": {"width": int(parts[0]), "height": int(parts[1])}}
        except ValueError:
            pass
    # Aspect ratio string (es. "portrait_4_3")
    return {"image_size": size}


def _upload_reference(image_path: Union[str, Path]) -> str:
    """Carica l'immagine su fal.ai e ritorna l'URL per image_url."""
    import fal_client
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Reference image non trovata: {path}")
    return fal_client.upload_file(str(path))


def _call_fal(
    model_id: str,
    arguments: dict,
    max_retries: int = 3,
    retry_delay: float = 5.0,
) -> bytes:
    """
    Chiama fal.ai con retry su rate limit / timeout.
    Ritorna i bytes dell'immagine.
    """
    import fal_client
    import httpx

    last_exc: Optional[Exception] = None

    for attempt in range(max_retries):
        try:
            result = fal_client.subscribe(
                model_id,
                arguments=arguments,
                with_logs=False,
            )

            # fal.ai ritorna URL — scarica i bytes
            if isinstance(result, dict):
                images = result.get("images", [])
                if images:
                    url = images[0].get("url", "")
                    if url:
                        resp = httpx.get(url, timeout=60.0)
                        resp.raise_for_status()
                        return resp.content

                # Fallback: alcuni modelli wrappano in "image"
                image_obj = result.get("image", {})
                if isinstance(image_obj, dict) and "url" in image_obj:
                    resp = httpx.get(image_obj["url"], timeout=60.0)
                    resp.raise_for_status()
                    return resp.content

            raise RuntimeError(
                f"Risposta fal.ai inattesa: {json.dumps(result)[:400]}"
            )

        except Exception as exc:
            last_exc = exc
            err_str = str(exc).lower()

            # Rate limit o timeout → aspetta e riprova
            is_retriable = any(
                kw in err_str
                for kw in ("rate", "limit", "timeout", "503", "502", "429")
            )

            if is_retriable and attempt < max_retries - 1:
                wait = retry_delay * (attempt + 1)
                print(f"[flux_image_gen] tentativo {attempt + 1}/{max_retries} fallito, "
                      f"attendo {wait:.0f}s... ({exc})")
                time.sleep(wait)
                continue

            raise

    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# API pubblica
# ---------------------------------------------------------------------------

def generate_image(
    prompt: str,
    *,
    tier: str = DEFAULT_TIER,
    size: str = "1024x1536",
    seed: Optional[int] = None,
    reference_image: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    max_retries: int = 3,
) -> GenerationResult:
    """
    Genera un'immagine con Flux via fal.ai.

    Args:
        prompt:          Descrizione dell'immagine da generare.
        tier:            Modello Flux da usare. Default: 'flux-kontext-pro'.
                         Opzioni: 'flux-schnell', 'flux-pro',
                                  'flux-kontext-pro', 'flux-kontext-max'.
        size:            Dimensione output nel formato 'WxH'. Default: '1024x1536'.
                         Esempi: '1024x1024', '1536x1024', '1024x1536'.
        seed:            Seed riproducibile. None = casuale.
        reference_image: Path a un'immagine di riferimento (solo Kontext).
                         Se passata con tier non-Kontext, viene ignorata con warning.
        output_path:     Se fornito, salva l'immagine al path specificato.
        max_retries:     Numero di tentativi su rate limit / timeout. Default: 3.

    Returns:
        GenerationResult con .image_bytes, .cost_usd, .seed e metodo .save().

    Raises:
        RuntimeError:    FAL_KEY mancante o risposta API inattesa.
        FileNotFoundError: reference_image non trovata su disco.
    """
    if tier not in _FAL_MODELS:
        available = ", ".join(sorted(_FAL_MODELS.keys()))
        raise ValueError(f"Tier '{tier}' non valido. Disponibili: {available}")

    # Setta la chiave nell'env (fal_client la legge da lì)
    api_key = _get_api_key()
    os.environ["FAL_KEY"] = api_key

    model_id = _FAL_MODELS[tier]
    args: dict = {"prompt": prompt, **_parse_size(size), "num_images": 1}

    if seed is not None:
        args["seed"] = seed

    if reference_image is not None:
        if tier in _SUPPORTS_REFERENCE:
            image_url = _upload_reference(reference_image)
            args["image_url"] = image_url
        else:
            print(
                f"[flux_image_gen] WARN: il tier '{tier}' non supporta reference_image. "
                "Usa 'flux-kontext-pro' o 'flux-kontext-max' per character consistency."
            )

    image_bytes = _call_fal(model_id, args, max_retries=max_retries)

    result = GenerationResult(
        image_bytes=image_bytes,
        provider="fal.ai",
        model=tier,
        cost_usd=_COSTS_USD[tier],
        seed=seed,
    )

    if output_path is not None:
        result.save(output_path)

    return result


def list_tiers() -> list[dict]:
    """Ritorna i tier disponibili con costi e supporto reference."""
    return [
        {
            "tier": k,
            "fal_model": v,
            "cost_usd": _COSTS_USD[k],
            "supports_reference": k in _SUPPORTS_REFERENCE,
        }
        for k, v in _FAL_MODELS.items()
    ]
