#!/usr/bin/env python3
"""
saga_canon.py — Loader del canone normativo machine-readable (saga_config.yaml).

Unico punto di accesso programmatico al canone: enum, vincoli, grammatica
marker, quote lessicali. I consumatori (writer, audit, futuri tool web/starter
kit) importano da qui e NON duplicano costanti.

Uso:
    import saga_canon
    C = saga_canon.load(repo_root)     # valida e ritorna un Canon
    C.hooks.types                      # frozenset enum
    C.markers.hook_re                  # regex compilata
    C.story_ids                        # ("s01", ..., "s12")

Il loader è FAIL-LOUD: config assente, YAML invalido o chiavi mancanti
sollevano CanonError con messaggio chiaro — meglio fermarsi che validare
contro un canone sbagliato.

Dipendenze: PyYAML (già in requirements.txt).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_NAME = "saga_config.yaml"


class CanonError(RuntimeError):
    """Canone assente o malformato: i tool devono fermarsi, non indovinare."""


# ---------------------------------------------------------------------------
# Sezioni tipizzate
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GraphCanon:
    expected_schema: str
    expected_graph: str
    backup_globs: tuple[str, ...]


@dataclass(frozen=True)
class HooksCanon:
    per_story: int
    id_re: re.Pattern
    focal_action_max_words: int
    max_signature_per_story: int
    max_consecutive_same_type: int
    min_distinct_types: int
    types: frozenset[str]
    composition_zones: frozenset[str]
    provenance: frozenset[str]
    required_fields: tuple[str, ...]


@dataclass(frozen=True)
class CorniciCanon:
    per_story: int
    id_re: re.Pattern
    required_fields: tuple[str, ...]
    who_kinds: frozenset[str]
    refs_min_for_nominati: int


@dataclass(frozen=True)
class PathsCanon:
    tier_a: frozenset[str]
    details_total: int


@dataclass(frozen=True)
class MarkersCanon:
    hook_re: re.Pattern
    subhook_re: re.Pattern


@dataclass(frozen=True)
class LexiconQuota:
    pattern: str
    max_per_story: int
    only_stories: tuple[str, ...] | None = None


@dataclass(frozen=True)
class LexiconCanon:
    quotas: tuple[LexiconQuota, ...]
    piano_family_patterns: tuple[str, ...]
    piano_family_saga_max: int


@dataclass(frozen=True)
class Canon:
    config_version: int
    saga_id: str
    saga_title: str
    story_ids: tuple[str, ...]
    graph: GraphCanon
    hooks: HooksCanon
    cornici: CorniciCanon
    quadrants: frozenset[str]
    paths: PathsCanon
    markers: MarkersCanon
    lexicon: LexiconCanon
    entity_categories: tuple[str, ...]
    source_path: Path = field(compare=False, default=Path(CONFIG_NAME))


# ---------------------------------------------------------------------------
# Caricamento + validazione
# ---------------------------------------------------------------------------

def _require(d: dict, key: str, ctx: str):
    if key not in d:
        raise CanonError(f"{CONFIG_NAME}: chiave mancante {ctx}.{key}")
    return d[key]


def _compile(rx: str, ctx: str) -> re.Pattern:
    try:
        return re.compile(rx)
    except re.error as e:
        raise CanonError(f"{CONFIG_NAME}: regex invalida in {ctx}: {e}") from e


def find_config(start: Path | None = None) -> Path:
    """Risale da `start` (o da questo file) fino alla root che contiene il config."""
    base = (start or Path(__file__).resolve().parent)
    for p in (base, *base.parents):
        cand = p / CONFIG_NAME
        if cand.exists():
            return cand
    raise CanonError(
        f"{CONFIG_NAME} non trovato risalendo da {base} — il canone normativo "
        f"è obbligatorio (vedi docs/CANONE_NORMATIVO.md)"
    )


def load(repo_root: Path | None = None) -> Canon:
    try:
        import yaml  # PyYAML
    except ImportError as e:
        raise CanonError("PyYAML assente: pip install -r requirements.txt") from e

    path = (Path(repo_root) / CONFIG_NAME) if repo_root else find_config()
    if not path.exists():
        raise CanonError(f"{path} non esiste")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise CanonError(f"{CONFIG_NAME}: YAML invalido: {e}") from e
    if not isinstance(raw, dict):
        raise CanonError(f"{CONFIG_NAME}: radice non è un mapping")

    saga = _require(raw, "saga", "")
    stories = _require(raw, "stories", "")
    count = int(_require(stories, "count", "stories"))
    id_format = _require(stories, "id_format", "stories")
    story_ids = tuple(id_format.replace("{n:02d}", f"{i:02d}")
                      for i in range(1, count + 1))

    g = _require(raw, "graph", "")
    graph = GraphCanon(
        expected_schema=str(_require(g, "expected_schema", "graph")),
        expected_graph=str(_require(g, "expected_graph", "graph")),
        backup_globs=tuple(_require(g, "backup_globs", "graph")),
    )

    h = _require(raw, "hooks", "")
    hooks = HooksCanon(
        per_story=int(_require(h, "per_story", "hooks")),
        id_re=_compile(_require(h, "id_regex", "hooks"), "hooks.id_regex"),
        focal_action_max_words=int(_require(h, "focal_action_max_words", "hooks")),
        max_signature_per_story=int(_require(h, "max_signature_per_story", "hooks")),
        max_consecutive_same_type=int(_require(h, "max_consecutive_same_type", "hooks")),
        min_distinct_types=int(_require(h, "min_distinct_types", "hooks")),
        types=frozenset(_require(h, "types", "hooks")),
        composition_zones=frozenset(_require(h, "composition_zones", "hooks")),
        provenance=frozenset(_require(h, "provenance", "hooks")),
        required_fields=tuple(_require(h, "required_fields", "hooks")),
    )

    c = _require(raw, "cornici", "")
    cornici = CorniciCanon(
        per_story=int(_require(c, "per_story", "cornici")),
        id_re=_compile(_require(c, "id_regex", "cornici"), "cornici.id_regex"),
        required_fields=tuple(_require(c, "required_fields", "cornici")),
        who_kinds=frozenset(_require(c, "who_kinds", "cornici")),
        refs_min_for_nominati=int(_require(c, "refs_min_for_nominati", "cornici")),
    )

    p = _require(raw, "paths", "")
    paths = PathsCanon(
        tier_a=frozenset(_require(p, "tier_a", "paths")),
        details_total=int(_require(p, "details_total", "paths")),
    )

    m = _require(raw, "markers", "")
    markers = MarkersCanon(
        hook_re=_compile(_require(m, "hook_regex", "markers"), "markers.hook_regex"),
        subhook_re=_compile(_require(m, "subhook_regex", "markers"), "markers.subhook_regex"),
    )

    lx = _require(raw, "lexicon", "")
    quotas = []
    for i, q in enumerate(_require(lx, "quotas", "lexicon")):
        only = q.get("only_stories")
        quotas.append(LexiconQuota(
            pattern=_require(q, "pattern", f"lexicon.quotas[{i}]"),
            max_per_story=int(_require(q, "max_per_story", f"lexicon.quotas[{i}]")),
            only_stories=tuple(only) if only else None,
        ))
    fam = _require(lx, "piano_family", "lexicon")
    lexicon = LexiconCanon(
        quotas=tuple(quotas),
        piano_family_patterns=tuple(_require(fam, "patterns", "lexicon.piano_family")),
        piano_family_saga_max=int(_require(fam, "saga_max", "lexicon.piano_family")),
    )

    return Canon(
        config_version=int(_require(raw, "config_version", "")),
        saga_id=str(_require(saga, "id", "saga")),
        saga_title=str(_require(saga, "title", "saga")),
        story_ids=story_ids,
        graph=graph,
        hooks=hooks,
        cornici=cornici,
        quadrants=frozenset(_require(raw, "quadrants", "")),
        paths=paths,
        markers=markers,
        lexicon=lexicon,
        entity_categories=tuple(_require(_require(raw, "entities", ""),
                                         "categories", "entities")),
        source_path=path,
    )


if __name__ == "__main__":
    # smoke: carica e stampa un riassunto
    C = load()
    print(f"canone OK — saga {C.saga_id!r}, {len(C.story_ids)} storie, "
          f"{len(C.hooks.types)} type hook, {len(C.lexicon.quotas)} quote lessicali, "
          f"grafo atteso {C.graph.expected_graph} (schema {C.graph.expected_schema})")
