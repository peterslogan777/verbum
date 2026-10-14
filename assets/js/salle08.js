/* =====================================================================
   VERBUM — Salle 08 · Gutenberg et l'imprimerie (étape E10)
   1. Onglets des étapes  2. Jeu « À vous de composer »  3. Anatomie d'une page
   4. La vague imprimée (carte canvas)  5. Globe des traductions (canvas)
   6. Barre des langues  7. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fmt = new Intl.NumberFormat("fr-FR");

  /* Onglets génériques (clavier compris) */
  const tablist = (tabs) => {
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
  };

  /* 1. Étapes */
  tablist($$(".et-tabs [role=tab]"));

  /* 2. À vous de composer */
  const cp = $(".cp");
  const dataEl = $("#cp-data");
  if (cp && dataEl) {
    const MOTS = JSON.parse(dataEl.textContent);
    const casse = $(".cp-casse", cp), stick = $(".cp-stick", cp), msg = $(".cp-msg", cp);
    const bEnc = $(".cp-encrer", cp), bPre = $(".cp-presser", cp), bAnn = $(".cp-annuler", cp);
    const motEl = $(".cp-mot", cp), frEl = $(".cp-fr", cp), imp = $(".cp-imprime", cp);
    let mot = "", pos = 0;
    const sort = (ch) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "sort"; b.dataset.ch = ch;
      b.setAttribute("aria-label", `Lettre ${ch}`);
      b.innerHTML = `<span aria-hidden="true">${ch}</span>`;
      return b;
    };
    const setEtat = (e) => { cp.dataset.etat = e; };
    const refresh = () => {
      const full = pos === mot.length;
      bEnc.disabled = !(full && cp.dataset.etat === "compose");
      bPre.disabled = cp.dataset.etat !== "encre";
      bAnn.disabled = pos === 0 || cp.dataset.etat === "imprime";
    };
    const load = (i) => {
      const m = MOTS[i];
      mot = m.mot; pos = 0;
      motEl.textContent = mot; frEl.textContent = m.fr;
      imp.textContent = mot;
      stick.innerHTML = "";
      cp.classList.remove("is-press");
      setEtat("compose");
      // lettres nécessaires + quelques intrus, mélangées
      const pool = [...mot];
      const extra = "AEIOUSTRNMCDPQ".split("").filter((c) => !mot.includes(c));
      while (pool.length < Math.max(10, mot.length + 5)) pool.push(extra.splice(Math.floor(Math.random() * extra.length), 1)[0]);
      for (let k = pool.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [pool[k], pool[j]] = [pool[j], pool[k]]; }
      casse.innerHTML = "";
      pool.forEach((ch) => casse.appendChild(sort(ch)));
      msg.innerHTML = "Cliquez sur les lettres de la casse, dans l'ordre du mot. Sur le plomb, elles apparaissent <b>en miroir</b>.";
      refresh();
    };
    casse.addEventListener("click", (ev) => {
      const b = ev.target.closest(".sort");
      if (!b || cp.dataset.etat !== "compose" || pos >= mot.length) return;
      if (b.dataset.ch === mot[pos]) {
        const s = sort(b.dataset.ch); s.tabIndex = -1; s.disabled = true;
        stick.appendChild(s);
        b.style.visibility = "hidden";
        b.dataset.used = "1";
        pos++;
        msg.innerHTML = pos === mot.length
          ? `Ligne composée : <b>${mot.length} caractères</b>. Regardez le composteur : le mot se lit à l'envers. Il faut maintenant <b>encrer</b>.`
          : `Bien. Lettre suivante : <b>${mot[pos]}</b>.`;
      } else {
        b.classList.remove("is-err"); void b.offsetWidth; b.classList.add("is-err");
        msg.innerHTML = `Ce n'est pas la bonne lettre : cherchez le <b>${mot[pos]}</b> (attention, il est retourné).`;
      }
      refresh();
    });
    bAnn.addEventListener("click", () => {
      if (!pos || cp.dataset.etat === "imprime") return;
      const last = stick.lastElementChild; if (last) last.remove();
      pos--;
      const back = $$(".sort[data-used='1']", casse).reverse().find((x) => x.dataset.ch === mot[pos]);
      if (back) { back.style.visibility = ""; delete back.dataset.used; }
      setEtat("compose");
      msg.innerHTML = `Lettre retirée. Lettre suivante : <b>${mot[pos]}</b>.`;
      refresh();
    });
    bEnc.addEventListener("click", () => {
      setEtat("encre");
      msg.innerHTML = "Les balles de cuir ont déposé l'encre grasse sur le plomb. Tirez le barreau !";
      refresh();
    });
    bPre.addEventListener("click", () => {
      cp.classList.add("is-press");
      setTimeout(() => {
        cp.classList.remove("is-press");
        setEtat("imprime");
        msg.innerHTML = `Imprimé ! Sur le papier, le mot se lit enfin à l'endroit. Vous avez placé <b>${mot.length} caractères</b> ; une page de la Bible de Gutenberg en compte près de <b>3 000</b>, et le livre <b>1 282 pages</b>.`;
        refresh();
      }, reduce ? 50 : 650);
    });
    const motsGroup = $(".cp-mots", cp);
    const mbtns = $$("button", motsGroup);
    mbtns.forEach((b, i) => {
      b.tabIndex = i === 0 ? 0 : -1;
      const set = (focus) => { mbtns.forEach((x) => { x.setAttribute("aria-checked", String(x === b)); x.tabIndex = x === b ? 0 : -1; }); if (focus) b.focus(); load(+b.dataset.i); };
      b.addEventListener("click", () => set());
      b.addEventListener("keydown", (ev) => {
        const d = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[ev.key];
        if (d) { ev.preventDefault(); mbtns[(i + d + mbtns.length) % mbtns.length].click(); mbtns[(i + d + mbtns.length) % mbtns.length].focus(); }
      });
    });
    load(0);
  }

  /* 3. Anatomie d'une page */
  const hs = $$(".hs");
  const infos = $$(".fi");
  const showHs = (k) => {
    hs.forEach((h) => h.setAttribute("aria-pressed", String(h.dataset.k === k)));
    infos.forEach((f) => { f.hidden = f.dataset.k !== k; });
  };
  hs.forEach((h) => h.addEventListener("click", () => showHs(h.dataset.k)));
  if (hs.length) showHs(hs[0].dataset.k);

  /* Outils canvas */
  const fit = (cv) => {
    const r = cv.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, Math.round(r.width * dpr)), h = Math.max(1, Math.round(r.height * dpr));
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; }
    return { w, h, dpr };
  };
  const GEO = window.VERBUM_GEO || { europe: [], globe: [] };

  /* 4. La vague imprimée */
  const vq = $(".vq");
  const vqData = $("#vq-data");
  if (vq && vqData) {
    const EV = JSON.parse(vqData.textContent);
    const cv = $(".vq-canvas", vq), ctx = cv.getContext("2d");
    const range = $(".vq-range", vq), out = $(".vq-out", vq), an = $(".vq-an", vq);
    const play = $(".vq-play", vq), nEl = $(".vq-n", vq), lnEl = $(".vq-ln", vq);
    const items = $$(".vq-list li", vq);
    const B = { x0: -11, x1: 29, y0: 37, y1: 61.5 };
    const K = Math.cos((49 * Math.PI) / 180);
    let year = +range.value, born = new Map();
    const proj = (lon, lat, w, h) => {
      const sx = w / ((B.x1 - B.x0) * K), sy = h / (B.y1 - B.y0), s = Math.min(sx, sy);
      const cx = (B.x0 + B.x1) / 2, cy = (B.y0 + B.y1) / 2;
      return [w / 2 + (lon - cx) * K * s, h / 2 - (lat - cy) * s];
    };
    const langs = (l) => l.toLowerCase().split(/ · | et /).map((x) => x.trim());
    const draw = (t) => {
      const { w, h, dpr } = fit(cv);
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = "rgba(201,168,76,.10)"; ctx.strokeStyle = "rgba(201,168,76,.35)"; ctx.lineWidth = 1 * dpr;
      GEO.europe.forEach((ring) => {
        ctx.beginPath();
        ring.forEach(([x, y], i) => { const [px, py] = proj(x, y, w, h); i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); });
        ctx.closePath(); ctx.fill(); ctx.stroke();
      });
      // liens depuis Mayence
      const mz = proj(8.27, 50.0, w, h);
      const vis = EV.filter((e) => e.a <= year);
      vis.forEach((e) => {
        if (e.v === "Mayence") return;
        const [px, py] = proj(e.x, e.y, w, h);
        const age = born.has(e) ? Math.min(1, (t - born.get(e)) / 900) : 1;
        ctx.strokeStyle = `rgba(230,204,122,${0.22 * age})`; ctx.lineWidth = 1 * dpr;
        ctx.beginPath(); ctx.moveTo(mz[0], mz[1]);
        const mx = (mz[0] + px) / 2, my = (mz[1] + py) / 2 - Math.hypot(px - mz[0], py - mz[1]) * 0.18;
        ctx.quadraticCurveTo(mx, my, mz[0] + (px - mz[0]) * age, mz[1] + (py - mz[1]) * age);
        ctx.stroke();
      });
      const seen = new Set();
      vis.forEach((e) => {
        const [px, py] = proj(e.x, e.y, w, h);
        const age = born.has(e) ? Math.min(1, (t - born.get(e)) / 700) : 1;
        const r = (e.v === "Mayence" ? 7 : 5) * dpr;
        if (age < 1) { ctx.beginPath(); ctx.arc(px, py, r + (1 - age) * 26 * dpr, 0, 7); ctx.strokeStyle = `rgba(230,204,122,${1 - age})`; ctx.lineWidth = 2 * dpr; ctx.stroke(); }
        const g = ctx.createRadialGradient(px, py, 0, px, py, r * 3);
        g.addColorStop(0, "rgba(255,230,150,.9)"); g.addColorStop(1, "rgba(201,168,76,0)");
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, r * 3, 0, 7); ctx.fill();
        ctx.fillStyle = e.v === "Mayence" ? "#fff3c4" : "#e6cc7a"; ctx.beginPath(); ctx.arc(px, py, r * 0.55, 0, 7); ctx.fill();
        if (!seen.has(e.v) && w > 420 * dpr) {
          seen.add(e.v);
          ctx.font = `${11 * dpr}px Inter, sans-serif`; ctx.fillStyle = "rgba(240,232,213,.85)";
          const left = ["Delft", "Anvers", "Londres", "Valence", "Alcalá de Henares", "Genève", "Neuchâtel", "Worms"].includes(e.v);
          ctx.textAlign = left ? "right" : "left";
          const dy = { "Worms": 12, "Mayence": -8, "Strasbourg": 10, "Bâle": 4, "Soncino": 10, "Neuchâtel": -6, "Genève": 10 }[e.v] || 4;
          ctx.fillText(e.v, px + (left ? -9 : 9) * dpr, py + dy * dpr);
        }
      });
    };
    let raf = 0;
    const loop = (t) => { draw(t); if ([...born.values()].some((b) => t - b < 1000)) raf = requestAnimationFrame(loop); else raf = 0; };
    const kick = () => { if (!raf) raf = requestAnimationFrame(loop); };
    const setYear = (y, animate) => {
      const prev = year; year = y;
      range.value = y; out.textContent = y; an.textContent = y;
      const now = performance.now();
      EV.forEach((e) => { if (animate && e.a > prev && e.a <= y) born.set(e, now); });
      const vis = EV.filter((e) => e.a <= y);
      nEl.textContent = vis.length;
      lnEl.textContent = new Set(vis.flatMap((e) => langs(e.l))).size;
      items.forEach((li) => {
        const a = +li.dataset.a;
        li.classList.toggle("is-off", a > y);
        li.classList.toggle("is-new", a <= y && a > y - 6);
      });
      kick();
    };
    range.addEventListener("input", () => setYear(+range.value, true));
    let timer = 0;
    const stop = () => { clearInterval(timer); timer = 0; play.classList.remove("is-on"); play.setAttribute("aria-label", "Lancer l'animation"); };
    play.addEventListener("click", () => {
      if (timer) return stop();
      if (year >= 1615) setYear(1450, false);
      play.classList.add("is-on"); play.setAttribute("aria-label", "Mettre l'animation en pause");
      timer = setInterval(() => { if (year >= 1615) return stop(); setYear(year + 1, true); }, reduce ? 30 : 110);
    });
    new ResizeObserver(() => kick()).observe(cv);
    setYear(year, false);
    // lancement automatique à la première apparition
    const io = new IntersectionObserver((en) => {
      if (en[0].isIntersecting) { io.disconnect(); if (!reduce) { setYear(1450, false); play.click(); } }
    }, { threshold: 0.45 });
    io.observe(cv);
  }

  /* 5. Globe des traductions */
  const gcv = $(".gl-canvas");
  if (gcv && GEO.globe.length) {
    const ctx = gcv.getContext("2d");
    const P = GEO.globe.map(([lo, la]) => {
      const a = (lo * Math.PI) / 180, b = (la * Math.PI) / 180;
      return [Math.cos(b) * Math.sin(a), Math.sin(b), Math.cos(b) * Math.cos(a), lo, la];
    });
    // foyers lumineux : Mayence puis quelques régions de traduction active
    const HOT = [[8.27, 50.0], [-1.5, 12.4], [36.8, -1.3], [147.2, -9.4], [-77, -12], [78, 22], [121, 14.6], [-99, 19.4], [31.2, 30], [116, -2], [20, 0], [-60, -3]];
    const HP = HOT.map(([lo, la]) => { const a = (lo * Math.PI) / 180, b = (la * Math.PI) / 180; return [Math.cos(b) * Math.sin(a), Math.sin(b), Math.cos(b) * Math.cos(a)]; });
    let rot = -0.3, tilt = 0.32, vel = reduce ? 0 : 0.0016, drag = null, visible = false;
    const frame = (t) => {
      const { w, h, dpr } = fit(gcv);
      const R = Math.min(w, h) * 0.44, cx = w / 2, cy = h / 2;
      ctx.clearRect(0, 0, w, h);
      // halo
      const halo = ctx.createRadialGradient(cx, cy, R * 0.85, cx, cy, R * 1.25);
      halo.addColorStop(0, "rgba(110,160,200,.25)"); halo.addColorStop(1, "rgba(110,160,200,0)");
      ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(cx, cy, R * 1.25, 0, 7); ctx.fill();
      const sea = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.1, cx, cy, R);
      sea.addColorStop(0, "#14304a"); sea.addColorStop(1, "#060d16");
      ctx.fillStyle = sea; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.fill();
      ctx.strokeStyle = "rgba(201,168,76,.35)"; ctx.lineWidth = 1 * dpr; ctx.stroke();
      const cr = Math.cos(rot), sr = Math.sin(rot), ct = Math.cos(tilt), st = Math.sin(tilt);
      const tr = (x, y, z) => { const x1 = x * cr - z * sr, z1 = x * sr + z * cr; const y2 = y * ct - z1 * st, z2 = y * st + z1 * ct; return [x1, y2, z2]; };
      const ds = Math.max(1.4, R / 140) * dpr;
      for (let i = 0; i < P.length; i++) {
        const [x, y, z] = tr(P[i][0], P[i][1], P[i][2]);
        if (z <= 0) continue;
        ctx.fillStyle = `rgba(230,204,122,${0.25 + z * 0.65})`;
        ctx.fillRect(cx + x * R - ds / 2, cy - y * R - ds / 2, ds, ds);
      }
      HP.forEach((p, i) => {
        const [x, y, z] = tr(p[0], p[1], p[2]);
        if (z <= 0.05) return;
        const px = cx + x * R, py = cy - y * R;
        const pulse = 0.5 + 0.5 * Math.sin(t / 600 + i * 1.7);
        const r = (i === 0 ? 10 : 6 + pulse * 5) * dpr * z;
        const g = ctx.createRadialGradient(px, py, 0, px, py, r * 2.2);
        g.addColorStop(0, i === 0 ? "rgba(255,245,200,.95)" : "rgba(255,225,140,.8)"); g.addColorStop(1, "rgba(255,200,90,0)");
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, r * 2.2, 0, 7); ctx.fill();
      });
      if (!drag) rot += vel;
      if (visible) requestAnimationFrame(frame);
    };
    const io = new IntersectionObserver((en) => {
      const was = visible; visible = en[0].isIntersecting;
      if (visible && !was) requestAnimationFrame(frame);
    });
    io.observe(gcv);
    gcv.addEventListener("pointerdown", (e) => { drag = { x: e.clientX, y: e.clientY, r: rot, t: tilt }; gcv.setPointerCapture(e.pointerId); });
    gcv.addEventListener("pointermove", (e) => {
      if (!drag) return;
      const k = 3 / gcv.getBoundingClientRect().width;
      rot = drag.r + (e.clientX - drag.x) * k;
      tilt = Math.max(-1.1, Math.min(1.1, drag.t + (e.clientY - drag.y) * k));
    });
    const up = () => { drag = null; };
    gcv.addEventListener("pointerup", up); gcv.addEventListener("pointercancel", up);
    requestAnimationFrame(frame);
  }

  /* 6. Barre des langues */
  const bar = $(".lg-bar");
  if (bar) {
    const segs = $$(".lg-seg", bar), leg = $$(".lg-leg li");
    const on = (k) => {
      bar.classList.toggle("has-focus", !!k);
      segs.forEach((s) => s.classList.toggle("is-on", s.dataset.k === k));
      leg.forEach((l) => { l.style.opacity = !k || l.dataset.k === k ? "1" : ".4"; });
    };
    [...segs, ...leg].forEach((el) => {
      el.addEventListener("mouseenter", () => on(el.dataset.k));
      el.addEventListener("mouseleave", () => on(null));
      el.addEventListener("focus", () => on(el.dataset.k));
      el.addEventListener("blur", () => on(null));
      el.addEventListener("click", () => on(el.dataset.k));
    });
  }

  /* 7. Sommaire actif */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
  void fmt;
})();
