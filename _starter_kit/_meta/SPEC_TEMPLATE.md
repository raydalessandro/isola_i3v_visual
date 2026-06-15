# SPEC — Template della pipeline narrativa (meta-spec)

**Versione:** 0.1 (bozza di lavoro)
**Data:** 2026-06-15
**Scope:** definisce *come* si estrae da `isola_i3v_visual` un template riusabile per produrre nuove saghe. Non è il template; è la spec che governa la sua costruzione, fase per fase, in sessioni separate.
**Stato:** scaffold di direzione. Le singole fasi verranno specificate e rispiegate da Ray al momento dell'estrazione.

> Questa cartella `_starter_kit/_meta/` è **materiale di build**: dirige chi costruisce il kit. **Non viaggia** nella saga istanziata (si scarta all'istanziazione). Il kit "vero" è il resto di `_starter_kit/`.

---

## §0. Cos'è il template — e cosa NON è

Il template **non è un clone dell'isola**. È:
1. il **contratto** machine-readable (`saga_config.yaml`) che ogni script legge;
2. un insieme di **spec-di-fase** che seguono uno scheletro comune (§4);
3. gli **scheletri di script** deterministici (reader/writer/audit) parametrizzati dal contratto;
4. i **template di documento** (schede, prompt, brief) con placeholder;
5. le **skill** delle fasi, con i riferimenti hardcoded alla saga sostituiti da placeholder.

Non è, e non deve diventare: il grafo reale, la Bible reale, la prosa, le immagini, la storia git dell'isola. Quello è **contenuto**, resta nell'isola.

## §1. Il principio cardine — CONTRATTO vs CONTENUTO

Per ogni file, una sola domanda: **"una saga nuova lo ri-esegue/eredita, o lo riscrive?"**

| Categoria | Test | Esempi | Va nel kit come |
|---|---|---|---|
| **Contratto** (eredita parametrizzato) | la logica è generica, i valori stanno nel config | audit 1-5, `saga_canon`, `write_hooks`, brieffer, reader world-state | script invariato + `saga_config` da riempire |
| **Identità** (riscrive lo specifico, tiene lo scheletro) | la *logica* è riusabile, i *valori* sono per-saga | `build_volume`, `design_system` (palette, font, glifi) | scheletro + segnaposto identità |
| **Contenuto** (non si copia) | è la saga stessa | grafo, Bible, prosa, schede, immagini, migrazioni one-shot | **nulla** — resta nell'isola |

Regola d'oro: **niente identità saga hardcoded nel codice del kit.** O sta nel `saga_config`, o è un placeholder da ri-autorare. (Nell'isola ci sono ~34 stringhe hardcoded in `build_volume`/`design_system`: sono il confine di lavoro della fase di astrazione presentazione.)

## §2. Il contratto — `saga_config.yaml`

È la **cucitura** dove la saga si stacca dal motore. Single source machine-readable: id, enum, lessico/quote, grammatica marker, quadranti, paths, schema-versioni attese. Caricato da `scripts/saga_canon.py`, consumato dagli audit + writer + dashboard.

Invarianti per il kit:
- ogni fase **legge** il config; nessuna fase duplica i suoi valori altrove;
- la **Fase 1 (seeding) produce il `saga_config` del nuovo mondo** come deliverable-macchina primario (vedi §5);
- estendere il config è un atto di canone: bump `config_version` + `make sync` + `make audit`.

**Debito noto da chiudere nel kit** (lo nomina la spec Fase 2 §15.8): gli enum `deployment_level`, `time_span.arc`, `presence.state`, `entry_point_type`, `closure_type`, `register` devono entrare in `saga_config` quando la fase nodo-storia entra in repo.

## §3. Metodo condiviso (le invarianti d'ingegneria, valgono per tutte le fasi)

Estratte dalla pratica dell'isola (principi P1-P7 della spec Fase 2). Ogni fase le rispetta:

