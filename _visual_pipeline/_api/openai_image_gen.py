"""
openai_image_gen.py — Modulo standalone per generazione immagini via OpenAI GPT Image.

Modelli supportati:
    gpt-image-1.5   qualità low: $0.011-0.016/img  → bozze, approvazione
                    qualità high: $0.167-0.260/img  → produzione

Supporta:
    - generate()  text-to-image
    - edit()      image-to-image con reference (input_fidelity="high")

Env vars richieste:
    OPENAI_API_KEY — chiave API OpenAI (https://platform.openai.com/api-keys)

Uso minimo:
    from openai_image_gen import generate_image
    generate_image("a watercolor fox in the forest", output_path="fox.png")
"""

from __future__ import annotations

import base64
import os
import time
from pathlib import Path
from typing import Optional, Union


# ---------------------------------------------------------------------------
# Costi per size (gpt-image-1, aggiornati aprile 2026)
# ---------------------------------------------------------------------------

_COST_LOW: dict[str, float] = {
    "1024x1024": 0.011,
    "1024x1536": 0.016,
    "1536x1024": 0.016,
    "1792x1024": 0.016,
    "1024x1792": 0.016,
}

_COST_HIGH: dict[str, float] = {
    "1024x1024": 0.167,
    "1024x1536": 0.260,
    "1536x1024": 0.260,
    "1792x1024": 0.260,
    "1024x1792": 0.260,
}

DEFAULT_MODEL = "gpt-image-1"
DEFAULT_SIZE  = "1024x1536"
DEFAULT_QUALITY = "low"


# ---------------------------------------------------------------------------
# Risultato (stessa interfaccia di flux_image_gen.GenerationResult)
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
        self.seed = seed  # OpenAI non restituisce seed — viene passato ma ignorato dall'API

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
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY non trovata. Setta la variabile d'ambiente "
            "o crea un file .env con OPENAI_API_KEY=<tua_chiave>."
        )
    return key


def _cost_for(size: str, quality: str) -> float:
    table = _COST_HIGH if quality == "high" else _COST_LOW
    return table.get(size, _COST_LOW[DEFAULT_SIZE])


# ---------------------------------------------------------------------------
# API pubblica
# ---------------------------------------------------------------------------

def generate_image(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    size: str = DEFAULT_SIZE,
    quality: str = DEFAULT_QUALITY,
    output_format: str = "png",
    seed: Optional[int] = None,
    output_path: Optional[Union[str, Path]] = None,
    max_retries: int = 3,
) -> GenerationResult:
    """
    Genera un'immagine con OpenAI GPT Image (text-to-image).

    Args:
        prompt:        Descrizione dell'immagine da generare.
        model:         Modello OpenAI. Default: 'gpt-image-1'.
        size:          Dimensione output. Valori accettati:
                       '1024x1024', '1024x1536', '1536x1024',
                       '1792x1024', '1024x1792'. Default: '1024x1536'.
        quality:       'low' (bozze, economico) o 'high' (produzione).
                       Default: 'low'.
        output_format: 'png' o 'jpeg'. Default: 'png'.
        seed:          Passato per completezza — OpenAI non lo supporta ancora.
        output_path:   Se fornito, salva l'immagine al path specificato.
        max_retries:   Tentativi su rate limit / timeout. Default: 3.

    Returns:
        GenerationResult con .image_bytes, .cost_usd e metodo .save().

    Raises:
        RuntimeError: OPENAI_API_KEY mancante o risposta API inattesa.
    """
    from openai import OpenAI, RateLimitError, APITimeoutError

    client = OpenAI(api_key=_get_api_key())

    last_exc: Optional[Exception] = None

    for attempt in range(max_retries):
        try:
            result = client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                output_format=output_format,
            )
            image_bytes = base64.b64decode(result.data[0].b64_json)
            break

        except (RateLimitError, APITimeoutError) as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                wait = 5.0 * (attempt + 1)
                print(f"[openai_image_gen] tentativo {attempt + 1}/{max_retries} fallito, "
                      f"attendo {wait:.0f}s... ({exc})")
                time.sleep(wait)
            else:
                raise
        except Exception:
            raise
    else:
        raise last_exc  # type: ignore[misc]

    res = GenerationResult(
        image_bytes=image_bytes,
        provider="openai",
        model=model,
        cost_usd=_cost_for(size, quality),
        seed=seed,
    )

    if output_path is not None:
        res.save(output_path)

    return res


def edit_image(
    prompt: str,
    reference_image: Union[str, Path],
    *,
    model: str = DEFAULT_MODEL,
    size: str = DEFAULT_SIZE,
    quality: str = DEFAULT_QUALITY,
    output_format: str = "png",
    input_fidelity: str = "high",
    seed: Optional[int] = None,
    output_path: Optional[Union[str, Path]] = None,
    max_retries: int = 3,
) -> GenerationResult:
    """
    Genera un'immagine partendo da una reference (image-to-image).

    Ideale per mantenere la coerenza visiva tra tavole dello stesso libro.
    GPT Image preserva stile, palette e tratti del personaggio dalla reference.

    Args:
        prompt:          Descrizione della nuova scena.
        reference_image: Path all'immagine di riferimento (PNG o JPEG).
        model:           Modello OpenAI. Default: 'gpt-image-1'.
        size:            Dimensione output. Default: '1024x1536'.
        quality:         'low' o 'high'. Default: 'low'.
        output_format:   'png' o 'jpeg'. Default: 'png'.
        input_fidelity:  'low', 'medium', 'high'. 'high' = massima fedeltà
                         alla reference. Default: 'high'.
        seed:            Non supportato da OpenAI — ignorato.
        output_path:     Se fornito, salva l'immagine al path specificato.
        max_retries:     Tentativi su rate limit / timeout. Default: 3.

    Returns:
        GenerationResult con .image_bytes, .cost_usd e metodo .save().

    Raises:
        FileNotFoundError: reference_image non trovata su disco.
        RuntimeError:      OPENAI_API_KEY mancante.
    """
    from openai import OpenAI, RateLimitError, APITimeoutError

    ref_path = Path(reference_image)
    if not ref_path.exists():
        raise FileNotFoundError(f"Reference image non trovata: {ref_path}")

    client = OpenAI(api_key=_get_api_key())
    last_exc: Optional[Exception] = None

    for attempt in range(max_retries):
        try:
            with open(ref_path, "rb") as ref:
                result = client.images.edit(
                    model=model,
                    image=ref,
                    prompt=prompt,
                    size=size,
                    quality=quality,
                    output_format=output_format,
                    input_fidelity=input_fidelity,
                )
            image_bytes = base64.b64decode(result.data[0].b64_json)
            break

        except (RateLimitError, APITimeoutError) as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                wait = 5.0 * (attempt + 1)
                print(f"[openai_image_gen] tentativo {attempt + 1}/{max_retries} fallito, "
                      f"attendo {wait:.0f}s... ({exc})")
                time.sleep(wait)
            else:
                raise
        except Exception:
            raise
    else:
        raise last_exc  # type: ignore[misc]

    res = GenerationResult(
        image_bytes=image_bytes,
        provider="openai",
        model=model,
        cost_usd=_cost_for(size, quality),
        seed=seed,
    )

    if output_path is not None:
        res.save(output_path)

    return res
