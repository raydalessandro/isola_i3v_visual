# Starter Kit — Pipeline Narrativa Riusabile

Scheletro **agnostico** per costruire una pipeline narrativa automatizzata "racconto umano → libro illustrato". Adatto a racconti brevi, romanzi lunghi, serie e saghe di qualsiasi lunghezza.

Il **formato** del prodotto è funzione del grafo (impostazione iniziale), non scelto a priori. Una volta fissato il grafo lo schema rimane invariato: ogni modifica successiva passa da script idempotenti.

## Cuore della pipeline

L'umano racconta la storia all'AI in conversazione. L'AI **inferisce il grafo completo** (entità, relazioni, vincoli, callback, semi) e lo fissa. Da quel punto tutto il flusso è deterministico: catalogo, hook, brief, prosa, composizione output. L'inferenza iniziale è la barriera anti-drift in scrittura.

## Cosa contiene questo starter kit

- Cartelle scheletro (`pipeline_narrativa/`, `visual/`, `cartografia/`, `catalogo_web/`, `scripts/`, `skills/`, `docs/`)
- Template di scheda personaggio / luogo / oggetto (con placeholder)
- Prompt operativi generici per agenti IA (inferenza grafo, estrazione hook, brieffer, prosa, audit)
- Script idempotenti adattati (`--dry-run` di default, `--apply` per scrivere, backup automatico)
- Skill agente IA (`SKILL.md` autoinizianti per ogni modalità riusabile)
- README di setup passo-passo

## Cosa NON contiene

Niente contenuto specifico de "L'Isola dei Tre Venti". Solo scheletro generico riusabile, placeholder per nomi progetto.

## Origine

Pattern operativi estratti dalla repo `isola_i3v_visual` (saga "L'Isola dei Tre Venti") e generalizzati. Isola è letta in sola lettura: nessun file della saga viene modificato per il template.

## Stato

In costruzione, fase per fase. Branch: `claude/starter-kit-*`. Commit prefix: `starter_kit:`.

| Fase | Stato |
|---|---|
| 0 — scheletro cartelle + README | in corso |

## Convenzioni

- Script idempotenti: `--dry-run` di default, `--apply` per scrivere, backup automatico
- Modifiche manuali ai file canonici (grafo, catalogo) vietate una volta fissati: solo via script
- Nessun riferimento hardcoded a una saga specifica: tutto configurato via `saga.config.yaml`
- Mai contaminare con contenuto saga reale: solo placeholder

## Output finale

Starter kit scaricabile (zip o `git clone` della sola directory `_starter_kit/`) per avviare una nuova saga / racconto da zero.
