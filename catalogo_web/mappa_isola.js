/* ===========================================================================
   mappa_isola.js — Mappa illustrata navigabile dell'Isola dei Tre Venti
   ===========================================================================

   Renderizza una mappa SVG dell'isola con:
   - sfondo: illustrazione master "isola_base_v1.jpg" (acquerello, no edifici)
   - sopra: edifici/luoghi posizionati come asset 3D PNG (Travian-style)
   - se manca l'asset 3D di un edificio, viene mostrato un placeholder
     trasparente cliccabile (cerchio + label).

   Ogni elemento è cliccabile -> apre la scheda dell'entità nel catalogo
   (riusa il routing #/entity/<id> esistente).

   FONTE COORDINATE:  cartografia/geo/island.geojson (dal geojson canonico)
   FONTE ASSET 3D:    cartografia/assets_mappa/<id>.png
   FONTE BASE:        cartografia/assets_mappa/_base/isola_base_v1.jpg

   Calibrazione bbox geografica -> viewBox SVG: vedi MAPPA_CONFIG.bbox_geo.
   Modalità debug: aggiungi #/mappa-isola?debug per vedere bbox + griglia.
   =========================================================================== */

const MAPPA_CONFIG = {
  // Path relativi al catalogo_web/ (servito come root o come sottocartella)
  base_image: "../cartografia/assets_mappa/_base/isola_base_v1.jpg",
  geojson_url: "../cartografia/geo/island.geojson",
  assets_dir: "../cartografia/assets_mappa/",

  // Dimensioni dell'immagine base (px reali del file).
  // viewBox SVG = stesse dimensioni per mappatura 1:1.
  image_w: 1120,
  image_h: 912,

  // Bounding box geografica che corrisponde all'AREA DIPINTA dell'isola
  // sull'immagine base. Calibrazione iniziale derivata dal geojson:
  //   island_outline bbox: lon 17.958198..18.044687, lat 34.468222..34.528694
  // L'immagine ha proporzioni 1.228:1 mentre il bbox geo è 1.43:1, quindi
  // l'isola dipinta NON copre tutto il viewBox: c'è un margine di mare
  // attorno. I 4 valori qui sotto definiscono il rettangolo geografico
  // che mappiamo sul viewBox intero (mare incluso).
  //
  // Se gli edifici cadono fuori posto, basta aggiustare questi 4 numeri
  // (allargare = isola appare piu' piccola; restringere = piu' grande).
  bbox_geo: {
    lon_min: 17.945,    // bordo ovest (un po' a ovest del bbox isola)
    lon_max: 18.060,    // bordo est
    lat_min: 34.460,    // bordo sud (incluso sfocio fiume)
    lat_max: 34.535     // bordo nord (incluso oltre montagne)
  },

  // Tipi GeoJSON che vogliamo mostrare come slot sulla mappa.
  // Le STRADE/SENTIERI/QUARTIERI/FIUMI non si mostrano: stanno gia'
  // dipinti nell'immagine base.
  slot_types: [
    "building",       // edifici (forno, fabbro, scuola, case...)
    "burrow",         // tane (casa salvia, casa zolla, tana rovo)
    "cave",           // grotte (grotta grunto)
    "pier",           // pontili
    "landmark",       // luoghi notevoli (albero vecchio, due massi, pozzo...)
    "water_pool",     // pozze (pozza pastori)
    "tree",           // alberi singoli notevoli (noce della scuola)
    "square"          // piazze (piazza villaggio)
  ],

  // Dimensione default degli slot in viewBox units (pixel-equivalenti).
  // Gli edifici avranno dimensione adattata a tipo (vedi slotSizeFor).
  slot_size_default: 60,

  // Soglia oltre la quale il PNG asset si scala invece di restare fisso
  // (per landmark grandi tipo "due_massi" o "albero_vecchio").
  large_landmarks: ["albero_vecchio", "due_massi", "roccia_alta", "noce_della_scuola"]
};

// ============================================================================
// STATO INTERNO
// ============================================================================
const mappaState = {
  geojson: null,        // contenuto island.geojson
  slots: [],            // array di {id, name, type, x, y, asset_url, has_asset}
  asset_check_cache: {} // id -> bool (esistenza asset 3D)
};

