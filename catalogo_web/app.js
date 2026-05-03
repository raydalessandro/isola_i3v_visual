/* Catalogo Visual — Isola dei Tre Venti
   Vanilla JS. Fetch entities.json, sidebar tree, hash routing, MD render,
   mobile drawer, lightbox gallery. No external deps beyond marked.js (CDN). */

const DATA_URL = "data/entities.json";
const MOBILE_MQ = "(max-width: 800px)";

const state = {
  data: null,           // {entities, tree, totals, ...}
  byId: new Map(),      // id -> entity
  search: "",
  // lightbox
  lbImages: [],
  lbIndex: 0,
};

/* ==================================================================
   BOOTSTRAP — always wire UI before any async work, so the hamburger
   works even if the data fetch fails.
   ================================================================== */
function bootstrap() {
  // wire static UI immediately (drawer, lightbox, hashchange)
  setupSidebar();
  setupLightbox();
  window.addEventListener("hashchange", route);

  // load data
  loadData();
}

async function loadData() {
  try {
    const r = await fetch(DATA_URL, { cache: "no-cache" });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    state.data = await r.json();
  } catch (e) {
    document.getElementById("content").innerHTML =
      `<p class="loading">Errore nel caricare <code>${DATA_URL}</code>: ${e.message}.<br>` +
      `Suggerimento: lancia il sito con <code>python3 -m http.server</code> dalla radice del repo, ` +
      `poi apri <code>/catalogo_web/</code>.</p>`;
    return;
  }
  state.data.entities.forEach(e => state.byId.set(e.id, e));
  renderMeta();
  renderTopbarCount();
  renderTree();
  setupSearch();
  route();
}

/* ==================================================================
   SIDEBAR DRAWER (mobile)
   State machine: only `body.sidebar-open` controls everything.
   Backdrop has no `hidden` attribute, no display:none — pure CSS opacity
   + pointer-events. This avoids the stale-state bug.
   ================================================================== */
function setupSidebar() {
  const toggle = document.getElementById("menu-toggle");
  const backdrop = document.getElementById("sidebar-backdrop");
  const sidebar = document.getElementById("sidebar");
  if (!toggle || !backdrop || !sidebar) return;

  const isMobile = () => window.matchMedia(MOBILE_MQ).matches;

  const openDrawer = () => {
    document.body.classList.add("sidebar-open");
    toggle.setAttribute("aria-expanded", "true");
  };
  const closeDrawer = () => {
    document.body.classList.remove("sidebar-open");
    toggle.setAttribute("aria-expanded", "false");
  };
  const toggleDrawer = (ev) => {
    if (ev) ev.preventDefault();
    if (document.body.classList.contains("sidebar-open")) closeDrawer();
    else openDrawer();
  };

  toggle.addEventListener("click", toggleDrawer);
  backdrop.addEventListener("click", closeDrawer);

  // ESC chiude (anche mentre lightbox e' aperto, lightbox ha la sua escape).
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("sidebar-open")) {
      closeDrawer();
    }
  });

  // Click su entita' (delegation) chiude il drawer su mobile.
  document.getElementById("tree-nav").addEventListener("click", (e) => {
    const entityNode = e.target.closest(".tree-node.is-entity > .tree-label");
    if (entityNode && isMobile()) {
      // chiudi DOPO la navigazione hash, lascia tempo al render.
      setTimeout(closeDrawer, 50);
    }
  });

  // Resize: se passiamo da mobile a desktop, chiudi sempre lo stato drawer.
  window.addEventListener("resize", () => {
    if (!isMobile()) closeDrawer();
  });

  // Cambio hash su mobile -> chiudi.
  window.addEventListener("hashchange", () => {
    if (isMobile()) closeDrawer();
  });
}

/* ==================================================================
   META + TOPBAR COUNT
   ================================================================== */
function renderMeta() {
  const m = document.getElementById("meta");
  if (!m) return;
  const ts = state.data.generated_at || "";
  m.textContent = `Generato: ${ts.replace("T", " ")}`;
}

