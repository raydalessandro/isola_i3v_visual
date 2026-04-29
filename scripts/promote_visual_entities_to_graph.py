#!/usr/bin/env python3
"""
Promuove entita' dal catalogo visual (`catalogo_web/data/entities.json`)
al grafo (`pipeline_narrativa/story_graph.json`) come sentinelle minime
per audit_3_navigability.

Idempotente: se l'id esiste gia' in entities.{locations|objects}, skip.

Input: lista di id da promuovere (hardcoded nel main, da estendere).
Output: grafo aggiornato + report stdout.

Campi minimi scritti per ogni entity:
  locations: type, quadrant, parent_location, role_saga (se inferibile),
             source ("promoted_from_catalog_<data>")
  objects:   category, appare_in_storie, source

Mapping quartiere catalogo -> quadrant grafo:
  aria  -> aria_nord
  terra -> terra_ovest
  acqua -> acqua_sud
  fuoco -> fuoco_est
  centro -> centro
"""
import json
from pathlib import Path
from datetime import date

REPO = Path(__file__).resolve().parent.parent
GRAPH = REPO / 'pipeline_narrativa' / 'story_graph.json'
CATALOG = REPO / 'catalogo_web' / 'data' / 'entities.json'

QUARTIERE_TO_QUADRANT = {
    'aria': 'aria_nord',
    'terra': 'terra_ovest',
    'acqua': 'acqua_sud',
    'fuoco': 'fuoco_est',
    'centro': 'centro',
}

# Lista esplicita: solo entita' richieste dagli hook ciclo A non ancora nel grafo.
# Estendere quando arrivano nuove storie con id non promossi.
ENTITIES_TO_PROMOTE = {
    'locations': [
        'sentiero_montagne_gemelle',
        'pozza_abbeveratoio_pastori',
        'radura_dei_pini',
    ],
    'objects': [
        'pallone_di_stoffa_cucita',
    ],
}

SOURCE_TAG = f'promoted_from_catalog_{date.today().isoformat()}'


def load_catalog():
    cw = json.loads(CATALOG.read_text(encoding='utf-8'))
    by_id = {e['id']: e for e in cw['entities']}
    return by_id


def build_location_entry(cat_entry):
    fm = cat_entry.get('frontmatter', {})
    quartiere = fm.get('quartiere') or cat_entry.get('quartiere')
    sottotipo = fm.get('sottotipo') or cat_entry.get('sottotipo') or 'luogo_generico'
    parent = fm.get('relazioni', {}).get('parent_location')
    return {
        'type': sottotipo,
        'quadrant': QUARTIERE_TO_QUADRANT.get(quartiere, '?'),
        'parent_location': parent,
        'source': SOURCE_TAG,
    }


def build_object_entry(cat_entry):
    fm = cat_entry.get('frontmatter', {})
    sottotipo = fm.get('sottotipo') or 'oggetto_generico'
    appare = fm.get('appare_in_storie', [])
    return {
        'category': sottotipo,
        'appare_in_storie': appare,
        'source': SOURCE_TAG,
    }


def main():
    g = json.loads(GRAPH.read_text(encoding='utf-8'))
    cat = load_catalog()
    ents = g['entities']

    summary = {'added': [], 'skipped_present': [], 'missing_in_catalog': []}

    for group, ids in ENTITIES_TO_PROMOTE.items():
        for eid in ids:
            if eid in ents.get(group, {}):
                summary['skipped_present'].append(f'{group}/{eid}')
                continue
            if eid not in cat:
                summary['missing_in_catalog'].append(f'{group}/{eid}')
                continue
            if group == 'locations':
                entry = build_location_entry(cat[eid])
            elif group == 'objects':
                entry = build_object_entry(cat[eid])
            else:
                raise ValueError(f'Group not supported: {group}')
            ents.setdefault(group, {})[eid] = entry
            summary['added'].append(f'{group}/{eid}')

    if summary['added']:
        # Append migration_log entry
        g.setdefault('migration_log', []).append({
            'version': g.get('graph_version', '1.0.0') + '-promote-entities',
            'date': date.today().isoformat(),
            'phase': 'pre_fase_g_promote_visual_entities',
            'summary': (
                'Promozione idempotente di entita\' dal catalogo visual al grafo. '
                'Aggiunte: ' + ', '.join(summary['added']) + '.'
            ),
        })
        g['last_updated'] = date.today().isoformat()
        GRAPH.write_text(
            json.dumps(g, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )

    print('=== PROMOTE VISUAL ENTITIES TO GRAPH ===')
    for k, v in summary.items():
        print(f'  {k}: {len(v)}')
        for it in v:
            print(f'    - {it}')


if __name__ == '__main__':
    main()
