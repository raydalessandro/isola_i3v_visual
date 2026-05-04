#!/usr/bin/env python3
"""
normalize_storie_finali.py — uno-shot

Trasforma le 12 storie definitive caricate sulla root nel formato canonico
con frontmatter YAML + marker hook predisposti per script futuri (compositore
del libro pagina+immagine).

Operazioni per ogni storia:
1. Estrae titolo dal primo H1
2. Normalizza i marker pagina (## Pagina N) — gestisce 3 formati di input:
   - "## Pagina N" (s01-s08, s11, s12) ← già ok
   - "### Pagina N" (s10) ← promuove a ##
   - separatori "---" tra pagine (s09) ← inserisce ## Pagina N
3. Aggiunge frontmatter YAML con metadati saga
4. Aggiunge dopo ogni ## Pagina N un commento HTML marker:
   <!-- @hook sNN_hMM | @page MM | @subhooks [] | @image TBD -->
5. Salva in pipeline_narrativa/storie_finali/sNN_<slug>.md
6. (Opzionale) elimina file originale dalla root

Il commento HTML è machine-readable da futuri script di composizione libro:
- @hook = id univoco hook visivo della pagina
- @page = numero pagina libro
- @subhooks = lista (vuota inizialmente) per future scomposizioni
- @image = path immagine composta (TBD = to be defined, da popolare poi)

Uso:
    python3 scripts/normalize_storie_finali.py            # dry-run
    python3 scripts/normalize_storie_finali.py --apply    # esegue
"""
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEST_DIR = REPO_ROOT / "pipeline_narrativa" / "storie_finali"

# Mapping da filename root → sid + slug canonico
MAPPING = {
    "s01_la_nebbia_delle_montagne_gemelle_.md": ("s01", "la_nebbia_delle_montagne_gemelle"),
    "s02_storia.md": ("s02", "il_riflesso_nella_pozza"),
    "s03_storia.md": ("s03", "il_pallone_oltre_la_foresta"),
    "s04_le_radici_che_parlano.md": ("s04", "le_radici_che_parlano"),
    "s05_il_ponte_di_rami.md": ("s05", "il_ponte_di_rami"),
    "s06_il_dono_per_memolo.md": ("s06", "il_dono_per_memolo"),
    "s07.md": ("s07", "la_zattera_dei_tre_rametti"),
    "s08_storia.md": ("s08", "lalbero_che_cadde_di_sera"),
    "s09_quel_pomeriggio_di_ottobre.md": ("s09", "quel_pomeriggio_di_ottobre"),
    "s10_la_notte_senza_luna.md": ("s10", "la_notte_senza_luna"),
    "s11_la_festa_del_raccolto.md": ("s11", "la_festa_del_raccolto"),
    "s12.md": ("s12", "quando_i_tre_venti_suonano_insieme"),
}

# Titolo canonico da scheda saga (senza prefisso SNN —)
TITLES = {
    "s01": "La Nebbia delle Montagne Gemelle",
    "s02": "Il Riflesso nella Pozza",
    "s03": "Il Pallone oltre la Foresta",
    "s04": "Le Radici che Parlano",
    "s05": "Il Ponte di Rami",
    "s06": "Il Dono per Mèmolo",
    "s07": "La Zattera dei Tre Rametti",
    "s08": "L'Albero che Cadde di Sera",
    "s09": "Quel Pomeriggio di Ottobre",
    "s10": "La Notte senza Luna",
    "s11": "La Festa del Raccolto",
    "s12": "Quando i Tre Venti Suonano Insieme",
}

CYCLES = {
    "s01": "A", "s02": "A", "s03": "A",
    "s04": "B", "s05": "B", "s06": "B",
    "s07": "C", "s08": "C", "s09": "C",
    "s10": "D", "s11": "D", "s12": "D",
}


