#!/usr/bin/env python3
"""
build_writing_brief.py
Costruisce un dossier di scrittura autosufficiente per una singola storia
de "L'Isola dei Tre Venti", da consegnare a un agente prosa.

Dato uno --story sNN, produce un file markdown in
pipeline_narrativa/writing_briefs/sNN_writing_brief.md
che contiene TUTTO E SOLO ciò che serve a scrivere quella storia, pescando
da: grafo, narrazione fattuale, hook, cornici, sentieri, saluti, formula
ritornello, schede catalogo personaggi/luoghi/oggetti.

L'agente prosa NON deve interrogare altre fonti — il brief è completo.

Uso:
    python3 build_writing_brief.py --story s01
    python3 build_writing_brief.py --story s01 --repo-root /path/to/repo
    python3 build_writing_brief.py --story s01 --output-dir custom/path
    python3 build_writing_brief.py --all  # tutte le 12 storie

Filosofia:
- Token budget: ~20-30k token per brief (denso ma autocontenuto)
- Idempotente, riscrivibile a comando
- Ordinato per priorità di lettura dell'agente
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path
from textwrap import indent


# =============================================================================
# UTILITY DI ESTRAZIONE
# =============================================================================

def load_graph(repo_root: Path) -> dict:
    path = repo_root / "pipeline_narrativa" / "story_graph.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_narrazione_fattuale(repo_root: Path, sid: str) -> str:
    """Cerca il file narrazione fattuale per la storia data."""
    nf_dir = repo_root / "pipeline_narrativa" / "narrazione_fattuale"
    if not nf_dir.exists():
        return f"_(narrazione fattuale non trovata in {nf_dir})_"
    candidates = list(nf_dir.glob(f"{sid}_*.md")) + list(nf_dir.glob(f"{sid}.md"))
    if candidates:
        return candidates[0].read_text(encoding="utf-8")
    return f"_(file narrazione fattuale per {sid} non trovato in {nf_dir})_"


def find_character_scheda(repo_root: Path, char_id: str) -> Path | None:
    """Cerca la scheda visual di un personaggio per id."""
    base = repo_root / "visual" / "personaggi"
    if not base.exists():
        return None
    for p in base.rglob(f"{char_id}/scheda.md"):
        return p
    return None


def find_location_scheda(repo_root: Path, loc_id: str) -> Path | None:
    base = repo_root / "visual" / "luoghi"
    if not base.exists():
        return None
    for p in base.rglob(f"{loc_id}/scheda.md"):
        return p
    return None


def find_object_scheda(repo_root: Path, obj_id: str) -> Path | None:
    base = repo_root / "visual" / "oggetti"
    if not base.exists():
        return None
    for p in base.rglob(f"{obj_id}/scheda.md"):
        return p
    return None


def find_grok_prompt(repo_root: Path, entity_id: str, kind: str) -> Path | None:
    """Cerca il prompt_grok.md per personaggio/luogo/oggetto.

    kind in {'character', 'location', 'object'}. Fa rglob per id/prompt_grok.md
    nelle cartelle pertinenti.
    """
    if kind == "character":
        base = repo_root / "visual" / "personaggi"
    elif kind == "location":
        base = repo_root / "visual" / "luoghi"
    elif kind == "object":
        base = repo_root / "visual" / "oggetti"
    else:
        return None
    if not base.exists():
        return None
    for p in base.rglob(f"{entity_id}/prompt_grok.md"):
        return p
    return None


def extract_grok_canon(grok_text: str) -> dict:
    """Estrae i blocchi canone visivo da un prompt_grok.md.

    Ritorna un dict con chiavi:
      - 'character_canon': blocco CHARACTER -- ... (canone fisso del personaggio)
      - 'location_canon':  blocco LOCATION/SCENE -- ... (canone luogo)
      - 'object_canon':    blocco OBJECT -- ... (canone oggetto)
      - 'main_prompt':     primo prompt principale tra triple backticks
    Tutti tradotti in italiano sintetico in build, lasciati così come sono qui.
    """
    out = {}
    # Cerca blocchi in triple backticks
    blocks = re.findall(r"```\s*\n(.*?)\n```", grok_text, re.DOTALL)
    for b in blocks:
        # Identifica blocco canone personaggio
        if re.search(r"^\s*CHARACTER\s*[—-]\s*\w+\s*:", b, re.MULTILINE):
            out.setdefault("character_canon", b.strip())
        # Blocco canone oggetto/scena
        elif re.search(r"^\s*OBJECT\s*[—-]", b, re.MULTILINE) or re.search(r"^\s*SCENE\s*[—-]\s*Canonical", b, re.MULTILINE):
            out.setdefault("object_or_scene_canon", b.strip())
        # Blocco style sheet
        elif re.search(r"^\s*ART STYLE\s*[—-]", b, re.MULTILINE):
            # Lo skip — non utile per la prosa
            pass
        else:
            # primo prompt scena come fallback
            if "main_prompt" not in out:
                out["main_prompt"] = b.strip()
    return out


def list_canonical_images(repo_root: Path, entity_id: str, kind: str) -> list[str]:
    """Restituisce path relativi delle immagini canoniche dell'entità (per riferimento)."""
    if kind == "character":
        base = repo_root / "visual" / "personaggi"
    elif kind == "location":
        base = repo_root / "visual" / "luoghi"
    elif kind == "object":
        base = repo_root / "visual" / "oggetti"
    else:
        return []
    if not base.exists():
        return []
    out = []
    for img_dir in base.rglob(f"{entity_id}/immagini"):
        for img in sorted(img_dir.glob("*.jpg")):
            out.append(str(img.relative_to(repo_root)))
        for img in sorted(img_dir.glob("*.png")):
            out.append(str(img.relative_to(repo_root)))
    return out


def extract_section(scheda_text: str, section_name: str) -> str:
    """Estrae il contenuto di una sezione ## da una scheda md."""
    pattern = rf"^##\s*{re.escape(section_name)}\s*\n(.+?)(?=\n##|\Z)"
    m = re.search(pattern, scheda_text, re.DOTALL | re.MULTILINE)
    if m:
        content = m.group(1).strip()
        if "_da popolare" in content:
            return ""
        return content
    return ""


def collect_dialogues_in_narration(narr_text: str, char_name_patterns: list[str]) -> list[str]:
    """Estrae le frasi virgolettate attribuibili a un personaggio dalla narrazione fattuale."""
    out = []
    quotes = list(re.finditer(r"«([^»]+)»", narr_text))
    for q in quotes:
        idx = q.start()
        ctx_before = narr_text[max(0, idx - 200) : idx]
        for pattern in char_name_patterns:
            if re.search(rf"\b{pattern}\b", ctx_before):
                out.append(q.group(1).strip())
                break
    # dedupe preservando ordine
    seen = set()
    out_dedup = []
    for q in out:
        if q not in seen:
            seen.add(q)
            out_dedup.append(q)
    return out_dedup


# =============================================================================
# COSTRUZIONE SEZIONI DEL BRIEF
# =============================================================================

