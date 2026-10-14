/* =====================================================================
   VERBUM — Salle 10 · Le Livre indestructible (étape E12)
   1. Le bûcher (canvas : page de 1526 consumée, braises)  2. Cartes recto/verso
   3. Routes clandestines (carte canvas)  4. Vrai ou légende ?  5. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 1. Le bûcher ---------- */
  const cv = $(".bu-canvas"), fx = $(".bu-fx"), bd = $("#bu-data");
  if (cv && fx && bd) {
    const data = JSON.parse(bd.textContent);
    const ctx = cv.getContext("2d", { willReadFrequently: true });
    const fctx = fx.getContext("2d");
    const btnGo = $(".bu-go"), btnReset = $(".bu-reset"), msg = $(".bu-msg");
    const MSG0 = msg ? msg.textContent : "";
    let W = 0, H = 0, base = null, field = null, out = null, T = -0.1, burning = false, done = false, raf = 0, last = 0;
    let embers = [], burnStart = 0;

    // bruit de valeur (plusieurs octaves), graine fixe
    const hash = (x, y) => { let h = (x * 374761393 + y * 668265263) ^ 0x5bd1e995; h = (h ^ (h >>> 13)) * 1274126177; return ((h ^ (h >>> 16)) >>> 0) / 4294967295; };
    const smooth = (t) => t * t * (3 - 2 * t);
    const vnoise = (x, y) => {
      const xi = Math.floor(x), yi = Math.floor(y), xf = smooth(x - xi), yf = smooth(y - yi);
      const a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
      return a + (b - a) * xf + (c - a) * yf + (a - b - c + d) * xf * yf;
    };
    const fbm = (x, y) => vnoise(x, y) * .5 + vnoise(x * 2.1, y * 2.1) * .27 + vnoise(x * 4.3, y * 4.3) * .15 + vnoise(x * 9.1, y * 9.1) * .08;

    const renderPage = () => {
      const r = cv.getBoundingClientRect();
      const dpr = Math.min(1.5, window.devicePixelRatio || 1);
      const scale = Math.min(dpr, 700 / Math.max(1, r.width));
      W = Math.max(2, Math.round(r.width * scale)); H = Math.max(2, Math.round(r.height * scale));
      cv.width = W; cv.height = H; fx.width = W; fx.height = H;
      const off = document.createElement("canvas"); off.width = W; off.height = H;
      const c = off.getContext("2d");
      // vélin
      const g = c.createRadialGradient(W * .4, H * .3, W * .1, W * .5, H * .5, W * .9);
      g.addColorStop(0, "#f1e2bf"); g.addColorStop(.7, "#dcc391"); g.addColorStop(1, "#b8955c");
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      for (let i = 0; i < 900; i++) { c.fillStyle = `rgba(110,75,35,${Math.random() * .06})`; c.beginPath(); c.arc(Math.random() * W, Math.random() * H, Math.random() * 2.2 * scale, 0, 7); c.fill(); }
      const u = W / 100;
      const mx = 11 * u, tw = W - 2 * mx;
      c.fillStyle = "#2a1c10"; c.textBaseline = "alphabetic";
      // en-tête
      c.font = `500 ${3.2 * u}px "EB Garamond", Georgia, serif`; c.textAlign = "center";
      c.fillText("S. Jhon.", W / 2, 10 * u);
      c.font = `italic ${4.4 * u}px "Cormorant Garamond", Georgia, serif`;
      c.fillText(data.titre, W / 2, 17 * u, tw);
      c.strokeStyle = "rgba(60,35,15,.55)"; c.lineWidth = Math.max(1, .25 * u);
      c.beginPath(); c.moveTo(mx, 20.5 * u); c.lineTo(W - mx, 20.5 * u); c.stroke();
      // lettrine
      const fs = 4.15 * u, lh = fs * 1.42;
      c.font = `600 ${fs * 3.1}px "Cormorant Garamond", Georgia, serif`; c.textAlign = "left"; c.fillStyle = "#8b1a1a";
      c.fillText("I", mx, 24 * u + fs * 2.45);
      c.fillStyle = "#2a1c10"; c.font = `${fs}px "EB Garamond", Georgia, serif`;
      const indent = fs * 1.7;
      const y = 24 * u + fs;
      // 2 premières lignes en retrait (lettrine), puis pleine largeur
      const words = data.texte.slice(1).split(" ");
      let rest = words.slice(), lines = [];
      for (let k = 0; rest.length && y + lines.length * lh < H - 14 * u; k++) {
        const maxW = k < 2 ? tw - indent : tw; let line = "";
        while (rest.length) { const t = line ? line + " " + rest[0] : rest[0]; if (c.measureText(t).width > maxW && line) break; line = t; rest.shift(); }
        lines.push([line, k < 2 ? indent : 0, maxW, rest.length > 0]);
      }
      lines.forEach(([line, ind, maxW, justify], k) => {
        const yy = y + k * lh;
        const ws = line.split(" ");
        if (justify && ws.length > 1) {
          const wsum = ws.reduce((a, w) => a + c.measureText(w).width, 0);
          const gap = (maxW - wsum) / (ws.length - 1);
          let x = mx + ind; ws.forEach((w) => { c.fillText(w, x, yy); x += c.measureText(w).width + gap; });
        } else c.fillText(line, mx + ind, yy);
      });
      // pied de page
      c.font = `italic ${2.9 * u}px "Cormorant Garamond", Georgia, serif`; c.textAlign = "center"; c.fillStyle = "rgba(42,28,16,.8)";
      c.fillText(data.pied, W / 2, H - 6 * u);
      // bords assombris
      const v = c.createRadialGradient(W / 2, H / 2, Math.min(W, H) * .35, W / 2, H / 2, Math.max(W, H) * .75);
      v.addColorStop(0, "rgba(80,50,20,0)"); v.addColorStop(1, "rgba(80,50,20,.45)");
      c.fillStyle = v; c.fillRect(0, 0, W, H);
      base = c.getImageData(0, 0, W, H);
      out = ctx.createImageData(W, H);
      // champ de combustion : bruit + distance au foyer (coin inférieur gauche)
      field = new Float32Array(W * H);
      const fx0 = W * .18, fy0 = H * 1.02, dmax = Math.hypot(W, H);
      for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
        const n = fbm(i / W * 6, j / W * 6);
        const d = Math.hypot(i - fx0, j - fy0) / dmax;
        field[j * W + i] = d * .62 + n * .48;
      }
      // normalisation 0..1
      let lo = Infinity, hi = -Infinity; for (let k = 0; k < field.length; k++) { if (field[k] < lo) lo = field[k]; if (field[k] > hi) hi = field[k]; }
      for (let k = 0; k < field.length; k++) field[k] = (field[k] - lo) / (hi - lo);
      paint();
    };

    const paint = () => {
      if (!base) return;
      const b = base.data, o = out.data, n = field.length;
      const E1 = .012, E2 = .045, E3 = .11;
      for (let k = 0; k < n; k++) {
        const f = field[k] - T, p = k * 4;
        if (f < 0) { o[p + 3] = 0; continue; }
        let r = b[p], g = b[p + 1], bl = b[p + 2], a = 255;
        if (f < E3) { // roussi
          const s = 1 - f / E3; const m = 1 - s * .55;
          r *= m; g *= m * .92; bl *= m * .8;
        }
        if (f < E2) { // carbonisé
          const s = 1 - f / E2; r = r * (1 - s) + 18 * s; g = g * (1 - s) + 10 * s; bl = bl * (1 - s) + 6 * s;
        }
        if (f < E1) { // braise
          const s = 1 - f / E1; const fl = .75 + Math.random() * .25;
          r = r + (255 - r) * s * fl; g = g + (150 - g) * s * s * fl; bl = bl * (1 - s);
          a = 255;
        }
        o[p] = r; o[p + 1] = g; o[p + 2] = bl; o[p + 3] = a;
      }
      ctx.putImageData(out, 0, 0);
    };

    const spawn = () => {
      for (let tries = 0; tries < 40; tries++) {
        const i = (Math.random() * W) | 0, j = (Math.random() * H) | 0, f = field[j * W + i] - T;
        if (f >= 0 && f < .02) {
          embers.push({ x: i, y: j, vx: (Math.random() - .5) * .6, vy: -(.6 + Math.random() * 1.6), life: 1, r: .8 + Math.random() * 2.2 });
          return;
        }
      }
    };
    const drawFx = (dt) => {
      fctx.clearRect(0, 0, W, H);
      fctx.globalCompositeOperation = "lighter";
      embers.forEach((p) => {
        p.x += p.vx * dt * 60 + Math.sin(p.y * .05) * .3; p.y += p.vy * dt * 60; p.life -= dt * (.45 + Math.random() * .3);
        const a = Math.max(0, p.life);
        const gr = fctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4);
        gr.addColorStop(0, `rgba(255,214,140,${a})`); gr.addColorStop(.4, `rgba(255,120,40,${a * .6})`); gr.addColorStop(1, "rgba(255,80,20,0)");
        fctx.fillStyle = gr; fctx.beginPath(); fctx.arc(p.x, p.y, p.r * 4, 0, 7); fctx.fill();
      });
      embers = embers.filter((p) => p.life > 0 && p.y > -10);
      fctx.globalCompositeOperation = "source-over";
    };

    const tick = (now) => {
      const dt = Math.min(.05, (now - last) / 1000 || .016); last = now;
      if (burning) {
        T = -0.1 + (now - burnStart) / 5600;
        for (let k = 0; k < 6; k++) spawn();
        if (T > 1.02) {
          burning = false; done = true; T = 1.2;
          if (msg) msg.textContent = "La page est en cendres… mais le texte a survécu : trois ans plus tard, il est imprimé par ordre du roi.";
          if (btnReset) btnReset.hidden = false;
        }
        paint();
      }
      drawFx(dt);
      if (burning || embers.length) raf = requestAnimationFrame(tick); else raf = 0;
    };

    const go = () => {
      if (burning || done) return;
      if (msg) msg.textContent = "Le feu prend…";
      if (btnGo) btnGo.disabled = true;
      if (reduce) {
        T = 1.2; done = true; paint();
        if (msg) msg.textContent = "La page est en cendres… mais le texte a survécu : trois ans plus tard, il est imprimé par ordre du roi.";
        if (btnReset) btnReset.hidden = false;
        return;
      }
      burning = true; last = burnStart = performance.now();
      if (!raf) raf = requestAnimationFrame(tick);
    };
    const reset = () => {
      burning = false; done = false; T = -0.1; embers = []; fctx.clearRect(0, 0, W, H);
      paint();
      if (btnGo) btnGo.disabled = false;
      if (btnReset) btnReset.hidden = true;
      if (msg) msg.textContent = MSG0;
    };
    btnGo?.addEventListener("click", go);
    btnReset?.addEventListener("click", reset);

    const init = () => renderPage();
    (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => {
      init();
      let lw = cv.getBoundingClientRect().width;
      new ResizeObserver(() => {
        const w = cv.getBoundingClientRect().width;
        if (Math.abs(w - lw) < 2) return; lw = w;
        const keepT = T; renderPage(); T = keepT; paint();
      }).observe(cv);
    });
  }

  /* ---------- 2. Cartes recto / verso (clic uniquement) ---------- */
  $$(".it-card").forEach((b) => b.addEventListener("click", () => {
    b.setAttribute("aria-pressed", String(b.getAttribute("aria-pressed") !== "true"));
  }));

  /* ---------- 3. Routes clandestines ---------- */
  const rc = $(".rt-canvas"), rd = $("#rt-data");
  if (rc && rd && window.VERBUM_GEO10) {
    const routes = JSON.parse(rd.textContent);
    const geo = window.VERBUM_GEO10;
    const ctx = rc.getContext("2d");
    const B = { lo0: -16, lo1: 128, la0: -28, la1: 63 };
    const K = Math.cos(25 * Math.PI / 180);
    let W = 0, H = 0, dpr = 1, s = 1, ox = 0, oy = 0, sel = null, selT = 0, t0 = performance.now(), visible = false;
    const proj = (lo, la) => [ox + (lo - B.lo0) * K * s, oy + (B.la1 - la) * s];
    const resize = () => {
      const r = rc.getBoundingClientRect();
      dpr = Math.min(2, window.devicePixelRatio || 1);
      W = Math.round(r.width * dpr); H = Math.round(r.height * dpr);
      rc.width = W; rc.height = H;
      s = Math.min(W / ((B.lo1 - B.lo0) * K), H / (B.la1 - B.la0));
      ox = (W - (B.lo1 - B.lo0) * K * s) / 2; oy = (H - (B.la1 - B.la0) * s) / 2;
    };
    const polyLen = (pts) => { let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return L; };
    const draw = (now) => {
      const t = (now - t0) / 1000;
      ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = 1 * dpr; ctx.strokeStyle = "rgba(201,168,76,.3)";
      const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#26241f"); g.addColorStop(1, "#2f2a20");
      geo.land.forEach((ring) => {
        ctx.beginPath();
        ring.forEach(([lo, la], i) => { const [x, y] = proj(lo, la); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
        ctx.closePath(); ctx.fillStyle = g; ctx.fill(); ctx.stroke();
      });
      ctx.font = `${10 * dpr}px Inter, sans-serif`; ctx.fillStyle = "rgba(201,168,76,.4)"; ctx.textAlign = "center";
      [["EUROPE", 30, 61], ["AFRIQUE", 18, 8], ["ASIE", 90, 50], ["Océan Indien", 75, -12], ["CHINE", 105, 33]].forEach(([n, lo, la]) => {
        const [x, y] = proj(lo, la); ctx.fillText(n, x, y);
      });
      const selP = sel ? Math.min(1, (now - selT) / 1400) : 0;
      routes.forEach((rt, i) => {
        const on = sel === rt.k;
        const pts = rt.pts.map(([lo, la]) => proj(lo, la));
        const pulse = reduce ? .5 : (Math.sin(t * 2 + i) + 1) / 2;
        if (pts.length > 1) {
          ctx.lineCap = "round"; ctx.lineJoin = "round";
          // tracé discret
          ctx.setLineDash([4 * dpr, 5 * dpr]); ctx.strokeStyle = on ? "rgba(255,177,92,.25)" : "rgba(255,177,92,.45)"; ctx.lineWidth = 1.4 * dpr;
          ctx.beginPath(); pts.forEach(([x, y], k) => k ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke(); ctx.setLineDash([]);
          if (on) { // tracé animé
            const L = polyLen(pts) * (reduce ? 1 : selP); let acc = 0;
            ctx.strokeStyle = "#ffcf8a"; ctx.lineWidth = 2.6 * dpr; ctx.shadowColor = "rgba(255,160,60,.9)"; ctx.shadowBlur = 10 * dpr;
            ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
            let head = pts[0];
            for (let k = 1; k < pts.length; k++) {
              const seg = Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]);
              if (acc + seg >= L) { const f = (L - acc) / seg; head = [pts[k - 1][0] + (pts[k][0] - pts[k - 1][0]) * f, pts[k - 1][1] + (pts[k][1] - pts[k - 1][1]) * f]; ctx.lineTo(head[0], head[1]); break; }
              acc += seg; ctx.lineTo(pts[k][0], pts[k][1]); head = pts[k];
            }
            ctx.stroke(); ctx.shadowBlur = 0;
            ctx.fillStyle = "#fff4d0"; ctx.beginPath(); ctx.arc(head[0], head[1], 3.2 * dpr, 0, 7); ctx.fill();
          }
        }
        // points de départ et d'arrivée
        [pts[0], pts[pts.length - 1]].forEach(([x, y], k) => {
          if (k === 1 && pts.length === 1) return;
          const r = (on ? 6 : 3.6) * dpr;
          const R = r * (2.6 + pulse * (on ? 2 : .8));
          const h = ctx.createRadialGradient(x, y, 0, x, y, R);
          h.addColorStop(0, on ? "rgba(255,210,140,.85)" : "rgba(255,170,90,.5)"); h.addColorStop(1, "rgba(255,170,90,0)");
          ctx.fillStyle = h; ctx.beginPath(); ctx.arc(x, y, R, 0, 7); ctx.fill();
          ctx.fillStyle = on ? "#fff4d0" : "#ffb15c"; ctx.beginPath(); ctx.arc(x, y, r * .5, 0, 7); ctx.fill();
        });
        if (on) {
          const [x, y] = pts[pts.length - 1];
          ctx.font = `${12 * dpr}px Inter, sans-serif`; ctx.fillStyle = "#fff4d0";
          const right = x > W * .7; ctx.textAlign = right ? "right" : "left";
          ctx.fillText(rt.y, x + (right ? -12 : 12) * dpr, y - 8 * dpr);
        }
      });
      if (visible && !reduce) requestAnimationFrame(draw);
    };
    const select = (k) => {
      sel = sel === k ? null : k; selT = performance.now();
      $$(".rt-item").forEach((li) => {
        const on = li.dataset.k === sel;
        $(".rt-btn", li).setAttribute("aria-pressed", String(on));
        $(".rt-info", li).hidden = !on;
      });
      if (reduce || !visible) draw(performance.now());
    };
    $$(".rt-item").forEach((li) => $(".rt-btn", li).addEventListener("click", () => select(li.dataset.k)));
    rc.addEventListener("click", (ev) => {
      const r = rc.getBoundingClientRect();
      const mx = (ev.clientX - r.left) * dpr, my = (ev.clientY - r.top) * dpr;
      let best = null, bdist = 22 * dpr;
      routes.forEach((rt) => rt.pts.forEach(([lo, la]) => { const [x, y] = proj(lo, la); const d = Math.hypot(x - mx, y - my); if (d < bdist) { bdist = d; best = rt.k; } }));
      if (best) select(best);
    });
    resize();
    new ResizeObserver(() => { resize(); draw(performance.now()); }).observe(rc);
    new IntersectionObserver((en) => {
      const was = visible; visible = en[0].isIntersecting;
      if (visible && !was) requestAnimationFrame(draw);
    }).observe(rc);
    draw(performance.now());
  }

  /* ---------- 4. Vrai ou légende ? ---------- */
  const qs = $$(".vl-q");
  if (qs.length) {
    let score = 0, answered = 0;
    const sEl = $(".vl-s"), dEl = $(".vl-done");
    qs.forEach((q) => {
      const btns = $$(".vl-b", q);
      btns.forEach((b) => b.addEventListener("click", () => {
        if (q.dataset.done) return;
        q.dataset.done = "1"; answered++;
        const ok = b.dataset.a === q.dataset.ok;
        if (ok) score++;
        btns.forEach((x) => { x.disabled = true; x.classList.toggle("is-pick", x === b); });
        q.classList.add(ok ? "is-ok" : "is-ko");
        $(".vl-you", q).textContent = ok ? "Bonne réponse" : "Ce n'était pas la bonne réponse";
        $(".vl-r", q).hidden = false;
        if (sEl) sEl.textContent = score;
        if (dEl && answered === qs.length) dEl.textContent = score === qs.length ? "· Sans faute !" : "· Terminé";
      }));
    });
  }

  /* ---------- 5. Sommaire actif ---------- */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
