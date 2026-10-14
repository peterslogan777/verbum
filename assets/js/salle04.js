/* =====================================================================
   VERBUM — Salle 04 · Les Grands Codex grecs (étape E06)
   1. Fragment P52 (recto/verso, texte restitué)  2. Scriptio continua
   3. Cartes 3D des codex  4. Graphique comparatif  5. Points des feuillets
   6. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* 1. P52 */
  const p52 = $(".p52");
  if (p52) {
    const faces = $$(".p52-faces [data-face]", p52), frs = $$(".p52-fr", p52);
    faces.forEach((b) => b.addEventListener("click", () => {
      const f = b.dataset.face;
      p52.dataset.face = f;
      faces.forEach((x) => x.setAttribute("aria-checked", String(x === b)));
      frs.forEach((p) => (p.hidden = p.dataset.for !== f));
    }));
    $(".p52-full", p52).addEventListener("change", (ev) => p52.classList.toggle("is-full", ev.target.checked));
  }

  /* 2. Scriptio continua */
  const sc = $(".sc");
  if (sc) {
    const btns = $$(".sc-steps [data-step]", sc);
    btns.forEach((b) => b.addEventListener("click", () => {
      const n = b.dataset.step;
      sc.dataset.step = n;
      btns.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      [0, 1, 2].forEach((i) => { const el = $(".sc-" + i, sc); if (el) el.hidden = String(i) !== n; });
    }));
  }

  /* 3. Cartes 3D (au clic uniquement) */
  $$(".cx").forEach((card) => {
    const front = $(".cx-front .cx-btn", card), back = $(".cx-back-btn", card);
    const set = (on) => {
      card.classList.toggle("is-flip", on);
      front.setAttribute("aria-expanded", String(on));
      $(".cx-front", card).setAttribute("aria-hidden", String(on));
      $(".cx-back", card).setAttribute("aria-hidden", String(!on));
      (on ? back : front).focus({ preventScroll: true });
    };
    $(".cx-back", card).setAttribute("aria-hidden", "true");
    front.addEventListener("click", () => set(true));
    back.addEventListener("click", () => set(false));
  });

  /* 4. Graphique */
  const chart = $(".chart");
  if (chart) {
    const btns = $$(".chart-mode [data-mode]", chart);
    btns.forEach((b) => b.addEventListener("click", () => {
      chart.dataset.mode = b.dataset.mode;
      btns.forEach((x) => x.setAttribute("aria-checked", String(x === b)));
    }));
  }

  /* 5. Apparition progressive des feuillets */
  const fe = $(".feuillets-s");
  if (fe) $$(".fe-dots i", fe).forEach((d, i) => (d.style.transitionDelay = Math.min(i * 4, 1600) + "ms"));

  /* 6. Sommaire actif */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