def build_frontmatter(g: dict, sid: str, s: dict) -> str:
    title = s.get("title_provvisorio", "?")
    cycle = s.get("cycle", "?")
    block = s.get("block_position", "?")
    season = s.get("season", "?")
    wind = s.get("wind_active") or "—"
    wind_sec = s.get("wind_secondary") or "—"
    attr = s.get("attribute_dominant", "?")
    length = s.get("estimated_length", "?")
    register = s.get("register", "?")
    entry = s.get("entry_point_type", "?")
    closure = s.get("closure_type", "?")

    return f"""# WRITING BRIEF — {sid.upper()}: {title}

> **Documento autosufficiente** per l'agente prosa. Contiene tutto e solo ciò che serve per scrivere la storia in voce autoriale finale. NON consultare altre fonti — è completo.
>
> **Fonti compilate:** grafo (story_graph.json), narrazione fattuale, hook visivi, cornici del mondo, sentieri attraversati con dettagli, schede catalogo personaggi/luoghi/oggetti, saluti dei gruppi, formula ritornello, quote tracker.

| Metadato | Valore |
|---|---|
| Storia | {sid} — {title} |
| Ciclo | {cycle} ({block}) |
| Stagione | {season} |
| Vento attivo | {wind} (secondario: {wind_sec}) |
| Attributo EAR | {attr} |
| Lunghezza target | {length} parole |
| Registro | {register} |
| Entry point | {entry} |
| Closure | {closure} |
"""


def build_core(s: dict) -> str:
    """Sezione 2 — Core narrativo dal grafo."""
    out = ["\n---\n\n## §2. CORE NARRATIVO\n"]
    out.append(f"**Premise.**\n\n{s.get('premise','').strip()}\n")
    out.append(f"\n**Problem.**\n\n{s.get('problem','').strip()}\n")
    out.append(f"\n**Threshold moment.**\n\n{s.get('threshold_moment','').strip()}\n")
    out.append(f"\n**Resolution mode.**\n\n{s.get('resolution_mode','').strip()}\n")
    out.append(f"\n**Palette emotiva.**\n\n{s.get('palette_emotiva','').strip()}\n")
    return "".join(out)


def build_stato_mondo(g: dict, sid: str) -> str:
    """Sezione 2-bis — STATO DEL MONDO all'inizio di sNN.

    Proiezione derivata piegando il grafo da s01 a s(N-1): nessuno stato
    mantenuto altrove, il grafo resta l'unica fonte (sola lettura). Dà a chi
    scrive la continuity senza dover rileggere le storie precedenti:
    semi attivi/da fiorire/chiusi, callback già spesi, chi ha già debuttato
    e chi debutta QUI, luoghi già visitati. (Branch timeline-worldstate;
    la coerenza temporale di questi dati è blindata da audit_5.)
    """
    order = lambda x: int(x[1:])
    n = order(sid)
    stories = g.get("stories", {})
    seeds = g.get("seeds", {})
    cbs = g.get("callbacks", {})

    out = [f"\n---\n\n## §2-bis. STATO DEL MONDO ALL'INIZIO DI {sid.upper()}\n\n"]
    out.append("> Derivato dal grafo (s01 → s" + f"{n-1:02d}" + "). Vincolante per la "
               "continuity: non ri-fiorire semi chiusi, non trattare i debutti "
               "come personaggi già noti, non ri-spendere callback già fatti.\n\n")

    if n == 1:
        out.append("**Mondo vergine.** Prima storia della saga: nessun seme "
                   "attivo, nessun personaggio già apparso, nessun callback "
                   "disponibile. Ogni elemento introdotto qui è un debutto.\n")
        return "".join(out)

    def as_list(v):
        return v if isinstance(v, list) else ([v] if v else [])

    def short(txt, lim=110):
        txt = (txt or "").strip().replace("\n", " ")
        return txt if len(txt) <= lim else txt[: lim - 1] + "…"

    # --- semi -------------------------------------------------------------
    attivi, fioriscono_qui, maturano_qui, chiusi = [], [], [], []
    for seed_id, sd in seeds.items():
        o = sd.get("origin_story")
        if not o or o not in stories or order(o) >= n:
            continue  # nati qui o dopo: non sono "mondo precedente"
        b = sd.get("bloomed_in_story")
        if b and b in stories and order(b) < n:
            chiusi.append((seed_id, b))
            continue
        riga = f"- `{seed_id}` (da {o}): {short(sd.get('description'))}"
        vc = sd.get("voice_constraint")
        if vc:
            riga += f" — voce: `{vc}`"
        bt = as_list(sd.get("bloom_target_stories"))
        if sid in bt:
            fioriscono_qui.append(riga + f" — **TARGET FIORITURA: QUI**")
        elif sid in as_list(sd.get("maturing_planned_stories")):
            maturano_qui.append(riga + " — *maturazione prevista qui*")
        else:
            attivi.append(riga + (f" (target: {', '.join(bt)})" if bt else ""))

    if fioriscono_qui:
        out.append(f"**Semi che il piano fa FIORIRE in {sid}** "
                   f"({len(fioriscono_qui)}):\n" + "\n".join(fioriscono_qui) + "\n\n")
    if maturano_qui:
        out.append(f"**Semi in maturazione prevista QUI** "
                   f"({len(maturano_qui)}):\n" + "\n".join(maturano_qui) + "\n\n")
    if attivi:
        out.append(f"**Altri semi attivi sullo sfondo** ({len(attivi)}) — "
                   "vivi, non forzarne la fioritura:\n" + "\n".join(attivi) + "\n\n")
    if chiusi:
        righe = ", ".join(f"`{s_}`→{b_}" for s_, b_ in sorted(chiusi, key=lambda x: x[1]))
        out.append(f"**Semi GIÀ FIORITI (chiusi)** ({len(chiusi)}) — eco "
                   f"ammessa, MAI ri-fiorire: {righe}\n\n")

    # --- callback già spesi -------------------------------------------------
    spesi = [(cid, cb) for cid, cb in cbs.items()
             if cb.get("registered_in_story") in stories
             and order(cb["registered_in_story"]) < n]
    if spesi:
        elementi = sorted({cb.get("element", cid) for cid, cb in spesi})
        out.append(f"**Callback già spesi nelle storie precedenti** "
                   f"({len(spesi)}) — non ripeterli come se fossero nuovi: "
                   + ", ".join(f"`{e}`" for e in elementi) + "\n\n")

    # --- debutti ------------------------------------------------------------
    def chars_of(story):
        out_ = []
        for f in ("characters_in_scene", "characters_offscreen_or_background"):
            for x in as_list(story.get(f)):
                cid = x if isinstance(x, str) else x.get("id")
                if cid:
                    out_.append(cid)
        return out_

    visti = set()
    for prev in sorted(stories):
        if order(prev) >= n:
            continue
        visti.update(chars_of(stories[prev]))
    qui = chars_of(stories.get(sid, {}))
    debutti = [c for c in dict.fromkeys(qui) if c not in visti]
    if debutti:
        out.append(f"**DEBUTTI in {sid}** — prima apparizione assoluta, vanno "
                   "presentati, non dati per noti: "
                   + ", ".join(f"`{c}`" for c in debutti) + "\n\n")
    gia = [c for c in dict.fromkeys(qui) if c in visti]
    if gia:
        out.append(f"**Già apparsi prima** ({len(gia)}): "
                   + ", ".join(f"`{c}`" for c in gia) + "\n\n")

    # --- luoghi -------------------------------------------------------------
    def locs_of(story):
        out_ = []
        lp = story.get("location_primary")
        for x in as_list(lp) + as_list(story.get("locations_secondary")):
            lid = x if isinstance(x, str) else x.get("id")
            if lid:
                out_.append(lid)
        return out_

    visitati = set()
    for prev in sorted(stories):
        if order(prev) >= n:
            continue
        visitati.update(locs_of(stories[prev]))
    qui_loc = list(dict.fromkeys(locs_of(stories.get(sid, {}))))
    nuovi = [l for l in qui_loc if l not in visitati]
    if nuovi:
        out.append("**Luoghi mai visti prima nella saga**: "
                   + ", ".join(f"`{l}`" for l in nuovi)
                   + " — la prima descrizione li fonda.\n")
    noti = [l for l in qui_loc if l in visitati]
    if noti:
        out.append("**Luoghi già visitati** (il lettore li conosce): "
                   + ", ".join(f"`{l}`" for l in noti) + "\n")

    return "".join(out)


