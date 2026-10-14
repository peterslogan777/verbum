/* =====================================================================
   VERBUM — Hall d'entrée (étape E02)
   Diaporama du hero · parchemin qui se déroule · audioguide avec
   visualisation · frise horizontale · carte de diffusion mondiale
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 1. Diaporama cinématographique ---------- */
  const slides = $$(".hero .slide");
  const dots = $$(".hero-dot");
  const capText = $(".cap-text");
  if (slides.length > 1) {
    const DUR = 8000;
    document.documentElement.style.setProperty("--slide-dur", DUR + "ms");
    let cur = 0, timer = null;
    const go = (n) => {
      slides[cur].classList.remove("is-active");
      dots[cur]?.classList.remove("is-active");
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add("is-active");
      dots.forEach((d, i) => { d.classList.toggle("is-done", i < cur); d.classList.remove("is-active"); });
      void dots[cur]?.offsetWidth; // relance l'animation de la jauge
      dots[cur]?.classList.add("is-active");
      if (capText) { capText.style.opacity = 0; setTimeout(() => { capText.textContent = slides[cur].dataset.caption; capText.style.opacity = 1; }, 400); }
      const next = slides[(cur + 1) % slides.length].querySelector("img");
      if (next && next.loading === "lazy") next.loading = "eager"; // précharge l'image suivante
    };
    const play = () => { clearInterval(timer); if (!reduced) timer = setInterval(() => go(cur + 1), DUR); };
    dots.forEach((d, i) => d.addEventListener("click", () => { go(i); play(); }));
    document.addEventListener("visibilitychange", () => (document.hidden ? clearInterval(timer) : play()));
    play();
  }

  /* ---------- 2. Parchemin qui se déroule ---------- */
  const io = new IntersectionObserver((en) => en.forEach((x) => {
    if (x.isIntersecting) { x.target.classList.add("is-open"); io.unobserve(x.target); }
  }), { threshold: 0.35 });
  $$("[data-unroll]").forEach((el) => io.observe(el));

  /* ---------- 3. Audioguide : voir assets/js/audio.js (commun à tout le site) ---------- */

  /* ---------- 4. Frise horizontale ---------- */
  const track = $(".fr-track");
  if (track) {
    const cards = $$(".fr-card", track), fdots = $$(".fr-dot"), cursor = $(".fr-cursor"), fill = $(".fr-fill");
    const count = $(".fr-count b"); $(".fr-count span").textContent = cards.length;
    let active = -1;
    const setActive = (i) => {
      if (i === active) return; active = i;
      cards.forEach((c, k) => c.classList.toggle("is-active", k === i));
      fdots.forEach((d, k) => { d.classList.toggle("is-active", k === i); d.classList.toggle("is-past", k < i); });
      const pos = +cards[i].dataset.pos * 100;
      cursor.style.left = pos + "%"; fill.style.width = pos + "%";
      count.textContent = i + 1;
    };
    const centerOf = (c) => c.offsetLeft + c.offsetWidth / 2 - track.clientWidth / 2;
    const goTo = (i) => {
      i = Math.max(0, Math.min(cards.length - 1, i));
      track.scrollTo({ left: centerOf(cards[i]), behavior: reduced ? "auto" : "smooth" });
      setActive(i);
    };
    const onScroll = () => {
      const mid = track.scrollLeft + track.clientWidth / 2;
      let best = 0, bd = Infinity;
      cards.forEach((c, k) => { const d = Math.abs(c.offsetLeft + c.offsetWidth / 2 - mid); if (d < bd) { bd = d; best = k; } });
      setActive(best);
    };
    track.addEventListener("scroll", () => requestAnimationFrame(onScroll), { passive: true });
    fdots.forEach((d) => d.addEventListener("click", () => goTo(+d.dataset.i)));
    $('[data-fr="prev"]').addEventListener("click", () => goTo(active - 1));
    $('[data-fr="next"]').addEventListener("click", () => goTo(active + 1));
    track.addEventListener("keydown", (ev) => {
      if (ev.key === "ArrowRight") { ev.preventDefault(); goTo(active + 1); }
      if (ev.key === "ArrowLeft") { ev.preventDefault(); goTo(active - 1); }
    });
    // glisser à la souris
    let down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener("pointerdown", (ev) => {
      if (ev.pointerType !== "mouse") return;
      down = true; moved = false; sx = ev.clientX; sl = track.scrollLeft;
    });
    addEventListener("pointermove", (ev) => {
      if (!down) return;
      const dx = ev.clientX - sx;
      if (Math.abs(dx) > 5 && !moved) { moved = true; track.classList.add("is-dragging"); }
      if (moved) track.scrollLeft = sl - dx;
    });
    addEventListener("pointerup", () => {
      if (!down) return; down = false;
      if (moved) { track.classList.remove("is-dragging"); onScroll(); goTo(active); }
    });
    setActive(0);
  }

  /* ---------- 5. Carte de diffusion mondiale ---------- */
  const map = $(".carte-svg");
  if (map) {
    const tabs = $$(".ep-tab"), panels = $$(".ep-panel"), pts = $$(".pt", map), arcs = $$(".arc", map);
    const tip = $(".carte-tip"), wrap = $(".carte-map"), auto = $(".ep-auto");
    arcs.forEach((a) => { const L = a.getTotalLength(); a.style.strokeDasharray = L; a.style.strokeDashoffset = L; a.dataset.len = L; });
    let era = -1, autoTimer = null;
    const show = (k) => {
      era = k;
      tabs.forEach((t, i) => { t.classList.toggle("is-active", i === k); t.setAttribute("aria-selected", String(i === k)); });
      panels.forEach((p, i) => p.classList.toggle("is-active", i === k));
      pts.forEach((p) => { const e = +p.dataset.era; p.classList.toggle("on", e <= k); p.classList.toggle("new", e === k); });
      arcs.forEach((a) => {
        const e = +a.dataset.era;
        a.classList.toggle("on", e <= k); a.classList.toggle("new", e === k);
        a.style.transition = "none";
        if (e < k) a.style.strokeDashoffset = 0;
        else if (e > k) a.style.strokeDashoffset = a.dataset.len;
        else {
          a.style.strokeDashoffset = a.dataset.len;
          requestAnimationFrame(() => requestAnimationFrame(() => {
            a.style.transition = `stroke-dashoffset ${reduced ? 0 : 1.6}s cubic-bezier(.65,0,.35,1), opacity .6s`;
            a.style.strokeDashoffset = 0;
          }));
        }
      });
    };
    tabs.forEach((t) => t.addEventListener("click", () => { stopAuto(); show(+t.dataset.era); }));
    const stopAuto = () => { clearInterval(autoTimer); autoTimer = null; auto.setAttribute("aria-pressed", "false"); };
    auto.addEventListener("click", () => {
      if (autoTimer) return stopAuto();
      auto.setAttribute("aria-pressed", "true");
      show(0);
      autoTimer = setInterval(() => { if (era >= tabs.length - 1) return stopAuto(); show(era + 1); }, 3200);
    });
    // infobulle
    const showTip = (p) => {
      const r = wrap.getBoundingClientRect(), b = p.getBoundingClientRect();
      tip.innerHTML = `<b>${p.dataset.name}</b>${p.dataset.detail}`;
      tip.style.left = Math.min(Math.max(b.left + b.width / 2 - r.left, 130), r.width - 130) + "px";
      tip.style.top = b.top - r.top + "px";
      tip.classList.add("is-on");
    };
    pts.forEach((p) => {
      p.addEventListener("pointerenter", () => showTip(p));
      p.addEventListener("focus", () => showTip(p));
      p.addEventListener("pointerleave", () => tip.classList.remove("is-on"));
      p.addEventListener("blur", () => tip.classList.remove("is-on"));
    });
    // première apparition : on déroule l'époque 0 quand la carte devient visible
    new IntersectionObserver((en, obs) => { if (en[0].isIntersecting) { show(0); obs.disconnect(); } }, { threshold: 0.3 }).observe(map);
  }
})();
