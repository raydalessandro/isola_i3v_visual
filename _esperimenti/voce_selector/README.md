# Esperimento — selettore "La Voce" alla prova della scrittura

Esperimento di stress-test del selettore di voci "La Voce" (companion HTML, 4 assi × 54 voci).
**NON è canone.** Vive qui in `_esperimenti/`, fuori da `pipeline_narrativa/` e da `visual/`.

## Cosa c'è
- `gen_brief.js` — estrazione fedele della logica `testoBriefer()` del selettore. Genera il blocco
  §10 VOCE per un codice Σ. Uso: `node gen_brief.js 113−` (il minus è U+2212).
- `briefs/` — i 6 blocchi §10 generati per le voci testate.
- `_contesto_invariante.md` — il contesto identico passato a ogni agente (fatti hook p4, voci
  fratelli, tabù universali).
- `output/raccolta_output.md` — le 6 rese prodotte dagli agenti prosa, affiancate.
- `STUDIO.md` — l'analisi: discriminazione, fedeltà, peso dei 4 assi, raccomandazioni.

## Come riprodurre
1. `node gen_brief.js <Σcodice>` per ogni voce → blocco §10.
2. Si lancia un agente prosa con [contesto invariante] + [blocco §10], compito: scrivere SOLO la
   pagina 4 di s01 (hook la nebbia), 80-130 parole + note tecniche.
3. Si confrontano le rese (stesso hook, unica variabile = la voce).

## Sintesi del risultato (dettaglio in STUDIO.md)
- Le ricette delle voci non-collaudate **reggono**: prosa coerente e on-brand.
- I due control collaudati si **riproducono senza copiare** l'esempio: la §10 codifica l'operazione.
- I 4 assi **non pesano uguale**: narratore = primario (cambia il senso), respiro = secondario
  (compresso dal registro picture-book), luce = scena-dipendente, verso = quasi cosmetico.
- "54 voci" è il conteggio combinatorio; le famiglie percettivamente distinte sono **~6**.
- Difetto da correggere: con un solo esempio di fatto-sigillo, le voci a sottrazione convergono
  sullo stesso prop (la pietra che rotola).

Sorgente del selettore: HTML companion fornito da Ray (resta presso Ray, non versionato qui).