// ============================================================================
// ENTRY POINT (chiamato da app.js quando hash = #/mappa-isola)
// ============================================================================
async function renderMappaIsola() {
  const c = document.getElementById("content");
  c.innerHTML = `<div class="mappa-loading">Caricamento mappa…</div>`;

  try {
    if (!mappaState.geojson) {
      const r = await fetch(MAPPA_CONFIG.geojson_url);
      if (!r.ok) throw new Error(`geojson HTTP ${r.status}`);
      mappaState.geojson = await r.json();
    }

    const slots = extractSlotsFromGeoJSON(mappaState.geojson);
    mappaState.slots = slots;

    // verifica esistenza asset 3D in parallelo (HEAD requests)
    await Promise.all(slots.map(s => checkAssetExists(s)));

    renderMapSVG(slots);

  } catch (err) {
    console.error("[mappa] errore caricamento:", err);
    c.innerHTML = `
      <div class="mappa-error">
        <h2>Errore caricamento mappa</h2>
        <p>${escapeHtmlMappa(String(err.message || err))}</p>
        <p>Verifica che <code>${MAPPA_CONFIG.geojson_url}</code> sia raggiungibile.</p>
      </div>`;
  }
}

// ============================================================================
// ESTRAZIONE SLOT DAL GEOJSON
// ============================================================================
function extractSlotsFromGeoJSON(geojson) {
  const slots = [];
  for (const f of geojson.features || []) {
    const p = f.properties || {};
    const t = p.type;
    if (!MAPPA_CONFIG.slot_types.includes(t)) continue;
    if (p.aggregate) continue; // skip features aggregate

    const center = featureCenter(f);
    if (!center) continue;
    const [lon, lat] = center;
    const [x, y] = lonLatToViewBox(lon, lat);

    slots.push({
      id: p.id,
      name: p.name || p.id,
      type: t,
      category: p.category || "",
      quarter: p.quarter || "",
      status: p.status || "provvisorio",
      lon, lat, x, y,
      size: slotSizeFor(p),
      asset_url: `${MAPPA_CONFIG.assets_dir}${p.id}.png`,
      has_asset: false  // popolato da checkAssetExists()
    });
  }
  return slots;
}

function featureCenter(f) {
  const g = f.geometry;
  if (!g) return null;
  if (g.type === "Point") {
    return g.coordinates;
  }
  if (g.type === "Polygon") {
    const ring = g.coordinates[0];
    let cx = 0, cy = 0;
    for (const c of ring) { cx += c[0]; cy += c[1]; }
    return [cx / ring.length, cy / ring.length];
  }
  if (g.type === "MultiPoint") {
    const pts = g.coordinates;
    let cx = 0, cy = 0;
    for (const c of pts) { cx += c[0]; cy += c[1]; }
    return [cx / pts.length, cy / pts.length];
  }
  return null;
}

function lonLatToViewBox(lon, lat) {
  const { lon_min, lon_max, lat_min, lat_max } = MAPPA_CONFIG.bbox_geo;
  const W = MAPPA_CONFIG.image_w, H = MAPPA_CONFIG.image_h;
  const x = ((lon - lon_min) / (lon_max - lon_min)) * W;
  const y = ((lat_max - lat) / (lat_max - lat_min)) * H;  // y SVG cresce verso il basso
  return [x, y];
}

function slotSizeFor(props) {
  if (MAPPA_CONFIG.large_landmarks.includes(props.id)) return 100;
  if (props.type === "square") return 90;       // piazza grande
  if (props.type === "landmark") return 50;
  if (props.type === "tree") return 80;
  if (props.type === "burrow" || props.type === "cave") return 55;
  return MAPPA_CONFIG.slot_size_default;        // building default
}

async function checkAssetExists(slot) {
  if (mappaState.asset_check_cache[slot.id] !== undefined) {
    slot.has_asset = mappaState.asset_check_cache[slot.id];
    return;
  }
  try {
    const r = await fetch(slot.asset_url, { method: "HEAD" });
    slot.has_asset = r.ok;
  } catch (_) {
    slot.has_asset = false;
  }
  mappaState.asset_check_cache[slot.id] = slot.has_asset;
}

