/* =====================================================================
   VERBUM — Salle 06 · Les Textes apocryphes (étape E08)
   1. Onglets des dossiers (clavier compris)  2. Jeu « Canonique ou non ? »
   3. Comparateur  4. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* 1. Onglets */
  const tabs = $$(".dos-tabs [role=tab]");
  const select = (t, focus) => {
    tabs.forEach((x) => {
      const on = x === t;
      x.setAttribute("aria-selected", String(on));
      x.tabIndex = on ? 0 : -1;
      document.getElementById(x.getAttribute("aria-controls")).hidden = !on;
    });
    if (focus) t.focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", (ev) => {
      const k = ev.key;
      if (k === "ArrowRight" || k === "ArrowLeft" || k === "Home" || k === "End") {
        ev.preventDefault();
        const n = k === "Home" ? 0 : k === "End" ? tabs.length - 1 : (i + (k === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
        select(tabs[n], true);
      }
    });
  });

  /* 2. Jeu */
  const qz = $(".quiz");
  if (qz) {
    let data = [];
    try { data = JSON.parse(qz.dataset.quiz); } catch (_) { data = []; }
    const q = $(".qz-q", qz), rep = $(".qz-rep", qz), fin = $(".qz-fin", qz), btns = $$(".qz-b", qz);
    const num = $(".qz-num b", qz), score = $(".qz-score b", qz), prog = $(".qz-prog i", qz);
    let i = 0, pts = 0;
    const badge = (it) => it.r === "canon"
      ? '<span class="badge badge-canon">Canonique</span>'
      : `<span class="badge badge-apo">${it.b || "Apocryphe"}</span>`;
    const show = () => {
      const it = data[i];
      q.textContent = it.q;
      num.textContent = i + 1;
      prog.style.width = (i / data.length) * 100 + "%";
      rep.hidden = true; rep.classList.remove("is-ok", "is-ko");
      btns.forEach((b) => { b.disabled = false; b.classList.remove("is-picked"); });
      $(".qz-btns", qz).hidden = false;
      q.hidden = false;
    };
    btns.forEach((b) => b.addEventListener("click", () => {
      const it = data[i], ok = b.dataset.r === it.r;
      if (ok) pts++;
      score.textContent = pts;
      btns.forEach((x) => (x.disabled = true));
      b.classList.add("is-picked");
      rep.classList.add(ok ? "is-ok" : "is-ko");
      $(".qz-verdict", rep).textContent = ok ? "Bonne réponse !" : "Pas tout à fait…";
      $(".qz-src", rep).innerHTML = "";
      const s = document.createElement("span"); s.textContent = it.src;
      $(".qz-src", rep).append(s); $(".qz-src", rep).insertAdjacentHTML("beforeend", badge(it));
      $(".qz-ex", rep).textContent = it.ex;
      $(".qz-next", rep).firstChild.textContent = i === data.length - 1 ? "Voir mon score " : "Phrase suivante ";
      rep.hidden = false;
      $(".qz-next", rep).focus({ preventScroll: true });
    }));
    $(".qz-next", qz).addEventListener("click", () => {
      i++;
      if (i < data.length) { show(); return; }
      prog.style.width = "100%";
      q.hidden = true; rep.hidden = true; $(".qz-btns", qz).hidden = true;
      $(".qz-fin-score", fin).textContent = `${pts} / ${data.length}`;
      fin.hidden = false;
    });
    $(".qz-again", qz).addEventListener("click", () => { i = 0; pts = 0; score.textContent = 0; fin.hidden = true; show(); });
    if (data.length) show();
  }

  /* 3. Comparateur */
  const cp = $(".cp");
  if (cp) {
    const bs = $$(".cp-mode [data-crit]", cp);
    bs.forEach((b) => b.addEventListener("click", () => {
      cp.dataset.crit = b.dataset.crit;
      bs.forEach((x) => x.setAttribute("aria-checked", String(x === b)));
    }));
  }

  /* 4. Sommaire actif */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
