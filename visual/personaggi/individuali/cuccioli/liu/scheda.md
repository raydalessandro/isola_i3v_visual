---
id: liu
name: Liu
famiglia: personaggio
sottotipo: cuccioli
specie: libellulina
tipo_grafo: cucciolo_scuola
ruolo_saga: presenza_aerea_discreta
status: stub
ultima_modifica: 2026-04-25
fonti: ["pipeline_narrativa/story_graph.json#entities.characters.liu"]
appare_in_storie: []
relazioni:
  dimora: null
  quadrante_grafo: null
  related_to: []
  cross_skill:
    cartografia: null
---

# Liu

> **Stato compilazione:** body provvisorio, in attesa revisione Ray. Compilato il 2026-04-25 (estrazione manuale, dopo timeout sub-agenti).

## Identità visuale (sintesi)

Libellulina minuscola, lunga come il dito di un bambino. Ali trasparenti con riflessi azzurro-verdi, corpo sottile come un fuscello, occhi grandissimi rispetto alla taglia. Appare e sparisce in fretta — entra in scena con un *frrr* d'ali rapide, dice una frase, riparte. Messaggera informale dell'isola e occhio del lettore-bambino.

## Aspetto / forma

- **Taglia:** ~5-7 cm di lunghezza, scala "dito di un fratello" (Bible §4.17). Corpo allungato e sottile, paragonato a un fuscello.
- **Ali:** quattro, trasparenti, con riflessi azzurro-verdi che cambiano col taglio della luce.
- **Occhi:** sproporzionatamente grandi rispetto alla testa — caratteristica delle libellule reali, accentuata.
- **Volo:** velocissimo a tratti rettilinei, capace di **stop assoluto a mezz'aria** (hover immobile), ripartenza di scatto.

## Espressione / comportamento

- Modalità di base: **moto perpetuo** salvo brevi soste in hover per parlare.
- Suono caratteristico: piccolissimo *frrr* del battito d'ali (non rumore di insetto fastidioso, frequenza sottile).
- Si appende a **cornicioni**, foglie sopra le teste, davanzali — abitanti la dimenticano lì e parlano: lei sente.
- Postura comunicativa: hover frontale, una frase, ripartenza. **Mai resta in scena a lungo.**
- Sceglie cosa ridire e cosa no. Non è pettegola.
- Funzione narrativa: **collegamento tra scene** (porta notizie da un quartiere all'altro), **occhio del bambino-lettore** (proiezione del lettore dentro l'isola).

## Palette e atmosfera

Cromatismi dominanti: **trasparenze ali + iridescenze azzurro-verdi**, in contrasto con i colori opachi dell'ambiente abitato (legno, terra, pietra). Quando attraversa una scena, la sua presenza è un baluginio rapido più che una figura ferma. In S8 entra in **fase cielo piombo** (prima del picco): la sua iridescenza diventa segno visivo del cambio di luce.

## Contesto e ambientazioni ricorrenti

- **Scuola di Stria** — frequenta "a modo suo": vola sopra il tetto, ascolta da fuori, entra qualche volta (non sta seduta come gli altri cuccioli).
- **Forno di Fiamma** — destinazione ricorrente delle sue rotte (porta notizie a Fiamma).
- **Finestre, cornicioni, davanzali, foglie alte** — punti di sosta tipici.
- **Tutta l'isola** — copre lunghe distanze in tempi brevi (capacità di volo).

## Coerenza cross-scena (cose che NON cambiano)

- Taglia minuscola (dito di un fratello).
- Ali trasparenti azzurro-verdi.
- Suono *frrr* del battito.
- Quota frase: **una frase per scena, breve** (non monologa mai).
- Permanenza scenica brevissima (entra → dice → esce).
- Non è pettegola: filtra cosa dire.

## Variabilità ammessa

- Destinazione del volo (forno, scuola, finestra fratelli, ecc.).
- Ora del giorno (mattino, sera, alba — varia per storia).
- Tono della frase (curiosità, ipotesi, invito) — purché breve.

## Cliché da evitare

Riferimento: `pipeline_narrativa/documenti_progetto/PATTERN_AI_DA_BANDIRE_v1.md` + vincoli Bible §4.17.

- **Mai "fatina luminosa"** — non è creatura magica, è una libellula reale dell'Isola.
- **Mai pettegola per cattiveria** — il filtraggio di cosa ridire è morale, non comico-meschino.
- **Mai voce comica in scene serie** (es. S8 "Forse l'acqua trema" è ipotesi inquieta, non battuta).
- **Mai sa cose che il narratore ha esplicitamente nascosto al lettore** — il suo sapere è limitato a ciò che ha visto/sentito sull'isola.
- **Mai resta in scena a lungo** — niente dialoghi prolungati, niente Liu seduta a chiacchierare.
- **Mai "occhietti che brillano di saggezza"**, "messaggera misteriosa", "antichi presagi". Lei è informale, terrena, libellula.

## Per stampa 3D

- **Scala:** mini, ~5-7 cm. In quadri di gruppo va modellata come accento, non come figura paritetica con i fratelli.
- **Volume:** corpo cilindrico molto sottile (~2 mm di diametro), ali piatte 4 unità, testa quasi sferica con occhi composti grandi.
- **Pose canoniche per le 4 vedute:** posizione raccomandata in **hover frontale ad ali aperte** (frontale e profili) + posizione **di scatto in volo** (per la veduta posteriore — visibile la coda allungata).
- **Materiali consigliati:** ali in resina trasparente con tinta iridescente; corpo in pittura azzurro-verde-grigia.

