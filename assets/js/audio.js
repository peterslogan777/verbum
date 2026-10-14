/* =====================================================================
   VERBUM — Audioguide (commun à toutes les pages)
   Lecteur MP3 personnalisé : visualisation (Web Audio), barre de
   progression, surlignage de la transcription, déclencheurs externes
   [data-audio-trigger="clé"] → <div class="audio-player" id="audio-clé">
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Lecteurs ---------- */
  const fmt = (t) => (isFinite(t) ? `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, "0")}` : "0:00");
  $$(".audio-player").forEach((box) => {
    const audio = new Audio();
    audio.preload = "metadata";
    audio.src = box.dataset.src;
    const btn = $(".ap-play", box), seek = $(".ap-seek", box), time = $(".ap-time", box), cvs = $(".ap-viz", box);
    const ctx2d = cvs.getContext("2d");
    const paras = $$(".transcript-body p", box.closest("[data-audio-zone]") || box.parentElement);
    const lens = paras.map((p) => p.textContent.length), total = lens.reduce((a, b) => a + b, 0);
    let actx, analyser, data, raf;

    const setupAnalyser = () => {
      if (actx) return;
      try {
        actx = new (window.AudioContext || window.webkitAudioContext)();
        const src = actx.createMediaElementSource(audio);
        analyser = actx.createAnalyser(); analyser.fftSize = 128; analyser.smoothingTimeConstant = 0.8;
        src.connect(analyser); analyser.connect(actx.destination);
        data = new Uint8Array(analyser.frequencyBinCount);
      } catch (_) { analyser = null; }
    };
    const draw = () => {
      const dpr = Math.min(devicePixelRatio || 1, 2), w = cvs.clientWidth, h = cvs.clientHeight;
      if (cvs.width !== w * dpr) { cvs.width = w * dpr; cvs.height = h * dpr; }
      ctx2d.setTransform(dpr, 0, 0, dpr, 0, 0); ctx2d.clearRect(0, 0, w, h);
      const n = Math.floor(w / 6), playing = !audio.paused;
      if (analyser && playing) analyser.getByteFrequencyData(data);
      const prog = audio.duration ? audio.currentTime / audio.duration : 0;
      for (let i = 0; i < n; i++) {
        let v;
        if (analyser && playing) v = data[Math.floor((i / n) * data.length * 0.75)] / 255;
        else v = 0.18 + 0.12 * Math.abs(Math.sin(i * 0.7)) + (playing ? 0.3 * Math.abs(Math.sin(performance.now() / 300 + i)) : 0);
        const bh = Math.max(2, v * h);
        ctx2d.fillStyle = i / n < prog ? "#E6CC7A" : "rgba(201,168,76,.35)";
        ctx2d.fillRect(i * 6, (h - bh) / 2, 3, bh);
      }
      raf = requestAnimationFrame(draw);
    };
    draw();

    const toggle = () => {
      setupAnalyser(); actx?.resume?.();
      if (audio.paused) audio.play().catch(() => {}); else audio.pause();
    };
    btn.addEventListener("click", toggle);
    audio.addEventListener("play", () => { box.classList.add("is-playing"); btn.setAttribute("aria-label", "Mettre en pause"); });
    audio.addEventListener("pause", () => { box.classList.remove("is-playing"); btn.setAttribute("aria-label", "Reprendre la lecture"); });
    audio.addEventListener("loadedmetadata", () => { time.textContent = `0:00 / ${fmt(audio.duration)}`; });
    audio.addEventListener("timeupdate", () => {
      const p = audio.duration ? audio.currentTime / audio.duration : 0;
      if (!seek.matches(":active")) seek.value = Math.round(p * 1000);
      seek.style.setProperty("--p", `${p * 100}%`);
      time.textContent = `${fmt(audio.currentTime)} / ${fmt(audio.duration)}`;
      // surlignage approximatif du paragraphe en cours de lecture
      let acc = 0, idx = 0;
      for (; idx < lens.length; idx++) { acc += lens[idx]; if (acc / total >= p) break; }
      paras.forEach((el, i) => el.classList.toggle("is-current", i === idx && !audio.paused));
    });
    seek.addEventListener("input", () => { if (audio.duration) audio.currentTime = (seek.value / 1000) * audio.duration; });

    // un seul lecteur à la fois dans tout le musée
    audio.addEventListener("play", () => document.dispatchEvent(new CustomEvent("verbum:audio", { detail: audio })));
    document.addEventListener("verbum:audio", (ev) => { if (ev.detail !== audio && !audio.paused) audio.pause(); });

    const key = box.id.replace(/^audio-/, "");
    $$(`[data-audio-trigger="${key}"]`).forEach((t) => t.addEventListener("click", () => {
      box.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
      setTimeout(() => { if (audio.paused) toggle(); }, reduced ? 0 : 700);
    }));
  });

})();
