#!/usr/bin/env python3
"""Split del sorgente narrazione fattuale nei 12 file
pipeline_narrativa/narrazione_fattuale/sNN_*.md (uno per storia).
Idempotente: sovrascrive se gia' presenti.

Sorgente atteso: pipeline_narrativa/narrazione_fattuale/_source/Ciclo*.txt
(esiste un solo file .txt nella cartella _source).
"""
from pathlib import Path
import re

REPO = Path(__file__).resolve().parent.parent
DST = REPO / 'pipeline_narrativa' / 'narrazione_fattuale'
SOURCE_DIR = DST / '_source'
sources = sorted(SOURCE_DIR.glob('Ciclo*.txt'))
assert len(sources) == 1, f'Atteso un solo Ciclo*.txt in {SOURCE_DIR}, trovati: {sources}'
SRC = sources[0]

text = SRC.read_text(encoding='utf-8')
lines = text.splitlines()

# Mappa slug per ogni storia (usata per filename)
SLUGS = {
    1:  'la_nebbia_delle_montagne_gemelle',
    2:  'il_riflesso_nella_pozza',
    3:  'il_pallone_oltre_la_foresta',
    4:  'le_radici_che_parlano',
    5:  'il_ponte_di_rami',
    6:  'il_dono_per_memolo',
    7:  'la_zattera_dei_tre_rametti',
    8:  'l_albero_che_cadde_di_sera',
    9:  'quel_pomeriggio_di_ottobre',
    10: 'la_notte_senza_luna',
    11: 'la_festa_del_raccolto',
    12: 'quando_i_tre_venti_suonano_insieme',
}

# Trova le linee dove inizia ogni storia
story_re = re.compile(r'^### S(\d+)\s+—\s+(.+)$')
cycle_re = re.compile(r'^## CICLO ([A-D])\s+—\s+(.+)$')

starts = []  # list of (story_num, title, line_idx, cycle_label)
current_cycle = None
for i, line in enumerate(lines):
    m_c = cycle_re.match(line)
    if m_c:
        current_cycle = (m_c.group(1), m_c.group(2).strip())
        continue
    m_s = story_re.match(line)
    if m_s:
        starts.append((int(m_s.group(1)), m_s.group(2).strip(), i, current_cycle))

assert len(starts) == 12, f'Trovate {len(starts)} storie, attese 12'

# Confine: prossima storia/ciclo, oppure separatori inter-ciclo
# (`*[Fine ...]*`, `# L'Isola...` h1 ripetuto, blockquote `> ` di transizione)
END_RE = re.compile(r'^\s*(\*\[Fine|# L\'Isola)')

def next_boundary(start_idx):
    for j in range(start_idx + 1, len(lines)):
        line = lines[j]
        if cycle_re.match(line) or story_re.match(line) or END_RE.match(line):
            return j
    return len(lines)

DST.mkdir(parents=True, exist_ok=True)

for idx, (num, title, line_idx, cycle) in enumerate(starts):
    end = next_boundary(line_idx)
    # Rimuovi separator "---" finale (riga di chiusura prima della storia successiva)
    body_lines = lines[line_idx:end]
    while body_lines and body_lines[-1].strip() in ('', '---'):
        body_lines.pop()

    body = '\n'.join(body_lines).rstrip() + '\n'

    cycle_letter, cycle_subtitle = cycle if cycle else ('?', '?')
    slug = SLUGS[num]
    fname = f's{num:02d}_{slug}.md'
    fpath = DST / fname

    header = (
        f'# S{num} — {title}\n\n'
        f'> Ciclo {cycle_letter} — {cycle_subtitle}\n'
        f'> Estratto da `Ciclo a-b-c-d_260429_111628.txt` (split meccanico).\n'
        f'> Italiano. Tempo presente. Registro medio-asciutto. '
        f'Cronaca fattuale (no voce autoriale finale).\n\n'
        f'---\n\n'
    )

    # body inizia con "### SN — titolo": lo sostituiamo con riga vuota,
    # tanto il titolo e' gia' nell'h1. Lasciamo solo il testo a partire
    # dalla riga successiva.
    body_text = '\n'.join(body_lines[1:]).lstrip('\n')
    body_text = body_text.rstrip() + '\n'

    fpath.write_text(header + body_text, encoding='utf-8')
    print(f'  {fname}  ({len(body_text):>6d} chars  da riga {line_idx+1} a {end})')

print(f'\nTotale: 12 file scritti in {DST}')
