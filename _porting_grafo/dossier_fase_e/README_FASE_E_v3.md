# FASE E v3.0 — KIT OPERATIVO

Sostituisce il kit v2.0. Introduce **3 sorgenti di verità** (Catalogo / Grafo / Bible), Passata 0 sentinella catalogo, schema canonico v1.2, agganci espliciti al repo `isola_i3v_visual`.

## File in questo bundle

### Da incollare nel progetto Claude (sostituisce istruzioni agente)
1. **`PROMPT_AGENTE_FASE_E_v3.md`** — prompt master.

### Da aggiungere al `dossier_fase_e.zip`

In `dossier/`:

2. **`story_graph_schema_canonical_v1_2.json`** — schema target v1.2 (sostituisce v1.1).
3. **`validation_checklist.json`** — 5 guardrail (sostituisce v2.0).
4. **`read_helpers.py`** — con modulo catalogo + resolve_legacy_location (sostituisce v2.0).
5. **`verify_output_integrity.py`** — gate UTF-8/JSON (sostituisce v2.0, aggiornato per nuovo nome rolling).
6. **`_provisional_state.json`** — rolling stato iniziale (invariato da v2.0).
7. **`_canon_misalignments.json`** — rolling misalignments (rinominato da `_bible_graph_misalignments.json`, schema esteso 3-source).
8. **`TEMPLATE_catalog_proposals.md`** — template guida per Passata 0.

### Opzionale
9. **`entities_snapshot.json`** — snapshot del catalogo (fallback se fetch GitHub fallisce). Da generare manualmente con `curl -o entities_snapshot.json https://raw.githubusercontent.com/raydalessandro/isola_i3v_visual/main/catalogo_web/data/entities.json` e mettere nel dossier.

### File di progetto (NON nella zip — già nel progetto Claude)
- `ISOLA_TRE_VENTI_BIBLE_v2.md`, `GLOSSARIO_ISOLA.md`, `ARCHI_12_STORIE_v1__1_.md`
- `MITI_FONDATORI_BREVI_v1.md`, `RIFERIMENTI_OPERATIVI-1.md`
- `VOCE_AUTORE_ESTRATTA_v1_1-1.md`, `CARTA_VOCE_v1_2.md`, `PATTERN_AI_DA_BANDIRE_v1.md`

---

## Setup prima di iniziare s01

1. Apri il `dossier_fase_e.zip` esistente.
2. **Sostituisci** dentro `dossier/`:
   - `story_graph_schema_canonical_v1_1.json` → `story_graph_schema_canonical_v1_2.json` (nuovo file, vecchio puoi tenerlo o rimuoverlo)
   - `validation_checklist.json` (sovrascrivi)
   - `read_helpers.py` (sovrascrivi)
   - `verify_output_integrity.py` (sovrascrivi)
3. **Rinomina** dentro `dossier/`:
   - `_bible_graph_misalignments.json` → `_canon_misalignments.json` (e sovrascrivi col nuovo contenuto: schema esteso, misalignments vuoto)
4. **Aggiungi** dentro `dossier/`:
   - `TEMPLATE_catalog_proposals.md`
   - (Opzionale) `entities_snapshot.json` come fallback
5. Richiudi la zip.
6. Sostituisci nel progetto Claude le istruzioni dell'agente con `PROMPT_AGENTE_FASE_E_v3.md`.

## Workflow per ogni chat S<NN>

1. Apri chat nuova nel progetto Claude.
2. Allega:
   - `dossier_fase_e.zip` (versione corrente, già aggiornata dalle chat precedenti)
   - `story_graph_v0_10_0.json`
3. Scrivi: "Migra s<NN>".
4. **Passata 0** (catalogo): l'agente fetcha catalogo, fa inventario, scrive `s<NN>_catalog_proposals.md`.
   - Se ci sono modifiche al repo da fare: **STOP**, applichi le patch al repo, commit+push, conferma.
   - Se nessuna modifica: ok, procede.
5. **Passata 1** (carpentiere): migrazione strutturale → `s<NN>_canonical.json` + `s<NN>_migration_notes.md`.
6. **Passata 2** (co-autore): provvisori narrativi → `s<NN>_provisional.json` + aggiornamento rolling files.
7. Ti consegna `dossier_fase_e_after_s<NN>.zip` con 6 file.
8. Tu:
   - Estrai i 4 file storia (`s<NN>_catalog_proposals.md`, `s<NN>_canonical.json`, `s<NN>_migration_notes.md`, `s<NN>_provisional.json`) e li archivi.
   - Apri `dossier_fase_e.zip`, sostituisci `_provisional_state.json` e `_canon_misalignments.json` con quelli dalla zip output.
   - Richiudi `dossier_fase_e.zip`. Diventa input per chat S<NN+1>.

## Cambia rispetto a v2.0

| Aspetto | v2.0 | v3.0 |
|---|---|---|
| Sorgenti di verità | Grafo + Bible (2) | Catalogo + Grafo + Bible (3) |
| Passate per chat | 2 | **3** (aggiunta Passata 0) |
| Schema canonico | v1.1 | **v1.2** |
| `scene_hook.location` | string libera | **oggetto `{id, qualifier, legacy_string}`** |
| Guardrail | 4 | **5** (aggiunto `locations_must_exist`) |
| Output per chat | 5 file | **6 file** (aggiunto `s<NN>_catalog_proposals.md`) |
| Rolling misalignments | `_bible_graph_misalignments.json`, schema 2-source | **`_canon_misalignments.json`**, schema 3-source |
| `oggetti_simbolo_presenti` | sorgente ambigua | **vincolato ai 13 ID del catalogo** |
| Pressing su Ray | leggero | **forte**: agente si rifiuta di proseguire se catalogo non aggiornato |

## Test del read_helpers v3

```bash
cd dossier/
python3 read_helpers.py s01
```

Stampa: riassunto seeds/quote/debt + test catalogo (fetch GitHub) + test resolve_legacy_location su 3 esempi.

## Cosa esce dalla saga (fine S12)

A fine S12 hai:
- **12 deliverable permanenti**: `s01_canonical.json` … `s12_canonical.json` (formato v1.2)
- **12 documenti di processo**: `s01_migration_notes.md` … `s12_migration_notes.md`
- **12 catalog_proposals**: `s01_catalog_proposals.md` … `s12_catalog_proposals.md` (storia degli arricchimenti applicati al repo)
- **12 file di lavoro**: `s01_provisional.json` … `s12_provisional.json`
- **2 rolling files finali**: `_provisional_state.json` + `_canon_misalignments.json`

Apri allora una chat dedicata di chiusura saga che:
1. Valida quote saga su tutti i 12 provisional aggregati.
2. Risolve i misalignment 3-source (eventualmente bumpando catalogo o bible).
3. Promuove i provvisori validati nei canonical (li fonde nei nodi).
4. **Snellisce `entities.*` del grafo** rimuovendo i campi ridondanti col catalogo (vedi schema v1.2 description).
5. Bumpa il grafo a v1.0.0.
