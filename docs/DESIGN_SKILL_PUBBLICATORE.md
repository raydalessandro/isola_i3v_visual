# Design — skill `pubblicatore` (proposta, NON ancora implementata)

**Stato:** bozza · aperta al confronto con Ray · 2026-06-15 (sessione kit copertina).

> Questo documento serve a **ragionare prima di scrivere la skill**. Lo scope è
> chiuso, le decisioni sono nere su bianco, e quando Ray dà l'OK si trasforma
> in `skills/pubblicatore/SKILL.md`. Fino ad allora resta solo un design doc.

## Cosa farebbe la skill

Una skill che **monta il pacchetto di pubblicazione Amazon KDP per un volume**
partendo dai tre input deterministici già presenti in repo:

1. Le 3 storie del volume (`pipeline_narrativa/storie_finali/sNN_*.md`) +
   apparato `@hook`/`@subhook` + immagini-scena;
2. L'illustrazione pulita di copertina (`visual/atlante/emblema/copertina_clean_volN.png`);
3. La mappa isola aerea (`visual/atlante/mappe/isola_aerea_v1.jpg`).

Output del pacchetto:

```
pacchetti_pubblicazione/volN/
  vol{N}_libro.pdf                         ← interno KDP (libro digitale)
  vol{N}_stampa.pdf                        ← interno KDP (stampa A5 + bleed)
  vol{N}_wrap_<style>_<back>.png           ← copertina wrap (fronte+dorso+quarta+bleed)
  vol{N}_copertina_<style>.png             ← solo fronte (preview)
  vol{N}_quarta_<back>.png                 ← solo quarta (preview)
  listing_volN.md                          ← bozza scheda Amazon (titolo, sottotitolo, descrizione, keywords, categorie BISAC)
  CHECKLIST_KDP_volN.md                    ← derivato: spina mm calcolata, DPI, file da caricare
```

## Confine — cosa la skill NON fa

- **Non genera prosa, non tocca grafo, non tocca catalogo visual.** Solo
  composizione meccanica di sorgenti già canonizzati.
- **Non modifica `pipeline_narrativa/`** né `visual/`. Legge in sola lettura.
- **Non pubblica** su Amazon (caricamento manuale Ray).
- **Non decide titoli, sottotitoli, keyword**: prende quanto già scritto nei
  sorgenti (listing) o solleva l'argomento a Ray. Tutto ciò che è opinione
  editoriale resta autoriale.
- **Non rigenera asset visivi.** Se manca `copertina_clean_volN.png` o
  l'illustrazione del volume, la skill si ferma e segnala — non improvvisa.

## Architettura proposta

Tre tooling, già esistenti o in arrivo, orchestrati da uno script unico:

| Tool | Esiste? | Output |
|---|---|---|
| `scripts/build_volume.py --volume N` | ✅ sì | PDF libro + stampa |
| `scripts/build_cover.py` (con `CURRENT_VOLUME = N`) | ✅ sì (nuovo, 2026-06-15) | PNG wrap + quarte |
| `scripts/build_listing.py --volume N` | ❌ da fare | bozza listing dal grafo + Bible |

Orchestratore (proposto): `scripts/montaggio_volume.py --volume N`.

```bash
python3 scripts/montaggio_volume.py --volume 1
# 1) controlla che tutti gli input esistano (scene HD, copertina pulita, mappa)
# 2) chiama build_volume.py (PDF libro + stampa)
# 3) chiama build_cover.py (wrap + quarte + preview fronte)
# 4) (opzionale) chiama build_listing.py se l'.md non esiste
# 5) genera CHECKLIST_KDP_volN.md (spina mm, DPI, n. pagine effettive)
# 6) sposta tutto in pacchetti_pubblicazione/volN/
```

## Decisioni aperte (da discutere con Ray)

### D1 — Top-level dir per output: `pacchetti_pubblicazione/` o `output/pubblicazione/`?

`/output/` è già in `.gitignore`. Se vogliamo che il pacchetto sia versionato
serve un top-level NON ignorato. Proposta: `pacchetti_pubblicazione/`,
analogo a `_pacchetti_consegnati/` ma con segno opposto (consegnati IN vs
consegnati OUT). Alternativa: tutto sotto `_output/` e zippato a parte.

### D2 — Listing: generabile o manuale?

La bozza `kdp/listing_vol1.md` è scritta a mano. Per i Vol 2-4 si può:
- (a) lasciarlo manuale (1 file ogni volume, scrive Ray);
- (b) generare uno stub deterministico da Bible + grafo (titoli storie, hook,
  vento, età, categorie fisse) e Ray lo rifinisce;
- (c) lasciare manuale ma la skill **verifica** che il file esista e contiene
  i campi minimi (Serie, Volume, Titolo, Sottotitolo, Autore, Descrizione,
  Keywords, BISAC, Età).

Proposta: **(c)**. Niente auto-generazione di prosa editoriale.

### D3 — Calcolo spina mm

`build_cover.py` ha `SPINE_MM = 6.4` provvisorio. La spina dipende da:
- numero di pagine effettive del PDF (`build_volume.py` lo conosce);
- carta KDP (premium color = 0.058 mm/pagina; standard = 0.0635 mm/pagina).

Proposta: l'orchestratore legge il PDF prodotto da `build_volume.py`, conta
le pagine, calcola la spina e **riesegue `build_cover.py`** con il valore
corretto (oppure passa `SPINE_MM` come argomento CLI a `build_cover.py` —
oggi è solo costante in testa al file, va parametrizzato).

### D4 — Naming output

`vol1_pres-dopo_libro.pdf` è il default di `build_volume.py`. Per il
pacchetto pubblicazione vogliamo qualcosa di più pulito (es. `vol1_libro.pdf`
+ `vol1_stampa.pdf` + `vol1_wrap.png` + `vol1_listing.md`). Decidere se
rinominare o se la skill copia/rinomina i file durante il montaggio.

### D5 — Multi-volume in un colpo solo?

`python3 scripts/montaggio_volume.py --tutti` per generare i 4 volumi
contemporaneamente? Utile per "dry-run di sanità" prima della stampa,
inutile altrimenti (1 volume = ~2 min di build).

### D6 — Test della skill

Per ciascun volume servirebbe un test integrazione:
- PDF generato esiste e ha N pagine attese;
- wrap PNG ha le dimensioni KDP attese (a + bleed + spine);
- listing.md ha tutti i campi obbligatori.

Già abbiamo `tests/test_build_volume.py` (60 test). Aggiungere
`tests/test_montaggio_volume.py` con un test per volume (4 test).

## Quando si fa

Quando Ray ha tutti gli input pronti per il Vol. 1 reale (post-finalizzazione
copertine + numero pagine effettive). Per ora i sorgenti del kit ci sono:
**lo script gira, il pacchetto si compone già a mano** richiamando i due
script in sequenza. La skill è il ramo che orchestra e formalizza il
processo.

## Riferimenti

- `scripts/build_volume.py` (compositore PDF, esistente)
- `scripts/build_cover.py` (NUOVO, 2026-06-15, questo branch)
- `kdp/listing_vol1.md` (NUOVO, bozza autoriale Ray)
- `scripts/design_system.py` (palette/font/glifi — usato da entrambi i build)
- Pattern: skill `manutentore` (governance), skill `illustratore` (consegna
  asset). La skill `pubblicatore` sta a valle di tutte le altre.
