---
role: atlantista
trigger: produrre le tavole-atlante full-page (prompt Manus + selezione + ingest) per le pagine abitanti/luoghi dei volumi
scope_write: "visual/atlante/ (tavole, prompt; spec SOLO via ingest_tavola.py) — branch claude/atlante-*"
commands: "python3 scripts/ingest_tavola.py <manifest> · pytest tests/test_atlante.py"
order: 55
---

# Skill — Agente atlantista

> Ramificazione della skill **illustratore** (`skills/illustratore/SKILL.md`).
> Per istanze IA o collaboratori che producono le **tavole-atlante**: pagine
> full-page in cui il soggetto vive nel suo posto sull'isola (Fiamma al
> Forno, Grunto al Burrone) e una zona della composizione resta quieta per
> il testo che la pipeline sovrappone.
>
> Versione: 1.0 — 2026-06-12

---

## TL;DR (in 60 secondi)

1. **La verità è in `visual/atlante/ATLANTE_SPEC.json`**: voce → variante
   assegnata (ritmo A C B D). Non scegliere la variante: leggerla.
2. **Prompt = 3 blocchi**: SAGA STYLESHEET (identico, sempre) + descrittori
   autorizzati dalla scheda canonica + blocco composizione dal template
   `visual/atlante/template/variante_<X>.md`. Mai descrittori dal training.
3. **Reference da allegare a Manus**: le immagini canoniche del catalogo
   (`visual/<categoria>/<id>/immagini/`, preferire `_hd/`).
4. **Output = immagine + manifest** (`tavole/<slug>_tavola_v1.jpg` +
   `tavole/<slug>_tavola_v1.json`). La dichiarazione non basta:
   `scripts/ingest_tavola.py` la verifica (dimensioni, quiete misurata
   delle zone testo) e solo allora scrive lo spec.
5. **Selezione umana prima dell'ingest**: checklist sotto. Ray approva.
6. **Branch + PR come l'illustratore**: una branch per scope
   (es. `claude/atlante-vol1`), un commit, niente merge in autonomia.
7. **Test sempre**: `python3 -m pytest tests/test_atlante.py -q` dopo ogni
   ingest. Il volume si monta comunque (fallback al layout classico).

---

## 0. Contesto di sessione — invariante e variante

L'efficienza (cache) e la qualità (zero ricerche, zero dubbi) di questo ruolo
dipendono da COME carichi il contesto, non solo da cosa contiene.

**Invariante di sessione** — si legge UNA volta, in quest'ordine, in testa,
e non si ritocca più (le correzioni sono nuovi messaggi, mai modifiche a monte):

1. questa SKILL
2. `visual/atlante/ATLANTE_SPEC.json` (la verità: voci, varianti, ritmo)
3. `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md`
4. **tutti e quattro** i template `visual/atlante/template/variante_{A,B,C,D}.md`
   — il ritmo A C B D li ruota: ognuno serve una voce ogni quattro, quindi si
   caricano subito tutti, non uno alla volta quando capita.

**Variante per voce** — l'unica cosa che cambia tra una voce e l'altra:
la voce dello spec (slug, variante assegnata) + `scheda.md` del personaggio
+ `scheda.md` del luogo-dimora (+ reference immagini da allegare a Manus).

**Una sessione = un volume intero.** Componi i prompt di tutte le voci del
volume in fila: l'invariante si paga una volta, ogni voce aggiunge solo le
sue schede. Non spezzare la sessione per voce.

> Nota sui due livelli: quest'ordine ottimizza il **contesto dell'agente**
> (è lì che lavora la cache). L'ordine dei 3 blocchi nel **prompt per Manus**
> resta quello del §2 (stylesheet → soggetto → composizione): quello serve
> alla resa dell'immagine, non alla cache — non invertirli per analogia.


## 1. Flusso per ogni voce