def build_narrazione_fattuale(repo_root: Path, sid: str) -> str:
    nf = load_narrazione_fattuale(repo_root, sid)
    out = "\n---\n\n## §3. NARRAZIONE FATTUALE (referente di verità)\n\n"
    out += "> Questa è la stesura fattuale, asciutta, della storia. NON è il testo del libro. È il *referente di verità* sui fatti, l'ordine, le frasi codificate. La voce autoriale che scriverai è altra cosa — userà i fatti qui ma li dirà con voce piena, ritmo da picture book, frasi dialoganti con l'illustrazione.\n\n"
    # rimuovo eventuale frontmatter del file di narrazione
    nf_clean = re.sub(r"^---\n.*?\n---\n", "", nf, count=1, flags=re.DOTALL)
    out += nf_clean.strip() + "\n"
    return out


def build_hooks(s: dict) -> str:
    """Sezione 4 — 10 hook visivi compatti."""
    hooks = s.get("visual_anchors", {}).get("scene_hooks", [])
    out = ["\n---\n\n## §4. HOOK VISIVI (10 illustrazioni del libro)\n\n"]
    out.append("> Le pagine del libro saranno strutturate intorno a queste 10 illustrazioni. Il testo di ogni pagina deve **dialogare con l'illustrazione corrispondente**: NON descrive ciò che il bambino vede già, completa o sottende.\n\n")
    for i, h in enumerate(hooks, 1):
        sig = " ⭐" if h.get("is_signature") else ""
        hid = h.get("hook_id", f"h{i}")
        htype = h.get("type", "—")
        moment = h.get("moment", "—")
        loc = h.get("location", {})
        loc_str = loc.get("id", "—")
        if loc.get("qualifier"):
            loc_str += f" ({loc['qualifier']})"
        focal = h.get("focal_action", "—")
        cast = ", ".join(h.get("characters_present", []))
        atm = h.get("atmosphere", "")
        pal = h.get("palette", "")
        ono = h.get("onomatopee", [])
        wind = h.get("wind_visible") or ""
        comp = h.get("composition_zone", "")

        out.append(f"### Hook {i}: `{hid}` — {htype}{sig}\n")
        out.append(f"- **Momento:** {moment}\n")
        out.append(f"- **Luogo:** {loc_str}\n")
        out.append(f"- **Cast:** {cast}\n")
        out.append(f"- **Azione focale:** {focal}\n")
        if atm: out.append(f"- **Atmosfera:** {atm}\n")
        if pal: out.append(f"- **Palette:** {pal}\n")
        if wind: out.append(f"- **Vento visibile:** {wind}\n")
        if ono: out.append(f"- **Onomatopee:** {', '.join(ono)}\n")
        if comp: out.append(f"- **Composition zone (testo overlay):** `{comp}`\n")
        if h.get("notes"): out.append(f"- **Note:** {h['notes']}\n")
        out.append("\n")
    return "".join(out)


def build_cast_in_scena(repo_root: Path, g: dict, s: dict, sid: str, narr: str) -> str:
    """Sezione 5 — Cast espanso da catalogo + frasi codificate dalla narrazione."""
    out = ["\n---\n\n## §5. CAST IN SCENA — voci, vincoli, frasi codificate\n\n"]
    out.append("> Per ogni personaggio in scena: voce-firma dal grafo, aspetto/comportamento dalle schede catalogo, vincoli specifici, frasi-codice già fissate (DEVONO comparire alla lettera).\n")

    chars_in_scene = s.get("characters_in_scene", [])
    chars_offscreen = s.get("characters_offscreen_or_background", [])

    name_patterns = {
        "gabriel": ["Gabriel"], "elias": ["Elias"], "noah": ["Noah"],
        "fiamma": ["Fiamma"], "stria": ["Stria"], "memolo": ["Mèmolo", "Memolo"],
        "nodo": ["Nodo"], "bartolo": ["Bartolo"], "salvia": ["Salvia"],
        "zolla": ["Zolla"], "grunto": ["Grunto"], "rovo": ["Rovo"], "amo": ["Amo"],
        "pun": ["Pun"], "toba": ["Toba"], "bru": ["Bru"], "cardo": ["Cardo"],
        "liu": ["Liù", "Liu"]
    }

    for c_ref in chars_in_scene:
        cid = c_ref.get("id")
        c = g["entities"]["characters"].get(cid, {})
        if not c:
            continue
        out.append(f"\n### {cid.upper()}\n")
        out.append(f"- **Specie:** {c.get('species','?')}\n")
        out.append(f"- **Età band:** {c.get('age_band','?')}\n")
        out.append(f"- **Ruolo in {sid}:** {c_ref.get('role','—')}\n")
        out.append(f"- **Peso narrativo qui:** {c_ref.get('narrative_weight','—')}\n")

        # Voice notes dal grafo
        if c.get("voice_notes"):
            out.append(f"- **Voce (firma sintattica):** {c['voice_notes']}\n")

        # Modalità (se presenti, es. fiamma)
        if c.get("voice_modes"):
            out.append(f"- **Modalità di voce:** {c['voice_modes']}\n")
        if c_ref.get("mode"):
            out.append(f"- **Modalità in {sid}:** `{c_ref['mode']}`\n")

        # Constraints generali
        if c.get("constraints"):
            cn = c["constraints"]
            if isinstance(cn, list):
                cn_str = "\n".join(f"  - {x}" for x in cn)
                out.append(f"- **Vincoli (cosa NON fa MAI):**\n{cn_str}\n")
            else:
                out.append(f"- **Vincoli:** {cn}\n")

        # Constraints specifici per questa storia
        if c_ref.get("constraints_active"):
            cn_str = "\n".join(f"  - {x}" for x in c_ref["constraints_active"])
            out.append(f"- **Vincoli specifici per {sid}:**\n{cn_str}\n")

        # Key actions
        if c_ref.get("key_actions"):
            ka_str = "\n".join(f"  - {x}" for x in c_ref["key_actions"])
            out.append(f"- **Azioni-chiave in {sid}:**\n{ka_str}\n")

        # Quote count estimate
        if c_ref.get("quote_count_estimate"):
            out.append(f"- **Quote attese in scena:** ~{c_ref['quote_count_estimate']}\n")

        # Detti notes per Fiamma
        if c_ref.get("detti_notes"):
            out.append(f"- **Detti previsti in {sid}:** {c_ref['detti_notes']}\n")

        # Frasi codificate dalla narrazione fattuale
        patterns = name_patterns.get(cid, [cid.capitalize()])
        quotes = collect_dialogues_in_narration(narr, patterns)
        if quotes:
            out.append(f"- **Frasi codificate (dalla narrazione fattuale, da preservare alla lettera o variare al minimo):**\n")
            for q in quotes:
                out.append(f"  - «{q}»\n")

        # Aspetto/comportamento dalla scheda catalogo
        scheda_path = find_character_scheda(repo_root, cid)
        scheda_complete = False
        if scheda_path:
            scheda_text = scheda_path.read_text(encoding="utf-8")
            aspetto = extract_section(scheda_text, "Aspetto / forma")
            espressione = extract_section(scheda_text, "Espressione / comportamento")
            abbigliamento = extract_section(scheda_text, "Abbigliamento / stato d'uso")
            palette_atm = extract_section(scheda_text, "Palette e atmosfera")
            voce_sez = extract_section(scheda_text, "Voce")
            # Una scheda è "completa" se ha tutte e 3 le sezioni primarie
            if aspetto and espressione and abbigliamento:
                scheda_complete = True
            if aspetto:
                out.append(f"\n  **Aspetto / forma (dal catalogo):**\n  {aspetto}\n")
            if abbigliamento:
                out.append(f"\n  **Abbigliamento (dal catalogo):**\n  {abbigliamento}\n")
            if espressione:
                out.append(f"\n  **Espressione / comportamento (dal catalogo):**\n  {espressione}\n")
            if palette_atm:
                out.append(f"\n  **Palette e atmosfera (dal catalogo):**\n  {palette_atm}\n")
            if voce_sez:
                out.append(f"\n  **Voce (dal catalogo):**\n  {voce_sez}\n")

        # FALLBACK GROK: incluso SEMPRE per schede non complete; incluso anche
        # per schede complete (ma chiaramente etichettato come "supporto canonico").
        # I prompt grok contengono dettagli che le schede a volte omettono.
        grok_path = find_grok_prompt(repo_root, cid, "character")
        if grok_path:
            grok_text = grok_path.read_text(encoding="utf-8")
            canon = extract_grok_canon(grok_text)
            if canon.get("character_canon"):
                if scheda_complete:
                    label = "Canone visivo (da `prompt_grok.md` — supporto, in inglese)"
                    note = "_La scheda catalogo sopra è il riferimento principale; questo è canone aggiuntivo per dettagli che la scheda potrebbe non coprire._"
                else:
                    label = "Canone visivo (da `prompt_grok.md` — fallback principale, in inglese)"
                    note = f"_Le schede del catalogo per `{cid}` sono parziali; questo è il canone fisso autoriale di riferimento._"
                out.append(f"\n  **{label}:**\n  > {note}\n\n")
                out.append("  ```\n")
                out.append(indent(canon["character_canon"], "  "))
                out.append("\n  ```\n")

        # Immagini canoniche disponibili (riferimento path)
        imgs = list_canonical_images(repo_root, cid, "character")
        if imgs:
            out.append(f"\n  **Immagini canoniche di riferimento:** {', '.join(imgs)}\n")


    # Personaggi offscreen
    if chars_offscreen:
        out.append("\n### PERSONAGGI OFFSCREEN / BACKGROUND\n\n")
        out.append("> Sono presenti senza essere centrali. Possono essere nominati o evocati, mai protagonisti di scena.\n\n")
        for c_ref in chars_offscreen:
            cid = c_ref.get("id")
            role = c_ref.get("role", "—")
            note = c_ref.get("note", c_ref.get("notes", ""))
            out.append(f"- **{cid}** — {role}")
            if note: out.append(f" — {note}")
            out.append("\n")

    return "".join(out)