function renderTopbarCount() {
  const el = document.getElementById("topbar-count");
  if (!el) return;
  const n = state.data?.totals?.totale ?? 0;
  el.textContent = `${n} entità`;
}

/* ==================================================================
   SIDEBAR TREE
   Uses .open class on .tree-section / .tree-node containers; CSS handles
   show/hide of children. No inline display: style, no MutationObserver.
   ================================================================== */
function renderTree() {
  const nav = document.getElementById("tree-nav");
  nav.innerHTML = "";
  const tree = state.data.tree;
  const order = ["personaggi", "luoghi", "oggetti", "venti", "visual_signatures"];
  const seen = new Set();
  for (const key of order) {
    if (!tree[key]) continue;
    nav.appendChild(buildSection(key, tree[key]));
    seen.add(key);
  }
  for (const [key, sub] of Object.entries(tree)) {
    if (!seen.has(key)) nav.appendChild(buildSection(key, sub));
  }
}

function buildSection(label, node) {
  const sec = document.createElement("div");
  sec.className = "tree-section";

  const head = document.createElement("div");
  head.className = "tree-label";
  const caret = document.createElement("span");
  caret.className = "caret";
  caret.textContent = "▶";
  const lab = document.createElement("span");
  lab.className = "label-text";
  lab.textContent = prettyLabel(label);
  const cnt = document.createElement("span");
  cnt.className = "badge";
  cnt.textContent = countLeavesInChildren(node._children || {});
  head.appendChild(caret);
  head.appendChild(lab);
  head.appendChild(cnt);
  head.addEventListener("click", () => sec.classList.toggle("open"));
  sec.appendChild(head);

  const children = document.createElement("div");
  children.className = "tree-children";
  buildChildren(children, node._children || {}, 1);
  sec.appendChild(children);

  // Top-level open by default for narrative families.
  if (["personaggi", "luoghi", "oggetti", "venti"].includes(label)) {
    sec.classList.add("open");
  }
  return sec;
}

function buildChildren(container, children, depth) {
  for (const [key, node] of Object.entries(children)) {
    const isEntity = node._entity_id !== undefined;
    const div = document.createElement("div");
    div.className = "tree-node";
    if (isEntity) div.classList.add("is-entity");

    const lab = document.createElement("div");
    lab.className = "tree-label";
    // visual indent that scales with depth (max ~26px to avoid overflow)
    lab.style.paddingLeft = (12 + Math.min(depth, 5) * 11) + "px";

    if (isEntity) {
      const e = state.byId.get(node._entity_id) || {};
      div.dataset.id = node._entity_id;
      if ((e.n_images || 0) > 0) div.classList.add("has-images");
      if (e.status) div.classList.add(e.status); // "canonico" / "provvisorio"

      const nameSpan = document.createElement("span");
      nameSpan.className = "name";
      nameSpan.textContent = e.name || node._entity_id;
      lab.appendChild(nameSpan);

      if ((e.n_images || 0) > 0) {
        const badge = document.createElement("span");
        badge.className = "badge";
        badge.textContent = e.n_images;
        badge.title = `${e.n_images} immagini`;
        lab.appendChild(badge);
      }

      lab.addEventListener("click", () => {
        location.hash = `#/entity/${node._entity_id}`;
      });
      div.appendChild(lab);
      container.appendChild(div);
    } else {
      const childCount = countLeaves(node);
      const caret = document.createElement("span");
      caret.className = "caret";
      caret.textContent = "▶";
      const labText = document.createElement("span");
      labText.className = "label-text";
      labText.textContent = prettyLabel(key);
      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = childCount;
      lab.appendChild(caret);
      lab.appendChild(labText);
      lab.appendChild(badge);

      lab.addEventListener("click", (ev) => {
        ev.stopPropagation();
        div.classList.toggle("open");
      });
      const sub = document.createElement("div");
      sub.className = "tree-children";
      buildChildren(sub, node._children || {}, depth + 1);
      div.appendChild(lab);
      div.appendChild(sub);
      container.appendChild(div);
    }
  }
}

