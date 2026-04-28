# `contributi/` — Proposte di aggiunta per le schede

Questa directory accoglie **proposte di aggiunte/modifiche alle schede `visual/`** da parte di collaboratori esterni. Le proposte qui dentro NON modificano direttamente le schede: sono **suggerimenti tracciati** che Ray (o un agente IA in modalità "integratore") leggerà, valuterà e — se approvate — riporterà nelle schede `visual/` con un commit dedicato.

## In sintesi (per chi entra ora)

✅ **Puoi:**
- Leggere tutto il repo (in particolare `visual/`, `pipeline_narrativa/`, `catalogo_web/`).
- Creare **un nuovo file `.md` datato** in questa directory con le tue proposte.
- Fare commit e push del **solo tuo file**.

❌ **Non puoi:**
- Modificare schede esistenti in `visual/` (le tue proposte vivono qui, non là).
- Modificare `pipeline_narrativa/` (grafo + Bible: read-only).
- Modificare `_porting_grafo/` (archivio chiuso).
- Modificare `cartografia/`, `catalogo_web/`, `scripts/`, `skills/`, `README.md`, `CLAUDE.md`, `PROJECT_STATE.md`, `SYNC_LOG.md`.
- Eseguire script Python.
- Creare branch nuovi (lavora su `main`).

Vedi `CLAUDE.md` (radice repo) per le regole complete.

---

## Pattern del nome file

```
<YYYY-MM-DD>_<nome>_<scope>.md
```

Esempi:
- `2026-05-03_anna_aggiunte_schede_personaggi.md`
- `2026-05-10_anna_proposte_oggetti_simbolo.md`
- `2026-05-15_marco_dettagli_burrone_grotta_grunto.md`

**Una sessione di lavoro = un file**. Se torni a lavorare in un altro giorno, crei un nuovo file (così resta tracciato il progresso).

---

## Schema consigliato del file

```markdown
# Aggiunte schede — <NOME> — <YYYY-MM-DD>

## Sommario

[1-3 righe che dicono cosa hai proposto e perché — es. "ho rivisto i 5 cuccioli e proposto dettagli su mannerismi e abbigliamento, basandomi sulla Bible §4.X e su una conversazione con Ray del DD/MM"]

---

## Per scheda: visual/personaggi/individuali/primari/grunto/scheda.md

### Sezione: Espressione / comportamento

**Aggiunta proposta:**
> [Testo che vorresti aggiungere — può essere una frase o un paragrafo]

**Fonte/motivazione:**
- [Da `pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md` §4.8, riga X]
- Oppure: [Conversazione con Ray del DD/MM (riepilogo)]
- Oppure: [Intuizione da revisione catalogo + grafo, vedi `pipeline_narrativa/story_graph.json#stories.s01.characters_in_scene[grunto]`]

### Sezione: Variabilità ammessa

[idem...]

---

## Per scheda: visual/luoghi/quartiere_aria/burrone/scheda.md

### Sezione: Aspetto / forma

**Aggiunta proposta:**
> ...

**Fonte/motivazione:**
- ...

---

## Note generali / domande aperte per Ray

- [Eventuali domande, dubbi, contraddizioni che hai notato nelle fonti]
- [Suggerimenti meta-livello (es. "secondo me la scheda di X ha sezione Y troppo scarna, andrebbe rivista per intero")]
```

---

## Best practice

1. **Cita sempre la fonte.** Se proponi un'aggiunta, deve essere tracciabile a:
   - Un passaggio della Bible (`pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md`).
   - Un campo del grafo (`pipeline_narrativa/story_graph.json`).
   - Una conversazione con Ray (riepilogo + data).
   - Una tua intuizione esplicitata come tale (Ray valuterà).

2. **Una sezione alla volta.** Non aggregare proposte di sezioni diverse della stessa scheda in un blocco unico — separa con `### Sezione: <nome>`.

3. **Niente invenzione narrativa.** Le proposte devono **arricchire** ciò che già esiste, non aggiungere lore nuova senza autorizzazione di Ray.

4. **Niente pattern AI da bandire.** Vedi `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md`. Esempi: "occhi che brillano di saggezza", "infanzia luminosa idilliaca", "fratellanza zuccherosa".

5. **Se in dubbio, chiedi prima di scrivere.** Meglio una domanda a Ray in più che una proposta da scartare.

---

## Workflow git

```bash
# 1. Allineati con main
git pull origin main

# 2. Crea il tuo file
# (esempio: 2026-05-03_anna_aggiunte_schede_personaggi.md)

# 3. Stage + commit + push
git add contributi/<tuo-file>.md
git commit -m "contributi: <nome> aggiunte schede <scope>"
git push origin main
```

**Mai `git push --force`. Mai modificare commit altrui. Mai branch nuovi.**

---

## Cosa succede dopo

1. Ray (o agente IA "integratore") legge il tuo file.
2. Valuta proposta per proposta. Approva, modifica o rifiuta.
3. Le proposte approvate vengono integrate nelle schede `visual/` con commit dedicato (es. `visual: integra aggiunte di <nome> da contributi/<file>`).
4. Il tuo file rimane qui come **trail di audit**: chi ha proposto cosa, quando, perché.
5. Se ti interessa sapere cosa è stato accettato, controlla i commit recenti su `main`.

---

**Domande?** Apri una issue o scrivi a Ray prima di committare se non sei sicuro/a.
