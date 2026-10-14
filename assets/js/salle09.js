/* =====================================================================
   VERBUM — Salle 09 · Les Preuves archéologiques (étape E11)
   1. Atlas des découvertes (carte canvas)  2. Lecteurs d'inscriptions
   3. Lampe rasante (Mésha)  4. Fouille (Tel Dan)  5. Réseau d'Éléphantine
   6. Comparateur du déluge  7. Registre filtrable  8. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Groupe de boutons radio (.seg) → callback(valeur) */
  const seg = (root, attr, cb) => {
    if (!root) return;
    const btns = $$("button[role=radio]", root);
    const pick = (b, focus) => {
      btns.forEach((x) => { const on = x === b; x.setAttribute("aria-checked", String(on)); x.tabIndex = on ? 0 : -1; });
      if (focus) b.focus();
      cb(b.dataset[attr]);
    };
    btns.forEach((b, i) => {
      b.tabIndex = b.getAttribute("aria-checked") === "true" ? 0 : -1;
      b.addEventListener("click", () => pick(b));
      b.addEventListener("keydown", (ev) => {
        const d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[ev.key];
        if (d) { ev.preventDefault(); pick(btns[(i + d + btns.length) % btns.length], true); }
      });
    });
  };

  /* ---------- 1. Atlas ---------- */
  const atCanvas = $(".at-canvas");
  const atData = $("#at-data");
  if (atCanvas && atData && window.VERBUM_GEO09) {
    const sites = JSON.parse(atData.textContent);
    const geo = window.VERBUM_GEO09;
    const ctx = atCanvas.getContext("2d");
    const B = { lo0: 21.5, lo1: 50, la0: 22.5, la1: 39.8 };
    const K = Math.cos(31 * Math.PI / 180);
    let W = 0, H = 0, dpr = 1, s = 1, ox = 0, oy = 0, sel = null, t0 = performance.now(), visible = false;
    const proj = (lo, la) => [ox + (lo - B.lo0) * K * s, oy + (B.la1 - la) * s];
    const resize = () => {
      const r = atCanvas.getBoundingClientRect();
      dpr = Math.min(2, window.devicePixelRatio || 1);
      W = Math.round(r.width * dpr); H = Math.round(r.height * dpr);
      atCanvas.width = W; atCanvas.height = H;
      const sx = W / ((B.lo1 - B.lo0) * K), sy = H / (B.la1 - B.la0);
      s = Math.min(sx, sy);
      ox = (W - (B.lo1 - B.lo0) * K * s) / 2; oy = (H - (B.la1 - B.la0) * s) / 2;
    };
    const LABELS_LEFT = new Set(["cesaree", "dan", "jerusalem", "elephantine"]);
    const draw = (now) => {
      const t = (now - t0) / 1000;
      ctx.clearRect(0, 0, W, H);
      // terres
      ctx.fillStyle = "#2a2a2c"; ctx.strokeStyle = "rgba(201,168,76,.35)"; ctx.lineWidth = 1 * dpr;
      geo.land.forEach((ring) => {
        ctx.beginPath();
        ring.forEach(([lo, la], i) => { const [x, y] = proj(lo, la); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
        ctx.closePath();
        const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#26241f"); g.addColorStop(1, "#2f2a20");
        ctx.fillStyle = g; ctx.fill(); ctx.stroke();
      });
      // fleuves
      ctx.strokeStyle = "rgba(110,160,200,.75)"; ctx.lineWidth = 1.6 * dpr; ctx.lineJoin = "round"; ctx.lineCap = "round";
      Object.values(geo.rivers).forEach((pts) => {
        ctx.beginPath(); pts.forEach(([lo, la], i) => { const [x, y] = proj(lo, la); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke();
      });
      // noms de régions
      ctx.font = `${11 * dpr}px Inter, sans-serif`; ctx.fillStyle = "rgba(201,168,76,.45)"; ctx.textAlign = "center";
      [["ÉGYPTE", 30.2, 26.5], ["ASSYRIE", 43.6, 37.3], ["BABYLONIE", 46.2, 30.9], ["MOAB", 37.0, 30.4], ["Mer Méditerranée", 28.5, 33.6]].forEach(([n, lo, la]) => {
        const [x, y] = proj(lo, la); ctx.fillText(n, x, y);
      });
      // sites
      sites.forEach((st, i) => {
        const [x, y] = proj(st.lon, st.lat);
        const on = sel === st.k;
        const pulse = reduce ? 0 : (Math.sin(t * 2 + i) + 1) / 2;
        const r = (on ? 9 : 5) * dpr;
        const halo = ctx.createRadialGradient(x, y, 0, x, y, r * (3 + pulse * (on ? 2.5 : 1)));
        halo.addColorStop(0, on ? "rgba(255,226,150,.85)" : "rgba(230,204,122,.55)"); halo.addColorStop(1, "rgba(230,204,122,0)");
        ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(x, y, r * (3 + pulse * (on ? 2.5 : 1)), 0, 7); ctx.fill();
        ctx.fillStyle = on ? "#fff4d0" : "#e6cc7a"; ctx.beginPath(); ctx.arc(x, y, r * .45, 0, 7); ctx.fill();
        if (W > 520 * dpr || on) {
          ctx.font = `${(on ? 13 : 11) * dpr}px Inter, sans-serif`;
          ctx.fillStyle = on ? "#fff4d0" : "rgba(240,232,213,.85)";
          const left = LABELS_LEFT.has(st.k);
          ctx.textAlign = left ? "right" : "left";
          const dy = st.k === "ninive" ? -8 : st.k === "nimrud" ? 12 : st.k === "jerusalem" ? 10 : st.k === "cesaree" ? -2 : 4;
          ctx.fillText(on ? `${st.n} · ${st.y}` : st.n, x + (left ? -12 : 12) * dpr, y + dy * dpr);
        }
      });
      if (visible && !reduce) requestAnimationFrame(draw);
    };
    const select = (k) => {
      sel = sel === k ? null : k;
      $$(".at-site").forEach((li) => {
        const on = li.dataset.k === sel;
        $(".at-btn", li).setAttribute("aria-pressed", String(on));
        $(".at-info", li).hidden = !on;
      });
      if (reduce || !visible) draw(performance.now());
    };
    $$(".at-site").forEach((li) => $(".at-btn", li).addEventListener("click", () => select(li.dataset.k)));
    atCanvas.addEventListener("click", (ev) => {
      const r = atCanvas.getBoundingClientRect();
      const mx = (ev.clientX - r.left) * dpr, my = (ev.clientY - r.top) * dpr;
      let best = null, bd = 22 * dpr;
      sites.forEach((st) => { const [x, y] = proj(st.lon, st.lat); const d = Math.hypot(x - mx, y - my); if (d < bd) { bd = d; best = st.k; } });
      if (best) select(best);
    });
    resize();
    new ResizeObserver(() => { resize(); draw(performance.now()); }).observe(atCanvas);
    new IntersectionObserver((en) => {
      const was = visible; visible = en[0].isIntersecting;
      if (visible && !was) requestAnimationFrame(draw);
    }).observe(atCanvas);
    draw(performance.now());
  }

  /* ---------- 2. Lecteurs d'inscriptions ---------- */
  $$(".insc").forEach((box) => {
    const words = $$(".w", box);
    const sel = $(".in-sel", box), hint = $(".in-hint", box);
    words.forEach((w) => w.addEventListener("click", () => {
      const on = w.getAttribute("aria-pressed") !== "true";
      words.forEach((x) => x.setAttribute("aria-pressed", "false"));
      if (!on) { sel.hidden = true; hint.hidden = false; return; }
      w.setAttribute("aria-pressed", "true");
      const paleoOn = box.classList.contains("is-paleo") && $(".w-p", w);
      $(".in-w", sel).textContent = (paleoOn ? $(".w-p", w) : $(".w-c", w)).textContent;
      $(".in-w", sel).style.fontFamily = paleoOn ? "var(--f-paleo)" : "";
      $(".in-tr", sel).textContent = w.dataset.tr ? `(${w.dataset.tr})` : "";
      $(".in-fr", sel).textContent = w.dataset.fr;
      $(".in-note", sel).textContent = w.dataset.note || "";
      sel.hidden = false; hint.hidden = true;
    }));
    words.forEach((w) => w.setAttribute("aria-pressed", "false"));
    seg($(".in-seg", box), "s", (v) => box.classList.toggle("is-paleo", v === "p"));
  });

  /* ---------- 3. Lampe rasante ---------- */
  const lampe = $(".lampe-in");
  if (lampe) {
    let used = false, raf = 0, t = 0, vis = false;
    const set = (x, y) => { lampe.style.setProperty("--x", `${x}%`); lampe.style.setProperty("--y", `${y}%`); };
    lampe.addEventListener("pointermove", (ev) => {
      const r = lampe.getBoundingClientRect();
      set(((ev.clientX - r.left) / r.width) * 100, ((ev.clientY - r.top) / r.height) * 100);
      if (!used) { used = true; lampe.classList.add("is-used"); }
    });
    const idle = () => {
      if (used || !vis) { raf = 0; return; }
      t += 0.012;
      set(50 + Math.sin(t) * 9, 42 + Math.sin(t * 1.7) * 26);
      raf = requestAnimationFrame(idle);
    };
    if (!reduce) new IntersectionObserver((en) => { vis = en[0].isIntersecting; if (vis && !raf) raf = requestAnimationFrame(idle); }).observe(lampe);
  }

  /* ---------- 4. Fouille ---------- */
  const fouille = $(".fouille");
  if (fouille) {
    const cv = $(".fouille-c", fouille), ctx = cv.getContext("2d", { willReadFrequently: true });
    const pc = $(".fouille-pc", fouille), ok = $(".fouille-ok", fouille), msg = $(".fouille-msg", fouille);
    let W = 0, H = 0, done = false, down = false, last = null, moves = 0;
    const soil = () => {
      const r = cv.getBoundingClientRect();
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      W = cv.width = Math.round(r.width * dpr); H = cv.height = Math.round(r.height * dpr);
      ctx.globalCompositeOperation = "source-over";
      const g = ctx.createLinearGradient(0, 0, W, H);
      g.addColorStop(0, "#8a6b49"); g.addColorStop(.5, "#a2825c"); g.addColorStop(1, "#6f5238");
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      // grains, cailloux et mottes (pseudo-aléatoire stable)
      let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
      for (let i = 0; i < 2600; i++) {
        const x = rnd() * W, y = rnd() * H, rr = rnd() * 2.2 * dpr + .4;
        ctx.fillStyle = `rgba(${rnd() < .5 ? "60,42,26" : "205,180,140"},${.25 + rnd() * .4})`;
        ctx.beginPath(); ctx.arc(x, y, rr, 0, 7); ctx.fill();
      }
      for (let i = 0; i < 70; i++) {
        const x = rnd() * W, y = rnd() * H, rr = (4 + rnd() * 14) * dpr;
        const gg = ctx.createRadialGradient(x - rr * .3, y - rr * .3, 1, x, y, rr);
        gg.addColorStop(0, "rgba(220,200,165,.9)"); gg.addColorStop(1, "rgba(110,85,60,.9)");
        ctx.fillStyle = gg; ctx.beginPath(); ctx.ellipse(x, y, rr, rr * (.6 + rnd() * .4), rnd() * 3, 0, 7); ctx.fill();
      }
      ctx.globalCompositeOperation = "destination-out";
      pc.textContent = "0 %";
    };
    const brush = (x, y) => {
      const r = Math.max(W, H) * 0.055;
      const g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, "rgba(0,0,0,1)"); g.addColorStop(.6, "rgba(0,0,0,.55)"); g.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
    };
    const progress = () => {
      const d = ctx.getImageData(0, 0, W, H).data;
      let clear = 0, n = 0;
      for (let i = 3; i < d.length; i += 4 * 37) { n++; if (d[i] < 90) clear++; }
      return clear / n;
    };
    const finish = () => {
      done = true; fouille.classList.add("is-done"); ok.hidden = false;
      msg.textContent = "La pierre est dégagée. Lisez maintenant les lignes 7 à 9 ci-dessous.";
      pc.textContent = "100 %";
      setTimeout(() => { ok.hidden = true; }, 6000);
      $$('.insc[data-insc="dan"] .w').forEach((w) => { if (w.dataset.tr === "bytdwd") w.classList.add("is-key"); });
    };
    const pos = (ev) => { const r = cv.getBoundingClientRect(); return [(ev.clientX - r.left) * W / r.width, (ev.clientY - r.top) * H / r.height]; };
    cv.addEventListener("pointerdown", (ev) => { if (done) return; down = true; cv.setPointerCapture(ev.pointerId); last = pos(ev); brush(...last); });
    cv.addEventListener("pointermove", (ev) => {
      if (done || (!down && ev.pointerType !== "mouse")) return;
      if (!down && ev.pointerType === "mouse" && ev.buttons === 0) { /* survol souris : brosse légère */ }
      const p = pos(ev);
      if (last) { const steps = Math.ceil(Math.hypot(p[0] - last[0], p[1] - last[1]) / 10); for (let i = 1; i <= steps; i++) brush(last[0] + (p[0] - last[0]) * i / steps, last[1] + (p[1] - last[1]) * i / steps); }
      else brush(...p);
      last = p;
      if (++moves % 12 === 0) { const v = progress(); pc.textContent = `${Math.min(99, Math.round(v * 100 / 0.6))} %`; if (v > 0.6) finish(); }
    });
    const up = () => { down = false; last = null; };
    cv.addEventListener("pointerup", up); cv.addEventListener("pointercancel", up);
    cv.addEventListener("pointerleave", () => { last = null; });
    $(".fouille-r", fouille).addEventListener("click", () => {
      done = false; fouille.classList.remove("is-done"); ok.hidden = true;
      msg.textContent = "À vous de fouiller : passez la brosse sur la terre pour dégager la pierre.";
      soil();
    });
    const ro = new ResizeObserver(() => { if (!done) soil(); });
    ro.observe(cv);
  }

  /* ---------- 5. Réseau d'Éléphantine ---------- */
  const net = $(".el-net");
  if (net) {
    const nodes = $$(".el-n", net), lines = $$(".el-lines line", net);
    nodes.forEach((n) => n.addEventListener("click", () => {
      const on = n.getAttribute("aria-pressed") !== "true";
      nodes.forEach((x) => x.setAttribute("aria-pressed", "false"));
      lines.forEach((l) => l.classList.remove("is-on"));
      if (!on) return;
      n.setAttribute("aria-pressed", "true");
      if (n.dataset.k === "papyrus") lines.forEach((l) => l.classList.add("is-on"));
      else lines.forEach((l) => l.classList.toggle("is-on", l.dataset.k === n.dataset.k));
    }));
  }

  /* ---------- 6. Comparateur du déluge ---------- */
  const dl = $(".dl-tab");
  seg($(".dl-seg"), "f", (v) => { if (dl) dl.dataset.f = v; });

  /* ---------- 7. Registre ---------- */
  const cards = $$(".rg-c");
  const count = $(".rg-count b");
  seg($(".rg-seg"), "f", (v) => {
    let n = 0;
    cards.forEach((c) => {
      const show = v === "tout" || c.dataset.cats.split(" ").includes(v);
      c.hidden = !show;
      if (show) { n++; c.classList.remove("is-in"); void c.offsetWidth; c.classList.add("is-in"); }
    });
    if (count) count.textContent = n;
  });

  /* ---------- 8. Sommaire actif ---------- */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