// ============================================================================
// RENDERING SVG
// ============================================================================
function renderMapSVG(slots) {
  const c = document.getElementById("content");
  const debug = (location.hash.includes("?debug"));
  const W = MAPPA_CONFIG.image_w, H = MAPPA_CONFIG.image_h;

  const slotsSVG = slots.map(s => slotToSVG(s, debug)).join("\n");

  const debugOverlay = debug ? renderDebugOverlay() : "";

  const total = slots.length;
  const placed = slots.filter(s => s.has_asset).length;

  c.innerHTML = `
    <div class="mappa-page">
      <header class="mappa-header">
        <h1>Mappa dell'Isola</h1>
        <p class="mappa-subtitle">
          ${placed}/${total} edifici con asset 3D ·
          <span class="mappa-hint">click su un punto per la scheda</span>
        </p>
      </header>

      <div class="mappa-stage" id="mappa-stage">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 ${W} ${H}"
          preserveAspectRatio="xMidYMid meet"
          class="mappa-svg"
          role="img"
          aria-label="Mappa illustrata dell'Isola dei Tre Venti">

          <image href="${MAPPA_CONFIG.base_image}"
                 x="0" y="0" width="${W}" height="${H}"
                 preserveAspectRatio="none" />

          ${debugOverlay}

          <g class="mappa-slots">
            ${slotsSVG}
          </g>
        </svg>
      </div>

      <footer class="mappa-footer">
        <details>
          <summary>Legenda &amp; come funziona</summary>
          <ul>
            <li>I punti cerchiati sono <strong>slot vuoti</strong>: la posizione è canonica
                ma manca ancora l'asset 3D. Genera un PNG (sfondo trasparente,
                stile Travian) e mettilo in
                <code>cartografia/assets_mappa/&lt;id&gt;.png</code>.</li>
            <li>Gli edifici 3D sono PNG sovrapposti all'illustrazione base.</li>
            <li>La posizione di ogni slot deriva dal centroide della feature
                in <code>cartografia/geo/island.geojson</code>. Per spostare un edificio,
                si modifica il geojson — non c'è un layout JSON separato.</li>
            <li>Per calibrare globalmente la proiezione, modifica
                <code>MAPPA_CONFIG.bbox_geo</code> in <code>mappa_isola.js</code>.</li>
            <li>Aggiungi <code>?debug</code> all'URL per vedere bbox e griglia.</li>
          </ul>
        </details>
      </footer>
    </div>
  `;

  // event listeners sui marker
  c.querySelectorAll(".mappa-slot").forEach(el => {
    el.addEventListener("click", e => {
      const id = el.dataset.id;
      if (id) location.hash = `#/entity/${encodeURIComponent(id)}`;
    });
    el.addEventListener("mouseenter", () => el.classList.add("hover"));
    el.addEventListener("mouseleave", () => el.classList.remove("hover"));
  });
}

function slotToSVG(slot, debug) {
  const { x, y, size, id, name, type, has_asset, asset_url, status } = slot;
  const half = size / 2;

  const tooltip = `
    <title>${escapeHtmlMappa(name)} (${id})</title>
  `;

  if (has_asset) {
    // asset 3D PNG centrato sullo slot
    return `
      <g class="mappa-slot mappa-slot--asset" data-id="${id}" data-type="${type}"
         tabindex="0" role="button" aria-label="${escapeHtmlMappa(name)}">
        ${tooltip}
        <image href="${asset_url}"
               x="${x - half}" y="${y - size * 0.85}"
               width="${size}" height="${size}"
               preserveAspectRatio="xMidYMax meet" />
        <text class="mappa-label" x="${x}" y="${y + 10}"
              text-anchor="middle">${escapeHtmlMappa(name)}</text>
      </g>
    `;
  }

  // placeholder: cerchio tratteggiato + label
  const statusColor = {
    canonico: "#5c4a28",
    provvisorio: "#a07020",
    stub: "#a04040"
  }[status] || "#666";

  return `
    <g class="mappa-slot mappa-slot--placeholder" data-id="${id}" data-type="${type}"
       tabindex="0" role="button" aria-label="${escapeHtmlMappa(name)} (slot vuoto)">
      ${tooltip}
      <circle cx="${x}" cy="${y}" r="${size / 3}"
              fill="rgba(255,255,255,0.55)"
              stroke="${statusColor}" stroke-width="1.6"
              stroke-dasharray="4 3" />
      <circle cx="${x}" cy="${y}" r="2.5" fill="${statusColor}" />
      <text class="mappa-label" x="${x}" y="${y + size / 3 + 14}"
            text-anchor="middle">${escapeHtmlMappa(name)}</text>
    </g>
  `;
}

function renderDebugOverlay() {
  const W = MAPPA_CONFIG.image_w, H = MAPPA_CONFIG.image_h;
  // griglia ogni 100px
  const lines = [];
  for (let x = 0; x <= W; x += 100) {
    lines.push(`<line x1="${x}" y1="0" x2="${x}" y2="${H}" stroke="rgba(200,0,0,0.25)" stroke-width="0.5"/>`);
    lines.push(`<text x="${x + 2}" y="12" font-size="10" fill="rgba(200,0,0,0.6)">${x}</text>`);
  }
  for (let y = 0; y <= H; y += 100) {
    lines.push(`<line x1="0" y1="${y}" x2="${W}" y2="${y}" stroke="rgba(200,0,0,0.25)" stroke-width="0.5"/>`);
    lines.push(`<text x="2" y="${y - 2}" font-size="10" fill="rgba(200,0,0,0.6)">${y}</text>`);
  }
  return `<g class="mappa-debug">${lines.join("\n")}</g>`;
}

// ============================================================================
// UTIL
// ============================================================================
function escapeHtmlMappa(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// Esposto a app.js
window.renderMappaIsola = renderMappaIsola;
