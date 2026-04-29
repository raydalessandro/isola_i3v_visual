#!/usr/bin/env python3
"""
Migrazione schema grafo: v1.2 -> v1.3 (estensione hook addittiva).

Cosa fa:
  1. bumpa schema_version 1.2 -> 1.3 e graph_version 1.0.0 -> 1.1.0-pre
  2. normalizza hook_id zero-pad (s01_h1 -> s01_h01)
  3. estrae is_signature:bool dal suffisso `_signature` nel hook_id legacy
     (es. s01_h4_signature -> hook_id=s01_h04 + is_signature=true)
  4. aggiunge provenance="original_v1" a tutti gli hook esistenti
  5. NON inferisce campi narrativi (type, composition_zone) sui legacy:
     restano assenti, sono opzionali per provenance=original_v1; saranno
     obbligatori solo per i nuovi hook con provenance=extended_v2 prodotti
     dal writer (write_hooks_to_graph.py).

Idempotente: se il grafo e' gia' v1.3, non fa nulla.

Backup pre-migrazione:
  pipeline_narrativa/story_graph.json.pre_v1_3.backup.json (one-shot).
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GRAPH = REPO / 'pipeline_narrativa' / 'story_graph.json'
BACKUP = REPO / 'pipeline_narrativa' / 'story_graph.json.pre_v1_3.backup.json'

LEGACY_ID_RE = re.compile(r'^s(\d{2})_h(\d+)(_signature)?$')
NEW_ID_RE = re.compile(r'^s(\d{2})_h(\d{2})$')


def normalize_hook(h: dict) -> dict:
    """Normalizza un singolo hook legacy v1.2 a forma v1.3-compat.

    Tutti i hook legacy verranno SOSTITUITI dal writer in fase G.
    Qui ci limitiamo a:
      - normalizzare hook_id zero-pad SE matcha il pattern standard
      - estrarre is_signature dal id (suffisso _signature o token signature)
      - aggiungere provenance=original_v1
    Per id legacy descrittivi (vh_sXX_..., hook_NN_..., sXX_hN_<descr>):
    hook_id viene preservato as-is. Tanto e' rimpiazzato dal writer.
    """
    hid = h['hook_id']
    if NEW_ID_RE.match(hid) and 'is_signature' in h and 'provenance' in h:
        return h  # gia' migrato

    new_h = dict(h)
    m = LEGACY_ID_RE.match(hid)
    if m:
        # pattern standard: sNN_hM[_signature]
        story_num, hook_num, sig_suffix = m.group(1), int(m.group(2)), m.group(3)
        new_h['hook_id'] = f's{story_num}_h{hook_num:02d}'
        new_h['is_signature'] = sig_suffix is not None
    else:
        # id descrittivo: preserva, deduci signature da contenuto
        new_h['is_signature'] = 'signature' in hid.lower()

    new_h['provenance'] = 'original_v1'
    return new_h


def main():
    g = json.loads(GRAPH.read_text(encoding='utf-8'))

    if g.get('schema_version') == '1.3':
        print('[skip] schema_version gia 1.3, nulla da fare.')
        return

    if g.get('schema_version') != '1.2':
        raise SystemExit(
            f'schema_version atteso 1.2, trovato {g.get("schema_version")!r}'
        )

    if not BACKUP.exists():
        shutil.copy2(GRAPH, BACKUP)
        print(f'[backup] -> {BACKUP.name}')

    total_hooks = 0
    total_sig = 0
    for sid in sorted(g['stories'].keys()):
        sh = g['stories'][sid].get('visual_anchors', {}).get('scene_hooks', [])
        new_sh = [normalize_hook(h) for h in sh]
        g['stories'][sid]['visual_anchors']['scene_hooks'] = new_sh
        total_hooks += len(new_sh)
        total_sig += sum(1 for h in new_sh if h.get('is_signature'))

    g['schema_version'] = '1.3'
    g['graph_version'] = '1.1.0-pre'
    g['last_updated'] = date.today().isoformat()
    g['phase'] = f'fase_g_pre_writeback_schema_v1_3_{date.today().isoformat()}'

    g.setdefault('migration_log', []).append({
        'version': '1.1.0-pre',
        'date': date.today().isoformat(),
        'phase': 'schema_v1_2_to_v1_3_migration',
        'summary': (
            f'Bump schema 1.2 -> 1.3 (estensione additiva hook). '
            f'Normalizzato hook_id zero-pad e estratto is_signature dal '
            f'suffisso legacy. Aggiunto provenance=original_v1 a tutti i '
            f'{total_hooks} hook esistenti ({total_sig} signature). '
            'Nessun campo narrativo inferito sui legacy: type e '
            'composition_zone restano assenti finche\' write_hooks_to_graph.py '
            'non sostituisce gli hook con provenance=extended_v2.'
        ),
    })

    GRAPH.write_text(
        json.dumps(g, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'[migrated] {total_hooks} hook ({total_sig} signature) -> schema v1.3')


if __name__ == '__main__':
    main()
