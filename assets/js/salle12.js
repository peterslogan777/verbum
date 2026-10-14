/* =====================================================================
   VERBUM — Salle 12 · La Bible en français (étape E15)
   1. Olivétan : orthographe 1535 / modernisée  2. Comparateur Jean 1:1
   3. Qui a traduit ?  4. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];

  /* ---------- 1. Olivétan ---------- */
  const page = $(".ol-page");
  if (page) {
    const btns = $$(".ol-seg [data-mode]", page);
    const set = (m) => {
      page.dataset.mode = m;
      btns.forEach((b) => b.setAttribute("aria-checked", String(b.dataset.mode === m)));
    };
    btns.forEach((b) => b.addEventListener("click", () => set(b.dataset.mode)));
    $(".ol-seg", page).addEventListener("keydown", (ev) => {
      if (ev.key !== "ArrowLeft" && ev.key !== "ArrowRight") return;
      ev.preventDefault();
      const next = page.dataset.mode === "old" ? "new" : "old";
      set(next);
      btns.find((b) => b.dataset.mode === next)?.focus();
    });
  }

  /* ---------- 2. Comparateur ---------- */
  const marque = (el) => {
    // souligne « Parole / parolle » (or) et « Verbe / Verbum » (bleu) sans toucher au reste du texte
    el.innerHTML = el.textContent
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/\b(Parole|parole|parolle)\b/g, '<mark class="m-parole">$1</mark>')
      .replace(/\b(Verbe|Verbum)\b/g, '<mark class="m-verbe">$1</mark>');
  };
  $$(".cp-txt, .cp-l").forEach(marque);

  const range = $(".cp-range");
  if (range) {
    const cards = $$(".cp-card"), ticks = $$(".cp-tick");
    const show = (i) => {
      i = Math.max(0, Math.min(cards.length - 1, i));
      cards.forEach((c, k) => { const on = k === i; c.hidden = !on; c.classList.toggle("is-on", on); });
      ticks.forEach((t, k) => t.classList.toggle("is-on", k === i));
      range.value = i;
      range.setAttribute("aria-valuetext", ticks[i]?.getAttribute("aria-label") || String(i));
    };
    range.addEventListener("input", () => show(+range.value));
    ticks.forEach((t) => t.addEventListener("click", () => show(+t.dataset.i)));
  }

  /* ---------- 3. Qui a traduit ? ---------- */
  const qs = $$(".qt-q");
  if (qs.length) {
    let score = 0, answered = 0;
    const sEl = $(".qt-s"), dEl = $(".qt-done");
    qs.forEach((q) => {
      const btns = $$(".qt-b", q);
      btns.forEach((b) => b.addEventListener("click", () => {
        if (q.dataset.done) return;
        q.dataset.done = "1"; answered++;
        const ok = b.dataset.a === q.dataset.ok;
        if (ok) score++;
        btns.forEach((x) => {
          x.disabled = true;
          x.classList.toggle("is-pick", x === b);
          x.classList.toggle("is-good", x.dataset.a === q.dataset.ok);
        });
        q.classList.add(ok ? "is-ok" : "is-ko");
        $(".qt-you", q).textContent = ok ? "Bonne réponse" : "C'était la bonne réponse";
        $(".qt-r", q).hidden = false;
        if (sEl) sEl.textContent = score;
        if (dEl && answered === qs.length) dEl.textContent = score === qs.length ? "· Sans faute !" : "· Terminé";
      }));
    });
  }

  /* ---------- 4. Sommaire actif ---------- */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
