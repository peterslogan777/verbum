/* =====================================================================
   VERBUM — Parchemin WebGL du hall d'entrée
   Une feuille de parchemin procédurale se déroule puis ondule lentement
   derrière le titre, comme portée par un souffle. Lignes réglées de
   scribe, fibres, bords usés et reflets dorés sont calculés dans le
   fragment shader (aucune image à charger).
   — se met en pause hors écran ou onglet masqué
   — image fixe si « réduire les animations » est activé
   — sans WebGL, rien n'est ajouté (le hall reste intact)
   ===================================================================== */
(() => {
  "use strict";
  const hero = document.querySelector(".hero");
  if (!hero) return;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const canvas = document.createElement("canvas");
  canvas.className = "hero-parchemin-gl";
  canvas.setAttribute("aria-hidden", "true");
  Object.assign(canvas.style, {
    position: "absolute", inset: "0", width: "100%", height: "100%", pointerEvents: "none",
    zIndex: "1", opacity: "0", transition: "opacity 2.4s ease", mixBlendMode: "screen",
  });
  const gl = canvas.getContext("webgl", { alpha: true, antialias: true, premultipliedAlpha: true });
  if (!gl) return;
  const anchor = hero.querySelector("#particles") || hero.querySelector(".hero-vignette");
  hero.insertBefore(canvas, anchor);

  // Grille : NX × NY segments ; aP = (u, v) dans [0,1]²
  const NX = 160, NY = 24;
  const VS = `
    attribute vec2 aP;
    uniform float uT, uRoll, uAsp;
    varying vec2 vUv; varying float vLight; varying float vBack;
    void main(){
      float W = 1.9, H = 0.62;
      float x = (aP.x - 0.5) * W, y = (aP.y - 0.5) * H;
      // ondulation douce
      float z = 0.05 * sin(aP.x * 5.0 + uT * 0.7) + 0.03 * sin(aP.y * 4.0 + aP.x * 2.0 + uT * 0.5);
      vec3 n = vec3(-0.25 * cos(aP.x * 5.0 + uT * 0.7), -0.12 * cos(aP.y * 4.0 + uT * 0.5), 1.0);
      // déroulement : au-delà de xr, la feuille s'enroule sur un cylindre
      float xr = (uRoll - 0.5) * W, R = 0.07;
      if (x > xr) {
        float a = (x - xr) / R;
        float r = max(R * (1.0 - 0.035 * a), 0.012);   // spirale serrée
        x = xr + r * sin(a);
        z = z + R - r * cos(a);
        n = vec3(sin(a) * -1.0, 0.0, cos(a));
      }
      // légère inclinaison de la feuille
      float ax = -0.38, ay = 0.18;
      vec3 p = vec3(x, y, z);
      p = vec3(p.x, p.y * cos(ax) - p.z * sin(ax), p.y * sin(ax) + p.z * cos(ax));
      p = vec3(p.x * cos(ay) + p.z * sin(ay), p.y, -p.x * sin(ay) + p.z * cos(ay));
      n = normalize(n);
      vLight = dot(n, normalize(vec3(-0.4, 0.6, 0.8)));
      vBack = n.z;
      vUv = aP;
      float zc = p.z - 2.25;
      float f = 1.0 / tan(0.42);
      gl_Position = vec4(p.x * f / uAsp, p.y * f + 0.06, -1.1 * zc - 1.05, -zc);
    }`;
  const FS = `
    precision mediump float;
    uniform float uTf;
    varying vec2 vUv; varying float vLight; varying float vBack;
    float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
    float n2(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
      return mix(mix(h(i), h(i + vec2(1, 0)), f.x), mix(h(i + vec2(0, 1)), h(i + vec2(1, 1)), f.x), f.y); }
    float fbm(vec2 p){ float s = 0.0, a = 0.5; for (int i = 0; i < 5; i++) { s += a * n2(p); p *= 2.03; a *= 0.5; } return s; }
    void main(){
      vec2 uv = vUv;
      float g = fbm(uv * vec2(9.0, 3.0));
      vec3 c = mix(vec3(0.55, 0.42, 0.25), vec3(0.96, 0.88, 0.70), g);
      c *= 0.85 + 0.15 * n2(uv * vec2(160.0, 40.0));                  // fibres
      // lignes réglées et colonnes de « texte » abstrait (simples traits, aucun signe)
      float line = smoothstep(0.012, 0.0, abs(fract(uv.y * 14.0) - 0.5) - 0.18);
      float col = step(0.08, fract(uv.x * 4.0)) * step(fract(uv.x * 4.0), 0.86);
      float mots = step(0.45, n2(vec2(uv.x * 70.0, floor(uv.y * 14.0) * 3.1)));
      float encre = line * col * mots * step(0.12, uv.y) * step(uv.y, 0.88);
      c = mix(c, vec3(0.22, 0.14, 0.07), encre * 0.55);
      // bords usés
      float e = min(min(uv.x, 1.0 - uv.x) * 3.2, min(uv.y, 1.0 - uv.y) * 1.0);
      float bord = smoothstep(0.0, 0.08 + 0.06 * fbm(uv * 12.0), e);
      float lum = 0.45 + 0.75 * clamp(vBack > 0.0 ? vLight : -vLight, 0.0, 1.0);
      c *= lum;
      // reflet doré qui glisse
      float glint = pow(max(0.0, sin(uv.x * 3.0 - uTf * 0.35 + uv.y)), 18.0);
      c += vec3(0.9, 0.7, 0.3) * glint * 0.35;
      float a = bord * 0.9;
      gl_FragColor = vec4(c * a, a);
    }`;
  function sh(t, s) { const o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }
  let prog;
  try {
    prog = gl.createProgram();
    gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  } catch (e) { console.warn("Parchemin WebGL :", e.message); canvas.remove(); return; }
  gl.useProgram(prog);

  // Maillage indexé
  const pos = [], idx = [];
  for (let j = 0; j <= NY; j++) for (let i = 0; i <= NX; i++) pos.push(i / NX, j / NY);
  for (let j = 0; j < NY; j++) for (let i = 0; i < NX; i++) {
    const a = j * (NX + 1) + i, b = a + 1, c = a + NX + 1, d = c + 1;
    idx.push(a, b, c, b, d, c);
  }
  const vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(pos), gl.STATIC_DRAW);
  const ib = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(idx), gl.STATIC_DRAW);
  const aP = gl.getAttribLocation(prog, "aP"); gl.enableVertexAttribArray(aP); gl.vertexAttribPointer(aP, 2, gl.FLOAT, false, 0, 0);
  const uT = gl.getUniformLocation(prog, "uT"), uTf = gl.getUniformLocation(prog, "uTf"), uRoll = gl.getUniformLocation(prog, "uRoll"), uAsp = gl.getUniformLocation(prog, "uAsp");
  gl.enable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

  let raf = 0, visible = true, t0 = performance.now();
  function resize() {
    const dpr = Math.min(innerWidth < 700 ? 1 : 1.5, devicePixelRatio || 1);
    const w = Math.round(hero.clientWidth * dpr), h = Math.round(hero.clientHeight * dpr);
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    gl.viewport(0, 0, w, h);
    // la feuille occupe environ 70 % de la largeur sur grand écran, davantage sur mobile
    gl.uniform1f(uAsp, Math.max(w / h, 0.9) * (innerWidth < 700 ? 1.0 : 1.35));
  }
  function draw(now) {
    raf = 0;
    const t = reduced ? 6 : (now - t0) / 1000;
    const roll = reduced ? 1.02 : Math.min(1.02, 0.08 + 0.94 * (1 - Math.pow(1 - Math.min(1, t / 5.5), 3)));
    resize();
    gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.uniform1f(uT, t); gl.uniform1f(uTf, t); gl.uniform1f(uRoll, roll);
    gl.drawElements(gl.TRIANGLES, idx.length, gl.UNSIGNED_SHORT, 0);
    if (!reduced && visible && !document.hidden) raf = requestAnimationFrame(draw);
  }
  const start = () => { if (!raf) raf = requestAnimationFrame(draw); };
  new IntersectionObserver((en) => { visible = en[0].isIntersecting; if (visible) start(); }).observe(hero);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) start(); });
  addEventListener("resize", start);
  // apparition après le chargeur calligraphique
  setTimeout(() => { canvas.style.opacity = innerWidth < 700 ? "0.22" : "0.32"; t0 = performance.now(); start(); }, reduced ? 0 : 1200);
})();