- **P1 — Fattorizzazione è architettura.** I ruoli si separano dal primo schema (es. strutturatore/critico), non come ottimizzazione tardiva.
- **P2 — Cache-native.** Input ordinati in blocco invariante (system, byte-identico tra le N storie) + blocco variante (da script). Mai elementi dinamici nell'invariante.
- **P4 — Review umana nel loop.** I checkpoint umani sono parte del flusso, non un'eccezione.
- **P5 — Mandate frazionate.** Output a blocchi, mai one-shot lungo (un errore al 10% non deve rigenerare tutto).
- **P6 — Niente esplorazione.** L'agente riceve il contesto instradato da script, non clona/esplora la repo.
- **P7 — Ogni regola esprimibile come script va nello script.** Il giudizio LLM resta solo dove non è sostituibile (la stessa conversione "bisogno-LLM → check meccanico" che ha reso deterministico l'audit drift e gran parte della fisica §13 della Fase 2).
- **Idempotenza + scritture atomiche + backup** in ogni script che tocca il grafo.
- **Audit come cancello a cricchetto**: le incoerenze note possono solo diminuire; ogni nuova blocca.

## §4. Scheletro standard di spec-di-fase

Ogni fase si specifica con **questa stessa forma** (modello aureo: la spec Fase 2 nodo-storia). È ciò che tiene coerenti le sessioni separate.

```
§0  Collocazione nel flusso (a monte / questa fase / a valle)
§1  Firma dei ruoli (P1 — input invariante I, input variante v, output)
§2  Architettura cache-nativa (Blocco A invariante / Blocco B variante)
§3  Output — il contratto della fase (campi: giudizio-LLM / derivabili-script / metadata)
§4  Confine giudizio / determinismo (tabella: chi fa cosa, natura)
§5  Procedura — mandate frazionate
§6  Punti di escalation ("fermati e chiedi se…")
§7  Reader (estrazione Blocco B, deterministico)
§8  Writer (scrittura nel grafo, calco di write_hooks: controlli, backup, dry-run, idempotente)
§9  Test di accettazione (verità a terra: ricostruisci un risultato noto)
§10 TODO fasi successive · §11 Domande aperte per Ray
```

## §5. Registro delle fasi (la pipeline)

Mappa viva. Stati: ⬜ da fare · 🟡 spec/skill parziale · ✅ in repo.

| # | Fase | Ruolo | Stato | Artefatto di riferimento |
|---|---|---|---|---|
| **1** | **Seeding conversazionale** | chat vergine che dialoga con l'umano e **riempie grafo + documenti autoriali + `saga_config`** del nuovo mondo. Più riempie, più semplice la Fase 2. | ⬜ da istituzionalizzare | (nessuno ancora — vedi nota) |
| **2** | **Costruzione nodo-storia** | strutturatore (+critico) compone la struttura narrativa del nodo, tra Tappa 1 e Tappa 2. §13 fisica deterministica, §14 livelli frattali L0-L3. | 🟡 spec v0.2 pronta (non in repo) | `SPEC_FASE_STRUTTURA_STORIA` (di Ray) |
| **2b** | Estrazione 10 hook (Tappa 2) | agente hook legge il nodo-storia, propone gli hook | ✅ prompt | `pipeline_narrativa/prompts/PROMPT_AGENTE_HOOK_ESTENSIONE_v1.md` |
| **2c** | Audit grafo (Tappa 5) | 5 audit deterministici, cancello CI | ✅ in repo | `scripts/audit/`, `make audit` |
| **3** | Brief (zero-token) | assembla il brief autosufficiente per la prosa | ✅ in repo | `scripts/build_writing_brief.py`, skill `brieffer` |
| **4** | Prosa (Tappa 6) | scrittura collaborativa una-pagina-alla-volta | ✅ skill | `skills/prosa/SKILL.md` |
| **5** | Presentazione / build volume | composizione PDF KDP | ✅ codice (identità da ri-autorare) | `build_volume.py`, `design_system.py` |
| **V** | Pipeline visual (parallela) | canonizzazione schede + immagini canoniche, 6 fasi | ✅ in repo | `_visual_pipeline/` |
| **O** | Orchestratore | concatena le tappe fermandosi ai checkpoint umani | ⬜ ultimo | `skills/pipeline_storia.md` (da creare) |

**Nota Fase 1 (caveat repo-vuoto):** il prompt di seeding va scritto per il caso *"documenti placeholder da elicitare e riempire"*, non per il caso isola *"documenti già pieni da leggere"*. Sono due prompt diversi; quello dell'isola, copiato nel kit, non funziona. Deliverable di Fase 1: `saga_config` popolato + Bible/Carta Voce/Archi/Pattern AI/METODO istanziati + grezzo iniziale nel grafo.

**Nota Orchestratore:** si fa per ultimo, quando tutte le fasi sono montate e visibili; la pipeline è sequenziale con checkpoint umani, quindi la skill è semplice da chiudere a quel punto.

## §6. Metodo di estrazione (come si costruisce il kit)

1. **Contract-first.** Prima di tutto: questo `SPEC_TEMPLATE.md` + il router del kit. Ogni sessione-fase li legge e li obbedisce. Antidoto alla deriva tra sessioni.
2. **Una fase per sessione.** L'agente sa in quale fase è, resta nel perimetro, non reinventa le fasi esistenti.
3. **Ledger unico** (`ESTRAZIONE.md`): ogni sessione registra cosa ha estratto (contratto) e cosa ha lasciato (contenuto). È la memoria condivisa tra sessioni.
4. **Storia pulita.** Il kit nasce a storia git nuova: **mai trascinare blob/immagini/zip dell'isola.** (La storia pesante dell'isola è storia di *costruzione*; il kit si *usa*, non si clona.)
5. **Risolvere il debito DENTRO il kit, non ereditarlo.** Es. i file generati committati con timestamp (`dashboard.js`, `entities.json`) causano conflitti su branch paralleli → nel kit si chiude (merge-driver `.gitattributes` o niente timestamp volatile committato), così non si propaga a ogni saga.
6. **Branch sempre.** Mai sul main dell'isola.

