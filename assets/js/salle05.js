/* =====================================================================
   VERBUM — Salle 05 · Découverte 2026 : le Codex H (étape E07)
   1. Curseur avant / après (+ bandes de lumière, retournement du miroir)
   2. Carte des feuillets dispersés  3. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* 1. Avant / après */
  const aa = $(".aa");
  if (aa) {
    const range = $(".aa-range", aa), flip = $(".aa-flip", aa), lecture = $(".aa-lecture", aa);
    const setPos = (v) => { aa.style.setProperty("--pos", v + "%"); range.value = v; };
    range.addEventListener("input", () => setPos(+range.value));

    // animation douce de la poignée
    let anim = 0;
    function glide(to) {
      cancelAnimationFrame(anim);
      const from = +range.value, t0 = performance.now(), d = reduced ? 1 : 700;
      const step = (now) => {
        const k = Math.min(1, (now - t0) / d), e = 1 - Math.pow(1 - k, 3);
        setPos(Math.round((from + (to - from) * e) * 10) / 10);
        if (k < 1) anim = requestAnimationFrame(step);
      };
      anim = requestAnimationFrame(step);
    }

    const bandes = $$(".aa-bandes [data-bande]", aa);
    bandes.forEach((b) => b.addEventListener("click", () => {
      aa.dataset.bande = b.dataset.bande;
      bandes.forEach((x) => x.setAttribute("aria-checked", String(x === b)));
    }));
    aa.dataset.bande = "visible";

    flip.addEventListener("click", () => {
      const on = !aa.classList.contains("is-flip");
      aa.classList.toggle("is-flip", on);
      flip.setAttribute("aria-pressed", String(on));
      flip.textContent = on ? "Revoir l'empreinte en miroir" : "Remettre le texte à l'endroit";
      lecture.hidden = !on;
      glide(on ? 15 : 50);
    });

    // petite démonstration à la première apparition
    if (!reduced) {
      const io = new IntersectionObserver((en) => {
        if (!en[0].isIntersecting) return;
        io.disconnect();
        setTimeout(() => { glide(72); setTimeout(() => glide(50), 800); }, 500);
      }, { threshold: .5 });
      io.observe(aa);
    }
  }

  /* 2. Carte des feuillets */
  const pts = $$(".ch-pt, .ch-lab"), rays = $$(".ch-ray"), panels = $$(".ch-panel");
  function lieu(key) {
    pts.forEach((p) => p.classList.toggle("is-on", p.dataset.key === key));
    rays.forEach((r) => r.classList.toggle("is-on", r.dataset.key === key));
    panels.forEach((p) => (p.hidden = p.dataset.key !== key));
  }
  pts.forEach((p) => {
    p.addEventListener("click", () => lieu(p.dataset.key));
    p.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); lieu(p.dataset.key); } });
  });

  /* 3. Sommaire actif */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
