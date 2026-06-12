# Atlante degli Abitanti — Tavole a pagina piena

**Stato:** infrastruttura pronta, tavole in produzione (Manus)
**Verità:** `ATLANTE_SPEC.json` — lo script di montaggio legge solo da lì.
**Skill operativa:** `skills/atlantista/SKILL.md` (ramificazione dell'illustratore)

## Cos'è

Le pagine-atlante dei volumi (galleria abitanti/luoghi) passano dal layout
classico (ritratto in cornice + colonna di testo) a **pagine in cui la
tavola È la pagina**: il soggetto vive nel suo posto sull'isola (Fiamma al
Forno, Grunto al Burrone), in stile SAGA STYLESHEET, e una zona della
composizione resta **spazio quieto diegetico** (cielo, nebbia, muro
intonacato, prato) dove la pipeline sovrappone il testo. Niente immagine
montata su carta: un tutt'uno.

Principio invariato: **design-back from the answer**. Le zone di testo
sono definite PRIMA (le 4 varianti in `ATLANTE_SPEC.json`); Manus riceve
il template della variante assegnata, compone la scena di conseguenza e
**dichiara** cosa ha fatto in un manifest JSON. La dichiarazione non
diventa mai verità diretta: `scripts/ingest_tavola.py` la **verifica**
(dimensioni, quiete misurata delle zone testo) e solo allora scrive lo
spec. Il testo lo piazza la pipeline, mai il modello immagine.

## Struttura

```
visual/atlante/
  ATLANTE_SPEC.json     ← verità: varianti di layout + assegnazioni voce→variante/tavola
  README.md             ← questo file
  template/
    variante_{A,B,C,D}.md       ← blocco composizione per Manus + contratto manifest
  prompt/
    _TEMPLATE_prompt_manus.md   ← schema del prompt a 3 blocchi
    <slug>_prompt_manus.md      ← un prompt per voce (prototipo: fiamma)
  tavole/
    <slug>_tavola_v1.jpg        ← tavola selezionata, SENZA TESTO
    <slug>_tavola_v1.json       ← manifest dichiarato dal generatore
```

## Le quattro varianti (il ritmo)

| Variante | Nome       | Figura            | Testo                    |
|----------|------------|-------------------|--------------------------|
| A        | riva       | destra            | colonna sinistra         |
| B        | controriva | sinistra          | colonna destra           |
| C        | radura     | metà alta         | fascia piena in basso    |
| D        | cielo alto | metà bassa        | fascia piena in alto     |

Ritmo: ciclo `A C B D` sulle voci di tipo `tavola`, nell'ordine del volume.
Mai due varianti uguali consecutive (blindato dai test). La voce "Questa è
l'isola" resta la mappa cartografica (tipo `mappa`, nessuna tavola).

## Flusso di lavoro per ogni voce

1. Leggere la voce in `ATLANTE_SPEC.json` (variante assegnata, ritmo A C B D).
2. Compilare il prompt a 3 blocchi (`prompt/_TEMPLATE_prompt_manus.md`):
   SAGA STYLESHEET + descrittori autorizzati dalle schede canoniche
   (personaggio E luogo-dimora) + blocco composizione da
   `template/variante_<X>.md`. Allegare le reference del catalogo.
3. Generare con Manus. **Pass di selezione umano** (checklist nella skill):
   zero pseudo-scrittura, zona quieta davvero quieta e diegetica, canone
   rispettato, stile saga.
4. Salvare `tavole/<slug>_tavola_v1.jpg` (min 1748×2480, JPEG q95, RGB)
   + manifest `tavole/<slug>_tavola_v1.json`.
5. `python3 scripts/ingest_tavola.py visual/atlante/tavole/<slug>_tavola_v1.json`
   — verifica meccanica e aggiornamento dello spec. Mai a mano.
6. `python3 -m pytest tests/test_atlante.py -q`, poi
   `python3 scripts/build_volume.py --volume N` — lo script usa la tavola
   automaticamente; le voci senza tavola cadono sul layout classico
   (degradazione dolce, il volume si monta sempre).

## Note di canone

- Il campo `binomio` (pseudo-binomio latino, es. *Ardea ventistria*) è
  previsto nello schema ma **null finché Ray non approva i nomi**: è canone
  nuovo, non si inventa in pipeline. Quando approvato, comparirà sotto il
  nome nella pagina.
- Stria: HOLD sulla reference HD (in volo) — la tavola va generata con posa
  a terra.
- Il testo dei trafiletti resta quello di `presentazioni_parziali.md`,
  invariato: cambia solo la veste.

## Test

`tests/test_atlante.py` blinda: schema uniforme della spec, zone in [0,1]
e non sovrapposte, copertura di tutte le voci della presentazione parziale,
ritmo senza ripetizioni consecutive, capienza delle zone per i trafiletti
reali (render di tutte le voci senza overflow), determinismo, fallback al
layout classico, warning per tavole sotto spec.