function countLeaves(node) {
  if (node._entity_id !== undefined) return 1;
  let c = 0;
  for (const child of Object.values(node._children || {})) {
    c += countLeaves(child);
  }
  return c;
}
function countLeavesInChildren(children) {
  let c = 0;
  for (const child of Object.values(children)) c += countLeaves(child);
  return c;
}

function prettyLabel(key) {
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, m => m.toUpperCase());
}

/* ==================================================================
   SEARCH
   ================================================================== */
function setupSearch() {
  const inp = document.getElementById("search");
  if (!inp) return;
  let t;
  inp.addEventListener("input", (e) => {
    state.search = e.target.value.trim().toLowerCase();
    clearTimeout(t);
    t = setTimeout(applySearchFilter, 60);
  });
  // ESC nel campo search -> svuota
  inp.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      inp.value = "";
      state.search = "";
      applySearchFilter();
    }
  });
}

function applySearchFilter() {
  const q = state.search;
  const nav = document.getElementById("tree-nav");
  const allEntityNodes = nav.querySelectorAll(".tree-node.is-entity");

  // helper: apply highlight or restore plain name
  const setName = (node, name, highlight) => {
    const span = node.querySelector(".name");
    if (!span) return;
    if (!highlight || !q) {
      span.textContent = name;
      return;
    }
    const idx = name.toLowerCase().indexOf(q);
    if (idx === -1) { span.textContent = name; return; }
    span.innerHTML =
      escapeHtml(name.slice(0, idx)) +
      "<mark>" + escapeHtml(name.slice(idx, idx + q.length)) + "</mark>" +
      escapeHtml(name.slice(idx + q.length));
  };

  if (!q) {
    allEntityNodes.forEach(n => {
      n.style.display = "";
      const e = state.byId.get(n.dataset.id);
      setName(n, e?.name || n.dataset.id, false);
    });
    nav.querySelectorAll(".tree-node:not(.is-entity), .tree-section").forEach(n => {
      n.style.display = "";
    });
    return;
  }

  allEntityNodes.forEach(n => {
    const id = n.dataset.id || "";
    const e = state.byId.get(id) || {};
    const name = e.name || id;
    const text = `${id} ${name}`.toLowerCase();
    const match = text.includes(q);
    n.style.display = match ? "" : "none";
    setName(n, name, match);
  });

  // Ancestors visible only if they contain a match; auto-open on match.
  nav.querySelectorAll(".tree-node:not(.is-entity)").forEach(n => {
    const visible = Array.from(n.querySelectorAll(".tree-node.is-entity"))
      .some(c => c.style.display !== "none");
    n.style.display = visible ? "" : "none";
    if (visible) n.classList.add("open");
  });
  nav.querySelectorAll(".tree-section").forEach(s => {
    const visible = Array.from(s.querySelectorAll(".tree-node.is-entity"))
      .some(c => c.style.display !== "none");
    s.style.display = visible ? "" : "none";
    if (visible) s.classList.add("open");
  });
}

/* ==================================================================
   ROUTING
   ================================================================== */
