/* =====================================================================
   VERBUM — Salle 01 · Les Origines (étape E03)
   Bascule d'écriture (paléo-hébreu / hébreu carré / translittération),
   mots lisibles sur l'amulette KH2, cartes à retourner, sommaire actif.
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* 1. Écriture affichée */
  const bened = $(".bened");
  if (bened) {
    const btns = $$(".seg [data-set]", bened);
    const set = (v) => {
      bened.dataset.script = v;
      btns.forEach((b) => b.setAttribute("aria-checked", String(b.dataset.set === v)));
    };
    btns.forEach((b) => b.addEventListener("click", () => set(b.dataset.set)));
    $(".seg", bened).addEventListener("keydown", (ev) => {
      if (!["ArrowLeft", "ArrowRight"].includes(ev.key)) return;
      const i = btns.findIndex((b) => b.dataset.set === bened.dataset.script);
      const n = btns[(i + (ev.key === "ArrowRight" ? 1 : -1) + btns.length) % btns.length];
      set(n.dataset.set); n.focus();
    });
    /* 2. Mots attestés sur KH2 */
    $("[data-kh-toggle]", bened)?.addEventListener("change", (ev) => bened.classList.toggle("show-kh", ev.target.checked));
  }

  /* 3. Cartes à retourner (clic / clavier / tactile) */
  $$(".flip-inner").forEach((c) => c.addEventListener("click", () => {
    const on = c.classList.toggle("is-flipped");
    c.setAttribute("aria-pressed", String(on));
  }));

  /* 4. Sommaire : lien actif selon la section visible */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
