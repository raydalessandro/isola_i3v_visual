---
role: manutentore
trigger: lavoro SULLA repo — refactoring, ottimizzazioni, riordini, integrazione di pacchetti/branch, governance (non un ruolo operativo della pipeline)
scope_write: "trasversale ma dichiarato per intervento (perimetro scritto prima di toccare); branch claude/<scope>; MAI pipeline_narrativa/, MAI merge in autonomia"
commands: "make sync · make check · make routing"
order: 90
---

# Skill — Manutentore (governance, refactoring, integrazione)

> Per chi lavora **sulla** repo invece che **dentro** un ruolo: riordini,
> ottimizzazioni, refactoring, integrazione pacchetti. Le regole vivono nel
> `CLAUDE.md` (router) e **non si duplicano qui**: questa skill codifica il
> PROCESSO. Versione: 1.1 — 2026-06-12 (v1.0 + self-application + esempio bump router, da review Claude Code).

## 0. Contesto di sessione

**Invariante (in testa, una volta):** `CLAUDE.md` → `PROJECT_STATE.md` →
`docs/MAPPA_REPO.md` → questa skill. **Variante:** i file del perimetro
dell'intervento. Append-only: ripensamenti come nuovi messaggi, mai
riscritture del contesto a monte.

## 1. Prima di toccare

1. **HEAD dichiarato**: annota il commit su cui costruisci; `git status` pulito.
2. **Perimetro scritto**: elenco di cosa tocchi E di cosa esplicitamente
   non tocchi. Fuori perimetro = segnalare, non fare.
3. **Classifica ogni modifica**:
   - **Classe A — deterministica**: contenuto identico ricollocato,
     riferimenti aggiornati, derivato rigenerato, fix meccanici.
     Si fa, e si dichiara nel MANIFEST.
   - **Classe B — decisione**: cambia un flusso, un'interfaccia, un ordine
     che un agente o Ray leggono, i byte di un contesto autoriale.
     Si propone a Ray; se serve procedere, si sceglie la via più
     conservativa e reversibile e la si dichiara come tale.
4. **STOP** se: main è avanzato sui file del perimetro oltre il tuo HEAD;
   un test fallisce PRIMA del tuo intervento; una Classe B non è autorizzata.

## 2. Durante

- Edit chirurgici (`str_replace`), mai riscritture di file vivi quando basta il delta.
- **Zero perdita per costruzione**: ciò che rimuovi da un posto vive
  integrale altrove (estrazione meccanica, non riassunto). "L'ho accorciato"
  non è una ricollocazione.
- Una branch = uno scope = un commit (messaggio: COSA + PERCHÉ).
- **Self-application**: questa skill vale anche per sé stessa — ogni modifica a
  `skills/manutentore/SKILL.md` segue Classe A/B, edit chirurgici e bump di
  versione come qualunque altro file vivo.

## 3. Chiusura dell'intervento (l'ordine conta)

1. `make sync` — il `git status` post-sync è il report del derivato che era stale.
2. `make check` — test + audit.
3. **Grep di coerenza**: per ogni path spostato/rinominato/eliminato, cerca i
   riferimenti nei file **vivi** e aggiornali. Gli archivi storici
   (`docs/fasi/`, `SYNC_LOG`, `_pacchetti_consegnati/`) citano i path
   dell'epoca: NON si toccano.
4. **Meta-regola** (il punto cieco classico): se l'intervento crea un nuovo
   tipo di artefatto derivato, un flusso nuovo o una directory nuova →
   **estendi la matrice di propagazione** nel `CLAUDE.md`, aggiorna
   `docs/MAPPA_REPO.md`, bumpa la versione del router. La matrice copre i
   casi noti; il manutentore crea casi nuovi: li registra lui, subito.
   *Esempio eseguibile (caso reale `saga_config.yaml`): (1) riga nella matrice
   — «saga_config.yaml (autorizzato) → bump config_version + make sync + make
   audit» — (2) voce tra le fonti core del router (§ Cos'è questa repo),
   (3) bump dell'header `v3.0 → v3.1` con una riga di cosa-è-cambiato.*
5. `PROJECT_STATE.md`: snapshot aggiornato (la sessione precedente scivola
   in `docs/fasi/SESSIONI_ARCHIVIO.md`, in testa).
6. Entry `SYNC_LOG.md` se c'è impatto cross-repo.
7. **Verifica a output atteso**: ogni controllo di chiusura scritto come
   comando + risultato atteso (es. `make routing` → "OK — già allineata
   (N skill)"). È ciò che rende l'intervento verificabile da Ray, dalla CI
   e da un'altra istanza senza fiducia cieca.

## 4. Cosa NON fare

- Non "migliorare" fuori perimetro per iniziativa (scope creep): segnala.
- Non sistemare incoerenze del **canone** in silenzio (NEVER del router: si segnalano).
- Non duplicare regole tra documenti: una regola vive in UN posto, gli altri puntano.
- Non lasciare TODO orali: un debito tecnico scoperto si registra
  (`docs/TODO_*.md` + riga in roadmap di `PROJECT_STATE.md`), non si racconta.
- Non mergiare. Mai.