## §7. Modello di permessi (per l'agente crea-template)

L'agente che costruisce il kit:
- **scrive SOLO dentro `_starter_kit/`** (incluso `_meta/`);
- **legge tutto il resto** della repo (è la sorgente da cui estrae);
- **non modifica NULLA** fuori da `_starter_kit/`.

Enforcement:
- **Soft (sempre):** codificato nel frontmatter `scope_write` e nelle NEVER della skill `crea-template`.
- **Hard (consigliato):** regola in `.claude/settings.json` che nega Write/Edit fuori da `_starter_kit/`:
```json
{
  "permissions": {
    "deny": [
      "Write(//home/user/isola_i3v_visual/**)",
      "Edit(//home/user/isola_i3v_visual/**)"
    ],
    "allow": [
      "Write(//home/user/isola_i3v_visual/_starter_kit/**)",
      "Edit(//home/user/isola_i3v_visual/_starter_kit/**)"
    ]
  }
}
```
(Da applicare con la skill `update-config` quando si apre il lavoro template — non applicato qui per non toccare la config globale senza richiesta.)

## §8. TODO / debito da chiudere nel kit (non ora)

1. File generati committati → conflitti su branch paralleli: chiudere nel kit (vedi §6.5). Si lega alla sessione web.
2. `build_volume`/`design_system`: separare identità (config/placeholder) da logica (scheletro) — sessione dedicata.
3. Enum nuovi della Fase 2 in `saga_config` (§2).
4. Orchestratore (`skills/pipeline_storia.md`) — ultimo.

## §9. Domande aperte per Ray

1. Posizione definitiva dei materiali di build: `_starter_kit/_meta/` va bene, o preferisci `docs/` / una repo separata per il kit?
2. La Fase 1 (seeding) produce il `saga_config` direttamente, o passa da un documento intermedio che uno script traduce in config?
3. Enforcement permessi: solo soft (skill), o anche hard (settings.json) fin da subito?
4. Il kit lo estrai *in questa repo* (`_starter_kit/`) o come repo nuova fin dall'inizio (storia pulita nativa)?

---

**FINE meta-spec v0.1 — scaffold di direzione, da rispiegare per fase all'estrazione.**