function route() {
  const hash = location.hash || "#/";
  document.querySelectorAll(".tree-node.is-entity").forEach(n => n.classList.remove("active"));

  if (hash === "#/" || hash === "") { renderHome(); return; }
  if (hash === "#/strade") { renderStradeIndex(); return; }

  const m = hash.match(/^#\/entity\/([^\/]+)$/);
  if (m) {
    const id = decodeURIComponent(m[1]);
    renderEntity(id);
    const node = document.querySelector(`.tree-node.is-entity[data-id="${CSS.escape(id)}"]`);
    if (node) {
      node.classList.add("active");
      let p = node.parentElement;
      while (p && p !== document) {
        if (p.classList && (p.classList.contains("tree-node") || p.classList.contains("tree-section"))) {
          p.classList.add("open");
        }
        p = p.parentElement;
      }
      // Scroll the entity into view in the sidebar (on desktop where sidebar is fixed).
      try {
        node.scrollIntoView({ block: "nearest", behavior: "smooth" });
      } catch (_) { /* old browsers */ }
    }
    return;
  }
  renderHome();
}

/* ==================================================================
   HOME
   ================================================================== */
function renderHome() {
  const c = document.getElementById("content");
  const t = state.data.totals || {};
  const bs = state.data.by_status || {};

  const labels = {
    totale: "Totale",
    personaggio: "Personaggi",
    luogo: "Luoghi",
    oggetto: "Oggetti",
    vento: "Venti",
    visual_signature: "Visual sig.",
  };
  const statsCards = Object.entries(t).map(([k, v]) =>
    `<div class="stats-card"><div class="num">${v}</div><div class="lab">${labels[k] || k}</div></div>`
  ).join("");

  const statusCards = Object.entries(bs).map(([k, v]) =>
    `<div class="stats-card"><div class="num">${v}</div><div class="lab">${escapeHtml(k)}</div></div>`
  ).join("");

  // Featured: entita' con immagini, ordinate per n_images desc poi nome.
  const featured = (state.data.entities || [])
    .filter(e => (e.n_images || 0) > 0)
    .sort((a, b) => (b.n_images - a.n_images) || a.name.localeCompare(b.name))
    .slice(0, 8);

  const featuredHtml = featured.length
    ? `<div class="featured-grid">${featured.map(e => {
        const cover = e.images && e.images[0]
          ? `<img src="../${escapeAttr(e.images[0].path)}" alt="${escapeAttr(e.name)}" loading="lazy">`
          : "";
        const meta = [
          e.famiglia,
          e.n_images > 1 ? `${e.n_images} img` : "1 img",
          e.status === "canonico" ? "canonico" : null,
        ].filter(Boolean).join(" · ");
        return `<a class="featured-card" href="#/entity/${encodeURIComponent(e.id)}">
          <div class="thumb">${cover}</div>
          <div class="info">
            <div class="name">${escapeHtml(e.name)}</div>
            <div class="meta">${escapeHtml(meta)}</div>
          </div>
        </a>`;
      }).join("")}</div>`
    : "";

  c.innerHTML = `
    <div class="home">
      <div class="home-hero">
        <h1>Catalogo Visual</h1>
        <p class="lead">Serbatoio di descrizioni visive di tutte le entità della saga
        <em>L'Isola dei Tre Venti</em>. Generato direttamente da <code>visual/</code> nel repo.</p>
      </div>

      <div class="section-label">Totali</div>
      <div class="stats-grid">${statsCards}</div>

      <div class="section-label">Stato schede</div>
      <div class="stats-grid">${statusCards}</div>

      ${featured.length ? `
      <div class="section-label">Entità con immagini</div>
      ${featuredHtml}
      ` : ""}

      <div class="section-label">Naviga</div>
      <ul class="help-list">
        <li>Albero a sinistra: stesso nesting di <code>visual/</code> nel repo.</li>
        <li>Click su un'entità per la scheda completa con frontmatter, body e gallery immagini.</li>
        <li>Filtro testuale in alto a sinistra per cercare per nome / id.</li>
        <li><a href="#/strade">Indice strade</a> — tabella riassuntiva delle strade secondarie.</li>
        <li><a href="../cartografia/geo/viewer/index.html" target="_blank" rel="noopener">Viewer cartografia</a> — la mappa interattiva (separata).</li>
      </ul>

      <div class="section-label">Aggiornare</div>
      <p style="color:var(--fg-soft);max-width:64ch;">Lo script Python <code>scripts/build_catalogo_web.py</code> rilegge tutte le schede
      e ricostruisce <code>catalogo_web/data/entities.json</code> in modo idempotente. Lancialo
      ogni volta che aggiungi o modifichi una scheda o un'immagine; il sito si auto-aggiorna al refresh.</p>
    </div>
  `;
  document.title = "Catalogo Visual — Isola dei Tre Venti";
  scrollMainTop();
}

/* ==================================================================
   ENTITY PAGE
   ================================================================== */
function renderEntity(id) {
  const e = state.byId.get(id);
  const c = document.getElementById("content");
  if (!e) {
    c.innerHTML = `<p class="loading">Entità <code>${escapeHtml(id)}</code> non trovata.</p>`;
    return;
  }
  document.title = `${e.name} — Catalogo Visual`;

  const tags = [
    e.famiglia ? `<span class="tag">${escapeHtml(e.famiglia)}</span>` : "",
    e.sottotipo ? `<span class="tag">${escapeHtml(e.sottotipo)}</span>` : "",
    e.quartiere ? `<span class="tag">quartiere ${escapeHtml(e.quartiere)}</span>` : "",
    e.categoria_strada ? `<span class="tag">${escapeHtml(e.categoria_strada)}</span>` : "",
    e.status ? `<span class="tag status ${escapeAttr(e.status)}">${escapeHtml(e.status)}</span>` : "",
  ].filter(Boolean).join("");

  const fmYaml = yamlStringify(e.frontmatter);

  const bodyHtml = e.body_md
    ? collapsibleBodySections(marked.parse(e.body_md, { gfm: true, breaks: false }))
    : "<p style=\"padding:0 28px;\"><em>(scheda non ancora compilata)</em></p>";

  const galleryHtml = (e.images && e.images.length)
    ? `<div class="grid">${e.images.map((img, i) =>
        `<button type="button" class="thumb" data-lb-index="${i}" aria-label="Apri ${escapeAttr(img.filename)} a tutto schermo">
          <img src="../${escapeAttr(img.path)}" alt="${escapeAttr(img.filename)}" loading="lazy" decoding="async">
          <span class="caption">${escapeHtml(img.filename)}</span>
        </button>`
      ).join("")}</div>`
    : `<div class="empty">Nessuna immagine in <code>${escapeHtml(e.folder_path)}/immagini/</code>.<br>
       Naming consigliato: <code>${escapeHtml(e.id)}_canonica_v1_fronte.jpg</code>,
       <code>${escapeHtml(e.id)}_canonica_v1_profilo_dx.jpg</code>, ecc.</div>`;

  const promptHtml = e.prompt_grok_md
    ? marked.parse(e.prompt_grok_md, { gfm: true, breaks: false })
    : null;

  c.innerHTML = `
    <div class="entity-header">
      <h1>${escapeHtml(e.name)}</h1>
      <div class="entity-paths">
        <code>${escapeHtml(e.id)}</code> · <code>${escapeHtml(e.scheda_path)}</code>
      </div>
      <div class="entity-meta">${tags}</div>
    </div>

    <div class="gallery">
      <div class="gallery-head">
        <h2>Immagini di riferimento</h2>
        <span class="gallery-count">${e.images?.length || 0} ${(e.images?.length === 1) ? "immagine" : "immagini"}</span>
      </div>
      ${galleryHtml}
    </div>

    <div class="frontmatter-block">
      <details>
        <summary>Metadati (frontmatter)</summary>
        <pre>${escapeHtml(fmYaml)}</pre>
      </details>
    </div>

    <div class="body-toolbar">
      <button type="button" data-action="expand-all">Espandi tutto</button>
      <button type="button" data-action="collapse-all">Comprimi tutto</button>
    </div>
    <div class="entity-body">${bodyHtml}</div>

    ${promptHtml ? `
    <div class="prompt-grok-block">
      <details>
        <summary>Prompt Grok (<code>prompt_grok.md</code>)</summary>
        <div class="entity-body">${promptHtml}</div>
      </details>
    </div>
    ` : ""}
  `;

  // Toolbar: expand/collapse all body sections.
  c.querySelectorAll(".body-toolbar button").forEach(btn => {
    btn.addEventListener("click", () => {
      const open = btn.dataset.action === "expand-all";
      c.querySelectorAll(".entity-body details.body-section").forEach(d => { d.open = open; });
    });
  });

  // Lightbox triggers
  if (e.images && e.images.length) {
    state.lbImages = e.images.slice();
    c.querySelectorAll(".gallery .thumb").forEach(btn => {
      btn.addEventListener("click", () => {
        const idx = parseInt(btn.dataset.lbIndex, 10) || 0;
        openLightbox(idx);
      });
    });
  } else {
    state.lbImages = [];
  }

  scrollMainTop();
}

/* Trasforma il body markdown renderizzato in sezioni <details> per ogni h2.
   Tutto il contenuto prima del primo h2 resta libero in cima.
   Le sezioni iniziano chiuse di default. */
function collapsibleBodySections(html) {
  const tmp = document.createElement("div");
  tmp.innerHTML = html;
  const out = document.createElement("div");
  let currentDetails = null;
  let currentContent = null;

  Array.from(tmp.childNodes).forEach(node => {
    if (node.nodeType === 1 && node.tagName === "H2") {
      currentDetails = document.createElement("details");
      currentDetails.className = "body-section";
      const summary = document.createElement("summary");
      summary.innerHTML = node.innerHTML;
      currentDetails.appendChild(summary);
      currentContent = document.createElement("div");
      currentContent.className = "body-section-content";
      currentDetails.appendChild(currentContent);
      out.appendChild(currentDetails);
    } else if (currentContent) {
      currentContent.appendChild(node.cloneNode(true));
    } else {
      out.appendChild(node.cloneNode(true));
    }
  });
  return out.innerHTML;
}

/* ==================================================================
   LIGHTBOX
   ================================================================== */
function setupLightbox() {
  const lb = document.getElementById("lightbox");
  if (!lb) return;

  lb.querySelector(".lb-close").addEventListener("click", closeLightbox);
  lb.querySelector(".lb-prev").addEventListener("click", (e) => { e.stopPropagation(); lbStep(-1); });
  lb.querySelector(".lb-next").addEventListener("click", (e) => { e.stopPropagation(); lbStep(1); });
  // Click sullo sfondo (non sull'immagine) chiude.
  lb.addEventListener("click", (e) => {
    if (e.target === lb || e.target.classList.contains("lb-stage")) closeLightbox();
  });

  document.addEventListener("keydown", (e) => {
    if (!document.body.classList.contains("lightbox-open")) return;
    if (e.key === "Escape") { closeLightbox(); }
    else if (e.key === "ArrowRight") { lbStep(1); }
    else if (e.key === "ArrowLeft") { lbStep(-1); }
  });

  // Touch swipe
  let startX = 0, startY = 0, tracking = false;
  const stage = lb.querySelector(".lb-stage");
  stage.addEventListener("touchstart", (e) => {
    if (!e.touches[0]) return;
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
    tracking = true;
  }, { passive: true });
  stage.addEventListener("touchend", (e) => {
    if (!tracking) return;
    tracking = false;
    const t = e.changedTouches[0];
    if (!t) return;
    const dx = t.clientX - startX;
    const dy = t.clientY - startY;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) {
      lbStep(dx < 0 ? 1 : -1);
    }
  });
}

