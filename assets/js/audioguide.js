/* =====================================================================
   VERBUM — Audioguide : lecture continue des narrations du musée
   Données : <script id="ag-data"> (générées par tools/pages.py)
   Mémoire : localStorage « verbum-audioguide » (chapitre, position, écoutés)
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const dataEl = $("#ag-data"), box = $(".ag-player");
  if (!dataEl || !box) return;
  const P = JSON.parse(dataEl.textContent);
  const ROOT = (document.querySelector('script[src$="assets/js/audioguide.js"]')?.getAttribute("src") || "").replace(/assets\/js\/audioguide\.js$/, "");
  const KEY = "verbum-audioguide";
  const fmt = (t) => (isFinite(t) && t > 0 ? `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, "0")}` : "0:00");

  const els = {
    img: $(".ag-img", box), grp: $(".ag-grp-now", box), t: $(".ag-t-now", box), cur: $(".ag-cur", box),
    seek: $(".ag-seek", box), tc: $(".ag-tc", box), td: $(".ag-td", box), play: $(".ag-play", box),
    prev: $(".ag-prev", box), next: $(".ag-next", box), back: $(".ag-back", box), fwd: $(".ag-fwd", box),
    rate: $(".ag-rate", box), auto: $(".ag-auto input", box), go: $(".ag-go", box),
    bar: $(".ag-total-bar i", box), txt: $(".ag-total-txt", box), reset: $(".ag-reset", box),
    tr: $(".ag-tr-body"),
  };
  const items = $$(".ag-it");
  const RATES = [1, 1.25, 1.5, 0.85];

  let st = { i: 0, t: 0, done: [], rate: 1, auto: true };
  try { st = { ...st, ...JSON.parse(localStorage.getItem(KEY) || "{}") }; } catch (_) { /* mémoire indisponible */ }
  if (!(st.i >= 0 && st.i < P.length)) st.i = 0;
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (_) { /* navigation privée */ } };

  const audio = new Audio();
  audio.preload = "metadata";
  let paras = [], lens = [], total = 0, pendingSeek = 0;

  const progress = () => {
    const n = st.done.length;
    els.bar.style.width = `${(n / P.length) * 100}%`;
    els.txt.textContent = `${n} ${n > 1 ? "chapitres écoutés" : "chapitre écouté"} sur ${P.length}`;
    items.forEach((b, k) => { b.classList.toggle("is-done", st.done.includes(k)); b.classList.toggle("is-current", k === st.i); b.setAttribute("aria-current", k === st.i ? "true" : "false"); });
  };

  const loadTrack = (i, { autoplay = false, at = 0 } = {}) => {
    st.i = Math.max(0, Math.min(P.length - 1, i));
    const d = P[st.i];
    audio.src = ROOT + d.src;
    audio.playbackRate = st.rate;
    pendingSeek = at;
    els.img.style.opacity = 0;
    setTimeout(() => { els.img.src = `${ROOT}${d.img}-960.jpg`; els.img.onload = () => { els.img.style.opacity = 1; }; }, 180);
    els.grp.textContent = d.g;
    els.t.textContent = d.t;
    els.cur.textContent = st.i + 1;
    els.td.textContent = fmt(d.d);
    els.tc.textContent = fmt(at);
    els.go.href = ROOT + d.h;
    els.go.style.visibility = d.h === "audioguide.html" ? "hidden" : "visible";
    els.prev.disabled = st.i === 0;
    els.next.disabled = st.i === P.length - 1;
    els.tr.innerHTML = d.tr.map((p) => `<p>${p.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]))}</p>`).join("") || "<p>Transcription disponible dans la salle.</p>";
    els.tr.scrollTop = 0;
    paras = $$("p", els.tr); lens = paras.map((p) => p.textContent.length); total = lens.reduce((a, b) => a + b, 0) || 1;
    st.t = at; save(); progress();
    if ("mediaSession" in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({ title: d.t, artist: "VERBUM — Musée Virtuel de la Bible", album: d.g,
        artwork: [{ src: `${ROOT}${d.img}-960.jpg`, sizes: "960x540", type: "image/jpeg" }] });
    }
    if (autoplay) audio.play().catch(() => {});
  };

  audio.addEventListener("loadedmetadata", () => {
    if (pendingSeek && pendingSeek < audio.duration - 2) audio.currentTime = pendingSeek;
    pendingSeek = 0;
    els.td.textContent = fmt(audio.duration);
  });
  let lastSave = 0;
  audio.addEventListener("timeupdate", () => {
    const p = audio.duration ? audio.currentTime / audio.duration : 0;
    if (!els.seek.matches(":active")) els.seek.value = Math.round(p * 1000);
    els.seek.style.setProperty("--p", `${p * 100}%`);
    els.tc.textContent = fmt(audio.currentTime);
    let acc = 0, idx = 0;
    for (; idx < lens.length; idx++) { acc += lens[idx]; if (acc / total >= p) break; }
    paras.forEach((el, k) => {
      const on = k === idx && !audio.paused;
      if (on && !el.classList.contains("is-current")) el.parentElement.scrollTo({ top: el.offsetTop - el.parentElement.offsetTop - 16, behavior: "smooth" });
      el.classList.toggle("is-current", on);
    });
    if (Date.now() - lastSave > 3000) { st.t = audio.currentTime; save(); lastSave = Date.now(); }
  });
  audio.addEventListener("play", () => {
    box.classList.add("is-playing");
    els.play.setAttribute("aria-label", "Mettre en pause");
    document.dispatchEvent(new CustomEvent("verbum:audio", { detail: audio }));
  });
  audio.addEventListener("pause", () => { box.classList.remove("is-playing"); els.play.setAttribute("aria-label", "Reprendre l'audioguide"); st.t = audio.currentTime; save(); });
  audio.addEventListener("ended", () => {
    if (!st.done.includes(st.i)) st.done.push(st.i);
    st.t = 0; save(); progress();
    if (st.auto && st.i < P.length - 1) loadTrack(st.i + 1, { autoplay: true });
  });
  document.addEventListener("verbum:audio", (ev) => { if (ev.detail !== audio && !audio.paused) audio.pause(); });

  const toggle = () => { if (audio.paused) audio.play().catch(() => {}); else audio.pause(); };
  els.play.addEventListener("click", toggle);
  els.prev.addEventListener("click", () => { if (audio.currentTime > 4) audio.currentTime = 0; else loadTrack(st.i - 1, { autoplay: !audio.paused }); });
  els.next.addEventListener("click", () => loadTrack(st.i + 1, { autoplay: !audio.paused }));
  els.back.addEventListener("click", () => { audio.currentTime = Math.max(0, audio.currentTime - 15); });
  els.fwd.addEventListener("click", () => { if (audio.duration) audio.currentTime = Math.min(audio.duration - 0.5, audio.currentTime + 15); });
  els.seek.addEventListener("input", () => { if (audio.duration) audio.currentTime = (els.seek.value / 1000) * audio.duration; });
  const showRate = () => { els.rate.textContent = `Vitesse ${String(st.rate).replace(".", ",")}×`; };
  els.rate.addEventListener("click", () => { st.rate = RATES[(RATES.indexOf(st.rate) + 1) % RATES.length]; audio.playbackRate = st.rate; showRate(); save(); });
  els.auto.checked = st.auto;
  els.auto.addEventListener("change", () => { st.auto = els.auto.checked; save(); });
  els.reset.addEventListener("click", () => { st.done = []; save(); loadTrack(0, { autoplay: false }); });
  items.forEach((b) => b.addEventListener("click", () => {
    loadTrack(+b.dataset.i, { autoplay: true });
    box.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
  }));

  document.addEventListener("keydown", (ev) => {
    if (ev.target.closest("input, textarea, select, button, a, [contenteditable]") || ev.ctrlKey || ev.metaKey || ev.altKey || document.querySelector("dialog[open]")) return;
    if (ev.key === " ") { ev.preventDefault(); toggle(); }
    else if (ev.key === "n" || ev.key === "N") loadTrack(st.i + 1, { autoplay: !audio.paused });
    else if (ev.key === "p" || ev.key === "P") loadTrack(st.i - 1, { autoplay: !audio.paused });
  });
  if ("mediaSession" in navigator) {
    const ms = navigator.mediaSession;
    ms.setActionHandler("play", () => audio.play());
    ms.setActionHandler("pause", () => audio.pause());
    ms.setActionHandler("previoustrack", () => loadTrack(st.i - 1, { autoplay: true }));
    ms.setActionHandler("nexttrack", () => loadTrack(st.i + 1, { autoplay: true }));
  }

  showRate();
  loadTrack(st.i, { at: st.t || 0 });
})();