def build_cornici(s: dict) -> str:
    """Sezione 6 — Cornici del mondo per questa storia."""
    cornici = s.get("cornice_dettagli", [])
    out = ["\n---\n\n## §6. CORNICI DEL MONDO (sfondo, MAI trama)\n\n"]
    out.append("> Le cornici sono micro-apparizioni che fanno girare l'isola in sottofondo. NON sono trama. Vanno integrate come sfondo silenzioso, max 2-3 frasi ognuna nel testo finale. Non devono mai distrarre dal core. Ogni cornice appartiene a uno dei 5 processi del mondo (A=cibo, B=cura, C=notizie, D=venti/stagioni, E=acqua).\n\n")
    if not cornici:
        out.append("_(nessuna cornice registrata)_\n")
        return "".join(out)
    for cd in cornici:
        proc = cd.get("process", "?")
        cid = cd.get("id", "?")
        ctype = cd.get("type", "—")
        who = cd.get("who", {})
        if isinstance(who, dict):
            who_str = f"{who.get('kind','?')}: `{who.get('ref','?')}`"
            if who.get("species_assigned"):
                who_str += f" (specie: {who['species_assigned']})"
        else:
            who_str = str(who)
        where = cd.get("where", {})
        where_str = where.get("location_id", "?") if isinstance(where, dict) else str(where)
        what = cd.get("what", "—")
        intensity = cd.get("intensity", "—")
        saluto = cd.get("saluto", False)
        formula = cd.get("formula_applicata", False)
        struct = cd.get("structural_role", "")
        proposed = cd.get("proposed_text", "")
        notes = cd.get("notes", "")
        out.append(f"### Cornice `{cid}` — Processo {proc} ({ctype})\n")
        out.append(f"- **Chi:** {who_str}\n")
        out.append(f"- **Dove:** {where_str}\n")
        out.append(f"- **Cosa accade:** {what}\n")
        out.append(f"- **Intensità:** {intensity}\n")
        if saluto:
            out.append(f"- **Saluto del gruppo:** APPLICATO (vedi §8 per il saluto specifico)\n")
        if formula:
            out.append(f"- **Formula ritornello:** APPLICATA (vedi §9)\n")
        if struct:
            out.append(f"- **Ruolo strutturale:** {struct}\n")
        if proposed:
            out.append(f"- **Resa testuale proposta:**\n  > {proposed}\n")
        if notes:
            out.append(f"- **Note:** {notes}\n")
        out.append("\n")
    return "".join(out)


