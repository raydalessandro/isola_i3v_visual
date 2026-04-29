#!/usr/bin/env python3
"""
Writer deterministico hook visivi nel grafo.

INPUT:
  - file YAML per storia, in pipeline_narrativa/hooks_proposals/cicloX/sNN.yaml
  - struttura attesa:
      story_id: s01
      hooks:
        - hook_id: s01_h01
          type: interno          # enum
          is_signature: false
          provenance: extended_v2
          moment: mattino_presto
          location:
            id: forno
            qualifier: interno
          characters_present: [fiamma, gabriel, elias, noah]
          focal_action: "Fiamma mette in mano due pagnotte..."
          focal_object: pagnotta_forno
          atmosphere: "..."
          palette: "..."
          composition_zone: vignette
          # opzionali: quadrant (auto), wind_visible, onomatopee, elements,
          # stratification, notes

OUTPUT: aggiorna `stories.<sid>.visual_anchors.scene_hooks` nel grafo,
bumpa `graph_version` 1.0.0 -> 1.1.0 + `schema_version` 1.2 -> 1.3 alla
PRIMA scrittura, aggiorna `last_updated`. Backup automatico in
`pipeline_narrativa/story_graph.json.pre_fase_g.backup.json` (solo
se non esiste gia').

VALIDAZIONE PRE-SCRITTURA (in ordine, fallisce subito al primo errore):
  1. esattamente 10 hook
  2. id pattern sNN_hMM, zero-pad
  3. type in {panorama,azione,introspettivo,atmosferico,transizione,interno,dettaglio}
  4. provenance in {original_v1, extended_v2}
  5. composition_zone in enum
  6. is_signature: bool
  7. campi obbligatori non vuoti (type, moment, location.id, characters_present,
     focal_action, atmosphere, palette, composition_zone)
  8. ogni location.id in entities.locations
  9. ogni focal_object (se non null) in entities.objects
 10. ogni character in entities.characters
 11. ogni wind_visible (se non null) in entities.winds
 12. focal_action <= 25 parole
 13. ogni hook quadrant matcha entities.locations[location.id].quadrant
 14. almeno 4 type diversi
 15. mai piu' di 3 hook consecutivi stesso type
 16. max 3 signature

USO:
    # validazione senza scrittura:
    python3 scripts/write_hooks_to_graph.py --story s01 --dry-run

    # scrittura:
    python3 scripts/write_hooks_to_graph.py --story s01

    # batch ciclo:
    python3 scripts/write_hooks_to_graph.py --cycle A
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
GRAPH = REPO / 'pipeline_narrativa' / 'story_graph.json'
BACKUP = REPO / 'pipeline_narrativa' / 'story_graph.json.pre_fase_g.backup.json'
PROPOSALS_DIR = REPO / 'pipeline_narrativa' / 'hooks_proposals'

VALID_TYPES = {
    'panorama', 'azione', 'introspettivo', 'atmosferico',
    'transizione', 'interno', 'dettaglio',
}
VALID_COMPOSITION_ZONES = {
    'sky_space', 'fog_space', 'ground_space', 'side_space',
    'vignette', 'corner_lower_left', 'corner_lower_right',
}
VALID_PROVENANCE = {'original_v1', 'extended_v2'}
HOOK_ID_RE = re.compile(r'^s(\d{2})_h(\d{2})$')

REQUIRED_FIELDS = (
    'hook_id', 'type', 'is_signature', 'provenance', 'moment',
    'location', 'characters_present', 'focal_action', 'atmosphere',
    'palette', 'composition_zone',
)

CYCLE_TO_STORIES = {
    'A': ['s01', 's02', 's03'],
    'B': ['s04', 's05', 's06'],
    'C': ['s07', 's08', 's09'],
    'D': ['s10', 's11', 's12'],
}


class ValidationError(Exception):
    pass


def load_graph() -> dict:
    return json.loads(GRAPH.read_text(encoding='utf-8'))


def save_graph(g: dict) -> None:
    GRAPH.write_text(
        json.dumps(g, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )


def find_proposal(story_id: str) -> Path:
    candidates = list(PROPOSALS_DIR.rglob(f'{story_id}.yaml'))
    if not candidates:
        raise ValidationError(
            f'Nessun YAML trovato per {story_id} in {PROPOSALS_DIR}'
        )
    if len(candidates) > 1:
        raise ValidationError(
            f'Trovati {len(candidates)} YAML per {story_id}: '
            + ', '.join(str(p) for p in candidates)
        )
    return candidates[0]


def validate_hooks(story_id: str, hooks: list, graph: dict) -> None:
    ents = graph['entities']
    locs = ents['locations']
    chars = ents['characters']
    objs = ents['objects']
    winds = ents.get('winds', {})

    if len(hooks) != 10:
        raise ValidationError(f'{story_id}: attesi 10 hook, trovati {len(hooks)}')

    types_seen = []
    sig_count = 0
    for i, h in enumerate(hooks, start=1):
        prefix = f'{story_id} hook[{i}]'

        # campi obbligatori (presenza). Liste possono essere vuote (es.
        # characters_present in scene di solo oggetto come s03_h04).
        for f in REQUIRED_FIELDS:
            if f not in h:
                raise ValidationError(f'{prefix}: campo obbligatorio mancante: {f}')
            v = h[f]
            if v is None:
                raise ValidationError(f'{prefix}: campo obbligatorio nullo: {f}')
            if isinstance(v, str) and v.strip() == '':
                raise ValidationError(f'{prefix}: campo obbligatorio stringa vuota: {f}')

        # hook_id formato + numero
        m = HOOK_ID_RE.match(h['hook_id'])
        if not m:
            raise ValidationError(
                f'{prefix}: hook_id {h["hook_id"]!r} non rispetta pattern sNN_hMM'
            )
        if m.group(1) != story_id[1:]:
            raise ValidationError(
                f'{prefix}: hook_id {h["hook_id"]!r} non corrisponde a {story_id}'
            )
        if int(m.group(2)) != i:
            raise ValidationError(
                f'{prefix}: hook_id {h["hook_id"]!r} fuori sequenza (atteso h{i:02d})'
            )

        # type
        if h['type'] not in VALID_TYPES:
            raise ValidationError(
                f'{prefix}: type {h["type"]!r} non in {sorted(VALID_TYPES)}'
            )
        types_seen.append(h['type'])

        # provenance
        if h['provenance'] not in VALID_PROVENANCE:
            raise ValidationError(
                f'{prefix}: provenance {h["provenance"]!r} non valida'
            )

        # composition_zone
        if h['composition_zone'] not in VALID_COMPOSITION_ZONES:
            raise ValidationError(
                f'{prefix}: composition_zone {h["composition_zone"]!r} non in enum'
            )

        # is_signature bool
        if not isinstance(h['is_signature'], bool):
            raise ValidationError(f'{prefix}: is_signature deve essere booleano')
        if h['is_signature']:
            sig_count += 1

        # location esistente
        loc_id = h['location'].get('id') if isinstance(h['location'], dict) else None
        if not loc_id or loc_id not in locs:
            raise ValidationError(
                f'{prefix}: location.id {loc_id!r} assente da entities.locations'
            )

        # quadrant coerente (se specificato esplicitamente)
        derived_q = locs[loc_id].get('quadrant')
        explicit_q = h.get('quadrant')
        if explicit_q and derived_q and explicit_q != derived_q:
            raise ValidationError(
                f'{prefix}: quadrant {explicit_q!r} non coerente con location '
                f'{loc_id!r} (atteso {derived_q!r})'
            )

        # characters
        for c in h['characters_present']:
            if c not in chars:
                raise ValidationError(
                    f'{prefix}: character {c!r} assente da entities.characters'
                )

        # focal_object opzionale
        fobj = h.get('focal_object')
        if fobj and fobj not in objs:
            raise ValidationError(
                f'{prefix}: focal_object {fobj!r} assente da entities.objects'
            )

        # wind_visible opzionale
        wv = h.get('wind_visible')
        if wv and wv not in winds:
            raise ValidationError(
                f'{prefix}: wind_visible {wv!r} assente da entities.winds'
            )

        # focal_action max 25 parole
        n_words = len(h['focal_action'].split())
        if n_words > 25:
            raise ValidationError(
                f'{prefix}: focal_action {n_words} parole > 25 (rendere piu\' neutra)'
            )

    # vincoli aggregate
    if len(set(types_seen)) < 4:
        raise ValidationError(
            f'{story_id}: tipologie diverse {len(set(types_seen))} < 4 '
            f'(trovate: {sorted(set(types_seen))})'
        )

    # max 3 consecutivi stesso type
    streak = 1
    for j in range(1, len(types_seen)):
        if types_seen[j] == types_seen[j-1]:
            streak += 1
            if streak > 3:
                raise ValidationError(
                    f'{story_id}: piu\' di 3 hook consecutivi stesso type '
                    f'a partire dal hook {j-2+1}'
                )
        else:
            streak = 1

    if sig_count > 3:
        raise ValidationError(f'{story_id}: signature {sig_count} > 3')


def normalize_hook(h: dict, graph: dict) -> dict:
    """Normalizza l'hook per la scrittura: deriva quadrant da location se
    omesso; ordina i campi in modo deterministico."""
    loc_id = h['location']['id']
    quadrant = h.get('quadrant') or graph['entities']['locations'][loc_id].get('quadrant')

    out = {
        'hook_id': h['hook_id'],
        'type': h['type'],
        'is_signature': bool(h['is_signature']),
        'provenance': h['provenance'],
        'moment': h['moment'],
        'location': {
            'id': loc_id,
            'qualifier': h['location'].get('qualifier'),
        },
        'quadrant': quadrant,
        'characters_present': list(h['characters_present']),
        'elements': list(h.get('elements') or []),
        'focal_action': h['focal_action'].strip(),
        'focal_object': h.get('focal_object'),
        'atmosphere': h['atmosphere'].strip(),
        'palette': h['palette'].strip(),
        'wind_visible': h.get('wind_visible'),
        'onomatopee': list(h.get('onomatopee') or []),
        'composition_zone': h['composition_zone'],
        'stratification': h.get('stratification'),
        'notes': (h.get('notes') or '').strip() or None,
    }
    return out


def write_story(story_id: str, dry_run: bool) -> None:
    yaml_path = find_proposal(story_id)
    raw = yaml.safe_load(yaml_path.read_text(encoding='utf-8'))
    if raw.get('story_id') != story_id:
        raise ValidationError(
            f'YAML story_id {raw.get("story_id")!r} != atteso {story_id!r}'
        )
    hooks_in = raw.get('hooks') or []

    g = load_graph()
    validate_hooks(story_id, hooks_in, g)

    hooks_out = [normalize_hook(h, g) for h in hooks_in]

    if dry_run:
        print(f'[DRY-RUN] {story_id}: 10 hook validi (no write).')
        types = [h['type'] for h in hooks_out]
        sig = sum(1 for h in hooks_out if h['is_signature'])
        print(f'  type distribution: {dict((t, types.count(t)) for t in set(types))}')
        print(f'  signature: {sig}')
        return

    # backup pre-scrittura
    if not BACKUP.exists():
        shutil.copy2(GRAPH, BACKUP)
        print(f'[backup] -> {BACKUP.name}')

    # scrittura
    g['stories'][story_id]['visual_anchors']['scene_hooks'] = hooks_out

    # bump versione (solo prima volta)
    if g.get('graph_version') == '1.0.0':
        g['graph_version'] = '1.1.0'
    if g.get('schema_version') == '1.2':
        g['schema_version'] = '1.3'

    g['last_updated'] = date.today().isoformat()
    g['phase'] = f'fase_g_in_corso_{date.today().isoformat()}'

    # migration log
    g.setdefault('migration_log', []).append({
        'version': g['graph_version'],
        'date': date.today().isoformat(),
        'phase': 'fase_g_hook_extension',
        'summary': f'{story_id}: scritti 10 scene_hooks v1.3 da {yaml_path.relative_to(REPO)}.',
    })

    save_graph(g)
    print(f'[written] {story_id} -> {GRAPH.name} (graph_version={g["graph_version"]}, schema_version={g["schema_version"]})')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument('--story', help='story id es. s01')
    grp.add_argument('--cycle', choices=list(CYCLE_TO_STORIES), help='ciclo A|B|C|D')
    p.add_argument('--dry-run', action='store_true', help='valida senza scrivere')
    args = p.parse_args()

    stories = [args.story] if args.story else CYCLE_TO_STORIES[args.cycle]

    errors = []
    for sid in stories:
        try:
            write_story(sid, args.dry_run)
        except ValidationError as e:
            errors.append((sid, str(e)))
            print(f'[FAIL] {sid}: {e}', file=sys.stderr)

    if errors:
        sys.exit(1)


if __name__ == '__main__':
    main()
