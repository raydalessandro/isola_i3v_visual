# s11 — Migration Notes

**Data**: 2026-04-28
**Output**: `s11_canonical.json` (52 campi top-level, 8 hooks, PASS verify)
**Esecuzione**: rigenerato da zero via `migrate_p1.py s11`. Lo zip `s9-s12.zip` aveva s11 corrotto (50KB di null bytes); ricostruito interamente da `INPUT_NODES/s11_input.json`.

## Storia
"La Festa del Raccolto" — centro_blocco_d, ciclo sigillo, autunno pieno. **CULMINE ARCHITRAVE STRATO 3** (Vecchie riconoscimento muto a Elias, "Va bene." come ACCETTARE). 19 personaggi in scena (record saga).

## Trasformazioni applicate
- `attribute_dominant: sigillo` (gia' canonico)
- `block_position: centro_blocco_d` (gia' canonico)
- `season: autunno` (gia' canonico)
- `pattern_a_active: attivo` (continua bloom)
- `key_phrase_indicative: "Va bene."` + `key_phrase_attributed_to: "elias"` (REGOLA 0.8 — quarto caso saga dopo s03/rovo, s06/memolo, s08/memolo)

### Hook resolution (8 hooks)
| hook_id | id catalogo | qualifier |
|---|---|---|
| hook_01 | orti_del_cerchio | alba_raccolto_rituale_inizio_giornata |
| hook_02 | piazza_villaggio | mattino_allestimento_banchi_festa |
| hook_03 | piazza_villaggio | mezzogiorno_stria_distribuisce_coni |
| hook_04 | piazza_villaggio | mezzogiorno_tre_cose_spostano_elias |
| hook_05 | **panca_di_pietra** (era `mercato_del_mezzogiorno_panca_di_pietra`) | pomeriggio_vecchie_culmine_architrave |
| hook_06 | pozzo_piazza | pomeriggio_elias_quattro_coni_bru |
| hook_07 | pontile_bocca | pomeriggio_tardi_bartolo_frutti_da_fuori |
| hook_08 | **piazza_villaggio** (era `villaggio_centrale`) | sera_mulinello_ritorno_casa |

### Fix manualizzati post-corruzione
- `mercato_del_mezzogiorno_panca_di_pietra` → `panca_di_pietra` (locations_secondary + hook_05): pattern di mis_006/mis_007 (gia' visto s06/s08)
- `vecchie_del_mercato` → `mercato_del_mezzogiorno` (characters_in_scene): coerente con fix s06
- `villaggio_centrale` → `piazza_villaggio` (hook_08 location): id non in catalogo, mappato a quartiere centro

## Debts (debt_vero_dict)
- **2 opened** (s11→s12): frutti_da_fuori_bartolo, coni_stria_gesto_annuale_eco
- **17 closed** (record saga, chiusura blocco D): s02/s03/s04/s05/s06/s08/s09/s10 → s11. Bloom architrave strato 3 + Pattern A variante collettiva.

## Auto-derivati
- `narrator_address: false`, `paronomastico_used: true`, `narrator_meta_voice: false`
- `onomatopee_firma: ["TOK-TOK-TOK"]`
- `quartieri_attraversati: ["terra_ovest", "centro_villaggio", "acqua_sud"]`
- `personaggi_vincoli_attivi`: 12 personaggi con vincoli individuali (record saga)
- `fear_touched`: elias (bloom: paura accolta non risolta)

## Misalignments
- `mis_007` ricorrenza pattern (mercato_del_mezzogiorno_panca_di_pietra): risolto in P1 con stesso pattern.
- `villaggio_centrale` non e' un mis nuovo: id semantico legacy, mappato a piazza_villaggio.

## Stato
PASS verify. 8 provvisori P2 (2A + 4B + 2C). I 5 `no_inference_fields` restano `null`.