def normalize_pages(content: str, sid: str) -> str:
    """Normalizza i marker pagina al formato '## Pagina N'."""
    # Caso 1: '### Pagina N' → '## Pagina N'
    content = re.sub(r"^### Pagina (\d+)\s*$", r"## Pagina \1", content, flags=re.M)

    # Caso 2: file con solo separatori '---' come separatori pagina (es s09).
    # Riconosciamo se non ci sono già '## Pagina N' nel contenuto.
    # Convenzione: ogni '---' su riga propria avvia una nuova pagina (10 ---  = 10 pagine).
    if not re.search(r"^## Pagina \d+\s*$", content, re.M):
        lines = content.split("\n")
        out = []
        page_counter = 0
        for line in lines:
            if line.strip() == "---":
                page_counter += 1
                out.append(line)
                out.append("")
                out.append(f"## Pagina {page_counter}")
            else:
                out.append(line)
        content = "\n".join(out)

    return content


def add_hook_markers(content: str, sid: str) -> str:
    """Aggiunge un commento HTML marker dopo ogni '## Pagina N'.

    Format: <!-- @hook sNN_hMM | @page MM | @subhooks [] | @image TBD -->
    """
    def replace(m):
        page_num = int(m.group(1))
        hook_id = f"{sid}_h{page_num:02d}"
        marker = f"<!-- @hook {hook_id} | @page {page_num} | @subhooks [] | @image TBD -->"
        return f"{m.group(0)}\n{marker}"

    # Skip se già presenti
    if re.search(r"<!-- @hook ", content):
        return content
    return re.sub(r"^## Pagina (\d+)\s*$", replace, content, flags=re.M)


def add_frontmatter(content: str, sid: str, slug: str) -> str:
    """Aggiunge frontmatter YAML in cima."""
    if content.startswith("---\n"):
        # Ha già frontmatter: non duplico
        return content
    title = TITLES[sid]
    cycle = CYCLES[sid]
    frontmatter = f"""---
sid: {sid}
title: {title}
slug: {slug}
cycle: {cycle}
total_pages: 10
total_hooks: 10
status: definitiva
ultima_modifica: 2026-05-04
fonti:
  - pipeline_narrativa/narrazione_fattuale/{sid}_*.md
  - pipeline_narrativa/writing_briefs/{sid}_writing_brief.md
  - pipeline_narrativa/story_graph.json#stories.{sid}
schema_marker: |
  Ogni '## Pagina N' è seguito da un commento HTML machine-readable:
  <!-- @hook sNN_hMM | @page MM | @subhooks [] | @image TBD -->
  Campi:
    @hook    : id univoco hook visivo della pagina (sNN_hMM, MM = 01..10)
    @page    : numero pagina libro (1..10)
    @subhooks: lista (vuota per ora) per future scomposizioni della pagina
    @image   : path immagine composta finale del libro (TBD da popolare)
---

"""
    return frontmatter + content


def process_story(src_path: Path, sid: str, slug: str) -> str:
    """Carica, normalizza, ritorna contenuto trasformato."""
    content = src_path.read_text(encoding="utf-8")
    content = normalize_pages(content, sid)
    content = add_hook_markers(content, sid)
    content = add_frontmatter(content, sid, slug)
    return content


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply (default: dry-run)")
    args = parser.parse_args()
    dry_run = not args.apply

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[load] {len(MAPPING)} storie da processare")
    print(f"[dest] {DEST_DIR.relative_to(REPO_ROOT)}")
    print()

    for src_name, (sid, slug) in MAPPING.items():
        src = REPO_ROOT / src_name
        dest = DEST_DIR / f"{sid}_{slug}.md"
        if not src.exists():
            print(f"  [!] {src_name} NOT FOUND")
            continue
        new_content = process_story(src, sid, slug)
        page_count = len(re.findall(r"^## Pagina \d+", new_content, re.M))
        hook_count = len(re.findall(r"<!-- @hook ", new_content))
        print(f"  [+] {src_name:50} → {dest.relative_to(REPO_ROOT)}")
        print(f"      pages: {page_count}, hooks: {hook_count}")
        if not dry_run:
            dest.write_text(new_content, encoding="utf-8")
            src.unlink()  # Rimuove dalla root

    if dry_run:
        print("\n[DRY-RUN] no changes written. Use --apply to write.")
    else:
        print(f"\n[applied] 12 storie spostate in {DEST_DIR.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