```
ATLANTE_SPEC.json ──→ voce (slug, variante, volume)
        │
        ▼
scheda canonica (visual/<categoria>/<id>/scheda.md)
        │  solo descrittori autorizzati: aspetto, firma visiva, dimora
        ▼
PROMPT = STYLESHEET + descrittori + template/variante_<X>.md
        │  + reference immagini canoniche allegate
        ▼
Manus ──→ N candidate
        │
        ▼
SELEZIONE UMANA (checklist §3) ──→ 1 tavola scelta
        │
        ▼
tavole/<slug>_tavola_v1.jpg + <slug>_tavola_v1.json (manifest)
        │
        ▼
python3 scripts/ingest_tavola.py tavole/<slug>_tavola_v1.json
        │  verifica meccanica: dimensioni, quiete zone, ritmo
        ▼
ATLANTE_SPEC.json aggiornato ──→ pytest ──→ build_volume.py la usa da solo
```

Stesso pattern della pipeline storie: giudizio a monte (scheda, selezione),
estrazione meccanica a valle (ingest, montaggio). Human-in-the-loop
intenzionale tra generazione e ingest.

## 2. Composizione del prompt

Ordine dei blocchi, senza omissioni:

1. **SAGA STYLESHEET v1** — da `_visual_pipeline/_canone/01_SAGA_STYLESHEET_v1.md`,
   incollato identico, con il negative prompt globale. Vale anche qui:
   le tavole-atlante sono pagine del libro, stesso stile della saga.
   *Qualunque deroga di stile (es. resa "taccuino sepia") è una decisione
   consapevole di Ray e va versionata nello stylesheet, mai improvvisata.*
2. **Soggetto e ambiente** — SOLO descrittori autorizzati dalla scheda
   (`scheda.md` del personaggio + `scheda.md` del luogo-dimora). Il
   soggetto va mostrato nel suo posto: la dimora o uno scorcio canonico
   del quartiere. Niente riempitivi dal training del modello.
3. **Blocco composizione** — copiato dal template della variante assegnata
   (`visual/atlante/template/variante_<X>.md`): definisce dove sta il
   soggetto, dove resta lo spazio quieto diegetico (cielo, nebbia, muro,
   prato), il divieto assoluto di testo, formato e risoluzione.

## 3. Checklist di selezione (umana, prima dell'ingest)

- [ ] Zero testo o pseudo-scrittura, ovunque, anche minuscola
- [ ] Zona quieta davvero quieta E diegetica (cielo/nebbia/muro, non carta
      bianca incollata): l'ingest la misura, ma l'occhio decide prima
- [ ] Soggetto coerente con le reference canoniche (colori, firma visiva,
      anatomia, proporzioni rispetto alle altre specie)
- [ ] Ambiente coerente con la scheda luogo (Forno, Burrone, ecc.)
      e con la fisica dell'isola (geografia, ora del giorno plausibile)
- [ ] Stile = SAGA STYLESHEET (niente derive sepia/3D/flat)
- [ ] Risoluzione ≥ 1748×2480, verticale, JPEG q95 RGB

## 4. Cosa NON fare

- NON scrivere direttamente in `ATLANTE_SPEC.json`: passa da
  `ingest_tavola.py` (è lui che verifica e scrive).
- NON cambiare variante per gusto compositivo senza segnalarlo: il ritmo
  A C B D è blindato dai test; l'ingest avvisa se lo rompi.
- NON toccare i trafiletti (`presentazioni_parziali.md`): se il testo non
  entra, il problema è della variante o del trafiletto, e decide Ray.
- NON usare `--force` dell'ingest in autonomia: è riservato ai casi in cui
  la selezione umana ha approvato una zona "tecnicamente" non quieta.
- NON caricare le candidate scartate nella repo: solo la selezionata.

## 5. Riferimenti

- `visual/atlante/README.md` — contratto della sezione
- `visual/atlante/ATLANTE_SPEC.json` — la verità (varianti, voci, ritmo)
- `visual/atlante/template/variante_{A,B,C,D}.md` — blocchi composizione
- `scripts/ingest_tavola.py` — ingest meccanico con verifica
- `tests/test_atlante.py` — invarianti blindate
- `skills/illustratore/SKILL.md` — regole comuni (formato, branch, PR)
