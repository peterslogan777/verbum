/* =====================================================================
   VERBUM — Salle 07 · La Septante et les grandes traductions (étape E09)
   1. Polyglotte : onglets des versets + alignement des segments
   2. Le nom divin (3 états)  3. Canon de la Peshitta  4. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* Groupes radio génériques (.seg) : met à jour aria-checked et renvoie la valeur */
  const radio = (group, attr, cb) => {
    if (!group) return;
    const btns = $$("button[role=radio]", group);
    const set = (b, focus) => {
      btns.forEach((x) => { const on = x === b; x.setAttribute("aria-checked", String(on)); x.tabIndex = on ? 0 : -1; });
      if (focus) b.focus();
      cb(b.dataset[attr]);
    };
    btns.forEach((b, i) => {
      b.tabIndex = b.getAttribute("aria-checked") === "true" ? 0 : -1;
      b.addEventListener("click", () => set(b));
      b.addEventListener("keydown", (ev) => {
        const d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[ev.key];
        if (d) { ev.preventDefault(); set(btns[(i + d + btns.length) % btns.length], true); }
      });
    });
  };

  /* 1. Polyglotte */
  const tabs = $$(".pg-tabs [role=tab]");
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
      if (["ArrowRight", "ArrowLeft", "Home", "End"].includes(k)) {
        ev.preventDefault();
        const n = k === "Home" ? 0 : k === "End" ? tabs.length - 1 : (i + (k === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
        select(tabs[n], true);
      }
    });
  });

  $$(".pg-panel").forEach((panel) => {
    const segs = $$(".pg-s", panel);
    const ids = (el) => (el.dataset.i || "").split(" ").filter(Boolean);
    const clear = () => segs.forEach((s) => s.classList.remove("is-on"));
    const light = (el) => {
      const want = ids(el);
      segs.forEach((s) => s.classList.toggle("is-on", ids(s).some((x) => want.includes(x))));
    };
    segs.forEach((s) => {
      s.addEventListener("mouseenter", () => light(s));
      s.addEventListener("focus", () => light(s));
      s.addEventListener("click", () => light(s));
      s.addEventListener("mouseleave", clear);
      s.addEventListener("blur", clear);
    });
  });

  /* 2. Le nom divin */
  const stage = $(".nd-stage");
  radio($(".nd-seg"), "etat", (v) => { if (stage) stage.dataset.etat = v; });

  /* 3. Canon de la Peshitta */
  const nt = $(".nt");
  const msg = $(".nt-msg");
  radio($(".nt-mode"), "mode", (v) => {
    if (!nt) return;
    nt.dataset.mode = v;
    if (msg) msg.textContent = v === "peshitta"
      ? "22 livres dans la Peshitta du Vᵉ siècle. 2 Pierre, 2 et 3 Jean, Jude et Révélation y ont été ajoutés en 508 et 616. Les 27 livres restent canoniques."
      : "Les 27 livres du Nouveau Testament, tous canoniques.";
  });

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