function openLightbox(index) {
  if (!state.lbImages || !state.lbImages.length) return;
  state.lbIndex = Math.max(0, Math.min(index, state.lbImages.length - 1));
  document.body.classList.add("lightbox-open");
  if (state.lbImages.length === 1) document.body.classList.add("lightbox-single");
  else document.body.classList.remove("lightbox-single");
  renderLightboxImage();
}
function closeLightbox() {
  document.body.classList.remove("lightbox-open");
  document.body.classList.remove("lightbox-single");
  // Clear src to free memory and stop any in-flight loading.
  const img = document.querySelector("#lightbox .lb-img");
  if (img) img.src = "";
}
function lbStep(delta) {
  if (!state.lbImages.length) return;
  const n = state.lbImages.length;
  state.lbIndex = (state.lbIndex + delta + n) % n;
  renderLightboxImage();
}
function renderLightboxImage() {
  const img = document.querySelector("#lightbox .lb-img");
  const fn = document.querySelector("#lightbox .lb-filename");
  const sz = document.querySelector("#lightbox .lb-size");
  const ct = document.querySelector("#lightbox .lb-counter");
  const cur = state.lbImages[state.lbIndex];
  if (!cur) return;
  img.src = "../" + cur.path;
  img.alt = cur.filename;
  fn.textContent = cur.filename;
  sz.textContent = cur.size_kb ? `${cur.size_kb} KB` : "";
  ct.textContent = state.lbImages.length > 1
    ? `${state.lbIndex + 1} / ${state.lbImages.length}`
    : "";
}

