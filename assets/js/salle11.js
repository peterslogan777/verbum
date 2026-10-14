/* =====================================================================
   VERBUM — Salle 11 · La Grande Frise chronologique (étape E13)
   1. Frise : glisser, molette, clavier, flèches, époques, filtres, mini-carte
   2. Fiche détaillée (dialogue) + commentaire audio de l'époque
   3. Cartes des époques  4. Jeu « Remettre dans l'ordre »  5. Sommaire actif
   ===================================================================== */
(() => {
  "use strict";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const sec = $("#frise");
  const ROOT = sec ? sec.dataset.root || "" : "";
  const DATA = JSON.parse($("#fr-data")?.textContent || "[]");

  /* ---------- 1. Frise ---------- */
  const track = $(".fr-track");
  const evs = $$(".ev");
  const ticks = $$(".mn-t");
  const win = $(".mn-win");
  const eraBtns = $$(".fr-eras button");
  const prev = $(".fr-prev"), next = $(".fr-next");

  const scrollToEl = (el, smooth = true) => {
    if (!track || !el) return;
    const left = el.offsetLeft - (track.clientWidth - el.offsetWidth) / 2;
    track.scrollTo({ left: Math.max(0, left), behavior: smooth && !reduce ? "smooth" : "auto" });
  };

  const update = () => {
    if (!track || !evs.length) return;
    const l = track.scrollLeft, r = l + track.clientWidth;
    let i0 = -1, i1 = -1, mid = -1, best = Infinity;
    const c = (l + r) / 2;
    evs.forEach((ev, i) => {
      const a = ev.offsetLeft, b = a + ev.offsetWidth;
      if (b > l + 20 && a < r - 20) { if (i0 < 0) i0 = i; i1 = i; }
      const d = Math.abs((a + b) / 2 - c);
      if (d < best) { best = d; mid = i; }
    });
    if (win && i0 >= 0) {
      const p0 = parseFloat(ticks[i0].style.left), p1 = parseFloat(ticks[i1].style.left);
      win.style.left = `calc(${p0}% - 6px)`;
      win.style.width = `calc(${Math.max(0.8, p1 - p0)}% + 12px)`;
    }
    ticks.forEach((t, i) => t.classList.toggle("is-on", i >= i0 && i <= i1));
    evs.forEach((ev, i) => ev.classList.toggle("is-current", i === mid));
    const era = evs[mid]?.dataset.era;
    eraBtns.forEach((b) => {
      const on = b.dataset.era === era;
      const was = b.getAttribute("aria-checked") === "true";
      b.setAttribute("aria-checked", String(on));
      b.tabIndex = on ? 0 : -1;
      // bande d'époques défilante (mobile) : garder l'époque active visible
      const bar = b.parentElement;
      if (on && !was && bar && bar.scrollWidth > bar.clientWidth + 2) {
        bar.scrollTo({ left: b.offsetLeft - bar.offsetLeft - 12, behavior: "smooth" });
      }
    });
    if (prev) prev.disabled = l <= 2;
    if (next) next.disabled = r >= track.scrollWidth - 2;
  };

  if (track) {
    let raf = 0;
    track.addEventListener("scroll", () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; update(); }); }, { passive: true });
    window.addEventListener("resize", update);
    // glisser à la souris
    let down = false, sx = 0, sl = 0, moved = false;
    track.addEventListener("pointerdown", (ev) => {
      if (ev.pointerType !== "mouse" || ev.button !== 0) return;
      down = true; moved = false; sx = ev.clientX; sl = track.scrollLeft;
    });
    window.addEventListener("pointermove", (ev) => {
      if (!down) return;
      const dx = ev.clientX - sx;
      if (!moved && Math.abs(dx) > 6) { moved = true; track.classList.add("is-drag"); }
      if (moved) track.scrollLeft = sl - dx;
    });
    window.addEventListener("pointerup", () => {
      if (!down) return; down = false;
      if (moved) setTimeout(() => track.classList.remove("is-drag"), 0);
    });
    // molette verticale → défilement horizontal (tant que la frise peut défiler)
    track.addEventListener("wheel", (ev) => {
      if (Math.abs(ev.deltaY) <= Math.abs(ev.deltaX)) return;
      const max = track.scrollWidth - track.clientWidth;
      if ((ev.deltaY < 0 && track.scrollLeft <= 0) || (ev.deltaY > 0 && track.scrollLeft >= max - 1)) return;
      ev.preventDefault();
      track.scrollLeft += ev.deltaY;
    }, { passive: false });
    // clavier
    track.addEventListener("keydown", (ev) => {
      const step = { ArrowRight: 1, ArrowLeft: -1, PageDown: 3, PageUp: -3 }[ev.key];
      if (step) { ev.preventDefault(); track.scrollBy({ left: step * (evs[0]?.offsetWidth || 280), behavior: reduce ? "auto" : "smooth" }); }
      if (ev.key === "Home") { ev.preventDefault(); track.scrollTo({ left: 0 }); }
      if (ev.key === "End") { ev.preventDefault(); track.scrollTo({ left: track.scrollWidth }); }
    });
    prev?.addEventListener("click", () => track.scrollBy({ left: -2 * (evs[0]?.offsetWidth || 280), behavior: reduce ? "auto" : "smooth" }));
    next?.addEventListener("click", () => track.scrollBy({ left: 2 * (evs[0]?.offsetWidth || 280), behavior: reduce ? "auto" : "smooth" }));
    // époques
    const goEra = (n, focusTrack) => {
      const first = evs.find((ev) => ev.dataset.era === String(n));
      if (!first) return;
      const left = first.offsetLeft - 24;
      track.scrollTo({ left: Math.max(0, left), behavior: reduce ? "auto" : "smooth" });
      if (focusTrack) track.focus({ preventScroll: true });
    };
    eraBtns.forEach((b, i) => {
      b.addEventListener("click", () => goEra(b.dataset.era));
      b.addEventListener("keydown", (ev) => {
        const d = { ArrowRight: 1, ArrowLeft: -1 }[ev.key];
        if (d) { ev.preventDefault(); const nb = eraBtns[(i + d + eraBtns.length) % eraBtns.length]; nb.focus(); goEra(nb.dataset.era); }
      });
    });
    // mini-carte : clic → événement le plus proche
    const band = $(".mn-band");
    band?.addEventListener("click", (ev) => {
      const r = band.getBoundingClientRect();
      const p = (ev.clientX - r.left) / r.width * 100;
      let bi = 0, bd = Infinity;
      ticks.forEach((t, i) => { const d = Math.abs(parseFloat(t.style.left) - p); if (d < bd && !evs[i].classList.contains("is-dim")) { bd = d; bi = i; } });
      scrollToEl(evs[bi]);
    });
    // filtres
    const cats = $$(".fr-cat");
    const applyCats = () => {
      const on = new Set(cats.filter((b) => b.getAttribute("aria-pressed") === "true").map((b) => b.dataset.cat));
      evs.forEach((ev, i) => { const dim = !on.has(ev.dataset.cat); ev.classList.toggle("is-dim", dim); ticks[i]?.classList.toggle("is-dim", dim); });
    };
    cats.forEach((b) => b.addEventListener("click", () => {
      const pressed = cats.filter((x) => x.getAttribute("aria-pressed") === "true");
      const isOn = b.getAttribute("aria-pressed") === "true";
      if (isOn && pressed.length === cats.length) { // premier clic : n'afficher que cette catégorie
        cats.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      } else if (isOn && pressed.length === 1) { // dernier filtre retiré : tout réafficher
        cats.forEach((x) => x.setAttribute("aria-pressed", "true"));
      } else b.setAttribute("aria-pressed", String(!isOn));
      applyCats();
      const firstOn = evs.find((ev) => !ev.classList.contains("is-dim"));
      if (firstOn && cats.some((x) => x.getAttribute("aria-pressed") === "false")) scrollToEl(firstOn);
    }));
    update();
    setTimeout(update, 400);
  }

  /* ---------- 2. Fiche détaillée ---------- */
  const dlg = $(".fe");
  let cur = 0, audio = null, lastFocus = null;
  const stopAudio = () => {
    if (audio) { audio.pause(); audio = null; }
    const b = $(".fe-audio", dlg); if (b) { b.setAttribute("aria-pressed", "false"); $("span", b).textContent = "Écouter le commentaire de l'époque"; }
  };
  const BADGE = { canon: '<span class="badge badge-canon">Canonique</span>', apo: '<span class="badge badge-apo">Apocryphe</span>', none: "" };
  const fill = (i) => {
    const d = DATA[i]; if (!d) return;
    cur = i;
    stopAudio();
    const im = $(".fe-img", dlg);
    im.src = `${ROOT}${d.img}-960.jpg`;
    im.srcset = `${ROOT}${d.img}-960.jpg 960w, ${ROOT}${d.img}.jpg 1920w`;
    im.sizes = "(max-width: 1000px) 100vw, 560px";
    im.alt = `Illustration : ${d.t}`;
    $(".fe-cap-t", dlg).textContent = "Reconstitution numérique.";
    $(".fe-era", dlg).textContent = `Époque ${d.era} · ${d.eraT} · ${d.eraP}`;
    $(".fe-y", dlg).textContent = d.lab;
    $(".fe-t", dlg).textContent = d.t;
    $(".fe-meta", dlg).innerHTML = `<span class="ev-cat" data-cat="${d.c}"><i aria-hidden="true"></i>${d.cat}</span>${BADGE[d.b] || ""}`;
    $(".fe-txt", dlg).textContent = d.txt;
    $(".fe-imp p", dlg).textContent = d.imp;
    dlg.setAttribute("data-cat", d.c);
    const sa = $(".fe-salle", dlg);
    sa.href = `${ROOT}salles/${d.sU}`;
    sa.textContent = `Salle ${d.s} · ${d.sT}`;
    const u = $(".fe-url", dlg);
    if (d.url) { u.hidden = false; u.href = d.url; u.textContent = `Voir l'original · ${d.urlT}`; } else u.hidden = true;
    $(".fe-prev", dlg).disabled = i === 0;
    $(".fe-next", dlg).disabled = i === DATA.length - 1;
    $(".fe-pos", dlg).textContent = `${i + 1} / ${DATA.length}`;
    $(".fe-body", dlg).scrollTop = 0;
    dlg.querySelector(".fe-in").scrollTop = 0;
  };
  const openFe = (i) => {
    if (!dlg) return;
    lastFocus = document.activeElement;
    fill(i);
    if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
    document.body.classList.add("no-scroll");
    $(".fe-close", dlg).focus();
  };
  if (dlg) {
    evs.forEach((ev) => $(".ev-card", ev).addEventListener("click", () => openFe(+ev.dataset.i)));
    $(".fe-close", dlg).addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
    dlg.addEventListener("close", () => {
      stopAudio();
      document.body.classList.remove("no-scroll");
      const el = evs[cur];
      if (el) scrollToEl(el, false);
      (el ? $(".ev-card", el) : lastFocus)?.focus({ preventScroll: true });
    });
    $(".fe-prev", dlg).addEventListener("click", () => fill(Math.max(0, cur - 1)));
    $(".fe-next", dlg).addEventListener("click", () => fill(Math.min(DATA.length - 1, cur + 1)));
    dlg.addEventListener("keydown", (ev) => {
      if (ev.target.closest("a, input")) return;
      if (ev.key === "ArrowRight" && cur < DATA.length - 1) { ev.preventDefault(); fill(cur + 1); }
      if (ev.key === "ArrowLeft" && cur > 0) { ev.preventDefault(); fill(cur - 1); }
    });
    document.addEventListener("verbum:audio", (ev) => { if (audio && ev.detail !== audio) stopAudio(); });
    $(".fe-audio", dlg).addEventListener("click", (ev) => {
      const b = ev.currentTarget;
      if (audio) { stopAudio(); return; }
      const d = DATA[cur];
      audio = new Audio(`${ROOT}assets/audio/salle11-${d.au}.mp3`);
      // un seul son à la fois : prévient les lecteurs de la page (audio.js)
      const mine = audio;
      audio.addEventListener("play", () => document.dispatchEvent(new CustomEvent("verbum:audio", { detail: mine })));
      const start = () => { try { audio.currentTime = d.at; } catch (e) { /* lecture depuis le début */ } audio.play().catch(() => stopAudio()); };
      audio.addEventListener("loadedmetadata", start, { once: true });
      audio.addEventListener("ended", stopAudio);
      // arrêt à la fin de l'époque (le fichier en contient deux)
      const next = DATA.find((x) => x.au === d.au && x.at > d.at);
      if (next) audio.addEventListener("timeupdate", () => { if (audio && audio.currentTime >= next.at - 0.3) stopAudio(); });
      audio.load();
      b.setAttribute("aria-pressed", "true");
      $("span", b).textContent = "Arrêter le commentaire";
    });
  }
  // lien direct vers un jalon (#jalon-12), utilisé par la recherche du musée
  const fromHash = () => {
    const m = /^#jalon-(\d+)$/.exec(location.hash);
    if (!m || !dlg) return;
    const i = Math.min(DATA.length, Math.max(1, +m[1])) - 1;
    sec?.scrollIntoView({ block: "start" });
    setTimeout(() => openFe(i), 350);
  };
  window.addEventListener("hashchange", fromHash);
  fromHash();

  /* ---------- 3. Cartes des époques ---------- */
  $$(".ep-btn").forEach((b) => b.addEventListener("click", () => {
    sec?.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    const btn = eraBtns.find((x) => x.dataset.era === b.dataset.era);
    setTimeout(() => btn?.click(), reduce ? 0 : 600);
  }));

  /* ---------- 4. Remettre dans l'ordre ---------- */
  const list = $(".or-list");
  if (list) {
    const msg = $(".or-msg");
    const refresh = () => {
      const items = $$(".or-it", list);
      items.forEach((it, i) => { $(".or-up", it).disabled = i === 0; $(".or-dn", it).disabled = i === items.length - 1; });
    };
    const clearMarks = () => $$(".or-it", list).forEach((it) => { it.classList.remove("is-ok", "is-ko"); $(".or-d", it).hidden = true; });
    list.addEventListener("click", (ev) => {
      const b = ev.target.closest("button"); if (!b) return;
      const it = b.closest(".or-it");
      clearMarks();
      if (b.classList.contains("or-up") && it.previousElementSibling) list.insertBefore(it, it.previousElementSibling);
      if (b.classList.contains("or-dn") && it.nextElementSibling) list.insertBefore(it.nextElementSibling, it);
      refresh();
      (b.disabled ? $(b.classList.contains("or-up") ? ".or-dn" : ".or-up", it) : b).focus();
      if (msg) msg.textContent = "Utilisez les flèches pour classer du plus ancien au plus récent.";
    });
    $(".or-check")?.addEventListener("click", () => {
      const items = $$(".or-it", list);
      const sorted = [...items].sort((a, b) => +a.dataset.y - +b.dataset.y);
      let ok = 0;
      items.forEach((it, i) => { const good = sorted[i] === it; if (good) ok++; it.classList.toggle("is-ok", good); it.classList.toggle("is-ko", !good); $(".or-d", it).hidden = false; });
      if (msg) msg.textContent = ok === items.length ? "Parfait : votre frise est dans le bon ordre !" : `${ok} sur ${items.length} à la bonne place. Les dates sont affichées : corrigez et vérifiez à nouveau.`;
    });
    $(".or-mix")?.addEventListener("click", () => {
      clearMarks();
      const items = $$(".or-it", list);
      for (let i = items.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [items[i], items[j]] = [items[j], items[i]]; }
      items.forEach((it) => list.appendChild(it));
      refresh();
      if (msg) msg.textContent = "Mélangé ! Classez du plus ancien au plus récent.";
    });
    refresh();
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
