# `_pacchetti_consegnati/` — archivio pacchetti autoriali Ray

> **Cosa è.** Archivio dei pacchetti operativi consegnati da Ray e già integrati nel canone (grafo, schede, script). I documenti qui dentro sono **fonte autorevole delle decisioni autoriali** e servono come trail di audit + reference per pacchetti futuri analoghi.
>
> **Scope.** Solo storico. Quando Ray consegna un pacchetto, l'agente IA esegue gli step di integrazione (script idempotenti dry-run/--apply, backup automatici, commit puntuali). Una volta integrato, i documenti del pacchetto vengono spostati qui.
>
> **Pattern coerente con `_porting_grafo/`** (archivio chiuso fase E migrazione grafo, non toccare).

---

## Pacchetti archiviati

| Pacchetto | Periodo | Stato | README |
|---|---|---|---|
| `cornice_mondo/` | 2026-04-30 | ✅ integrato (7 step) | [`cornice_mondo/README.md`](./cornice_mondo/README.md) |
| `mappa_isola_v1/` | 2026-05-05 | ✅ integrato (route `#/mappa-isola` su catalogo_web + 30 slot dal geojson + asset 3D progressivi) | [`mappa_isola_v1/README.md`](./mappa_isola_v1/README.md) |

---

## Cosa NON fare

- **Mai modificare** i documenti qui dentro. Sono storico.
- **Mai eseguire** script che ne modifichino i contenuti.
- **Mai considerarli "bozze"**: sono decisioni Ray fissate, applicate, e tracciate.

## Cosa fare invece

- **Leggerli** per capire il razionale di una decisione (es. "perché 6° gruppo Pescatori? perché formula ritornello sg/pl?").
- **Imitare il pattern** quando arriva un pacchetto futuro affine (es. Tier B + Tier C dettagli sentieri).

---

## Come integrare un pacchetto futuro

Quando Ray consegna un pacchetto nuovo (zip o file in root):

1. Scompatta/sposta i documenti del pacchetto in `_pacchetti_consegnati/<nome_pacchetto>/`.
2. Esegui gli script di integrazione (in `scripts/<nome_pacchetto>/` se è un pacchetto operativo come cornice_mondo, oppure ad-hoc per pacchetti minori).
3. Aggiorna grafo/catalogo come richiesto, sempre additivo + retrocompatibile.
4. Backup canonico del grafo prima di apply: `story_graph.json.pre_<nome_pacchetto>.backup.json`.
5. Aggiungi entry in `migration_log` del grafo + entry in `SYNC_LOG.md`.
6. Aggiorna README/CLAUDE.md/PROJECT_STATE.md per registrare il pacchetto integrato.
7. Crea `_pacchetti_consegnati/<nome_pacchetto>/README.md` che riassume cosa è stato fatto.
