/* =====================================================================
   VERBUM — Salle 02 · Les Copistes et les Massorètes (étape E04)
   Couches du texte, « un mot, trois lectures », page massorétique,
   jeu du copiste, voyage du Codex d'Alep, sommaire actif.
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* 1. Trois couches */
  const couches = $(".couches");
  if (couches) {
    const btns = $$(".seg [data-set]", couches);
    btns.forEach((b) => b.addEventListener("click", () => {
      couches.dataset.layer = b.dataset.set;
      btns.forEach((x) => x.setAttribute("aria-checked", String(x === b)));
    }));
  }

  /* 2. Un mot, trois lectures */
  const dvBig = $(".dv-big");
  $$(".dv-opts button").forEach((b) => b.addEventListener("click", () => {
    $$(".dv-opts button").forEach((x) => x.classList.toggle("is-on", x === b));
    dvBig.textContent = $("[lang=he]", b).textContent;
    dvBig.animate([{ opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "none" }], { duration: 500 });
  }));
  $(".dv-cons")?.addEventListener("click", () => { dvBig.textContent = "דבר"; $$(".dv-opts button").forEach((x) => x.classList.remove("is-on")); });

  /* 3. Page massorétique */
  const dots = $$(".mp-dot"), infos = $$(".mp-info p");
  const showMp = (k) => {
    dots.forEach((d) => d.classList.toggle("is-on", d.dataset.mp === k));
    infos.forEach((p) => p.classList.toggle("is-on", p.dataset.mp === k));
  };
  dots.forEach((d) => { d.addEventListener("click", () => showMp(d.dataset.mp)); d.addEventListener("mouseenter", () => showMp(d.dataset.mp)); });

  /* 4. Jeu du copiste */
  const jeu = $(".jeu");
  if (jeu) {
    const rounds = $$(".jeu-round", jeu), jdots = $$(".jeu-dots i", jeu), score = $(".jeu-score b", jeu);
    const next = $(".jeu-next", jeu), reset = $(".jeu-reset", jeu), fin = $(".jeu-fin", jeu);
    let cur = 0, found = 0;
    rounds.forEach((r) => $$(".lt", r).forEach((lt) => lt.addEventListener("click", () => {
      if (r.classList.contains("is-solved")) return;
      if (lt.dataset.faute) {
        lt.classList.add("is-found"); r.classList.add("is-solved");
        $(".jr-expl", r).hidden = false; found++; score.textContent = found;
        jdots[cur].classList.add("is-done");
        if (cur < rounds.length - 1) next.hidden = false; else { fin.hidden = false; reset.hidden = false; }
      } else {
        lt.classList.remove("is-wrong"); void lt.offsetWidth; lt.classList.add("is-wrong");
      }
    })));
    next.addEventListener("click", () => {
      rounds[cur].classList.remove("is-active"); cur++;
      rounds[cur].classList.add("is-active"); jdots[cur].classList.add("is-on"); next.hidden = true;
    });
    reset.addEventListener("click", () => {
      cur = 0; found = 0; score.textContent = 0; fin.hidden = true; reset.hidden = true;
      rounds.forEach((r, i) => {
        r.classList.toggle("is-active", i === 0); r.classList.remove("is-solved"); $(".jr-expl", r).hidden = true;
        $$(".lt", r).forEach((l) => l.classList.remove("is-found", "is-wrong"));
      });
      jdots.forEach((d, i) => { d.classList.remove("is-done"); d.classList.toggle("is-on", i === 0); });
    });
  }

  /* 5. Voyage du Codex d'Alep */
  const steps = $$(".cv-steps li");
  if (steps.length) {
    const keys = ["tiberiade", "jerusalem", "caire", "alep", "jerusalem"];
    const go = (i) => {
      steps.forEach((s, j) => s.classList.toggle("is-on", j === i));
      $$(".cv-seg").forEach((s) => s.classList.toggle("is-on", +s.dataset.seg <= i));
      $$(".cv-pt").forEach((p) => p.classList.toggle("is-on", p.dataset.key === keys[i]));
    };
    steps.forEach((s, i) => $("button", s).addEventListener("click", () => go(i)));
    $$(".cv-pt").forEach((p) => p.addEventListener("click", () => { const i = keys.lastIndexOf(p.dataset.key); go(i); }));
    go(0);
  }

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
