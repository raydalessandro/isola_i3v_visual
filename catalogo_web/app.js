/* Catalogo Visual — Isola dei Tre Venti
   Vanilla JS, fetch entities.json, sidebar tree, hash routing, MD render. */

const DATA_URL = "data/entities.json";

const state = {
  data: null,           // {entities, tree, totals, ...}
  byId: new Map(),      // id -> entity
  search: "",
};

/* ---------- BOOTSTRAP ---------- */
async function init() {
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
  renderTree();
  setupSearch();
  window.addEventListener("hashchange", route);
  route();
}

function renderMeta() {
  const m = document.getElementById("meta");
  const ts = state.data.generated_at || "";
  m.textContent = `Generato: ${ts.replace("T", " ")}`;
}

/* ---------- SIDEBAR TREE ---------- */
function renderTree() {
  const nav = document.getElementById("tree-nav");
  nav.innerHTML = "";
  const tree = state.data.tree;
  // ordina top-level: personaggi, luoghi, oggetti, venti, visual_signatures
  const order = ["personaggi", "luoghi", "oggetti", "venti", "visual_signatures"];
  for (const key of order) {
    if (!tree[key]) continue;
    nav.appendChild(buildSection(key, tree[key]));
  }
  // Eventuali altre top-level
  for (const [key, sub] of Object.entries(tree)) {
    if (!order.includes(key)) {
      nav.appendChild(buildSection(key, sub));
    }
  }
}

function buildSection(label, node) {
  const sec = document.createElement("div");
  sec.className = "tree-section";
  const head = document.createElement("div");
  head.className = "tree-label";
  head.innerHTML = `<span class="caret">▶</span> ${prettyLabel(label)}`;
  head.addEventListener("click", () => sec.classList.toggle("open"));
  sec.appendChild(head);
  const children = document.createElement("div");
  children.className = "tree-children";
  buildChildren(children, node._children || {}, 1);
  sec.appendChild(children);
  // espandi di default le top-level più rilevanti
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
    div.dataset.id = node._entity_id || "";

    const lab = document.createElement("div");
    lab.className = "tree-label";
    lab.style.paddingLeft = (16 + depth * 10) + "px";

    if (isEntity) {
      const e = state.byId.get(node._entity_id);
      lab.innerHTML =
        `<span>${e.name || node._entity_id}</span>` +
        (e.n_images > 0 ? `<span class="badge">${e.n_images}</span>` : "");
      lab.addEventListener("click", () => {
        location.hash = `#/entity/${node._entity_id}`;
      });
    } else {
      const childCount = countLeaves(node);
      lab.innerHTML =
        `<span class="caret">▶</span> ${prettyLabel(key)} ` +
        `<span class="badge" style="margin-left:6px">${childCount}</span>`;
      lab.addEventListener("click", (ev) => {
        ev.stopPropagation();
        div.classList.toggle("open");
      });
      const sub = document.createElement("div");
      sub.className = "tree-children";
      sub.style.display = "none";
      buildChildren(sub, node._children || {}, depth + 1);
      div.appendChild(lab);
      div.appendChild(sub);
      // toggle visibility on open class
      const obs = new MutationObserver(() => {
        sub.style.display = div.classList.contains("open") ? "block" : "none";
      });
      obs.observe(div, { attributes: true, attributeFilter: ["class"] });
      container.appendChild(div);
      continue;
    }

    div.appendChild(lab);
    container.appendChild(div);
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

function prettyLabel(key) {
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, m => m.toUpperCase());
}

/* ---------- SEARCH ---------- */
function setupSearch() {
  const inp = document.getElementById("search");
  inp.addEventListener("input", (e) => {
    state.search = e.target.value.trim().toLowerCase();
    applySearchFilter();
  });
}

