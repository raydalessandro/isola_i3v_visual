#!/usr/bin/env python3
"""
audit_delivery.py — Cancello TECNICO per le PR di consegna scene/reference
(una storia per PR, tipicamente da una collaboratrice esterna).

NON valuta la coerenza narrativa o visiva. Verifica solo il LATO TECNICO:
che i file siano nel posto giusto, con i nomi giusti, e che non ci sia
"una foto in più che è qualcos'altro". Se la consegna è pulita → PASS
(mergeabile senza revisione umana). Se c'è qualunque cosa fuori dal
contratto → FAIL (blocca e chiede revisione a noi).

CONTRATTO DI CONSEGNA — una sola storia sNN per PR. Sono ammessi SOLO:
  A) pipeline_narrativa/storie_finali/_annotations/sNN.yaml   (annotations)
  B) _proposte/sNN_<slug>/**            (README.md + immagini reference)
  C) pipeline_narrativa/storie_finali/_scene/sNN/_hd/**       (scene HD)

REGOLE (tecniche, deterministiche):
  0. Se la PR NON tocca nessun path A/B/C → il cancello non si applica:
     PASS "non una consegna" (la PR segue la normale revisione).
  1. Se È una consegna, ogni altro file fuori da A/B/C → FAIL (consegna mista).
  2. Una sola storia per PR: se i path citano più sNN → FAIL.
  3. _annotations/sNN.yaml (se presente sul disco) deve essere YAML valido.
  4. _proposte/sNN_<slug>/:
       - deve contenere un README.md (manifest della consegna)
       - solo README.md + immagini (.png/.jpg/.jpeg/.webp); altri file → FAIL
       - ogni immagine dev'essere CITATA per nome nel README, altrimenti FAIL
         (è la "foto in più che è qualcos'altro")
       - ogni immagine dev'essere un file immagine valido (magic bytes)
  5. _scene/sNN/_hd/:
       - solo .jpg/.jpeg, nessun PNG, nessun suffisso _v2 → altrimenti FAIL
       - ogni immagine {id}_hd.jpg deve corrispondere a un subhook di sNN.yaml
         → immagine orfana = FAIL (foto senza posto)
       - ogni immagine dev'essere un file immagine valido (magic bytes)

Volutamente FUORI scope (sono qualità/coerenza, non lato tecnico):
  - dimensioni/DPI delle immagini (standard scene v1.1) → banner in build_volume
  - correttezza narrativa, entità canoniche mancanti, disallineamenti fonti
  - subhook senza immagine (consegna parziale lecita) → solo avviso, non blocco

Convenzione output: exit 0 = PASS, exit 1 = FAIL. Messaggi umano-leggibili.

Uso:
    python3 scripts/audit/audit_delivery.py                       # base=origin/main head=HEAD
    python3 scripts/audit/audit_delivery.py --base <SHA> --head <SHA>
    python3 scripts/audit/audit_delivery.py --changed a.yaml,b.png  # lista esplicita (CI/test)
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

RE_ANNOT = re.compile(r"^pipeline_narrativa/storie_finali/_annotations/s(\d{2})\.yaml$")
RE_PROPOSTE = re.compile(r"^_proposte/s(\d{2})_[^/]+/")
RE_SCENE = re.compile(r"^pipeline_narrativa/storie_finali/_scene/s(\d{2})/_hd/")

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
IMG_MAGIC = {
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpeg",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
}


def _fail(problems: list[str], msg: str) -> None:
    problems.append(msg)


def sniff_image(path: Path) -> str | None:
    """Ritorna il tipo immagine dai magic bytes, o None se non è un'immagine nota."""
    try:
        head = path.read_bytes()[:16]
    except OSError:
        return None
    for magic, kind in IMG_MAGIC.items():
        if head.startswith(magic):
            return kind
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None


def git_changed(base: str, head: str) -> list[str]:
    """File modificati (A/M/D/R) su head rispetto al merge-base con base."""
    out = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--name-only", f"{base}...{head}"],
        capture_output=True, text=True, check=True,
    ).stdout
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def classify(changed: list[str]) -> tuple[dict, list[str], set[str]]:
    """Partiziona i file: delivery (A/B/C) vs other; raccoglie le storie citate."""
    delivery = {"annot": [], "proposte": [], "scene": []}
    other: list[str] = []
    stories: set[str] = set()
    for f in changed:
        m = RE_ANNOT.match(f)
        if m:
            delivery["annot"].append(f); stories.add(m.group(1)); continue
        m = RE_PROPOSTE.match(f)
        if m:
            delivery["proposte"].append(f); stories.add(m.group(1)); continue
        m = RE_SCENE.match(f)
        if m:
            delivery["scene"].append(f); stories.add(m.group(1)); continue
        other.append(f)
    return delivery, other, stories


def load_subhook_ids(sid: str) -> set[str] | None:
    """id dei subhook dichiarati in sNN.yaml (dal working tree), o None se assente/illeggibile."""
    p = REPO / "pipeline_narrativa" / "storie_finali" / "_annotations" / f"s{sid}.yaml"
    if not p.exists():
        return None
    try:
        import yaml
        data = yaml.safe_load(p.read_text())
        return {sh["id"] for h in data.get("hooks", {}).values()
                for sh in (h.get("subhooks") or []) if sh.get("id")}
    except Exception:
        return None


