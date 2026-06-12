# TODO — Brieffer: riordino in blocchi A/B per il prompt caching

**Stato:** debito tecnico aperto · registrato 2026-06-12 · priorità: prima del seeding "Rocco e Idvara" (il template eredita il pattern)

## Cosa

`scripts/build_writing_brief.py` oggi emette brief monolitici con il contenuto
comune a tutte le storie (~66% delle righe: vincoli universali, PATTERN_AI_DA_BANDIRE
integrale, formula ritornello, cornici) **sparso in mezzo** al documento.
La cache dei modelli è a prefisso: contenuto condiviso non-in-testa vale zero
tra storie diverse.

Intervento: il brieffer emette **due blocchi ordinati** —
- **Blocco A (invariante di saga):** byte-identico per tutte le 12 storie, in testa
  (vincoli universali, pattern banditi, formula ritornello, convenzioni mondo).
- **Blocco B (invariante di storia):** core narrativo, narrazione fattuale, hook,
  cast in scena, cornici applicabili, echi/callback, quote tracker, §2-bis stato
  del mondo, istruzione operativa.

Due breakpoint cache: A resta caldo tra storie e tra riprese nella stessa
giornata; B si scrive una volta per storia.

## Perché

- Risparmio diretto ~1 $/saga + robustezza a ogni ripresa di sessione (A non si ripaga).
- Coerenza col principio P1/P2 (cfr. doc "La cache come architettura"): invariante
  in testa, variante dopo. Il brieffer è il pezzo della spina dorsale che produce
  il contesto della prosa: deve produrlo già cache-nativo.
- Il pattern va ereditato dallo starter kit v2 → farlo PRIMA dell'estrazione template.

## Vincolo di test (bloccante)

Il riordino cambia ciò che l'agente prosa legge per primo (oggi i pattern banditi
stanno vicino alla coda, domani in testa). **Validare con una storia di test di Ray**
prima di adottare: stessa pagina scritta con brief vecchio e nuovo, confronto voce.
Il §13 (istruzione operativa) resta in coda in entrambi i casi: è il richiamo dei
vincoli nel punto di massima attenzione.

## Riferimenti

- Misura del 66% condiviso: `sort | comm` tra s05 e s06 (2026-06-11).
- Filosofia e formule di break-even: doc interno "La cache come architettura"
  (EAR LAB, v1.0 — §3.2 causa 3, §6.1, Appendice A).