## Per narrativa e social

- **Registro testuale:** sempre brevissimo. Una frase, mai più. Tipica forma a domanda aperta o ipotesi.
- **Onomatopea:** *frrr* — usabile come marker testuale e visuale (post, didascalie).
- **Pattern di apparizione:** "Liu vola via", "Liu si ferma sul cornicione", "Liu fa frrr e riparte" — formule corte e ricorrenti.
- **Nelle didascalie social:** funziona come "voce del lettore-bambino" — può ospitare la domanda implicita di chi guarda.
- **Tono da evitare:** mistero pomposo, saggezza ammiccante. Tono giusto: curiosità, leggerezza, ipotesi.

## Storie / scene di apparizione

- **s06** — primo cammeo saga. "Frrr messaggera non veggente, una frase breve" (`s06.scene_hook`).
- **s08** — entra in fase cielo piombo (prima del picco Mulinello forte). Si aggrappa al cornicione del Forno: *"Il vento sale forte stasera. Forse l'acqua trema."* — **prima menzione saga del fenomeno `quando l'acqua trema`** come ipotesi (lore-hook, non certezza). Modalità coerente con S6.
- **s09** — vola dalla scuola al Forno **prima dei fratelli** (canonico). I cuccioli a scuola la sentono passare; lei porta notizia a Fiamma.
- **s10** — assente.
- **s11** — assente esplicita (discrepanza archi tabella vs dettaglio risolta a favore "assente", `s11.note`).
- **s12** — apertura saga simmetrica (S1 ↔ S12). Vola alla finestra dei fratelli col suo *frrr*: *"Oggi suonano. Andate?"*. **Prima a chiamare il fenomeno "suonano"** — installa il nome canonico del Concerto dei Tre Venti (deferred #22 chiuso).

## Disallineamenti / domande aperte

- **Nome canonico:** Bible §4.17 usa **"Liù"** (con accento grave). Grafo usa id `liu` senza accento e non ha campo `name` esplicito, quindi lo script genera `name: Liu`. Decisione: il display name dovrebbe essere **Liù**? Se sì, il fix va nel grafo (`entities.characters.liu.name = "Liù"`), poi rilanciare lo script visual per propagare.
- **Apparizioni non documentate:** S1-S5, S7, S10 non hanno menzione di Liu. È intenzionale (cuccioli compaiono dal blocco B in poi)? Confermare con Ray.
- **Genitori:** Bible dice "non in scena". Restano fuori canone visivo? Confermare.

## Riferimenti puntuali (citazioni dirette dalle fonti)

- `pipeline_narrativa/story_graph.json#entities.characters.liu`: `species: libellulina`, `type: cucciolo_scuola`, `role_saga: presenza_aerea_discreta`, `constraints: []`.
- `ISOLA_TRE_VENTI_BIBLE_v2.md` §4.17 LIÙ:
  - "Libellulina. Genitori non in scena. Frequenta la scuola di Stria a modo suo (vola sopra, ascolta da fuori, entra qualche volta)."
  - "Minuscola — lunga come un dito di un fratello. Le ali trasparenti con riflessi azzurro-verdi, il corpo sottile come un fuscello, gli occhi grandissimi (per la sua taglia). Vola velocissima, si ferma in aria immobile, riparte di scatto."
  - "Liù fa cose-da-libellula. Vola dappertutto — copre l'isola in poco tempo. Sente conversazioni — sta sulle foglie sopra le teste degli abitanti, e gli abitanti la dimenticano lì."
  - "Si ferma in aria per parlare — il battito d'ali fa un piccolissimo *frrr*."
  - "Sceglie cosa ridire e cosa no. Non è pettegola."
  - Voci tipiche: *"Ho sentito che."* / *"Indovina chi è dal forno adesso."* / *"Aspetta, vado a vedere."* / *"Torno!"*
  - "Cucciola della **informazione veloce**. Collegamento tra le scene. Funzione anche di **occhio del bambino-lettore** — è una proiezione del lettore-bambino dentro l'isola."
  - Vincoli: "Mai Liù che resta in scena a lungo — entra, dice, va. Mai Liù che fa la pettegola per cattiveria. Mai Liù in scene serie come voce comica. Mai Liù che sa cose che il narratore ha esplicitamente nascosto al lettore."
- `pipeline_narrativa/story_graph.json#stories.s06.characters_in_scene[liu]`: "frrr_messaggera_non_veggente_una_frase_breve".
- `pipeline_narrativa/story_graph.json#stories.s08`: "Liu passa con frrr modalita coerente con prima apparizione S6. Porta annuncio fenomeno raro 'forse l'acqua trema' come ipotesi (non certezza). Prima menzione saga — 1 di 2 in saga."
- `pipeline_narrativa/story_graph.json#stories.s09.scene_hook`: "cuccioli sentono Liu vola al forno"; "liu_precede_fratelli_al_forno_canonico_chiude_ipotesi_d_archi_8".
- `pipeline_narrativa/story_graph.json#stories.s11`: "LIU_ASSENTE_S11_DISCREPANZA_ARCHI_TABELLA_VS_DETTAGLIO_RISOLTA_DETTAGLIO_WINS".
- `pipeline_narrativa/story_graph.json#stories.s12`: "Liu prima a chiamarlo 'suonano' - implica fenomeno gia noto agli abitanti"; callback `cb_s12_008_liu_mestiere_informale_apertura_concerto_oggi_suonano_nome_installato`; visual_anchor: "liu_appena_volata_via_frrr_oggi_suonano_andate_interrogativo".
