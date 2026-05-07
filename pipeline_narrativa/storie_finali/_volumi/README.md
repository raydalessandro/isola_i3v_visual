# `_volumi/` — Cornice editoriale 4 volumi

Tutto il materiale che precede e segue le 12 storie del libro, organizzato per i **4 volumi** della saga (uno per ciclo, 3 storie per volume).

Le storie definitive vivono accanto a questa cartella, in `pipeline_narrativa/storie_finali/sNN_<slug>.md`.

## Mappa volumi → cicli → storie

| Volume | Ciclo grafo | Etichetta editoriale¹ | Stagione | Vento | Storie |
|---|---|---|---|---|---|
| Volume 1 | A | Distinguere | inverno → primavera | Taglio | s01, s02, s03 |
| Volume 2 | B | Connettere | primavera → estate | Intreccio | s04, s05, s06 |
| Volume 3 | C | Cambiare | estate → autunno | Mulinello | s07, s08, s09 |
| Volume 4 | D | Integrazione | autunno → inverno | tutti e tre | s10, s11, s12 |

¹ Il pacchetto v1 originale usava simboli `Δ / ⇄ / ⟳ / Integrazione`. **Decisione 2026-05-05 (Ray): sostituiti con A / B / C / D** (i simboli sono troppo "EAR-leggibili", e EAR resta invisibile). **Sostituzione applicata 2026-05-07** ai 5 file di questa cartella (`introduzioni_cicli.md`, `porte.md`, `stato_zero_e_sigilli.md`, `presentazioni_parziali.md`, `PIANO_EDITORIALE_4VOLUMI_v1.md`). Il resto della repo (`documenti_progetto/`, `story_graph.json`, `writing_briefs/`, `visual/`) conserva ancora i simboli originali perché lì hanno funzione canonica/diagnostica e non finiscono nei libri pubblicati.

## Struttura di ogni volume (7 sezioni)

```
1. SOGLIA                  → soglia.md (identica in tutti i 4)
2. INTRODUZIONE AL CICLO   → introduzioni_cicli.md § "VOLUME N"
3. STATO ZERO              → stato_zero_e_sigilli.md § "VOLUME N"
4. LE 3 STORIE             → pipeline_narrativa/storie_finali/sNN_<slug>.md
5. PRESENTAZIONE PARZIALE  → presentazioni_parziali.md § "VOLUME N"
6. LE PORTE                → porte.md § "VOLUME N"
7. CHIUSURA:
   ├─ Volumi 1-2-3         → stato_zero_e_sigilli.md § "SIGILLO Vol N → Vol N+1"
   └─ Volume 4             → congedo.md (solo qui)
```

## File in questa cartella

### Bozze editoriali (modificare qui)

| File | Contenuto | Note |
|---|---|---|
| `PIANO_EDITORIALE_4VOLUMI_v1.md` | piano operativo: visione, ordine di scrittura, riserva (Pirandello), file da produrre | doc di pianificazione, riferimento storico |
| `soglia.md` | apertura — "Prima di leggere" — identica in tutti e 4 | estratta da `.docx`, solo voce-narratore |
| `introduzioni_cicli.md` | 4 introduzioni (una per volume), ~150-200 parole, voce-isola | marker `## VOLUME N` interni |
| `stato_zero_e_sigilli.md` | 4 stato zero (apertura ciclo, doppia illustrazione + trafiletto) + 3 sigilli (chiusura tra volumi, 2-3 righe) | marker `## VOLUME N` + `## SIGILLO Vol N → Vol N+1` |
| `presentazione_completa.md` | **sorgente unica** delle 23 doppie pagine (mappa, Villaggio, quartieri, case, gruppi, mercato) | estratta da `.docx` |
| `presentazioni_parziali.md` | 4 presentazioni assemblate per ciclo (sottoinsieme di `presentazione_completa.md`); doppie 1+2 ricorrono in tutti i volumi | marker `## VOLUME N` |
| `porte.md` | 4 sezioni "Le Porte" — apertura comune + tracce bambini per volume (9 totali + 1 egizio senza libro) + avvertenza sui libri da non leggere; nota finale Ray solo Vol 4 | marker `# VOLUME N` |
| `congedo.md` | chiusura — "A te che torni" — solo Volume 4 | estratto da `.docx` |

