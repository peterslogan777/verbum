/* =====================================================================
   VERBUM — Salle 03 · Les Manuscrits de la mer Morte (étape E05)
   1. Visualiseur 3D WebGL du rouleau (Ésaïe 53)
   2. Plan des grottes  3. Comparateur  4. Barres des livres  5. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------
     1. Rouleau 3D
     Une bande de parchemin (longueur L, hauteur 1) : la partie centrale
     est à plat, les deux extrémités s'enroulent en spirale autour de deux
     cylindres. Le décalage uOffV fait défiler le texte sous les yeux.
     NB : uniformes du vertex shader et du fragment shader nommés
     différemment (précisions distinctes).
     ------------------------------------------------------------------ */
  const v3d = $(".v3d");
  if (v3d) initViewer(v3d);

  function initViewer(root) {
    const canvas = $(".v3d-canvas", root), stage = $(".v3d-stage", root);
    const range = $(".v3d-range", root), hint = $(".v3d-hint", root);
    const data = JSON.parse($("#v3d-data").textContent);
    const cols = data.colonnes, fr = data.fr;
    const uStart = cols[0].x_centre, uEnd = cols[cols.length - 1].x_centre;
    const L = 4, HW = 0.56, R = 0.15;
    let u = uStart, target = uStart, yaw = 0, curCol = -1, gl = null, prog, tex, ready = false, inView = false, raf = 0, t0 = performance.now();

    // Panneau d'information
    const elCol = $(".v3d-col", root), elN = $(".v3d-ncol", root), elVV = $(".v3d-vv", root), elFr = $(".v3d-fr", root);
    elN.textContent = cols.length;
    function info() {
      let best = 0, d = 9;
      cols.forEach((c, i) => { const dd = Math.abs(c.x_centre - u); if (dd < d) { d = dd; best = i; } });
      if (best === curCol) return;
      curCol = best;
      const c = cols[best];
      elCol.textContent = c.col;
      elVV.textContent = `Ésaïe 53:${c.de}-${c.a}`;
      let h = "";
      for (let v = c.de; v <= c.a; v++) h += `<p><b>${v}</b>${fr[v - 1]}</p>`;
      elFr.innerHTML = h;
    }
    const syncRange = () => { range.value = Math.round((uStart - target) / (uStart - uEnd) * 1000); };
    const clamp = (x) => Math.min(uStart + 0.03, Math.max(uEnd - 0.03, x));
    const hideHint = () => hint && hint.classList.add("is-hidden");

    range.addEventListener("input", () => { target = uStart - (range.value / 1000) * (uStart - uEnd); hideHint(); kick(); });
    $$(".v3d-btn", root).forEach((b) => b.addEventListener("click", () => {
      const dir = +b.dataset.dir; // -1 : colonne suivante (texte plus à gauche)
      let i = curCol < 0 ? 0 : curCol;
      i = Math.min(cols.length - 1, Math.max(0, i - dir));
      target = cols[i].x_centre; syncRange(); hideHint(); kick();
    }));

    // Glisser
    let drag = null;
    canvas.addEventListener("pointerdown", (ev) => { drag = { x: ev.clientX, u: target }; canvas.setPointerCapture(ev.pointerId); canvas.classList.add("is-drag"); });
    canvas.addEventListener("pointermove", (ev) => {
      if (!drag) return;
      const dx = ev.clientX - drag.x;
      target = clamp(drag.u - dx / canvas.clientWidth * 0.36);
      syncRange(); hideHint(); kick();
    });
    const end = () => {
      if (!drag) return;
      drag = null; canvas.classList.remove("is-drag");
      // aimantation douce vers la colonne la plus proche
      let best = cols[0].x_centre, d = 9;
      cols.forEach((c) => { const dd = Math.abs(c.x_centre - target); if (dd < d) { d = dd; best = c.x_centre; } });
      if (d < 0.05) target = best;
      target = Math.min(uStart, Math.max(uEnd, target)); syncRange(); kick();
    };
    canvas.addEventListener("pointerup", end); canvas.addEventListener("pointercancel", end);
    canvas.addEventListener("keydown", (ev) => {
      if (ev.key === "ArrowLeft") { target = clamp(target - 0.04); } else if (ev.key === "ArrowRight") { target = clamp(target + 0.04); } else return;
      ev.preventDefault(); syncRange(); kick();
    });
    canvas.tabIndex = 0;
    info();

    // WebGL
    try { gl = canvas.getContext("webgl", { antialias: true, alpha: true, premultipliedAlpha: false }); } catch (e) { gl = null; }
    if (!gl) return fallback();

    const VS = `
      attribute vec2 aP;               // x : abscisse le long de la bande (0..1), y : -0.5..0.5
      uniform float uOffV, uHWV, uRV, uLV, uTiltV, uYawV, uCamZV, uAspV;
      varying vec2 vUv; varying float vShade; varying float vSide;
      void main(){
        float t = aP.x * uLV - uOffV;          // position le long de la bande, 0 au centre
        float s = sign(t); float at = abs(t);
        vec3 p; vec3 n;
        if (at <= uHWV) { p = vec3(t, aP.y, 0.0); n = vec3(0.0, 0.0, 1.0); }
        else {
          float e = at - uHWV;
          float a = e / uRV;
          float r = max(uRV * (1.0 - 0.055 * a / 6.2831), 0.03);   // spirale : chaque tour un peu plus serré
          p = vec3(s * (uHWV + r * sin(a)), aP.y, -uRV + r * cos(a));
          n = vec3(s * sin(a), 0.0, cos(a));
        }
        // inclinaison (axe x) puis lacet (axe y)
        float ct = cos(uTiltV), st = sin(uTiltV);
        p = vec3(p.x, p.y * ct - p.z * st, p.y * st + p.z * ct);
        n = vec3(n.x, n.y * ct - n.z * st, n.y * st + n.z * ct);
        float cy = cos(uYawV), sy = sin(uYawV);
        p = vec3(p.x * cy + p.z * sy, p.y, -p.x * sy + p.z * cy);
        n = vec3(n.x * cy + n.z * sy, n.y, -n.x * sy + n.z * cy);
        vec3 lig = normalize(vec3(-0.35, 0.55, 0.9));
        vShade = dot(n, lig);
        vSide = n.z;
        vUv = vec2(aP.x, 0.5 - aP.y);
        float z = p.z - uCamZV;
        float f = 1.0 / tan(0.30);
        gl_Position = vec4(p.x * f / uAspV, p.y * f, -1.105 * z - 1.0526, -z);   // near 0,5 · far 10
      }`;
    const FS = `
      precision mediump float;
      uniform sampler2D uTexF;
      uniform float uGlowF;
      varying vec2 vUv; varying float vShade; varying float vSide;
      void main(){
        vec3 c;
        float sh = vShade;
        if (gl_FrontFacing) { c = texture2D(uTexF, vUv).rgb; }
        else { c = vec3(0.62, 0.50, 0.34) * (0.85 + 0.15 * texture2D(uTexF, vec2(1.0 - vUv.x, vUv.y)).r); sh = -sh; }
        float lum = 0.36 + 0.72 * clamp(sh, 0.0, 1.0);
        // assombrissement des bords haut et bas (cuir usé)
        float edge = smoothstep(0.0, 0.05, vUv.y) * smoothstep(1.0, 0.95, vUv.y);
        c *= lum * mix(0.55, 1.0, edge);
        c += vec3(0.09, 0.06, 0.02) * uGlowF * clamp(sh, 0.0, 1.0);
        gl_FragColor = vec4(c, 1.0);
      }`;
    function sh(type, src) {
      const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    }
    try {
      prog = gl.createProgram();
      gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    } catch (e) { console.warn("Rouleau 3D :", e.message); return fallback(); }
    gl.useProgram(prog);

    // Maillage : bande de N segments (triangle strip)
    const N = 720, verts = new Float32Array((N + 1) * 4);
    for (let i = 0; i <= N; i++) { const x = i / N; verts.set([x, 0.5, x, -0.5], i * 4); }
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);
    const aP = gl.getAttribLocation(prog, "aP"); gl.enableVertexAttribArray(aP); gl.vertexAttribPointer(aP, 2, gl.FLOAT, false, 0, 0);
    const U = {}; ["uOffV", "uHWV", "uRV", "uLV", "uTiltV", "uYawV", "uCamZV", "uAspV", "uTexF", "uGlowF"].forEach((k) => (U[k] = gl.getUniformLocation(prog, k)));
    gl.uniform1f(U.uHWV, HW); gl.uniform1f(U.uRV, R); gl.uniform1f(U.uLV, L); gl.uniform1f(U.uTiltV, -0.42); gl.uniform1i(U.uTexF, 0);
    gl.enable(gl.DEPTH_TEST);

    // Texture
    tex = gl.createTexture();
    const img = new Image();
    img.onload = () => {
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img);
      // 4096×1024 : puissances de deux → mipmaps
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      const an = gl.getExtension("EXT_texture_filter_anisotropic");
      if (an) gl.texParameterf(gl.TEXTURE_2D, an.TEXTURE_MAX_ANISOTROPY_EXT, Math.min(8, gl.getParameter(an.MAX_TEXTURE_MAX_ANISOTROPY_EXT)));
      ready = true; kick();
    };
    img.onerror = fallback;
    img.src = $(".v3d-fallback img", root).getAttribute("src");

    function resize() {
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      const w = Math.round(stage.clientWidth * dpr), h = Math.round(stage.clientHeight * dpr);
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      gl.viewport(0, 0, w, h);
      const asp = w / h;
      gl.uniform1f(U.uAspV, asp);
      // recul de la caméra pour que le rouleau tienne en largeur et en hauteur
      const halfW = HW + R + 0.12, tanH = Math.tan(0.30);
      gl.uniform1f(U.uCamZV, Math.max(halfW / (tanH * asp), 0.7 / tanH) + 0.15);
    }
    function frame(now) {
      raf = 0;
      if (!ready) return;
      const k = reduced ? 1 : 0.12;
      u += (target - u) * k;
      if (Math.abs(target - u) < 1e-4) u = target;
      const t = (now - t0) / 1000;
      yaw = reduced ? 0 : Math.sin(t * 0.5) * 0.05;
      resize();
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.uniform1f(U.uOffV, u * L); gl.uniform1f(U.uYawV, yaw); gl.uniform1f(U.uGlowF, 0.6 + 0.4 * Math.sin(t * 1.3));
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, (N + 1) * 2);
      info();
      if (inView && (!reduced || u !== target)) raf = requestAnimationFrame(frame);
    }
    function kick() { if (gl && !raf) raf = requestAnimationFrame(frame); else if (!gl) info(); }
    new IntersectionObserver((en) => { inView = en[0].isIntersecting; if (inView) kick(); }, { rootMargin: "100px" }).observe(stage);
    addEventListener("resize", kick);
    syncRange();

    function fallback() {
      gl = null; canvas.hidden = true;
      $(".v3d-fallback", root).hidden = false;
      if (hint) hint.hidden = true;
      // le curseur fait alors défiler l'image à plat
      const box = $(".v3d-fallback", root);
      const scroll = () => { box.scrollLeft = target * box.scrollWidth - box.clientWidth / 2; u = target; info(); };
      range.addEventListener("input", scroll); $$(".v3d-btn", root).forEach((b) => b.addEventListener("click", scroll)); scroll();
    }
  }

  /* ------------------------------------------------------------------
     2. Plan des grottes
     ------------------------------------------------------------------ */
  const pts = $$(".gr-pt"), panels = $$(".gr-panel");
  function grotte(n) {
    pts.forEach((p) => p.classList.toggle("is-on", p.dataset.g === n));
    panels.forEach((p) => (p.hidden = p.dataset.g !== n));
  }
  pts.forEach((p) => {
    p.addEventListener("click", () => grotte(p.dataset.g));
    p.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); grotte(p.dataset.g); } });
  });
  if (pts.length) grotte("1");

  /* ------------------------------------------------------------------
     3. Comparateur (onglets accessibles)
     ------------------------------------------------------------------ */
  const tabs = $$(".cmp-tabs [role=tab]");
  function onglet(t, focus) {
    tabs.forEach((x) => {
      const on = x === t;
      x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1;
      const p = document.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = !on;
    });
    if (focus) t.focus();
  }
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => onglet(t));
    t.addEventListener("keydown", (ev) => {
      const d = ev.key === "ArrowRight" ? 1 : ev.key === "ArrowLeft" ? -1 : 0;
      if (d) { ev.preventDefault(); onglet(tabs[(i + d + tabs.length) % tabs.length], true); }
    });
  });

  /* ------------------------------------------------------------------
     4. Barres des livres (déclenchées à l'apparition)
     ------------------------------------------------------------------ */
  const livres = $(".livres");
  if (livres) new IntersectionObserver((en, io) => { if (en[0].isIntersecting) { livres.classList.add("is-visible"); io.disconnect(); } }, { threshold: .3 }).observe(livres);

  /* ------------------------------------------------------------------
     5. Sommaire actif
     ------------------------------------------------------------------ */
  const links = $$(".s-sommaire a");
  if (links.length) {
    const map = new Map(links.map((a) => [a.getAttribute("href").slice(1), a]));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { links.forEach((a) => a.classList.remove("is-active")); map.get(en.target.id)?.classList.add("is-active"); }
    }), { rootMargin: "-45% 0px -50% 0px" });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
