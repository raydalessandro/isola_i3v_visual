# Font della collana

Font usati dallo script `scripts/build_volume.py` + `scripts/design_system.py`.
Tutti distribuiti sotto **SIL Open Font License 1.1** (OFL) — uso commerciale
e ridistribuzione consentiti, copyright presso gli autori originali.

| File | Famiglia | Autore / Fonderia | Uso |
|---|---|---|---|
| `Fraunces.ttf` | Fraunces | Undercase Type | display/corpo storia (Eredita Spirale, caldo) |
| `Fraunces-Italic.ttf` | Fraunces Italic | Undercase Type | corsivi eleganti |
| `Nunito.ttf` | Nunito | Vernon Adams + contributors | eyebrow, metadati, didascalie |
| `Nunito-Italic.ttf` | Nunito Italic | Vernon Adams + contributors | corsivi sans |
| `Fredoka.ttf` | Fredoka | Milena Brandao | marchio collana, numeri grandi |
| `Lora-Variable.ttf` | Lora | Cyreal | fallback serif corpo |
| `Lora-Italic-Variable.ttf` | Lora Italic | Cyreal | fallback corsivo serif |

I font sono **inclusi nella repo** per garantire build riproducibili dello
script di impaginazione (KDP, A5, 300 DPI). Lo script ha fallback a font di
sistema con warning se i .ttf qui mancassero.

Per dettagli OFL: https://openfontlicense.org/
