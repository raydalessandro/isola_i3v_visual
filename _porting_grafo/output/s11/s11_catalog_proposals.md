# Catalog Proposals — s11

**Data**: 2026-04-28
**Esecuzione**: rigenerato post-corruzione zip s11.

## Sintesi
- Entita' inventariate: **22** (19 personaggi in scena + 3 offscreen + 7 luoghi)
- In catalogo: **22 / 22** (con 2 mismatch nominali — fix in mapping)
- Da AGGIUNGERE: **0**
- Misalignments: **1** (mis_007 ricorrenza, gia' resolved pattern)

## Personaggi in scena (19, record saga)
gabriel, elias, noah, stria, fiamma, nodo, memolo, salvia, zolla, amo, bartolo, pun, toba, bru, cardo, vecchie_del_mercato (→ mercato_del_mezzogiorno), coltivatori_del_cerchio, mantenitori, pastori.

12 con vincoli individuali in `character_constraints.json`.

## Locations (7 secondary + 1 primary)
piazza_villaggio (primary), albero_vecchio, mercato_del_mezzogiorno_panca_di_pietra (→ panca_di_pietra), pozzo_piazza, forno, orti_del_cerchio, pontile_bocca, pascoli_alti.

## Hook resolution
- 8 hook in formato standard (location stringa, no hook_dict pesanti).
- 1 hook con location 'villaggio_centrale' (non in catalogo) → mappato a `piazza_villaggio` con qualifier preservato.
- 1 hook con location 'mercato_del_mezzogiorno_panca_di_pietra' → mappato a `panca_di_pietra` (id catalogo).

## Misalignment
**mis_007 (ricorrenza pattern già nota)**: `mercato_del_mezzogiorno_panca_di_pietra` non in catalogo. Risolto con `locations_secondary_id_renames`. Stesso pattern di s06 e s08 (decisione post-saga: aggiornare grafo nelle storie successive).

## Note
S11 e' la **chiusura del blocco D** (architrave strato 3 culminata): 17 debts_closed bloom finale.
Pattern A in variante collettiva (festa che non si vince — succede).
key_phrase_indicative attribuita a Elias (terna strato 3: dire/accettare/tenere). Quarto caso saga key_phrase a personaggio.
