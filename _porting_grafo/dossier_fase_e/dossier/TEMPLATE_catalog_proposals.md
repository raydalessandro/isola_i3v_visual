# Catalog Proposals — s<NN>

**Data**: <YYYY-MM-DD>
**Schema target**: v1.2
**Catalogo source**: <github_raw | local_snapshot>
**Catalogo generated_at**: <data del catalogo letto>

---

## Sintesi

- Entità inventariate dal nodo s<NN>: <N>
- Entità presenti in catalogo: <X> / <N>
- Entità da AGGIUNGERE al catalogo: <Y> (vedi sezioni dettaglio)
- Schede compilate (>500 char): <A>
- Schede stub (<200 char) candidate ad arricchimento: <B>
- Misalignments rilevati (per `_canon_misalignments.json`): <Q>

## Tabella inventario

| Tipo | ID | In catalogo? | Stato scheda | Azione richiesta |
|---|---|---|---|---|
| personaggio | <id> | sì | compilata | nessuna |
| personaggio | <id> | sì | stub | proposta arricchimento §A |
| luogo | <id> | sì | stub | proposta arricchimento §B |
| oggetto | <id> | NO | — | aggiunta al catalogo §C |
| ... | ... | ... | ... | ... |

---

## A. Arricchimento scheda `<entity_id>` (stub → compilato)

**Path scheda**: `visual/<famiglia>/<...>/<entity_id>/scheda.md`

### Info canoniche emerse dal nodo s<NN>

[Lista delle info che il nodo s<NN> contiene su questa entità e che sono **canoniche** (caratteristiche permanenti) vs **di scena** (specifiche del momento). Solo le canoniche vanno proposte per la scheda.]

- ...

### Patch proposta alla scheda

```markdown
## Aspetto / forma

[Aggiungere/modificare:]
- ...

## Espressione / comportamento

[Aggiungere/modificare:]
- ...
```

### Fonti da citare nella sezione "Riferimenti puntuali"

- `pipeline_narrativa/story_graph.json#stories.s<NN>` (premise, threshold, voice_notes)
- `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md§<X>.<Y>` (se rilevante)

---

## B. Arricchimento scheda `<entity_id>`

[stessa struttura]

---

## C. Aggiunta NUOVA entità al catalogo: `<proposed_id>`

**Famiglia**: luogo | personaggio | oggetto | vento | visual_signature
**Sottotipo**: <es. building, individuale, ecc.>
**Path proposto scheda**: `visual/<famiglia>/<...>/<proposed_id>/scheda.md`

### Motivazione

[Perché va aggiunta. Es. "Il nodo s<NN> cita 'fune di tela' come oggetto centrale di scena, non presente nei 13 oggetti canonici del catalogo."]

### Frontmatter proposto

```yaml
---
id: <proposed_id>
name: <Nome leggibile>
famiglia: <famiglia>
sottotipo: <sottotipo>
status: stub
ultima_modifica: <YYYY-MM-DD>
fonti: ["pipeline_narrativa/story_graph.json#stories.s<NN>"]
appare_in_storie: ["s<NN>"]
---
```

### Contenuto body iniziale

[Solo le sezioni essenziali. Il resto resterà stub fino ad arricchimento futuro.]

---

## D. Misalignments rilevati (per `_canon_misalignments.json`)

[Lista di entry da aggiungere al rolling. Schema: vedi `_canon_misalignments.json._misalignment_schema`.]

```json
{
  "id": "mis_<NNN>",
  "discovered_in_story": "s<NN>",
  "between": "catalog_vs_graph",
  "type": "<type>",
  "catalog_reference": "...",
  "graph_reference": "...",
  "bible_reference": null,
  "description": "...",
  "severity": "media",
  "proposed_resolution": null,
  "status": "open"
}
```

---

## Azione richiesta a Ray

PRIMA di passare a Passata 1:

1. Apri il repo `isola_i3v_visual` localmente.
2. Applica le patch elencate (sezioni §A, §B, §C).
3. Esegui `python3 scripts/build_catalogo_web.py` per rigenerare `catalogo_web/data/entities.json`.
4. Commit + push:
   ```bash
   git add visual/ catalogo_web/
   git commit -m "Fase E s<NN>: arricchimento catalogo (<X> schede + <Y> nuove entità)"
   git push origin main
   ```
5. Conferma in chat: "Repo aggiornato, push fatto."

Quando confermi, l'agente **rifetcha il catalogo** e verifica che le modifiche siano arrivate. Solo dopo verifica positiva procede a Passata 1.

**SE NESSUNA modifica al repo è richiesta**: questo file viene scritto comunque, con sezioni A/B/C/D vuote o con la nota "nessuna modifica richiesta". Il file documenta che la verifica è stata fatta.