function applySearchFilter() {
  const q = state.search;
  const nav = document.getElementById("tree-nav");
  const allEntityNodes = nav.querySelectorAll(".tree-node.is-entity");
  if (!q) {
    allEntityNodes.forEach(n => n.style.display = "");
    nav.querySelectorAll(".tree-node:not(.is-entity), .tree-section").forEach(n => n.style.display = "");
    return;
  }
  // hide entities not matching
  allEntityNodes.forEach(n => {
    const id = n.dataset.id || "";
    const e = state.byId.get(id);
    const text = `${id} ${e?.name || ""}`.toLowerCase();
    n.style.display = text.includes(q) ? "" : "none";
  });
  // show parents only if any visible child + auto-open
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

/* ---------- ROUTING ---------- */
function route() {
  const hash = location.hash || "#/";
  // segna entità attiva
  document.querySelectorAll(".tree-node.is-entity").forEach(n => n.classList.remove("active"));

  if (hash === "#/" || hash === "") {
    renderHome();
    return;
  }
  if (hash === "#/strade") {
    renderStradeIndex();
    return;
  }
  const m = hash.match(/^#\/entity\/([^\/]+)$/);
  if (m) {
    const id = decodeURIComponent(m[1]);
    renderEntity(id);
    const node = document.querySelector(`.tree-node.is-entity[data-id="${CSS.escape(id)}"]`);
    if (node) {
      node.classList.add("active");
      // espandi tutti i parent
      let p = node.parentElement;
      while (p && p !== document) {
        if (p.classList && (p.classList.contains("tree-node") || p.classList.contains("tree-section"))) {
          p.classList.add("open");
        }
        p = p.parentElement;
      }
      node.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
    return;
  }
  renderHome();
}

/* ---------- HOME ---------- */
function renderHome() {
  const c = document.getElementById("content");
  const t = state.data.totals;
  const bs = state.data.by_status || {};
  const cards = [];
  const labels = {
    totale: "TOTALE",
    personaggio: "PERSONAGGI",
    luogo: "LUOGHI",
    oggetto: "OGGETTI",
    vento: "VENTI",
    visual_signature: "VISUAL SIG.",
  };
  for (const [k, v] of Object.entries(t)) {
    cards.push(`<div class="stats-card"><div class="num">${v}</div><div class="lab">${labels[k] || k}</div></div>`);
  }

  c.innerHTML = `
    <div class="home">
      <h1>Catalogo Visual — L'Isola dei Tre Venti</h1>
      <p class="lead">Serbatoio di descrizioni visive di tutte le entità della saga.
      Generato direttamente da <code>visual/</code> nel repo. Aggiorna lanciando
      <code>python3 scripts/build_catalogo_web.py</code>.</p>

      <h2 style="margin-top:24px;font-size:16px;color:var(--fg-muted);text-transform:uppercase;letter-spacing:0.5px;">Totali</h2>
      <div class="stats-grid">${cards.join("")}</div>

      <h2 style="margin-top:24px;font-size:16px;color:var(--fg-muted);text-transform:uppercase;letter-spacing:0.5px;">Stato compilazione schede</h2>
      <div class="stats-grid">
        ${Object.entries(bs).map(([k, v]) =>
          `<div class="stats-card"><div class="num">${v}</div><div class="lab">${k}</div></div>`
        ).join("")}
      </div>

      <h2 style="margin-top:24px;font-size:16px;color:var(--fg-muted);text-transform:uppercase;letter-spacing:0.5px;">Come si usa</h2>
      <ul>
        <li>Naviga l'albero a sinistra: stesso nesting di <code>visual/</code>.</li>
        <li>Click su un'entità per la scheda completa con frontmatter, body, gallery immagini.</li>
        <li>Filtro testuale in alto a sinistra per cercare per nome/id.</li>
        <li><a href="#/strade">📋 Indice strade</a> per la tabella riassuntiva delle 31 strade secondarie.</li>
        <li><a href="../cartografia/geo/viewer/index.html" target="_blank">🗺 Viewer cartografia</a> per la mappa interattiva (separata).</li>
      </ul>

      <h2 style="margin-top:24px;font-size:16px;color:var(--fg-muted);text-transform:uppercase;letter-spacing:0.5px;">Aggiornare il catalogo</h2>
      <p>Lo script Python <code>scripts/build_catalogo_web.py</code> rilegge tutte le schede
      e ricostruisce <code>catalogo_web/data/entities.json</code> in modo idempotente. Lancialo
      ogni volta che aggiungi o modifichi una scheda o un'immagine. Il sito si auto-aggiorna
      al refresh.</p>
    </div>
  `;
  document.title = "Catalogo Visual — Isola dei Tre Venti";
}

/* ---------- ENTITY PAGE ---------- */
function renderEntity(id) {
  const e = state.byId.get(id);
  const c = document.getElementById("content");
  if (!e) {
    c.innerHTML = `<p class="loading">Entità <code>${id}</code> non trovata.</p>`;
    return;
  }
  document.title = `${e.name} — Catalogo Visual`;

  const tags = [
    e.famiglia ? `<span class="tag">${e.famiglia}</span>` : "",
    e.sottotipo ? `<span class="tag">${e.sottotipo}</span>` : "",
    e.quartiere ? `<span class="tag">quartiere ${e.quartiere}</span>` : "",
    e.categoria_strada ? `<span class="tag">${e.categoria_strada}</span>` : "",
    e.status ? `<span class="tag status ${e.status}">${e.status}</span>` : "",
  ].filter(Boolean).join("");

  // Frontmatter pretty (YAML-like display)
  const fmYaml = yamlStringify(e.frontmatter);

  // Body MD -> HTML via marked
  const bodyHtml = e.body_md
    ? marked.parse(e.body_md, { gfm: true, breaks: false })
    : "<p><em>(scheda non ancora compilata)</em></p>";

  // Images
  const galleryHtml = e.images && e.images.length > 0
    ? e.images.map(img =>
        `<a href="../${img.path}" target="_blank" rel="noopener">` +
        `<img src="../${img.path}" alt="${img.filename}" title="${img.filename} (${img.size_kb} KB)" loading="lazy">` +
        `</a>`
      ).join("")
    : `<div class="empty">Nessuna immagine in <code>${e.folder_path}/immagini/</code>.<br>` +
      `Naming consigliato: <code>${e.id}_fronte_v1.png</code>, ` +
      `<code>${e.id}_retro_v1.png</code>, <code>${e.id}_profilo_dx_v1.png</code>, ` +
      `<code>${e.id}_profilo_sx_v1.png</code> (4 vedute per stampa 3D).</div>`;

  // Prompt Grok (se presente)
  const promptHtml = e.prompt_grok_md
    ? marked.parse(e.prompt_grok_md, { gfm: true, breaks: false })
    : null;

  c.innerHTML = `
    <div class="entity-header">
      <h1>${escapeHtml(e.name)}</h1>
      <div style="color:var(--fg-muted);font-size:13px;">
        <code>${e.id}</code> · <code>${e.scheda_path}</code>
      </div>
      <div class="entity-meta">${tags}</div>
    </div>

    <div class="gallery">
      <h2>Immagini di riferimento (${e.images?.length || 0})</h2>
      ${e.images?.length ? `<div class="grid">${galleryHtml}</div>` : galleryHtml}
    </div>

    <div class="frontmatter-block">
      <details>
        <summary>Metadati (frontmatter)</summary>
        <pre>${escapeHtml(fmYaml)}</pre>
      </details>
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
  // scroll a top
  document.getElementById("main").scrollTo({ top: 0, behavior: "instant" });
}

/* ---------- STRADE INDEX ---------- */
function renderStradeIndex() {
  const c = document.getElementById("content");
  const md = state.data.aux?.strade_index_md;
  if (!md) {
    c.innerHTML = "<p class='loading'>Indice strade non disponibile.</p>";
    return;
  }
  // Trasforma i link relativi in hash routing
  // pattern: [`...`](./luoghi/.../<id>/scheda.md)
  let html = marked.parse(md, { gfm: true });
  html = html.replace(/href="\.\/luoghi\/[^"]+\/([^\/"]+)\/scheda\.md"/g,
    (_, id) => `href="#/entity/${id}"`);
  c.innerHTML = `<div class="entity-body">${html}</div>`;
  document.getElementById("main").scrollTo({ top: 0, behavior: "instant" });
  document.title = "Indice strade — Catalogo Visual";
}

/* ---------- HELPERS ---------- */
function escapeHtml(s) {
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
  // string
  if (/[:#\[\]{}&*!|>%@`,]/.test(x)) return JSON.stringify(x);
  return String(x);
}

/* GO */
init();
