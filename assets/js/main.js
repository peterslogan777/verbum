/* =====================================================================
   VERBUM — Script principal (JavaScript natif, aucune dépendance)
   Loader · en-tête · plan du musée · révélations · compteurs · parallaxe
   · particules dorées · curseur plume · cartes inclinables · audioguide
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const body = document.body;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ---------- 1. Loader calligraphique ---------- */
  const loader = $(".loader");
  if (loader) {
    let seen = false;
    try { seen = sessionStorage.getItem("verbum-seen") === "1"; } catch (_) {}
    const minTime = reduced ? 200 : seen ? 900 : 3300;
    const start = performance.now();
    const finish = () => {
      const wait = Math.max(0, minTime - (performance.now() - start));
      setTimeout(() => {
        loader.classList.add("is-done");
        body.classList.remove("is-loading");
        body.classList.add("is-ready");
        try { sessionStorage.setItem("verbum-seen", "1"); } catch (_) {}
      }, wait);
    };
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => {
      if (document.readyState === "complete") finish(); else addEventListener("load", finish, { once: true });
    });
    setTimeout(finish, 6000); // filet de sécurité
  } else {
    body.classList.remove("is-loading");
    body.classList.add("is-ready");
  }

  /* ---------- 2. En-tête + barre de progression ---------- */
  const header = $(".site-header");
  const progress = $(".scroll-progress");
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    const max = document.documentElement.scrollHeight - innerHeight;
    if (progress) progress.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    if (header) {
      header.classList.toggle("is-scrolled", y > 40);
      header.classList.toggle("is-hidden", y > 400 && y > lastY && !body.classList.contains("drawer-open"));
    }
    lastY = y;
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- 3. Plan du musée (panneau latéral) ---------- */
  const drawer = $("#plan-musee");
  const openers = $$("[data-drawer-open]");
  let lastFocus = null;
  const setDrawer = (open) => {
    if (!drawer) return;
    body.classList.toggle("drawer-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    drawer.toggleAttribute("inert", !open);
    openers.forEach((b) => b.setAttribute("aria-expanded", String(open)));
    if (open) { lastFocus = document.activeElement; setTimeout(() => $(".drawer-close", drawer)?.focus(), 50); }
    else lastFocus?.focus?.();
  };
  openers.forEach((b) => b.addEventListener("click", () => setDrawer(true)));
  $$("[data-drawer-close]").forEach((b) => b.addEventListener("click", () => setDrawer(false)));
  addEventListener("keydown", (ev) => { if (ev.key === "Escape" && body.classList.contains("drawer-open")) setDrawer(false); });
  $$("#plan-musee a").forEach((a) => a.addEventListener("click", () => setDrawer(false)));

  /* ---------- 4. Révélations au défilement ---------- */
  const revealIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target;
      const siblings = [...el.parentElement.children].filter((c) => c.hasAttribute("data-reveal"));
      el.style.transitionDelay = `${Math.min(siblings.indexOf(el), 6) * 0.08}s`;
      el.classList.add("is-visible");
      revealIO.unobserve(el);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
  $$("[data-reveal]").forEach((el) => revealIO.observe(el));

  /* ---------- 5. Compteurs animés ---------- */
  const fmt = new Intl.NumberFormat("fr-FR");
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target, target = +el.dataset.count, prefix = el.dataset.prefix || "";
      const dur = reduced ? 1 : 2200, t0 = performance.now();
      const tick = (t) => {
        const p = Math.min(1, (t - t0) / dur), eased = 1 - Math.pow(1 - p, 4);
        el.textContent = prefix + fmt.format(Math.round(target * eased));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      countIO.unobserve(el);
    });
  }, { threshold: 0.5 });
  $$("[data-count]").forEach((el) => countIO.observe(el));

  /* ---------- 6. Cartes inclinables (effet 3D + halo doré) ---------- */
  if (finePointer && !reduced) {
    $$("[data-tilt]").forEach((card) => {
      card.addEventListener("pointermove", (ev) => {
        const r = card.getBoundingClientRect();
        const x = (ev.clientX - r.left) / r.width, y = (ev.clientY - r.top) / r.height;
        card.style.setProperty("--mx", `${x * 100}%`);
        card.style.setProperty("--my", `${y * 100}%`);
        card.style.transform = `perspective(1000px) rotateX(${(0.5 - y) * 6}deg) rotateY(${(x - 0.5) * 8}deg) translateY(-4px)`;
      });
      card.addEventListener("pointerleave", () => { card.style.transform = ""; });
    });
  }

  /* ---------- 7. Parallaxe du paysage (défilement + souris) ---------- */
  const layers = $$("[data-depth]");
  if (layers.length && !reduced) {
    let mx = 0, my = 0, cx = 0, cy = 0;
    addEventListener("pointermove", (ev) => { mx = ev.clientX / innerWidth - 0.5; my = ev.clientY / innerHeight - 0.5; }, { passive: true });
    const loop = () => {
      cx += (mx - cx) * 0.05; cy += (my - cy) * 0.05;
      if (scrollY < innerHeight * 1.2) {
        layers.forEach((l) => {
          const d = +l.dataset.depth;
          l.style.transform = `translate3d(${-cx * d * 120}px, ${scrollY * d * 0.9 - cy * d * 30}px, 0)`;
        });
      }
      requestAnimationFrame(loop);
    };
    loop();
  }

  /* ---------- 8. Particules dorées (poussière de lumière) ---------- */
  const cvs = $("#particles");
  if (cvs && !reduced) {
    const ctx = cvs.getContext("2d");
    let W, H, dpr, parts = [], visible = true, pointer = { x: -999, y: -999 };
    const resize = () => {
      dpr = Math.min(devicePixelRatio || 1, 2);
      W = cvs.clientWidth; H = cvs.clientHeight;
      cvs.width = W * dpr; cvs.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(160, (W * H) / 9000));
      parts = Array.from({ length: n }, () => spawn(true));
    };
    const spawn = (anywhere) => ({
      x: Math.random() * W, y: anywhere ? Math.random() * H : H + 10,
      r: Math.random() * 1.8 + 0.3, vy: -(Math.random() * 0.35 + 0.08), vx: (Math.random() - 0.5) * 0.15,
      a: Math.random() * 0.6 + 0.2, tw: Math.random() * Math.PI * 2, hue: 38 + Math.random() * 12,
    });
    cvs.parentElement.addEventListener("pointermove", (ev) => {
      const r = cvs.getBoundingClientRect(); pointer.x = ev.clientX - r.left; pointer.y = ev.clientY - r.top;
    });
    new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) requestAnimationFrame(draw); }).observe(cvs);
    const draw = () => {
      if (!visible) return;
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = "lighter";
      for (const p of parts) {
        p.tw += 0.03; p.x += p.vx + Math.sin(p.tw * 0.5) * 0.12; p.y += p.vy;
        const dx = p.x - pointer.x, dy = p.y - pointer.y, d2 = dx * dx + dy * dy;
        if (d2 < 14000) { const f = (14000 - d2) / 14000; p.x += dx * f * 0.03; p.y += dy * f * 0.03; }
        if (p.y < -10 || p.x < -10 || p.x > W + 10) Object.assign(p, spawn(false));
        const alpha = p.a * (0.6 + 0.4 * Math.sin(p.tw));
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4);
        g.addColorStop(0, `hsla(${p.hue}, 80%, 75%, ${alpha})`);
        g.addColorStop(1, `hsla(${p.hue}, 80%, 60%, 0)`);
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2); ctx.fill();
      }
      requestAnimationFrame(draw);
    };
    addEventListener("resize", resize);
    resize(); requestAnimationFrame(draw);
  }

  /* ---------- 9. Curseur plume de scribe ---------- */
  if (finePointer && !reduced) {
    const quill = document.createElement("div");
    quill.className = "quill"; quill.setAttribute("aria-hidden", "true");
    quill.innerHTML = '<svg viewBox="0 0 34 34" fill="none"><defs><linearGradient id="qg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#8C7330"/><stop offset=".5" stop-color="#E6CC7A"/><stop offset="1" stop-color="#F5E6C8"/></linearGradient></defs><path d="M2 32 C8 22 14 14 31 2 C27 12 20 21 9 27 Z" fill="url(#qg)" opacity=".95"/><path d="M2 32 L20 13" stroke="#0A0A0F" stroke-width=".8" opacity=".7"/><path d="M2 32 l2.2-4.6" stroke="#F5E6C8" stroke-width="1.2" stroke-linecap="round"/></svg>';
    const ink = document.createElement("div"); ink.className = "quill-ink"; ink.setAttribute("aria-hidden", "true");
    body.append(quill, ink); body.classList.add("has-quill");
    let x = -100, y = -100, qx = -100, qy = -100;
    addEventListener("pointermove", (ev) => { x = ev.clientX; y = ev.clientY; ink.style.transform = `translate3d(${x}px, ${y}px, 0)`; }, { passive: true });
    const follow = () => {
      qx += (x - qx) * 0.28; qy += (y - qy) * 0.28;
      quill.style.transform = `translate3d(${qx - 2}px, ${qy - 32}px, 0)`; // la pointe de la plume suit le pointeur
      requestAnimationFrame(follow);
    };
    follow();
    document.addEventListener("pointerover", (ev) => quill.classList.toggle("is-hover", !!ev.target.closest("a, button, [data-tilt]")));
    document.addEventListener("pointerleave", () => { quill.style.opacity = 0; ink.style.opacity = 0; });
    document.addEventListener("pointerenter", () => { quill.style.opacity = 1; ink.style.opacity = .9; });
  }

  /* ---------- 10. Parallaxe douce des images d'en-tête [data-parallax="0.15"] ---------- */
  const plx = $$("[data-parallax]");
  if (plx.length && !reduced) {
    const tickP = () => {
      plx.forEach((im) => { if (scrollY < innerHeight * 1.3) im.style.transform = `translate3d(0, ${scrollY * +im.dataset.parallax}px, 0) scale(1.08)`; });
    };
    addEventListener("scroll", () => requestAnimationFrame(tickP), { passive: true }); tickP();
  }

  /* ---------- 11. Visionneuse plein écran (modale de zoom) [data-lightbox] ----------
     <img data-lightbox data-full="grande.jpg" data-caption="Légende"> ou <a data-lightbox href="…"> */
  const lbItems = $$("[data-lightbox]");
  if (lbItems.length) {
    const lb = document.createElement("div");
    lb.className = "lightbox"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true"); lb.setAttribute("aria-label", "Image agrandie");
    lb.innerHTML = `<button class="lb-close" type="button" aria-label="Fermer">Fermer</button>
      <button class="lb-nav lb-prev" type="button" aria-label="Image précédente">‹</button>
      <figure class="lb-fig"><div class="lb-stage"><img alt=""></div><figcaption></figcaption></figure>
      <button class="lb-nav lb-next" type="button" aria-label="Image suivante">›</button>
      <p class="lb-hint">Molette ou double-clic pour zoomer · glisser pour déplacer · Échap pour fermer</p>`;
    body.append(lb);
    const img = $("img", lb), cap = $("figcaption", lb), stage = $(".lb-stage", lb);
    let idx = 0, z = 1, tx = 0, ty = 0, last = null;
    const apply = () => { img.style.transform = `translate(${tx}px, ${ty}px) scale(${z})`; lb.classList.toggle("is-zoomed", z > 1); };
    const show = (i) => {
      idx = (i + lbItems.length) % lbItems.length;
      const el = lbItems[idx];
      img.src = el.dataset.full || el.getAttribute("href") || el.currentSrc || el.src;
      img.alt = el.getAttribute("alt") || "";
      cap.textContent = el.dataset.caption || el.getAttribute("alt") || "";
      z = 1; tx = ty = 0; apply();
    };
    const open = (i) => { last = document.activeElement; show(i); lb.classList.add("is-open"); body.classList.add("no-scroll"); $(".lb-close", lb).focus(); };
    const close = () => { lb.classList.remove("is-open"); body.classList.remove("no-scroll"); last?.focus?.(); };
    lbItems.forEach((el, i) => {
      if (!el.matches("a, button")) { el.tabIndex = 0; el.setAttribute("role", "button"); }
      el.addEventListener("click", (ev) => { ev.preventDefault(); open(i); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(i); } });
    });
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", () => show(idx - 1));
    $(".lb-next", lb).addEventListener("click", () => show(idx + 1));
    if (lbItems.length < 2) lb.classList.add("is-single");
    lb.addEventListener("click", (ev) => { if (ev.target === lb || ev.target === stage) close(); });
    addEventListener("keydown", (ev) => {
      if (!lb.classList.contains("is-open")) return;
      if (ev.key === "Escape") close();
      if (ev.key === "ArrowRight") show(idx + 1);
      if (ev.key === "ArrowLeft") show(idx - 1);
    });
    stage.addEventListener("wheel", (ev) => { ev.preventDefault(); z = Math.min(5, Math.max(1, z * (ev.deltaY < 0 ? 1.15 : 0.87))); if (z === 1) tx = ty = 0; apply(); }, { passive: false });
    img.addEventListener("dblclick", () => { z = z > 1 ? 1 : 2.5; tx = ty = 0; apply(); });
    let drag = null;
    img.addEventListener("pointerdown", (ev) => { if (z > 1) { drag = { x: ev.clientX - tx, y: ev.clientY - ty }; img.setPointerCapture(ev.pointerId); } });
    img.addEventListener("pointermove", (ev) => { if (drag) { tx = ev.clientX - drag.x; ty = ev.clientY - drag.y; apply(); } });
    img.addEventListener("pointerup", () => { drag = null; });
  }

  /* ---------- 12. Loupe [data-loupe] : grossissement circulaire au survol ---------- */
  $$("[data-loupe]").forEach((wrap) => {
    const im = $("img", wrap); if (!im) return;
    const lens = document.createElement("span"); lens.className = "loupe-lens"; lens.setAttribute("aria-hidden", "true");
    wrap.append(lens);
    const zoom = +wrap.dataset.loupe || 2.5;
    const src = im.dataset.full || im.src;
    lens.style.backgroundImage = `url("${src}")`;
    const move = (ev) => {
      const r = im.getBoundingClientRect();
      const x = ev.clientX - r.left, y = ev.clientY - r.top;
      if (x < 0 || y < 0 || x > r.width || y > r.height) { wrap.classList.remove("is-loupe"); return; }
      wrap.classList.add("is-loupe");
      const L = lens.offsetWidth / 2;
      lens.style.left = `${x + im.offsetLeft - L}px`; lens.style.top = `${y + im.offsetTop - L}px`;
      lens.style.backgroundSize = `${r.width * zoom}px ${r.height * zoom}px`;
      lens.style.backgroundPosition = `${-(x * zoom - L)}px ${-(y * zoom - L)}px`;
    };
    wrap.addEventListener("pointermove", move);
    wrap.addEventListener("pointerdown", move);
    wrap.addEventListener("pointerleave", () => wrap.classList.remove("is-loupe"));
  });

  function toast(msg) {
    let t = $(".toast");
    if (!t) {
      t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status");
      Object.assign(t.style, { position: "fixed", left: "50%", bottom: "28px", transform: "translateX(-50%) translateY(20px)", zIndex: 90, padding: ".9rem 1.4rem", borderRadius: "999px", background: "rgba(13,27,42,.92)", border: "1px solid rgba(201,168,76,.45)", color: "#F0E8D5", font: "500 .82rem Inter, sans-serif", letterSpacing: ".04em", opacity: 0, transition: "all .5s cubic-bezier(.16,1,.3,1)", backdropFilter: "blur(10px)" });
      body.append(t);
    }
    t.textContent = msg;
    requestAnimationFrame(() => { t.style.opacity = 1; t.style.transform = "translateX(-50%)"; });
    clearTimeout(t._h); t._h = setTimeout(() => { t.style.opacity = 0; t.style.transform = "translateX(-50%) translateY(20px)"; }, 3200);
  }
})();