def build_sentieri(repo_root: Path, g: dict, s: dict, sid: str) -> str:
    """Sezione 7 — Sentieri attraversati con dettagli stabili pertinenti."""
    out = ["\n---\n\n## §7. SENTIERI ATTRAVERSATI E DETTAGLI STABILI\n\n"]
    out.append("> I dettagli sono **oggetti/presenze fissi del mondo** che il bambino può imparare a riconoscere alla rilettura. Solo i dettagli marcati per QUESTA storia sono mostrati. Vanno integrati nel testo come sfondo riconoscibile, NON come trama.\n\n")

    # Identifica sentieri percorsi: prendili da locations_secondary (che ora include i fantasma)
    loc_secs = s.get("locations_secondary", [])
    sentieri_in_storia = []
    for ls in loc_secs:
        lid = ls.get("id", "")
        if "sentiero" in lid or "via_" in lid or "viottolo" in lid or lid == "guado_di_pietre_piatte":
            sentieri_in_storia.append(lid)
    # Aggiungi anche location_primary se è sentiero
    lp = s.get("location_primary", {}).get("id", "")
    if ("sentiero" in lp or "via_" in lp or "viottolo" in lp) and lp not in sentieri_in_storia:
        sentieri_in_storia.append(lp)

    if not sentieri_in_storia:
        out.append("_(nessun sentiero registrato per questa storia)_\n")
        return "".join(out)

    paths_data = g.get("world_conventions", {}).get("path_details", {}).get("paths", {})

    for sentiero_id in sentieri_in_storia:
        out.append(f"### `{sentiero_id}`\n")
        # Path details dal grafo
        pdata = paths_data.get(sentiero_id, {})
        rel_details = []
        for d in pdata.get("details", []):
            if sid in d.get("appears_in_stories", []):
                rel_details.append(d)
        if rel_details:
            for d in rel_details:
                out.append(f"\n**Dettaglio per {sid}:** `{d.get('id','?')}`\n")
                out.append(f"- **Cosa:** {d.get('what','—')}\n")
                if d.get("where_along_path"):
                    out.append(f"- **Dove lungo il sentiero:** {d['where_along_path']}\n")
                if d.get("visibility"):
                    out.append(f"- **Visibilità:** {d['visibility']}\n")
                if d.get("perception_pattern"):
                    out.append(f"- **Pattern di percezione:** {d['perception_pattern']}\n")
                if d.get("state_by_story"):
                    out.append(f"- **Stato in {sid}:** {d['state_by_story'].get(sid, '—')}\n")
                if d.get("notes"):
                    out.append(f"- **Note:** {d['notes']}\n")
        else:
            # Sentiero senza dettaglio per questa storia (Tier B/C non ancora popolato, o questa storia non ha dettaglio assegnato)
            out.append(f"_(nessun dettaglio stabile assegnato a {sid} per questo sentiero — è di passaggio)_\n")

        # Aspetto generale dalla scheda catalogo
        scheda_path = find_location_scheda(repo_root, sentiero_id)
        scheda_complete = False
        if scheda_path:
            scheda_text = scheda_path.read_text(encoding="utf-8")
            aspetto = extract_section(scheda_text, "Aspetto / forma")
            atm = extract_section(scheda_text, "Palette e atmosfera")
            esp = extract_section(scheda_text, "Espressione / comportamento")
            coe = extract_section(scheda_text, "Coerenza cross-scena (cose che NON cambiano)")
            ctx = extract_section(scheda_text, "Contesto e ambientazioni ricorrenti")
            if aspetto and atm and (esp or coe):
                scheda_complete = True
            if aspetto:
                out.append(f"\n**Aspetto generale (catalogo):** {aspetto}\n")
            if atm:
                out.append(f"\n**Palette/atmosfera (catalogo):** {atm}\n")
            if esp:
                out.append(f"\n**Comportamento (catalogo):** {esp}\n")
            if coe:
                out.append(f"\n**Coerenza cross-scena (catalogo):** {coe}\n")
            if ctx:
                out.append(f"\n**Contesto ricorrente (catalogo):** {ctx}\n")
        # Grok sempre se esiste
        grok_path = find_grok_prompt(repo_root, sentiero_id, "location")
        if grok_path:
            grok_text = grok_path.read_text(encoding="utf-8")
            canon = extract_grok_canon(grok_text)
            block = canon.get("object_or_scene_canon") or canon.get("main_prompt") or ""
            if block:
                label = "Canone visivo (da `prompt_grok.md` — supporto)" if scheda_complete else "Canone visivo (da `prompt_grok.md` — fallback principale)"
                out.append(f"\n**{label}:**\n")
                out.append("```\n")
                out.append(block)
                out.append("\n```\n")
        out.append("\n")
    return "".join(out)


def build_luoghi_chiave(repo_root: Path, g: dict, s: dict) -> str:
    """Sezione 7-bis — Luoghi non-sentiero chiave (location_primary + alcuni secondary)."""
    out = ["\n---\n\n## §7-bis. LUOGHI CHIAVE (non sentieri)\n\n"]
    out.append("> Aspetto/atmosfera dei luoghi principali della storia, dal catalogo schede. Il testo deve evocarli senza descriverli per intero.\n\n")

    luoghi_da_dettagliare = []
    lp = s.get("location_primary", {})
    if lp.get("id") and not any(k in lp["id"] for k in ["sentiero","via_","viottolo"]):
        luoghi_da_dettagliare.append(("primario", lp["id"], lp.get("note","")))

    # Solo luoghi non-sentiero, e non più di 5 secondari per non gonfiare
    count = 0
    for ls in s.get("locations_secondary", []):
        lid = ls.get("id","")
        if not lid: continue
        if any(k in lid for k in ["sentiero","via_","viottolo"]): continue
        if count >= 6: break
        luoghi_da_dettagliare.append(("secondario", lid, ls.get("note","")))
        count += 1

    if not luoghi_da_dettagliare:
        out.append("_(nessun luogo chiave non-sentiero)_\n")
        return "".join(out)

    for ruolo, lid, note in luoghi_da_dettagliare:
        out.append(f"### `{lid}` ({ruolo})\n")
        if note:
            out.append(f"- **Note dal grafo:** {note}\n")
        scheda_path = find_location_scheda(repo_root, lid)
        scheda_complete = False
        if scheda_path:
            scheda_text = scheda_path.read_text(encoding="utf-8")
            aspetto = extract_section(scheda_text, "Aspetto / forma")
            atm = extract_section(scheda_text, "Palette e atmosfera")
            esp = extract_section(scheda_text, "Espressione / comportamento")
            coe = extract_section(scheda_text, "Coerenza cross-scena (cose che NON cambiano)")
            ctx = extract_section(scheda_text, "Contesto e ambientazioni ricorrenti")
            if aspetto and esp and atm:
                scheda_complete = True
            if aspetto:
                out.append(f"- **Aspetto:** {aspetto}\n")
            if esp:
                out.append(f"- **Comportamento:** {esp}\n")
            if atm:
                out.append(f"- **Atmosfera:** {atm}\n")
            if coe:
                out.append(f"- **Coerenza fissa:** {coe}\n")
            if ctx:
                out.append(f"- **Contesto e ambientazioni ricorrenti:** {ctx}\n")
        # Grok sempre incluso se esiste
        grok_path = find_grok_prompt(repo_root, lid, "location")
        if grok_path:
            grok_text = grok_path.read_text(encoding="utf-8")
            canon = extract_grok_canon(grok_text)
            block = canon.get("object_or_scene_canon") or canon.get("main_prompt") or ""
            if block:
                if scheda_complete:
                    label = "Canone visivo (da `prompt_grok.md` — supporto, in inglese)"
                else:
                    label = "Canone visivo (da `prompt_grok.md` — fallback principale, in inglese)"
                out.append(f"\n- **{label}:**\n")
                out.append("  ```\n")
                out.append(indent(block, "  "))
                out.append("\n  ```\n")
        imgs = list_canonical_images(repo_root, lid, "location")
        if imgs:
            out.append(f"- **Immagini canoniche di riferimento:** {', '.join(imgs)}\n")
        out.append("\n")
    return "".join(out)


def build_oggetti(repo_root: Path, g: dict, s: dict) -> str:
    """Sezione 7-ter — Oggetti simbolo presenti."""
    objs = s.get("oggetti_simbolo_presenti", [])
    out = ["\n---\n\n## §7-ter. OGGETTI SIMBOLO PRESENTI\n\n"]
    if not objs:
        out.append("_(nessun oggetto simbolo registrato)_\n")
        return "".join(out)
    for obj_ref in objs:
        oid = obj_ref.get("id") if isinstance(obj_ref, dict) else obj_ref
        if not oid: continue
        out.append(f"### `{oid}`\n")
        if isinstance(obj_ref, dict):
            for k, v in obj_ref.items():
                if k == "id": continue
                out.append(f"- **{k}:** {v}\n")
        # Da scheda
        scheda_complete = False
        scheda_path = find_object_scheda(repo_root, oid)
        if scheda_path:
            scheda_text = scheda_path.read_text(encoding="utf-8")
            aspetto = extract_section(scheda_text, "Aspetto / forma")
            funz = extract_section(scheda_text, "Funzione narrativa")
            simb = extract_section(scheda_text, "Simbolismo")
            if aspetto:
                scheda_complete = True
                out.append(f"- **Aspetto (catalogo):** {aspetto}\n")
            if funz:
                out.append(f"- **Funzione narrativa:** {funz}\n")
            if simb:
                out.append(f"- **Simbolismo:** {simb}\n")
        # Grok sempre se esiste
        grok_path = find_grok_prompt(repo_root, oid, "object")
        if grok_path:
            grok_text = grok_path.read_text(encoding="utf-8")
            canon = extract_grok_canon(grok_text)
            block = canon.get("object_or_scene_canon") or canon.get("main_prompt") or ""
            if block:
                label = "Canone visivo (da `prompt_grok.md` — supporto)" if scheda_complete else "Canone visivo (da `prompt_grok.md` — fallback principale)"
                out.append(f"- **{label}:**\n")
                out.append("  ```\n")
                out.append(indent(block, "  "))
                out.append("\n  ```\n")
        # Da grafo
        og = g["entities"].get("objects", {}).get(oid, {})
        if og.get("description"):
            out.append(f"- **Descrizione (grafo):** {og['description']}\n")
        # Immagini
        imgs = list_canonical_images(repo_root, oid, "object")
        if imgs:
            out.append(f"- **Immagini canoniche di riferimento:** {', '.join(imgs)}\n")
        out.append("\n")
    return "".join(out)


