# `pipeline_narrativa/prompts/`

Prompt operativi per agenti IA che lavorano sul progetto. Versionati e archiviati come **canone** dell'istruzione data all'agente.

## File

- **`PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md`** — fase G (estensione hook visivi 5→10 per storia, grafo v1.0.0 → v1.1.0).

## Convenzione versioning

`PROMPT_<NOME_FASE>_v<MAJOR>.md`. Le revisioni minori si fanno in-place con commit descrittivo. I major bump quando il contenuto cambia significativamente.

## Read-only per agenti operativi

Solo Ray (o agenti in modalità "preparazione fase") modificano i prompt. Gli agenti operativi che eseguono il prompt leggono e basta.