### `_elementi_fissi/` — riferimenti read-only

File originali consegnati da Ray nel pacchetto, conservati per traccia/audit. **Non modificare.**

| File | Cos'è |
|---|---|
| `STATO_ZERO_originale.md` | versione originale dello Stato Zero (base per il Vol 1) |
| `LE_PORTE_cornice_narrativa_v2.md` | cornice narrativa v2 da cui sono state derivate le 4 sezioni Porte |

## Pattern per il compositore libro futuro

Ogni file consolidato (`introduzioni_cicli.md`, `stato_zero_e_sigilli.md`, `presentazioni_parziali.md`, `porte.md`) usa marker `## VOLUME N` come delimitatori interni di volume — stesso paradigma dei marker `@hook` nelle storie. Il compositore può:

```python
import re
def split_per_volume(path):
    text = Path(path).read_text(encoding='utf-8')
    # split su "## VOLUME N" o "# VOLUME N — ..."
    parts = re.split(r"^#{1,2}\s+VOLUME\s+(\d+)", text, flags=re.M)
    # parts = [pre, '1', body1, '2', body2, ...]
    return {int(parts[i]): parts[i+1] for i in range(1, len(parts), 2)}
```

Per `stato_zero_e_sigilli.md` il compositore distingue ulteriormente:
- `## VOLUME N` → Stato Zero del volume N
- `## SIGILLO Vol N → Vol N+1` → sigillo da inserire in chiusura volume N

## Vincoli

- **Non modificare** nessun file di `_volumi/` senza autorizzazione esplicita di Ray. Sono bozze autoriali.
- **Le revisioni editoriali** (es. "un po' troppa morale" segnalata da Ray nel piano) si fanno **direttamente qui** prima della composizione libri — non si versionano in file paralleli.
- I file `_elementi_fissi/` sono **read-only** in senso forte (traccia origine).
- Pattern marker `## VOLUME N` = parte del contratto con il compositore — non rinominare i marker.
- Naming volume in markdown coerente: sempre `VOLUME 1` / `VOLUME 2` / etc. (numero, non `Δ`).

## Stato di completamento (al 2026-05-05)

| Elemento | Stato |
|---|---|
| Soglia | ✅ scritta (estratta da docx) |
| Congedo | ✅ scritto (estratto da docx, solo Vol 4) |
| Presentazione completa (23 doppie) | ✅ scritta (estratta da docx, sorgente unica) |
| Presentazioni parziali (4) | ✅ assemblate |
| Introduzioni cicli (4) | ✅ scritte (revisione "morale" pendente — Ray) |
| Stato Zero adattati (4) | ✅ scritti (Vol 1 = quasi-originale) |
| Sigilli chiusura (3) | ✅ scritti |
| Le Porte — sezioni (4) | ✅ scritte (apertura + avvertenza identiche; tracce bambini per ciclo) |
| Le Porte — tracce bambini (9 + 1 egizio) | ✅ scritte |
| Revisione editoriale finale | ⬜ da fare prima della composizione libri |
| Sostituzione etichette `Δ/⇄/⟳/Integrazione` → `A/B/C/D` | ✅ fatto 2026-05-07 (5 file: introduzioni_cicli, porte, stato_zero_e_sigilli, presentazioni_parziali, PIANO_EDITORIALE_4VOLUMI_v1) |

## Origine

Pacchetto consegnato da Ray il 2026-05-05 come zip `isola_4volumi_v2.zip`. Estratto in questa struttura con opzione C (per funzione + marker `## VOLUME N` interni). Traccia: `SYNC-2026-05-05-011`.