/* ==================================================================
   STRADE INDEX
   ================================================================== */
function renderStradeIndex() {
  const c = document.getElementById("content");
  const md = state.data.aux?.strade_index_md;
  if (!md) {
    c.innerHTML = "<p class='loading'>Indice strade non disponibile.</p>";
    return;
  }
  let html = marked.parse(md, { gfm: true });
  html = html.replace(/href="\.\/luoghi\/[^"]+\/([^\/"]+)\/scheda\.md"/g,
    (_, id) => `href="#/entity/${id}"`);
  c.innerHTML = `<div class="entity-body" style="padding:24px 28px;">${html}</div>`;
  document.title = "Indice strade — Catalogo Visual";
  scrollMainTop();
}

/* ==================================================================
   HELPERS
   ================================================================== */
function scrollMainTop() {
  const main = document.getElementById("main");
  // On desktop, #main is the scroll container. On mobile, the window scrolls.
  if (main) {
    try { main.scrollTo({ top: 0, behavior: "instant" }); }
    catch (_) { main.scrollTop = 0; }
  }
  if (window.matchMedia(MOBILE_MQ).matches) {
    try { window.scrollTo({ top: 0, behavior: "instant" }); }
    catch (_) { window.scrollTo(0, 0); }
  }
}

function escapeHtml(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}
function escapeAttr(s) {
  if (s == null) return "";
  return String(s).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

function yamlStringify(obj, indent = 0) {
  if (obj == null) return "null";
  const pad = "  ".repeat(indent);
  if (Array.isArray(obj)) {
    if (obj.length === 0) return "[]";
    if (obj.every(x => typeof x !== "object" || x === null)) {
      return "[" + obj.map(yamlScalar).join(", ") + "]";
    }
    return "\n" + obj.map(x => pad + "- " + yamlScalar(x)).join("\n");
  }
  if (typeof obj === "object") {
    const lines = [];
    for (const [k, v] of Object.entries(obj)) {
      if (v && typeof v === "object" && !Array.isArray(v) && Object.keys(v).length) {
        lines.push(`${pad}${k}:`);
        lines.push(yamlStringify(v, indent + 1));
      } else if (Array.isArray(v) && v.length && v.some(x => typeof x === "object" && x !== null)) {
        lines.push(`${pad}${k}:`);
        lines.push(yamlStringify(v, indent + 1));
      } else {
        lines.push(`${pad}${k}: ${yamlScalar(v)}`);
      }
    }
    return lines.join("\n");
  }
  return yamlScalar(obj);
}
function yamlScalar(x) {
  if (x === null || x === undefined) return "null";
  if (typeof x === "boolean") return x ? "true" : "false";
  if (typeof x === "number") return String(x);
  if (Array.isArray(x)) return "[" + x.map(yamlScalar).join(", ") + "]";
  if (typeof x === "object") return JSON.stringify(x);
  if (/[:#\[\]{}&*!|>%@`,]/.test(x)) return JSON.stringify(x);
  return String(x);
}

/* GO */
bootstrap();
