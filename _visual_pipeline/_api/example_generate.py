"""
example_generate.py — Mini esempio d'uso di flux_image_gen.

Genera 1 immagine di test (con e senza ChatGPT enhancement).
Costo atteso: ~$0.04 (flux-kontext-pro).

Setup:
    1. cp .env.example .env
    2. Compila FAL_KEY nel .env (e OPENAI_API_KEY se vuoi l'enhancement)
    3. pip install -r requirements.txt
    4. python example_generate.py
"""

from pathlib import Path
from dotenv import load_dotenv

# Carica .env dalla stessa directory
load_dotenv(Path(__file__).parent / ".env")

from flux_image_gen import generate_image, list_tiers

# ---------------------------------------------------------------------------
# Prompt grezzo
# ---------------------------------------------------------------------------
RAW_PROMPT = (
    "A young boy with curly red hair and a green wool sweater stands at the edge "
    "of a misty forest at dawn. Soft watercolor illustration, children's picture book style, "
    "warm morning light, visible paper texture, dreamy atmosphere."
)

# ---------------------------------------------------------------------------
# (Opzionale) Enhancement ChatGPT
# Decommentare per attivare — richiede OPENAI_API_KEY nel .env
# ---------------------------------------------------------------------------
USE_CHATGPT_ENHANCEMENT = False

if USE_CHATGPT_ENHANCEMENT:
    from prompt_enhancer import enhance_prompt
    prompt = enhance_prompt(
        RAW_PROMPT,
        style_context="soft watercolor, children's picture book, warm palette",
    )
    print(f"[enhanced prompt]\n{prompt}\n")
else:
    prompt = RAW_PROMPT

# ---------------------------------------------------------------------------
# Generazione
# ---------------------------------------------------------------------------
print("Tiers disponibili:")
for t in list_tiers():
    ref = "✓ reference" if t["supports_reference"] else "  text-only"
    print(f"  {t['tier']:<22} ${t['cost_usd']:.3f}  {ref}")

print(f"\nGenerazione con flux-kontext-pro...")

result = generate_image(
    prompt,
    tier="flux-kontext-pro",
    size="1024x1536",
    seed=42,                          # riproducibile — rimuovi per variazione
    output_path="output_test.png",
)

print(f"Salvata: output_test.png")
print(f"Costo:   ${result.cost_usd:.3f}")
print(f"Modello: {result.model}")
print(f"Seed:    {result.seed}")
print(f"Size:    {len(result.image_bytes) // 1024} KB")