def build_saluti(repo_root: Path, s: dict) -> str:
    """Sezione 8 — Saluti dei gruppi presenti."""
    out = ["\n---\n\n## §8. SALUTI DEI GRUPPI APPLICABILI IN QUESTA STORIA\n\n"]
    out.append("> Quando un membro di un gruppo-istituzione appare in scena, il suo saluto va integrato come fatto del mondo (mai spiegato).\n\n")

    # Identifica gruppi presenti via cornici e cast
    gruppi_presenti = set()
    for cd in s.get("cornice_dettagli", []):
        who = cd.get("who", {})
        if isinstance(who, dict) and who.get("kind") == "gruppo":
            gruppi_presenti.add(who.get("ref"))
    for c in s.get("characters_in_scene", []) + s.get("characters_offscreen_or_background", []):
        cid = c.get("id")
        if cid in {"camminanti","mantenitori","coltivatori_del_cerchio","mercato_del_mezzogiorno","pastori","pescatori_case_basse"}:
            gruppi_presenti.add(cid)

    if not gruppi_presenti:
        out.append("_(nessun gruppo-istituzione in scena)_\n")
        return "".join(out)

    for grp in sorted(gruppi_presenti):
        scheda = repo_root / "visual" / "personaggi" / "collettivi" / grp / "scheda.md"
        if scheda.exists():
            txt = scheda.read_text(encoding="utf-8")
            saluto = extract_section(txt, "Saluto del gruppo")
            if saluto:
                w = saluto.split()
                if len(w) > 200: saluto = " ".join(w[:200]) + "…"
                out.append(f"### `{grp}`\n\n{saluto}\n\n")
            else:
                out.append(f"### `{grp}`\n_(saluto non trovato in scheda)_\n\n")
    return "".join(out)


def build_formula_ritornello(g: dict, sid: str) -> str:
    """Sezione 9 — Formula ritornello applicata in questa storia."""
    out = ["\n---\n\n## §9. FORMULA RITORNELLO «che animale è»\n\n"]
    refrain = g.get("world_conventions", {}).get("refrain_animal_identification", {})
    formula = refrain.get("formula", {})
    if formula:
        out.append("**Formula canonica:**\n")
        out.append(f"- Singolare: `{formula.get('singular','—')}`\n")
        out.append(f"- Plurale: `{formula.get('plural','—')}`\n\n")

    # Applicazioni in questa storia dal quote_tracker
    qt = g.get("quote_tracker", {}).get("refrain_animal_used_per_story", [])
    apps = [entry for entry in qt if (isinstance(entry, list) and len(entry) >= 1 and entry[0] == sid)]
    if apps:
        out.append(f"**Applicazioni in {sid}:**\n\n")
        for entry in apps:
            # entry: [sid, gruppo, animale, modalità]
            grp = entry[1] if len(entry) > 1 else "?"
            animal = entry[2] if len(entry) > 2 else "?"
            mode = entry[3] if len(entry) > 3 else "singular"
            if mode == "singular":
                example = formula.get("singular", "").replace("<ruolo del gruppo>", grp.replace("_", " ")).replace("<animale>", animal if isinstance(animal, str) else str(animal))
            else:
                if isinstance(animal, list):
                    rep = ", ".join(animal)
                    example = formula.get("plural", "").replace("<gruppo>", grp.replace("_", " ")).replace("<animale>, <animale>, <animale>", rep)
                else:
                    example = "(plurale ma animale non lista)"
            out.append(f"- Gruppo: **{grp}** | Modalità: `{mode}` | Animale: `{animal}`\n")
            out.append(f"  - Frase da inserire: «{example}»\n")
    else:
        out.append("_(nessuna applicazione registrata per questa storia)_\n")

    out.append("\n**Vincoli:**\n")
    out.append(f"- Solo a individui anonimi dei gruppi-istituzione\n")
    out.append(f"- Mai a personaggi nominati (Fiamma, Stria, ecc. hanno specie canonica fissa)\n")
    out.append(f"- Solo al primo incontro di un membro del gruppo nella storia\n")
    return "".join(out)


def build_vincoli_universali(repo_root: Path, g: dict, s: dict) -> str:
    """Sezione 10 — Vincoli universali e voice notes essenziali."""
    out = ["\n---\n\n## §10. VINCOLI UNIVERSALI DELLA SCRITTURA\n\n"]

    out.append("### §10.1 Voci dei tre fratelli (Carta Voce §1.3)\n\n")
    for cid in ["gabriel", "elias", "noah"]:
        c = g["entities"]["characters"].get(cid, {})
        out.append(f"- **{cid}**: {c.get('voice_notes','?')}\n")
    out.append("\nTest di validazione: togliendo i nomi dai dialoghi dei fratelli, almeno 7 su 10 dovrebbero essere riconoscibili.\n\n")

    # Voice_notes_essential della storia
    if s.get("voice_notes_essential"):
        out.append("### §10.2 Voice notes essenziali per QUESTA storia\n\n")
        vne = s["voice_notes_essential"]
        if isinstance(vne, list):
            for v in vne:
                out.append(f"- {v}\n")
        else:
            out.append(f"{vne}\n")
        out.append("\n")

    # Narrator_address e narrator_meta_voice
    if s.get("narrator_address"):
        out.append("### §10.3 Narrator address (rivolgersi al lettore)\n\n")
        na = s["narrator_address"]
        if isinstance(na, dict):
            out.append(f"- **Permesso:** {na.get('allowed','?')}\n")
            if na.get("instances"):
                for inst in na["instances"]:
                    out.append(f"- **Istanza:** {inst}\n")
            if na.get("notes"):
                out.append(f"- **Note:** {na['notes']}\n")
        elif isinstance(na, list):
            for inst in na:
                out.append(f"- {inst}\n")
        else:
            out.append(f"{na}\n")
        out.append("\n")

    if s.get("narrator_meta_voice"):
        out.append("### §10.4 Narrator meta-voice\n\n")
        nmv = s["narrator_meta_voice"]
        out.append(f"{nmv}\n\n" if isinstance(nmv, str) else f"{json.dumps(nmv, ensure_ascii=False, indent=2)}\n\n")

    # Pattern AI da bandire — INTEGRALE
    out.append("### §10.5 Pattern AI da bandire (documento integrale)\n\n")
    pattern_path = repo_root / "pipeline_narrativa" / "documenti_progetto" / "PATTERN_AI_DA_BANDIRE_v1.md"
    if pattern_path.exists():
        pattern_text = pattern_path.read_text(encoding="utf-8")
        # rimuovo eventuale frontmatter del file
        pattern_clean = re.sub(r"^---\n.*?\n---\n", "", pattern_text, count=1, flags=re.DOTALL)
        out.append(pattern_clean.strip() + "\n\n")
    else:
        out.append("_(PATTERN_AI_DA_BANDIRE_v1.md non trovato — fallback minimo)_\n\n")
        out.append("- triple di aggettivi sequenziali\n- metafore innestate\n- registro alto sistematico\n- avverbi-firma ripetuti\n- 'danza', 'abbraccio', 'sussurro' come verbi metaforici\n- chiusure morali esplicite\n- ridondanza testo↔immagine\n\n")

    out.append("### §10.6 Regole di registro picture book (3-6 anni)\n\n")
    out.append("- Frasi corte. Pause nette. Mai subordinate concatenate.\n")
    out.append("- Ritmo regolare al servizio della lettura ad alta voce.\n")
    out.append("- Il testo NON descrive l'illustrazione: la sottende, completa, dialoga.\n")
    out.append("- Una pagina = un hook visivo. Il testo per pagina è breve (50-150 parole tipicamente).\n")
    out.append("- Onomatopee mantenute pulite, come elementi del mondo (mai stilizzate via *italics*).\n")
    out.append("- Mai giudizio morale, mai 'lezione'. Far accadere, non spiegare.\n")
    return "".join(out)


