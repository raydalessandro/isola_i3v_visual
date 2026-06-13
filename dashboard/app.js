/* dashboard/app.js — unico file JS della dashboard.
   Legge window.DASHBOARD_DATA (generato da scripts/build_dashboard.py)
   e renderizza la pagina indicata da <body data-page="...">.
   Zero framework, zero dipendenze. */

(function () {
  const D = window.DASHBOARD_DATA;
  const page = document.body.dataset.page;

  const PAGES = [
    ["index.html", "home", "Home"],
    ["agent-entry.html", "agent-entry", "Agent entry"],
    ["skills.html", "skills", "Skills"],
    ["pipeline.html", "pipeline", "Pipeline"],
    ["repo-map.html", "repo-map", "Repo map"],
    ["documenti.html", "documenti", "Documenti"],
    ["todo.html", "todo", "TODO + debito"],
    ["make.html", "make", "Make"],
  ];

  const esc = (s) => String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const kb = (b) => (b / 1024).toFixed(1) + " kB";
  const day = (iso) => (iso || "").slice(0, 10);
  const lineUrl = (url, ln) => url + "?plain=1#L" + ln;

  /* ── nav ── */
  document.getElementById("nav").innerHTML = `
    <div class="brand">
      <div class="title">isola_i3v_visual</div>
      <div class="sub">dashboard di sistema</div>
    </div>
    ${PAGES.map(([href, id, label]) => `
      <a href="${href}" class="${id === page ? "active" : ""}">
        <span class="dot"></span>${label}</a>`).join("")}
    <div class="head-meta">
      HEAD ${esc(D.head.sha)}<br>
      generata ${day(D.generated_at)}
    </div>`;

  const main = document.getElementById("content");
  const R = {};

  /* ── 1. Home ── */
  R.home = () => {
    const c = D.counts;
    main.innerHTML = `
      <h1>Dashboard di sistema</h1>
      <p class="lede">Vista meta della repo: come è organizzato il sistema che
        produce <em>L'Isola dei Tre Venti</em> — non il contenuto della saga,
        ma le regole, i ruoli e lo stato della macchina che la costruisce.</p>

      <div class="kpis">
        <div class="kpi"><div class="v">${c.skills}</div><div class="l">skill</div></div>
        <div class="kpi"><div class="v">${c.documents}</div><div class="l">doc di sistema</div></div>
        <div class="kpi"><div class="v">${D.pipeline.length}</div><div class="l">tappe pipeline</div></div>
        <div class="kpi"><div class="v">${D.todos.total}</div><div class="l">voci aperte</div></div>
        <div class="kpi"><div class="v">${D.make.length}</div><div class="l">target make</div></div>
      </div>

      <h2>TL;DR</h2>
      <p>Un agente che entra nella repo legge <code>CLAUDE.md</code> (router),
        poi <code>PROJECT_STATE.md</code> (stato), poi la skill del proprio
        ruolo — e <strong>resta nel suo scope</strong>. Le decisioni editoriali
        vivono nei dati strutturati; gli script sono idempotenti e l'estrazione
        è meccanica. La verità è nel grafo.</p>

      <h2>Le tre fonti</h2>
      <div class="fonti">
        <div class="fonte bible">
          <h3>Bible</h3>
          <div class="where">pipeline_narrativa/documenti_progetto/ISOLA_TRE_VENTI_BIBLE_v2.md</div>
          <p>Canone narrativo: funzione e voce dei personaggi, vincoli, archi.</p>
        </div>
        <div class="fonte grafo">
          <h3>Grafo storie</h3>
          <div class="where">pipeline_narrativa/story_graph.json</div>
          <p>Dinamica delle storie: scene, ruoli, seeds, callbacks, visual_anchors.</p>
        </div>
        <div class="fonte catalogo">
          <h3>Catalogo visual</h3>
          <div class="where">visual/&lt;famiglia&gt;/…/&lt;id&gt;/scheda.md</div>
          <p>Visivo: aspetto, palette, materiali, vincoli, prompt, immagini.</p>
        </div>
      </div>
      <div class="note"><strong>Regola di non-duplicazione:</strong> un dato vive
        in una sola fonte. Aspetto → catalogo · voce → Bible · ruolo nella
        scena → grafo.</div>

      <h2>Per chi è ogni pagina</h2>
      <table>
        <tr><th>Pagina</th><th>Cosa</th><th>Per chi</th></tr>
        <tr><td><a href="agent-entry.html">Agent entry</a></td><td>cosa legge un agente entrando, in che ordine, quanto costa</td><td class="num">Ray + orchestratore</td></tr>
        <tr><td><a href="skills.html">Skills</a></td><td>i ${c.skills} ruoli con scope e comandi</td><td class="num">umano + agente</td></tr>
        <tr><td><a href="pipeline.html">Pipeline</a></td><td>le ${D.pipeline.length} tappe del flusso storia</td><td class="num">umano</td></tr>
        <tr><td><a href="repo-map.html">Repo map</a></td><td>albero annotato delle directory</td><td class="num">umano + agente</td></tr>
        <tr><td><a href="documenti.html">Documenti</a></td><td>tutti i .md di sistema, classificati e filtrabili</td><td class="num">Ray</td></tr>
        <tr><td><a href="todo.html">TODO + debito</a></td><td>voci aperte estratte dai doc + known_issues</td><td class="num">Ray (operativo)</td></tr>
        <tr><td><a href="make.html">Make</a></td><td>target disponibili</td><td class="num">umano</td></tr>
      </table>`;
  };

  /* ── 2. Agent entry ── */
  R["agent-entry"] = () => {
    const ae = D.agent_entry;
    const max = ae.base_tokens_est;
    main.innerHTML = `
      <h1>Agent entry</h1>
      <p class="lede">La sequenza letterale di file che un agente legge entrando
        nella repo. Per ogni file: peso, righe, ultima modifica e costo
        cumulativo stimato in token (~4 byte/token) — per capire se una
        modifica al router gonfia troppo il prompt iniziale.</p>

      ${ae.sequence.map((s, i) => `
        <div class="entry-step">
          <div class="marker">${i + 1}</div>
          <div class="body">
            <div class="file"><a href="${s.url}">${esc(s.path)}</a></div>
            <div class="role">${esc(s.role)}</div>
            <div class="stats">${kb(s.bytes)} · ${s.lines} righe ·
              mod. ${day(s.mtime)} ·
              ~${s.tokens_est} tok (cum. ${s.tokens_cumulative})</div>
            <div class="gauge"><i style="width:${Math.round(100 * s.tokens_cumulative / max)}%"></i></div>
          </div>
        </div>`).join("")}

      <div class="note">Base d'ingresso: <strong>~${ae.base_tokens_est} token</strong>
        prima della skill. ${esc(ae.note)}</div>

      <h2>+ la skill pertinente</h2>
      <table>
        <tr><th>Skill</th><th>Peso</th><th>Righe</th><th>~Token</th><th>Totale ingresso</th></tr>
        ${ae.skills_cost.map(s => `
          <tr>
            <td class="path"><a href="${s.url}">${esc(s.role)}</a></td>
            <td class="num">${kb(s.bytes)}</td>
            <td class="num">${s.lines}</td>
            <td class="num">${s.tokens_est}</td>
            <td class="num"><strong>~${s.tokens_total_entry}</strong></td>
          </tr>`).join("")}
      </table>`;
  };

  /* ── 3. Skills ── */
  R.skills = () => {
    main.innerHTML = `
      <h1>Skills</h1>
      <p class="lede">${D.skills.length} ruoli, ordinati per <code>order</code>
        del frontmatter (lo stesso che genera la tabella di routing in
        CLAUDE.md via <code>make routing</code>). Una sessione = una skill.</p>
      <div class="cards">
        ${D.skills.map(s => `
          <div class="card">
            <h3>${esc(s.role)}</h3>
            <p class="trigger">${esc(s.trigger)}</p>
            <dl>
              <dt>Scrive in</dt><dd>${esc(s.scope_write) || "—"}</dd>
              <dt>Comandi</dt><dd>${esc(s.commands) || "—"}</dd>
            </dl>
            <div class="foot">
              <span>${kb(s.bytes)} · ${s.lines} righe</span>
              <a href="${s.url}">SKILL.md →</a>
            </div>
          </div>`).join("")}
      </div>`;
  };

  /* ── 4. Pipeline ── */
  R.pipeline = () => {
    const cls = (auto) => {
      const n = parseInt(auto) || 0;
      return n >= 80 ? "auto" : n > 0 ? "mixed" : "human";
    };
    main.innerHTML = `
      <h1>Pipeline</h1>
      <p class="lede">Il flusso end-to-end di una storia, dall'idea autoriale al
        commit. Colore del bordo: <span style="color:var(--mulinello)">●</span>
        umano · <span style="color:var(--taglio)">●</span> misto ·
        <span style="color:var(--intreccio)">●</span> automatico.
        Fonte: <a href="${"https://github.com/raydalessandro/isola_i3v_visual/blob/main/docs/PIPELINE.md"}">docs/PIPELINE.md</a>.</p>
      ${D.pipeline.map(t => `
        <div class="tappa ${cls(t.auto)}">
          <span class="auto-pill">${esc(t.auto || "")}</span>
          <h3><span class="n">T${t.n}</span>${esc(t.title)}</h3>
          ${t.input ? `<div class="row"><b>Input</b> ${esc(t.input)}</div>` : ""}
          ${t.output ? `<div class="row"><b>Output</b> ${esc(t.output)}</div>` : ""}
          ${t.prompt ? `<div class="row"><b>Prompt</b> <code>${esc(t.prompt)}</code></div>` : ""}
        </div>`).join("")}`;
  };

  /* ── 5. Repo map ── */
  R["repo-map"] = () => {
    const rm = D.repo_map;
    main.innerHTML = `
      <h1>Repo map</h1>
      <p class="lede">Albero annotato delle directory, da
        <a href="${rm.url}">docs/MAPPA_REPO.md</a>
        (agg. ${day(rm.mtime)}).</p>
      <pre class="tree">${esc(rm.tree)}</pre>`;
  };

  /* ── 6. Documenti ── */
  R.documenti = () => {
    const cats = [
      ["tutti", "Tutti"],
      ["core", "Core"],
      ["operativo", "Operativo"],
      ["progetto", "Progetto"],
      ["archivio", "Storia/Archivio"],
    ];
    const byCat = D.counts.docs_by_category;
    let current = "tutti";

    const renderRows = () => D.documents
      .filter(d => current === "tutti" || d.category === current)
      .map(d => `
        <tr>
          <td><span class="badge ${d.category}">${d.category}</span></td>
          <td class="path"><a href="${d.url}">${esc(d.path)}</a>
            ${d.preview ? `<div style="font-family:Nunito,sans-serif;font-size:12.5px;color:var(--ink-soft);margin-top:2px">${esc(d.preview)}</div>` : ""}</td>
          <td class="num">${d.lines}</td>
          <td class="num">${kb(d.bytes)}</td>
          <td class="num">${day(d.mtime)}</td>
        </tr>`).join("");

    main.innerHTML = `
      <h1>Documenti</h1>
      <p class="lede">${D.counts.documents} documenti di sistema (esclusi prosa,
        brief, annotazioni e schede entità: quello è contenuto, non meta).
        Core ${byCat.core} · Operativo ${byCat.operativo} ·
        Progetto ${byCat.progetto} · Archivio ${byCat.archivio}.</p>
      <div class="filters" id="filters">
        ${cats.map(([id, label]) =>
          `<button data-cat="${id}" class="${id === "tutti" ? "on" : ""}">${label}</button>`).join("")}
      </div>
      <table>
        <thead><tr><th></th><th>Documento</th><th>Righe</th><th>Peso</th><th>Mod.</th></tr></thead>
        <tbody id="doc-rows">${renderRows()}</tbody>
      </table>`;

    document.getElementById("filters").addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      current = b.dataset.cat;
      document.querySelectorAll("#filters button")
        .forEach(x => x.classList.toggle("on", x === b));
      document.getElementById("doc-rows").innerHTML = renderRows();
    });
  };

  /* ── 7. TODO + debito ── */
  R.todo = () => {
    const ki = D.todos.known_issues;
    const kinds = [
      ["tutti", "Tutte"],
      ["todo", "TODO/FIXME"],
      ["warning", "⚠️"],
      ["checklist", "Checklist [ ]"],
      ["sezione", "Sezioni"],
      ["voce", "Voci"],
    ];
    let current = "tutti";

    const renderGroups = () => D.todos.groups.map(g => {
      const items = g.items.filter(i => current === "tutti" || i.kind === current);
      if (!items.length) return "";
      return `
        <div class="todo-file">
          <h3><a href="${g.url}">${esc(g.path)}</a>
            <span class="count">· ${items.length}</span></h3>
          ${items.map(i => `
            <div class="todo-item">
              <a class="ln" href="${lineUrl(g.url, i.line)}">:${i.line}</a>
              <span class="badge ${i.kind}">${i.kind}</span>
              <span class="txt">${esc(i.text)}</span>
            </div>`).join("")}
        </div>`;
    }).join("");

    main.innerHTML = `
      <h1>TODO + debito</h1>
      <p class="lede">${D.todos.total} voci aperte estratte automaticamente dai
        documenti di sistema (esclusi archivio, log e checklist operative).
        Ogni numero di riga linka il punto preciso su GitHub.</p>

      <h2>known_issues.yaml (baseline audit)</h2>
      <div class="note">${ki.count === 0
        ? `✅ <strong>Vuoto</strong> — nessuna incoerenza referenziale nota nel grafo. Obiettivo raggiunto a HEAD.`
        : `<strong>${ki.count} voci</strong> in attesa di decisione autoriale.`}
        <a href="${ki.url}">file →</a></div>

      <h2>Voci nei documenti</h2>
      <div class="filters" id="kind-filters">
        ${kinds.map(([id, label]) =>
          `<button data-kind="${id}" class="${id === "tutti" ? "on" : ""}">${label}</button>`).join("")}
      </div>
      <div id="todo-groups">${renderGroups()}</div>`;

    document.getElementById("kind-filters").addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      current = b.dataset.kind;
      document.querySelectorAll("#kind-filters button")
        .forEach(x => x.classList.toggle("on", x === b));
      document.getElementById("todo-groups").innerHTML = renderGroups();
    });
  };

  /* ── 8. Make ── */
  R.make = () => {
    main.innerHTML = `
      <h1>Make</h1>
      <p class="lede">Target disponibili (<code>make help</code> renderizzato).
        Fonte: <a href="https://github.com/raydalessandro/isola_i3v_visual/blob/main/Makefile">Makefile</a>.</p>
      <table>
        <tr><th>Target</th><th>Cosa fa</th></tr>
        ${D.make.map(t => `
          <tr>
            <td class="path"><code>make ${esc(t.target)}</code></td>
            <td>${esc(t.desc)}</td>
          </tr>`).join("")}
      </table>
      <div class="note"><code>make sync</code> rigenera tutto il derivato
        (catalogo + briefs + routing + dashboard); il <code>git status</code>
        dopo il sync è il report di cosa era disallineato.</div>`;
  };

  (R[page] || R.home)();
})();