def validate_proposte(paths: list[str], problems: list[str]) -> None:
    """Regola 4: ogni cartella _proposte toccata deve avere README + solo immagini documentate."""
    dirs = sorted({"/".join(p.split("/")[:2]) for p in paths})  # _proposte/sNN_slug
    for d in dirs:
        folder = REPO / d
        if not folder.is_dir():
            continue  # cartella eliminata: nulla da validare sul disco
        readme = folder / "README.md"
        if not readme.exists():
            _fail(problems, f"[proposte] {d}/ senza README.md (manca il manifest della consegna)")
            readme_text = ""
        else:
            readme_text = readme.read_text(errors="ignore")
        for child in sorted(folder.iterdir()):
            if child.name == "README.md":
                continue
            if child.is_dir():
                _fail(problems, f"[proposte] sottocartella inattesa: {d}/{child.name}/")
                continue
            if child.suffix.lower() not in IMG_EXT:
                _fail(problems, f"[proposte] file non-immagine nella consegna: {d}/{child.name}")
                continue
            if sniff_image(child) is None:
                _fail(problems, f"[proposte] non è un'immagine valida: {d}/{child.name}")
            if child.name not in readme_text:
                _fail(problems, f"[proposte] foto in più non documentata nel README: {d}/{child.name}")


def validate_scene(paths: list[str], stories: set[str], problems: list[str]) -> None:
    """Regola 5: scene HD solo jpg, nome {id}_hd.jpg agganciato a un subhook reale."""
    sid = next(iter(stories))
    subs = load_subhook_ids(sid)
    for f in paths:
        p = REPO / f
        name = Path(f).name
        if not p.exists():
            continue  # eliminazione: ok
        if "_v2" in name:
            _fail(problems, f"[scene] residuo di lavorazione (_v2): {f}")
        if Path(f).suffix.lower() not in {".jpg", ".jpeg"}:
            _fail(problems, f"[scene] le scene HD devono essere .jpg (trovato {name})")
            continue
        if sniff_image(p) != "jpeg":
            _fail(problems, f"[scene] non è un JPEG valido: {f}")
        m = re.match(r"^(s\d{2}_h\d{2}[a-z]?)_hd\.jpe?g$", name)
        if not m:
            _fail(problems, f"[scene] nome fuori convenzione {{id}}_hd.jpg: {name}")
            continue
        if subs is None:
            _fail(problems, f"[scene] impossibile leggere i subhook di s{sid} per verificare {name}")
        elif m.group(1) not in subs:
            _fail(problems, f"[scene] scena HD orfana (nessun subhook '{m.group(1)}' in s{sid}.yaml): {name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--changed", default=None,
                    help="lista esplicita di file (virgola-separata); scavalca il git diff")
    args = ap.parse_args()

    if args.changed is not None:
        changed = [x.strip() for x in args.changed.split(",") if x.strip()]
    else:
        changed = git_changed(args.base, args.head)

    print("=" * 64)
    print("  audit_delivery — cancello tecnico consegne scene/reference")
    print("=" * 64)
    print(f"  file cambiati: {len(changed)}")

    delivery, other, stories = classify(changed)
    is_delivery = any(delivery.values())

    if not is_delivery:
        print("\n  Nessun path di consegna (_annotations / _proposte / _scene) toccato.")
        print("  → Cancello NON applicabile: non è una consegna scene/reference.")
        print("\nESITO: PASS (non una consegna — segue la normale revisione)")
        return 0

    print(f"  storia/e citate: {', '.join('s'+s for s in sorted(stories)) or '—'}")
    print(f"  annotations={len(delivery['annot'])} proposte={len(delivery['proposte'])} scene_hd={len(delivery['scene'])}")

    problems: list[str] = []

    # Regola 1 — consegna mista
    for f in other:
        _fail(problems, f"[contratto] file fuori dal contratto di consegna: {f}")

    # Regola 2 — una sola storia
    if len(stories) > 1:
        _fail(problems, f"[contratto] la PR tocca più storie ({', '.join('s'+s for s in sorted(stories))}): una storia per PR")

    # Regola 3 — yaml valido
    for f in delivery["annot"]:
        p = REPO / f
        if p.exists():
            try:
                import yaml
                yaml.safe_load(p.read_text())
            except Exception as e:
                _fail(problems, f"[annotations] YAML non valido ({f}): {e}")

    # Regola 4 — proposte
    if delivery["proposte"]:
        validate_proposte(delivery["proposte"], problems)

    # Regola 5 — scene HD (solo se una sola storia, altrimenti già bloccato sopra)
    if delivery["scene"] and len(stories) == 1:
        validate_scene(delivery["scene"], stories, problems)

    print()
    if problems:
        print(f"  {len(problems)} problema/i tecnico/i — la consegna richiede revisione umana:")
        for pb in problems:
            print(f"    ✗ {pb}")
        print("\nESITO: FAIL (consegna NON pulita — blocca il merge, chiede revisione)")
        return 1

    print("  Nessun problema tecnico: file nei posti giusti, nomi corretti, nessun extra.")
    print("\nESITO: PASS (consegna tecnicamente pulita — mergeabile senza revisione)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