def build_quote_tracker_awareness(g: dict, sid: str, s: dict) -> str:
    """Sezione 11 — Quote tracker awareness."""
    out = ["\n---\n\n## §11. QUOTE TRACKER — quote di saga e pattern attivi\n\n"]
    out.append("> Il tracker monitora la distribuzione di pattern, frasi-firma, frammenti, onomatopee in tutta la saga. Per QUESTA storia, qui ciò che è rilevante.\n\n")

    qt = g.get("quote_tracker", {})

    # Pattern A
    if "pattern_a_pre_eco_stories" in qt or "pattern_a_full_stories" in qt:
        out.append("### Pattern A («quando l'acqua trema»)\n")
        pre = qt.get("pattern_a_pre_eco_stories", [])
        full = qt.get("pattern_a_full_stories", [])
        out.append(f"- Pre-eco già piazzati in: {pre}\n")
        out.append(f"- Pattern A pieno in: {full}\n")
        if sid in pre:
            out.append(f"- **In {sid}:** pre-eco da inserire (incresparsi controcorrente, anomalia minima non nominata)\n")
        if sid in full:
            out.append(f"- **In {sid}:** pattern pieno (esplicitazione del fenomeno)\n")
        if s.get("pattern_a_active"):
            out.append(f"- **Pattern A active in {sid}:** {s['pattern_a_active']}\n")
        if s.get("pattern_a_notes"):
            out.append(f"- **Pattern A notes:** {s['pattern_a_notes']}\n")
        out.append("\n")

    # When water trembles
    if s.get("when_water_trembles"):
        out.append(f"### \"Quando l'acqua trema\" in {sid}\n")
        wwt = s["when_water_trembles"]
        if isinstance(wwt, dict):
            for k, v in wwt.items():
                out.append(f"- **{k}:** {v}\n")
        else:
            out.append(f"{wwt}\n")
        out.append("\n")

    # TOK-TOK-TOK
    tok = qt.get("tok_tok_tok_stories", [])
    out.append(f"### Onomatopea TOK-TOK-TOK (Nodo)\n")
    out.append(f"- Storie con TOK-TOK-TOK pieno: {tok}\n")
    out.append(f"- Quota saga: max 4-5 storie\n")
    if sid in tok:
        out.append(f"- **In {sid}:** TOK-TOK-TOK presente\n")
    out.append("\n")

    # Frammenti pre-Vento Grunto
    gf = qt.get("grunto_fragments_planned_stories", [])
    if gf:
        out.append(f"### Frammenti pre-Vento di Grunto\n")
        out.append(f"- Storie pianificate: {gf}\n")
        if sid in gf:
            out.append(f"- **In {sid}:** frammento pre-Vento da inserire (incompleto, mai didascalico)\n")
        if s.get("grunto_memory_fragment"):
            out.append(f"- **Frammento per {sid}:** {s['grunto_memory_fragment']}\n")
        out.append("\n")

    # Notti
    night = qt.get("night_scenes", [])
    if sid in night or s.get("night_scene"):
        out.append(f"### Scena notturna\n")
        out.append(f"- Storie con notte: {night}\n")
        if s.get("night_scene_notes"):
            out.append(f"- **Note notte in {sid}:** {s['night_scene_notes']}\n")
        out.append("\n")

    # Onomatopee firma di questa storia
    if s.get("onomatopee_firma"):
        out.append(f"### Onomatopee-firma in {sid}\n")
        of = s["onomatopee_firma"]
        if isinstance(of, list):
            for o in of:
                out.append(f"- {o}\n")
        else:
            out.append(f"{of}\n")
        out.append("\n")

    # Active constraints
    if s.get("active_constraints_touched"):
        out.append(f"### Vincoli attivi in {sid}\n")
        for c in s["active_constraints_touched"]:
            out.append(f"- {c}\n")
        out.append("\n")

    # Personaggi vincoli attivi
    if s.get("personaggi_vincoli_attivi"):
        out.append(f"### Vincoli per personaggio specifici di {sid}\n")
        pv = s["personaggi_vincoli_attivi"]
        if isinstance(pv, dict):
            for k, v in pv.items():
                out.append(f"- **{k}:** {v}\n")
        elif isinstance(pv, list):
            for v in pv:
                out.append(f"- {v}\n")
        out.append("\n")

    return "".join(out)


