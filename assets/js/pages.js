/* VERBUM — Sources : filtre de la bibliographie (sans accents ni casse) */
(() => {
  "use strict";
  const inp = document.getElementById("bi-q");
  if (!inp) return;
  const fold = (s) => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const grps = [...document.querySelectorAll(".bi-grp")];
  const out = document.querySelector(".bi-n");
  const all = grps.reduce((n, g) => n + g.querySelectorAll("li").length, 0);
  const run = () => {
    const q = fold(inp.value.trim());
    let n = 0;
    grps.forEach((g) => {
      const theme = fold(g.querySelector("summary span").textContent);
      let k = 0;
      g.querySelectorAll("li").forEach((li) => {
        const on = !q || theme.includes(q) || fold(li.textContent).includes(q);
        li.hidden = !on; if (on) k++;
      });
      g.hidden = k === 0;
      g.open = !!q && k > 0;
      n += k;
    });
    out.textContent = q ? `${n} sur ${all}` : `${all} références`;
  };
  inp.addEventListener("input", run);
  run();
})();

/* VERBUM — Sommaire de page : met en valeur la vitrine visible */
(() => {
  "use strict";
  const links = [...document.querySelectorAll(".s-sommaire a[href^='#']")];
  if (!links.length || !("IntersectionObserver" in window)) return;
  const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
  const io = new IntersectionObserver((ents) => {
    ents.forEach((en) => {
      if (!en.isIntersecting) return;
      links.forEach((a) => a.classList.remove("is-active"));
      const a = map.get(en.target.id);
      if (a) {
        a.classList.add("is-active");
        const c = a.parentElement;
        if (c.scrollWidth > c.clientWidth + 2) c.scrollTo({ left: a.offsetLeft - c.offsetLeft - 16, behavior: "smooth" });
      }
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
})();
