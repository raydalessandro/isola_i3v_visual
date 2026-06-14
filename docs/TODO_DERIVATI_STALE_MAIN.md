# TODO — Derivati stale su `main` (scoperto in sessione, NON risolto qui)

**Stato:** aperto · registrato 2026-06-14 (sessione manutentore montaggio volume) · HEAD `e533771`

## Cosa

Lanciando `make sync` durante la preparazione del branch
`claude/montaggio-volume-spread-e-leggibilita`, il `git status` post-sync ha
rivelato **derivato disallineato su `main`, NON causato dalle modifiche di
questa sessione**:

- **Tutti i 12 `pipeline_narrativa/writing_briefs/sNN_writing_brief.md`** si
  rigenerano con sezioni nuove: `## §2-bis. STATO DEL MONDO` (proiezione
  world-state dal grafo) e `**Immagini canoniche di riferimento:**`. Sono
  output del generatore (`build_writing_brief.py`) mai ricommittati dopo
  l'aggiornamento del generatore. Nota: `PROJECT_STATE.md` afferma già
  "Brief: 12/12 ... con §2-bis", quindi lo stato dichiarato e i byte su main
  divergono.
- **`catalogo_web/data/entities.json`** e **`web/public/data/entities.json`**
  si rigenerano (derivato da `visual/**`, presumibilmente da schede aggiornate
  non ancora sincronizzate).
- **`dashboard/data/dashboard.js`** si rigenera (aggrega quanto sopra).

## Perché NON è stato sistemato in questo branch

Fuori dal perimetro dichiarato (spread orizzontali + leggibilità testo). Foldare
un refresh di 12 brief + catalogo non legato alla feature sarebbe scope creep e
renderebbe la PR illeggibile. I file rigenerati sono stati **revocati** dal
branch; il branch contiene solo sorgenti + test della feature.

## Azione consigliata (sessione manutentore dedicata)

1. Su `main` pulito: `make sync`.
2. Verificare che i diff siano solo rigenerazione attesa (nessun contenuto
   sorgente toccato).
3. Commit dedicato `chore: rigenera derivati stale (briefs §2-bis + entities)`.
4. Allineare la dicitura in `PROJECT_STATE.md` se necessario.

Nessun impatto sul montaggio volume: `build_volume.py` legge i marker `.md` e le
immagini, non i writing_briefs né il catalogo.