def build_callbacks_seeds(s: dict) -> str:
    """Sezione 12 — Echi, callback, semi."""
    out = ["\n---\n\n## §12. ECHI, CALLBACK, SEMI\n\n"]
    out.append("> Cosa questa storia richiama da prima e cosa lascia per dopo. Il testo finale deve onorare i callback senza sottolinearli.\n\n")

    # Callbacks made (questa storia richiama)
    cb_made = s.get("callbacks_made", [])
    if cb_made:
        out.append("### Callback fatti (cose richiamate da storie precedenti)\n")
        for cb in cb_made:
            if isinstance(cb, dict):
                out.append(f"- **{cb.get('id','?')}:** {cb.get('description', cb.get('note',''))}\n")
                if cb.get("from_story"): out.append(f"  - Da storia: {cb['from_story']}\n")
            else:
                out.append(f"- {cb}\n")
        out.append("\n")

    # Callback summary
    if s.get("callback_summary"):
        out.append(f"### Callback summary\n{s['callback_summary']}\n\n")

    # Seeds
    sp = s.get("seeds_planted", [])
    if sp:
        out.append("### Semi piantati (per storie future)\n")
        for seed in sp:
            if isinstance(seed, dict):
                out.append(f"- **{seed.get('id','?')}:** {seed.get('description', seed.get('note',''))}\n")
                if seed.get("for_story"): out.append(f"  - Per: {seed['for_story']}\n")
            else:
                out.append(f"- {seed}\n")
        out.append("\n")

    sm = s.get("seeds_maturing_here", [])
    if sm:
        out.append("### Semi che maturano in questa storia\n")
        for seed in sm:
            if isinstance(seed, dict):
                out.append(f"- **{seed.get('id','?')}:** {seed.get('description', seed.get('note',''))}\n")
            else:
                out.append(f"- {seed}\n")
        out.append("\n")

    sb = s.get("seeds_bloomed_here", [])
    if sb:
        out.append("### Semi che fioriscono in questa storia\n")
        for seed in sb:
            if isinstance(seed, dict):
                out.append(f"- **{seed.get('id','?')}:** {seed.get('description', seed.get('note',''))}\n")
            else:
                out.append(f"- {seed}\n")
        out.append("\n")

    spu = s.get("seeds_picked_up", [])
    if spu:
        out.append("### Semi raccolti (callback chiusi qui)\n")
        for seed in spu:
            if isinstance(seed, dict):
                out.append(f"- **{seed.get('id','?')}:** {seed.get('description', seed.get('note',''))}\n")
                if seed.get("from_story"): out.append(f"  - Da: {seed['from_story']}\n")
            else:
                out.append(f"- {seed}\n")
        out.append("\n")

    # Debiti narrativi
    do = s.get("debts_opened", [])
    dc = s.get("debts_closed", [])
    if do or dc:
        out.append("### Debiti narrativi\n")
        if do:
            out.append("**Aperti qui:**\n")
            for d in do:
                if isinstance(d, dict):
                    out.append(f"- {d.get('id','?')}: {d.get('description','')}\n")
                else:
                    out.append(f"- {d}\n")
        if dc:
            out.append("\n**Chiusi qui:**\n")
            for d in dc:
                if isinstance(d, dict):
                    out.append(f"- {d.get('id','?')}: {d.get('description','')}\n")
                else:
                    out.append(f"- {d}\n")
        out.append("\n")

    # Fear arc touched
    if s.get("fear_touched"):
        out.append(f"### Arco paura toccato qui\n")
        ft = s["fear_touched"]
        if isinstance(ft, dict):
            for k, v in ft.items():
                out.append(f"- **{k}:** {v}\n")
        else:
            out.append(f"{ft}\n")
        out.append("\n")

    # Quartieri attraversati
    if s.get("quartieri_attraversati"):
        out.append(f"### Quartieri attraversati\n")
        qa = s["quartieri_attraversati"]
        if isinstance(qa, list):
            out.append(f"- {', '.join(qa)}\n\n")
        else:
            out.append(f"- {qa}\n\n")

    # Structural notes
    if s.get("structural_notes"):
        out.append(f"### Note strutturali\n{s['structural_notes']}\n\n")

    return "".join(out)


def build_closing_instruction(s: dict) -> str:
    """Sezione finale — istruzioni operative all'agente prosa."""
    length = s.get("estimated_length", "?")
    out = "\n---\n\n## §13. ISTRUZIONE OPERATIVA ALL'AGENTE PROSA\n\n"
    out += "Hai tutto. La scrittura sarà **collaborativa** in chat con Ray, non one-shot.\n\n"
    out += "**Modalità di lavoro:**\n"
    out += "- Procedi **una sezione/pagina alla volta**, allineata agli hook visivi (§4).\n"
    out += "- Ogni hook = una pagina di libro = un blocco di testo (50-150 parole tipicamente).\n"
    out += "- Dopo ogni blocco, **fermati**. Ray rivede, eventualmente chiede modifiche, e dice 'avanti'.\n"
    out += "- Se Ray non interviene tra un blocco e il successivo, prosegui in modo lineare ma **senza fretta**: è sempre meglio una pagina ben pesata che due pagine medie.\n\n"
    out += f"**Lunghezza target totale:** circa **{length} parole** (±15% accettabile).\n\n"
    out += "**Vincoli sul testo che produci:**\n"
    out += "- Voce autoriale finale, italiano picture book 3-6 anni, registro come specificato in §1.\n"
    out += "- Frasi-codice e frasi-formula (§5, §9) integrate alla lettera dove indicato — sono inalterabili.\n"
    out += "- Cornici (§6) come sfondo silenzioso, max 2-3 frasi ognuna nel testo finale.\n"
    out += "- Saluti dei gruppi (§8) integrati come fatti del mondo, mai spiegati.\n"
    out += "- Sentieri (§7) attraversati col loro dettaglio stabile pertinente, mai descritti per intero.\n"
    out += "- Il testo per pagina **dialoga con l'illustrazione**: NON descrive ciò che il bambino vede già, completa o sottende.\n"
    out += "- I pattern AI banditi (§10.5) sono inderogabili.\n\n"
    out += "**Ogni volta che produci un blocco di testo:**\n"
    out += "- Indica chiaramente a quale hook si riferisce (`### Pagina X — hook sNN_hMM`)\n"
    out += "- Sotto il testo, una breve nota tecnica (1-3 punti):\n"
    out += "  - frasi-codice integrate in questo blocco\n"
    out += "  - vincoli/quote che hai considerato (es. 'Pattern A pre-eco inserito', 'cornice C1 integrata di striscio')\n"
    out += "  - eventuali domande o punti di incertezza per Ray\n"
    out += "- Mai commento prosaico estraneo, mai apologie, mai meta-discussione.\n\n"
    out += "**Quando hai finito tutto il libro** (10 pagine), scrivi un breve consuntivo finale (5-8 punti):\n"
    out += "- pattern-firma applicati (triade asimmetrica, coppia spezzata, ecc.)\n"
    out += "- frasi-codice integrate complessivamente\n"
    out += "- callback chiusi e semi piantati onorati\n"
    out += "- punti di incertezza residui\n"
    return out


# =============================================================================
# MAIN
# =============================================================================

def build_brief(repo_root: Path, sid: str) -> str:
    g = load_graph(repo_root)
    s = g["stories"].get(sid)
    if not s:
        raise ValueError(f"Storia {sid} non trovata nel grafo.")
    narr = load_narrazione_fattuale(repo_root, sid)

    parts = []
    parts.append(build_frontmatter(g, sid, s))
    parts.append(build_core(s))
    parts.append(build_stato_mondo(g, sid))
    parts.append(build_narrazione_fattuale(repo_root, sid))
    parts.append(build_hooks(s))
    parts.append(build_cast_in_scena(repo_root, g, s, sid, narr))
    parts.append(build_cornici(s))
    parts.append(build_sentieri(repo_root, g, s, sid))
    parts.append(build_luoghi_chiave(repo_root, g, s))
    parts.append(build_oggetti(repo_root, g, s))
    parts.append(build_saluti(repo_root, s))
    parts.append(build_formula_ritornello(g, sid))
    parts.append(build_vincoli_universali(repo_root, g, s))
    parts.append(build_quote_tracker_awareness(g, sid, s))
    parts.append(build_callbacks_seeds(s))
    parts.append(build_closing_instruction(s))
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Costruisce il writing brief per una storia.")
    ap.add_argument("--story", help="ID storia (es. s01). Obbligatorio se non --all.")
    ap.add_argument("--all", action="store_true", help="Genera brief per tutte le 12 storie.")
    ap.add_argument("--repo-root", default=".", help="Path della repo (default: .)")
    ap.add_argument("--output-dir", default="pipeline_narrativa/writing_briefs",
                    help="Directory output (default: pipeline_narrativa/writing_briefs)")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = repo_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.all:
        g = load_graph(repo_root)
        sids = sorted(g["stories"].keys())
    elif args.story:
        sids = [args.story]
    else:
        ap.error("Usa --story sNN oppure --all")

    for sid in sids:
        print(f"Generazione brief per {sid}…", file=sys.stderr)
        try:
            brief = build_brief(repo_root, sid)
            out_path = output_dir / f"{sid}_writing_brief.md"
            out_path.write_text(brief, encoding="utf-8")
            words = len(brief.split())
            print(f"  ✓ {out_path} ({words} parole)", file=sys.stderr)
        except Exception as e:
            print(f"  ✗ errore su {sid}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
