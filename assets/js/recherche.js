/* =====================================================================
   VERBUM — Recherche plein texte (toutes les pages)
   - bouton [data-search-open], touche « / » ou Ctrl/Cmd + K : fenêtre
   - page recherche.html : résultats complets (?q=…)
   L'index (assets/js/recherche-index.js) n'est chargé qu'au premier usage.
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const me = document.currentScript;
  const ROOT = (me && me.getAttribute("src") || "").replace(/assets\/js\/recherche\.js.*$/, "");
  let INDEX = null, loading = null;

  /* ---------- Normalisation : minuscules, sans accents, longueur conservée ---------- */
  const fold = (s) => {
    let out = "";
    for (const ch of s) {
      const b = ch.normalize("NFD").replace(/[\u0300-\u036f\u0591-\u05c7]/g, "").toLowerCase();
      out += b.length === 1 ? b : (b[0] || " ");
      if (ch.length === 2) out += " "; // caractères hors plan de base : garder l'alignement
    }
    return out;
  };
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  const load = () => {
    if (INDEX) return Promise.resolve(INDEX);
    if (loading) return loading;
    loading = new Promise((ok, ko) => {
      const s = document.createElement("script");
      s.src = ROOT + "assets/js/recherche-index.js";
      s.onload = () => {
        INDEX = (window.VERBUM_INDEX || []).map((d) => ({ ...d, fs: fold(d.s), fk: fold(d.k || ""), fp: fold(d.p), ft: fold(d.t) }));
        ok(INDEX);
      };
      s.onerror = ko;
      document.head.appendChild(s);
    });
    return loading;
  };

  /* ---------- Recherche ---------- */
  const terms = (q) => fold(q).split(/[\s,;:.'’\-]+/).filter((t) => t.length >= 2 || /\d/.test(t));
  const count = (hay, t) => { let n = 0, i = hay.indexOf(t); while (i !== -1 && n < 50) { n++; i = hay.indexOf(t, i + t.length); } return n; };

  // expression entière, non suivie d'une lettre (« codex h » ne doit pas valoir « codex hébreu »)
  const hasPhrase = (hay, ph) => {
    let i = hay.indexOf(ph);
    while (i !== -1) { if (!/[a-z0-9]/.test(hay.charAt(i + ph.length))) return true; i = hay.indexOf(ph, i + 1); }
    return false;
  };

  const search = (q, max = 40) => {
    const ts = terms(q);
    if (!ts.length || !INDEX) return [];
    const phrase = fold(q).trim().replace(/\s+/g, " ");
    const multi = phrase.includes(" ");
    const res = [];
    for (const d of INDEX) {
      let score = 0, ok = true;
      for (const t of ts) {
        const inS = d.fs.includes(t), inK = d.fk.includes(t), inP = d.fp.includes(t), nT = count(d.ft, t);
        if (!inS && !inK && !inP && !nT) { ok = false; break; }
        score += (inS ? 12 : 0) + (inK ? 4 : 0) + (inP ? 3 : 0) + Math.min(nT, 12);
      }
      if (!ok) continue;
      if (multi) {
        if (hasPhrase(d.fs, phrase) || hasPhrase(d.fp, phrase)) score += 30;
        else if (hasPhrase(d.ft, phrase)) score += 15;
      }
      if (d.k && d.k.startsWith("Jalon")) score -= 1;
      res.push({ d, score });
    }
    res.sort((a, b) => b.score - a.score);
    return res.slice(0, max).map((r) => r.d);
  };

  const mark = (txt, ftxt, ts) => {
    // repère les zones à surligner sur le texte replié, puis découpe le texte original
    const zones = [];
    ts.forEach((t) => { let i = ftxt.indexOf(t); while (i !== -1) { zones.push([i, i + t.length]); i = ftxt.indexOf(t, i + t.length); } });
    zones.sort((a, b) => a[0] - b[0]);
    let out = "", pos = 0;
    zones.forEach(([a, b]) => { if (a < pos) return; out += esc(txt.slice(pos, a)) + "<mark>" + esc(txt.slice(a, b)) + "</mark>"; pos = b; });
    return out + esc(txt.slice(pos));
  };

  const snippet = (d, ts) => {
    const first = ts.map((t) => d.ft.indexOf(t)).filter((i) => i >= 0).sort((a, b) => a - b)[0];
    if (first === undefined) return esc(d.t.slice(0, 220)) + (d.t.length > 220 ? "…" : "");
    let a = Math.max(0, first - 90);
    if (a > 0) { const sp = d.t.indexOf(" ", a); if (sp !== -1 && sp < first) a = sp + 1; }
    const b = Math.min(d.t.length, a + 280);
    return (a > 0 ? "… " : "") + mark(d.t.slice(a, b), d.ft.slice(a, b), ts) + (b < d.t.length ? " …" : "");
  };

  const item = (d, ts) => `<li class="sr-it"><a href="${ROOT}${d.u}">
      <span class="sr-p">${esc(d.p)}${d.k ? " · " + esc(d.k) : ""}</span>
      <span class="sr-s">${mark(d.s, d.fs, ts)}</span>
      <span class="sr-x">${snippet(d, ts)}</span></a></li>`;

  const plural = (n, a, b) => `${n} ${n > 1 ? b : a}`;
  const SUGG = ["Ketef Hinnom", "Jéhovah", "Codex H", "Septante", "Tyndale", "P52"];

  /* ---------- Fenêtre ---------- */
  let dlg, input, list, foot, active = -1, lastFocus = null;
  const build = () => {
    dlg = document.createElement("dialog");
    dlg.className = "srch";
    dlg.setAttribute("aria-label", "Rechercher dans le musée");
    dlg.innerHTML = `
      <div class="srch-head">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.4 15.4 20.5 20.5"/></svg>
        <input type="search" placeholder="Rechercher un manuscrit, un nom, un lieu…" autocomplete="off" spellcheck="false" aria-label="Rechercher" aria-controls="srch-list" aria-autocomplete="list">
        <button class="srch-close" type="button">Fermer <span class="sb-kbd">Échap</span></button>
      </div>
      <div class="srch-body"><ol class="sr-results" id="srch-list" role="listbox"></ol><div class="srch-empty"></div></div>
      <div class="srch-foot"><span class="srch-keys"><kbd>↑</kbd><kbd>↓</kbd> naviguer · <kbd>Entrée</kbd> ouvrir · <kbd>Échap</kbd> fermer</span><a class="srch-all" href="${ROOT}recherche.html">Page de recherche</a></div>`;
    document.body.appendChild(dlg);
    input = $("input", dlg); list = $(".sr-results", dlg); foot = $(".srch-all", dlg);
    const empty = $(".srch-empty", dlg);
    const render = () => {
      const q = input.value.trim(), ts = terms(q);
      foot.href = `${ROOT}recherche.html${q ? "?q=" + encodeURIComponent(q) : ""}`;
      active = -1;
      if (!ts.length) {
        list.innerHTML = "";
        empty.innerHTML = `Essayez par exemple : ${SUGG.map((s) => `<span class="tag" role="button" tabindex="0">${s}</span>`).join("")}`;
        return;
      }
      if (!INDEX) { empty.textContent = "Chargement de l'index…"; load().then(render); return; }
      const r = search(q, 30);
      list.innerHTML = r.map((d) => item(d, ts)).join("");
      empty.textContent = r.length ? "" : "Aucun résultat. Vérifiez l'orthographe ou essayez un autre mot.";
    };
    input.addEventListener("input", render);
    empty.addEventListener("click", (ev) => { const t = ev.target.closest(".tag"); if (t) { input.value = t.textContent; render(); input.focus(); } });
    empty.addEventListener("keydown", (ev) => { const t = ev.target.closest(".tag"); if (t && ev.key === "Enter") { input.value = t.textContent; render(); input.focus(); } });
    const setActive = (i) => {
      const its = [...list.children];
      if (!its.length) return;
      active = (i + its.length) % its.length;
      its.forEach((li, k) => li.classList.toggle("is-active", k === active));
      its[active].scrollIntoView({ block: "nearest" });
    };
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "ArrowDown") { ev.preventDefault(); setActive(active + 1); }
      else if (ev.key === "ArrowUp") { ev.preventDefault(); setActive(active - 1); }
      else if (ev.key === "Enter") {
        const a = list.children[Math.max(active, 0)]?.querySelector("a");
        if (a) { ev.preventDefault(); location.href = a.href; dlg.close(); }
      }
    });
    list.addEventListener("click", () => dlg.close());
    $(".srch-close", dlg).addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
    dlg.addEventListener("close", () => { document.documentElement.style.overflow = ""; lastFocus?.focus?.(); });
    render();
  };
  const open = (q = "") => {
    if (!dlg) build();
    lastFocus = document.activeElement;
    if (q) input.value = q;
    input.dispatchEvent(new Event("input"));
    dlg.showModal();
    document.documentElement.style.overflow = "hidden";
    input.focus(); input.select();
    load().catch(() => {});
  };

  document.addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-search-open]");
    if (b) { ev.preventDefault(); open(); }
  });
  document.addEventListener("keydown", (ev) => {
    const typing = ev.target.closest?.("input, textarea, select, [contenteditable]");
    if ((ev.key === "k" || ev.key === "K") && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); open(); }
    else if (ev.key === "/" && !typing && !document.querySelector("dialog[open]")) { ev.preventDefault(); open(); }
  });

  /* ---------- Page recherche.html ---------- */
  const page = $(".sr-results-page");
  if (page) {
    const q0 = new URLSearchParams(location.search).get("q") || "";
    const inp = $("#sr-q"), cnt = $(".sr-count");
    inp.value = q0;
    const run = () => {
      const q = inp.value.trim(), ts = terms(q);
      if (!ts.length) { page.innerHTML = ""; cnt.textContent = "Saisissez un mot pour lancer la recherche."; return; }
      cnt.textContent = "Recherche en cours…";
      load().then(() => {
        const r = search(q, 100);
        page.innerHTML = r.map((d) => item(d, ts)).join("");
        cnt.textContent = r.length ? `${plural(r.length, "résultat", "résultats")} pour « ${q} »` : `Aucun résultat pour « ${q} ».`;
      }).catch(() => { cnt.textContent = "L'index de recherche n'a pas pu être chargé."; });
    };
    let t;
    inp.addEventListener("input", () => {
      clearTimeout(t);
      t = setTimeout(() => { history.replaceState(null, "", inp.value.trim() ? "?q=" + encodeURIComponent(inp.value.trim()) : location.pathname); run(); }, 160);
    });
    $(".sr-form").addEventListener("submit", (ev) => { ev.preventDefault(); run(); });
    run();
    if (!q0) inp.focus({ preventScroll: true });
  }
})();
