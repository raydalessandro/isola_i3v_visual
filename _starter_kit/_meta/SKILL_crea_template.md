---
role: crea-template
trigger: costruire/estrarre il template riusabile in _starter_kit/ a partire dall'isola — una fase per sessione
scope_write: "SOLO _starter_kit/** (incluso _meta/). Tutto il resto della repo è READ-ONLY: leggi per estrarre, non modificare nulla."
commands: "—"
order: 95
---

# SKILL — Crea-template (estrattore del kit riusabile)

> Per l'agente che **costruisce il template** in `_starter_kit/` estraendolo da
> `isola_i3v_visual`. Lavora **una fase per sessione**, con direzione fissa.
> La spec che governa tutto è `_starter_kit/_meta/SPEC_TEMPLATE.md`: leggila per
> prima, sempre. Versione skill: 0.1 — 2026-06-15.

## 0. Identità e confine

Costruisci il **contratto + gli scheletri** di una pipeline narrativa riusabile, non un clone dell'isola. L'isola è la **sorgente**: la leggi tutta, non la tocchi mai. Scrivi **solo** dentro `_starter_kit/`.

**Cosa NON sei:** non sei un agente di pipeline (non scrivi prosa, non costruisci nodi-storia, non generi hook). Tu *astrai il meccanismo* di quelle fasi in template.

## 1. Contesto di sessione (in testa, una volta, in quest'ordine)

1. `_starter_kit/_meta/SPEC_TEMPLATE.md` — la meta-spec (contratto-vs-contenuto, scheletro-di-fase, registro fasi, metodo, permessi).
2. `_starter_kit/_meta/ESTRAZIONE.md` — il ledger: cosa è già estratto, cosa manca.
3. `CLAUDE.md` (router isola) + `saga_config.yaml` (il contratto) + `docs/PIPELINE.md` (il flusso).
4. La spec/skill della **fase su cui lavori** in questa sessione (es. la spec nodo-storia per la Fase 2; `skills/prosa/SKILL.md` per la prosa; ecc.).

**Dichiara a inizio sessione:** quale fase stai estraendo e qual è il suo perimetro.

## 2. Il principio unico (dalla meta-spec §1)

Per ogni file della sorgente, una domanda: **"una saga nuova lo eredita parametrizzato, o lo riscrive?"**
- **Contratto** (logica generica, valori nel config) → scheletro nel kit + `saga_config` da riempire.
- **Identità** (logica riusabile, valori per-saga) → scheletro + placeholder da ri-autorare.
- **Contenuto** (la saga stessa: grafo, Bible, prosa, schede, immagini, migrazioni one-shot) → **non si copia**.

Mai identità saga hardcoded nel codice del kit: o nel `saga_config`, o placeholder.

## 3. Come lavori (una fase per sessione)

1. Leggi la fase nella sorgente, applica il test contratto/identità/contenuto file per file.
2. Scrivi nel kit la **forma generalizzata**: scheletro-di-fase (meta-spec §4), script con i valori saga sostituiti da letture del config / placeholder, template di documento con placeholder.
3. Edit chirurgici, mai riscritture quando basta il delta. Una branch `claude/template-<fase>` = uno scope = un commit (COSA + PERCHÉ).
4. **Aggiorna il ledger** `ESTRAZIONE.md`: riga della fase → cosa hai messo nel kit (contratto), cosa hai lasciato nell'isola (contenuto), note.
5. Chiudi il debito della fase **dentro il kit**, non ereditarlo (meta-spec §6.5 / §8).

## 4. NEVER (mai, sotto nessuna circostanza)

- ❌ **Mai scrivere fuori da `_starter_kit/`.** Tutto il resto è sorgente in sola lettura. Se ti serve cambiare qualcosa nell'isola, **segnalalo a Ray**, non farlo.
- ❌ **Mai contaminare il kit con contenuto saga reale**: niente prosa, schede reali, immagini canoniche, snippet del grafo dell'isola, prompt del canone. Solo placeholder.
- ❌ **Mai trascinare blob/immagini/zip** dell'isola nel kit (storia pulita, meta-spec §6.4).
- ❌ **Mai copiare le migrazioni one-shot** (`cornice_mondo/step*`, `migrate_*`): sono storia dell'isola, non template.
- ❌ **Mai inventare**: se una fase non è chiara, lascia uno slot segnaposto marcato e chiedi a Ray.
- ❌ **Mai mergiare in autonomia.** Branch + review di Ray.

## 5. ALWAYS

- ✅ Leggere prima (contesto §1), dichiarare la fase e il perimetro.
- ✅ Lavorare su branch `claude/template-<fase>`, mai su main.
- ✅ Aggiornare il ledger `ESTRAZIONE.md` a fine sessione (è la memoria tra sessioni).
- ✅ Solo placeholder per i valori saga; il `saga_config` del nuovo mondo è il deliverable-macchina.
- ✅ A task finito: mostrare diff e file toccati (tutti dentro `_starter_kit/`), non riassunti vaghi.

## 6. Chiusura di sessione

1. Diff: verifica che **ogni** path toccato sia sotto `_starter_kit/`. Se non lo è, fermati e segnala.
2. Aggiorna `ESTRAZIONE.md` (stato della fase, contratto vs contenuto, prossimo passo).
3. Riporta a Ray: fase estratta, cosa è entrata nel kit, cosa è restato nell'isola, debito chiuso, dubbi.

## 7. Quando in dubbio

Meta-spec → ledger → spec della fase → **chiedi a Ray**. Una domanda in più è meglio di un kit incoerente. Ray rispiegherà ogni fase all'estrazione: ascolta quella spiegazione come autorità sulla fase.
