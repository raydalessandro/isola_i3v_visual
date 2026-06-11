# Canone normativo machine-readable — `saga_config.yaml`

**Introdotto:** branch `claude/canone-machine-readable` (2026-06-10)

## Cos'è

L'unica fonte di verità per tutto ciò che del canone è **verificabile da una
macchina**: enum (type hook, composition zone, who.kind, quadranti), vincoli
numerici (10 hook/storia, focal_action ≤30 parole, max 3 signature), versioni
attese del grafo, grammatica dei marker `@hook`/`@subhook`, quote lessicali
(proiezione di `PATTERN_AI_DA_BANDIRE_v1.md` §6).

Prima viveva duplicato in 5 file (writer, audit 1-4); ora vive qui e i
consumatori **importano** via `scripts/saga_canon.py` (loader fail-loud:
config assente o malformato → i tool si fermano, non indovinano).

## Cosa NON è

Le regole **qualitative** (voce, triadi, pugno emotivo, sguardo adulto-tenero)
restano nei documenti progetto, `PATTERN_AI_DA_BANDIRE_v1.md` in testa: il
config ne è la proiezione meccanica, il documento resta la fonte autoritativa.
La grammatica resa formale qui non è una DSL nuova: è la formalizzazione del
linguaggio già in uso (markdown + marker HTML + JSON), leggibile dagli LLM
senza addestramento in contesto.

## Chi lo consuma oggi

| Consumatore | Cosa prende |
|---|---|
| `scripts/write_hooks_to_graph.py` | enum hook, required fields, soglia focal_action |
| `scripts/audit/audit_1_integrity.py` | `graph.expected_schema/expected_graph`, backup globs |
| `scripts/audit/audit_2_schema.py` | enum + vincoli hook/cornici, sentieri Tier A |
| `scripts/audit/audit_3_navigability.py` | quadranti, story ids |
| `scripts/audit/audit_4_drift.py` | quote lessicali, grammatica marker |
| `tests/test_canon.py` | verifica che i consumatori derivino davvero da qui |

Follow-up previsti (fuori da questa branch): `build_volume.py` (il suo parser
marker è blindato dai 60 test esistenti: unificazione a basso valore finché la
grammatica non evolve), `web/` (dopo il merge di catalogo-v2), starter kit
(il config diventa il punto di istanziazione di ogni nuova saga).

## Come si evolve

- **Bump versione grafo autorizzato** → aggiornare `graph.expected_*` qui,
  stessa PR della modifica al grafo. Gli audit lo verificano.
- **Nuovo valore enum** (es. il `who.kind: nominati` di step8) → aggiungerlo
  qui con commento data+motivo; writer e audit lo vedono automaticamente.
- **Nuova quota lessicale** → riga in `lexicon.quotas`; audit_4 la applica
  al prossimo run. Aggiornare anche il documento PATTERN se è regola nuova.
- Ogni modifica al config è una modifica di canone: passa da PR con audit
  verdi, mai a mano su main.

## Per la prossima saga

Lo starter kit copierà `saga_config.yaml` come template e la nuova saga lo
riempirà con i propri valori (id, enum, sentieri, quote): gli script non
cambiano. È il pezzo che rende il tooling saga-agnostico.
