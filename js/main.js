// Scroll reveal
const io = new IntersectionObserver((es) => es.forEach((e) => {
  if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
}), { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

// Card spotlight follows the cursor
document.querySelectorAll(".card").forEach((c) => c.addEventListener("pointermove", (e) => {
  const r = c.getBoundingClientRect();
  c.style.setProperty("--mx", e.clientX - r.left + "px");
  c.style.setProperty("--my", e.clientY - r.top + "px");
}));

// Theme toggle: switches between the system theme and the opposite choice
const root = document.documentElement;
try { const saved = localStorage.getItem("kiwili-theme"); if (saved) root.dataset.theme = saved; } catch (e) {}
document.getElementById("theme-toggle")?.addEventListener("click", () => {
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : !matchMedia("(prefers-color-scheme: light)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("kiwili-theme", root.dataset.theme); } catch (e) {}
});

// ===== Hero: interactive product viewer =====
(() => {
  const $ = (id) => document.getElementById(id);
  const viewer = $("viewer"), shot = $("shot"), cur = $("cursor"), toast = $("toast");
  if (!viewer) return;
  const tabs = [...viewer.querySelectorAll(".vtab")], panels = [...viewer.querySelectorAll(".vpanel")];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fmt = (n, d = 0) => new Intl.NumberFormat("fr-CA", { minimumFractionDigits: d, maximumFractionDigits: d }).format(n);
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const DWELL = 9000;
  let cur_i = -1, token = 0, auto = !reduce, paused = false, elapsed = 0, k2 = 3487238, clockTimer = 0;

  const tween = (el, to, { suffix = "", dec = 0, from = 0, ms = 1200 } = {}) => {
    if (reduce) { el.textContent = fmt(to, dec) + suffix; return; }
    const t0 = performance.now(), tk = token;
    const step = (t) => {
      if (tk !== token && el.dataset.keep !== "1") return;
      const p = Math.min((t - t0) / ms, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(from + (to - from) * e, dec) + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  const cursorTo = async (el, tk) => {
    const sr = shot.getBoundingClientRect(), r = el.getBoundingClientRect();
    const x = r.left - sr.left + r.width / 2, y = r.top - sr.top + r.height / 2;
    cur.style.opacity = 1;
    await cur.animate([{ transform: `translate(${sr.width * 0.6}px,${sr.height * 0.9}px)` }, { transform: `translate(${x}px,${y}px)` }],
      { duration: 1300, easing: "cubic-bezier(.2,.7,.2,1)", fill: "forwards" }).finished;
    if (tk !== token) return false;
    await cur.animate([{ scale: 1 }, { scale: 0.78 }, { scale: 1 }], { duration: 240 }).finished;
    return tk === token;
  };
  const showToast = (t, d, ms = 2600) => {
    $("toast-t").textContent = t; $("toast-d").textContent = d;
    toast.classList.add("on"); const tk = token;
    setTimeout(() => { if (tk === token) toast.classList.remove("on"); }, ms);
  };
  const retire = () => cur.animate({ opacity: [1, 0] }, { duration: 350, fill: "forwards" });

  const setTag = (el, cls, txt) => { el.className = "tag " + cls; el.textContent = txt; };
  const flash = (el) => { el.classList.remove("flash"); void el.offsetWidth; el.classList.add("flash"); };

  // Final (static) values, used by reduced motion and as reset targets
  const resets = {
    0() { setTag($("live-tag"), "wait", "En attente"); k2 = 3487238; $("k2").textContent = "3 487 238 $"; $("k1").textContent = "1 626 583 $"; $("k3").textContent = "70 600 $"; $("k4").textContent = "208,5 h"; },
    1() { setTag($("inv-status"), "wait", "Brouillon"); $("inv-total").textContent = "9 588,92 $"; $("inv-send").classList.remove("pressed"); $("inv-send").textContent = "Envoyer la facture"; },
    2() { const n = $("move-note"), cols = panels[2].querySelectorAll(".board .col"); cols[1].appendChild(n); panels[2].querySelectorAll(".hrs").forEach((h) => (h.textContent = h.dataset.to)); },
    3() { $("b-fact").textContent = "31 200 $"; $("b-marge").textContent = "29,4 %"; },
    4() { $("clock").textContent = "02:14:07"; $("timer-btn").textContent = "Arrêter"; $("timer-btn").classList.add("stop"); },
  };
  const scenes = [
    async (tk) => {
      resets[0]();
      tween($("k1"), 1626583, { suffix: " $" }); tween($("k2"), 3487238, { suffix: " $" }); tween($("k3"), 70600, { suffix: " $" }); tween($("k4"), 208.5, { suffix: " h", dec: 1 });
      await sleep(2300); if (tk !== token) return;
      if (!(await cursorTo($("live-tag"), tk))) return;
      setTag($("live-tag"), "ok", "Payée"); flash($("row-live"));
      const next = k2 + 8912.5; $("k2").dataset.keep = "0"; tween($("k2"), next, { suffix: " $", from: k2, ms: 900 }); k2 = next;
      showToast("Facture payée", "Cabinet d'architecture · 8 912,50 $"); await sleep(700); retire();
    },
    async (tk) => {
      resets[1](); $("inv-total").textContent = "0,00 $";
      await sleep(1500); if (tk !== token) return;
      tween($("inv-total"), 9588.92, { suffix: " $", dec: 2, ms: 1000 });
      await sleep(1900); if (tk !== token) return;
      if (!(await cursorTo($("inv-send"), tk))) return;
      $("inv-send").classList.add("pressed"); $("inv-send").textContent = "Envoyée";
      setTag($("inv-status"), "sent", "Envoyée");
      showToast("Facture envoyée", "Cabinet d'architecture · 9 588,92 $"); await sleep(700); retire();
    },
    async (tk) => {
      resets[2](); panels[2].querySelectorAll(".hrs").forEach((h) => (h.textContent = "0"));
      panels[2].querySelectorAll(".hrs").forEach((h) => tween(h, +h.dataset.to, { ms: 1400 }));
      await sleep(2800); if (tk !== token) return;
      const n = $("move-note"), cols = panels[2].querySelectorAll(".board .col");
      const a = n.getBoundingClientRect(); cols[2].appendChild(n); const b = n.getBoundingClientRect();
      n.animate([{ transform: `translate(${a.left - b.left}px,${a.top - b.top}px)` }, { transform: "none" }], { duration: 650, easing: "cubic-bezier(.2,.7,.2,1)" });
      n.classList.remove("d"); n.classList.add("g");
      showToast("Tâche terminée", "Premiers dessins · Amélie C.");
    },
    async (tk) => {
      $("b-fact").textContent = "0 $"; $("b-marge").textContent = "0 %";
      await sleep(500); if (tk !== token) return;
      tween($("b-fact"), 31200, { suffix: " $", ms: 1500 }); tween($("b-marge"), 29.4, { suffix: " %", dec: 1, ms: 1500 });
    },
    async (tk) => {
      resets[4]();
      let s = 2 * 3600 + 14 * 60 + 7; const btn = $("timer-btn"); let running = true;
      const paint = () => { $("clock").textContent = [Math.floor(s / 3600), Math.floor(s / 60) % 60, s % 60].map((v) => String(v).padStart(2, "0")).join(":"); };
      clearInterval(clockTimer); clockTimer = setInterval(() => { if (tk !== token) return clearInterval(clockTimer); if (running) { s++; paint(); } }, 1000);
      await sleep(3200); if (tk !== token) return;
      if (!(await cursorTo(btn, tk))) return;
      running = false; btn.textContent = "Reprendre"; btn.classList.remove("stop");
      showToast("Temps enregistré", "2 h 14 · Rénovation condo"); await sleep(700); retire();
    },
  ];

  const pauseBtn = $("vpause");
  const setAuto = (v) => {
    auto = v && !reduce; viewer.classList.toggle("manual", !auto);
    if (pauseBtn) {
      pauseBtn.classList.toggle("paused", !auto);
      pauseBtn.setAttribute("aria-label", auto ? "Mettre en pause la démonstration animée" : "Reprendre la démonstration animée");
    }
  };
  pauseBtn?.addEventListener("click", () => { if (!auto) elapsed = 0; setAuto(!auto); });
  const select = (i, user = false) => {
    if (user) setAuto(false);
    token++; clearInterval(clockTimer); elapsed = 0;
    cur.getAnimations().forEach((a) => a.cancel()); cur.style.opacity = 0; toast.classList.remove("on");
    tabs.forEach((t, k) => { const on = k === i; t.classList.toggle("on", on); t.setAttribute("aria-selected", on); t.tabIndex = on ? 0 : -1; t.style.setProperty("--p", 0); });
    panels.forEach((p, k) => { if (k !== i) { p.hidden = true; p.classList.remove("play"); } });
    const p = panels[i]; p.hidden = false; void p.offsetWidth; p.classList.add("play");
    shot.querySelectorAll(".app-side a").forEach((a) => a.classList.toggle("on", a.dataset.nav === p.dataset.nav));
    cur_i = i;
    const tl = viewer.querySelector(".vtabs"); tl.scrollTo({ left: Math.max(0, tabs[i].offsetLeft - 16), behavior: reduce ? "auto" : "smooth" });
    if (reduce) resets[i](); else scenes[i](token);
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(i, true));
    t.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      const n = (i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length; tabs[n].focus(); select(n, true);
    });
  });

  // autoplay with a progress line on the active tab; pauses on hover and when off-screen
  let visible = true, last = performance.now();
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; }, { threshold: 0.25 }).observe(viewer);
  viewer.addEventListener("pointerenter", () => (paused = true));
  viewer.addEventListener("pointerleave", () => (paused = false));
  const tick = (t) => {
    const dt = Math.min(t - last, 100); last = t;
    if (auto && !paused && visible && !document.hidden) {
      elapsed += dt; tabs[cur_i].style.setProperty("--p", Math.min(elapsed / DWELL, 1));
      if (elapsed >= DWELL) { if (cur_i === tabs.length - 1) setAuto(false); else select(cur_i + 1); }
    }
    requestAnimationFrame(tick);
  };
  setAuto(auto);
  select(0);
  if (!reduce) requestAnimationFrame(tick);

  // gentle tilt that follows the pointer
  const wrap = shot.parentNode;
  if (!reduce) {
    wrap.addEventListener("pointermove", (e) => {
      const r = wrap.getBoundingClientRect();
      shot.style.setProperty("--ry", ((e.clientX - r.left) / r.width - 0.5) * 3 + "deg");
      shot.style.setProperty("--rx", (0.5 - (e.clientY - r.top) / r.height) * 1.5 + "deg");
    });
    wrap.addEventListener("pointerleave", () => { shot.style.setProperty("--rx", "0deg"); shot.style.setProperty("--ry", "0deg"); });
  }
})();

// ===== Navigation: dropdown, mobile menu =====
(() => {
  const btn = document.querySelector(".dd-btn"), panel = document.getElementById("dd-feat");
  const close = () => { if (btn) { btn.setAttribute("aria-expanded", "false"); panel.hidden = true; } };
  btn?.addEventListener("click", (e) => { e.stopPropagation(); const o = btn.getAttribute("aria-expanded") === "true"; btn.setAttribute("aria-expanded", !o); panel.hidden = o; });
  document.addEventListener("click", (e) => { if (panel && !panel.contains(e.target)) close(); });
  panel?.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));
  const mb = document.getElementById("menu-btn"), mm = document.getElementById("mobile-menu");
  const mclose = () => { if (mb) { mb.setAttribute("aria-expanded", "false"); mm.hidden = true; } };
  mb?.addEventListener("click", () => { const o = mb.getAttribute("aria-expanded") === "true"; mb.setAttribute("aria-expanded", !o); mm.hidden = o; });
  mm?.querySelectorAll("a").forEach((a) => a.addEventListener("click", mclose));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { close(); mclose(); } });
  matchMedia("(min-width: 861px)").addEventListener("change", mclose);
})();

// ===== Workflow: light up each step in order as it scrolls into view =====
(() => {
  const list = document.getElementById("steps"); if (!list) return;
  const steps = [...list.querySelectorAll(".step")], fill = document.getElementById("rail-fill"), rail = list.querySelector(".rail");
  const vertical = () => matchMedia("(max-width: 900px)").matches;
  const set = (n) => {
    steps.forEach((s, i) => s.classList.toggle("on", i < n));
    rail.classList.toggle("v", vertical());
    const frac = n <= 1 ? 0 : (n - 1) / (steps.length - 1);
    if (vertical()) fill.style.height = frac * 100 + "%"; else fill.style.width = frac * 100 + "%";
  };
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) { set(steps.length); return; }
  let done = false;
  new IntersectionObserver((es) => {
    if (!es[0].isIntersecting || done) return; done = true;
    steps.forEach((_, i) => setTimeout(() => set(i + 1), 350 * i + 150));
  }, { threshold: 0.35 }).observe(list);
})();

// ===== Lead dialog (front-end only; no endpoint is wired) =====
(() => {
  const dlg = document.getElementById("lead-dialog"); if (!dlg || !dlg.showModal) return;
  const form = document.getElementById("lead-form"), err = document.getElementById("f-err"), done = document.getElementById("f-done");
  const copy = { trial: ["Essai gratuit", "14 jours, sans carte de crédit.", "Commencer"], demo: ["Réserver une démo", "Un de nos experts vous contacte pour évaluer vos besoins.", "Prenons rendez-vous"] };
  document.querySelectorAll("[data-open]").forEach((a) => a.addEventListener("click", (e) => {
    e.preventDefault(); const c = copy[a.dataset.open];
    document.getElementById("dlg-title").textContent = c[0]; document.getElementById("dlg-sub").textContent = c[1]; document.getElementById("f-submit").textContent = c[2];
    err.hidden = done.hidden = true; dlg.showModal(); document.getElementById("f-name").focus();
  }));
  dlg.querySelector("[data-close]").addEventListener("click", () => dlg.close());
  dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
  form.addEventListener("submit", (e) => {
    e.preventDefault(); done.hidden = true;
    const name = form.elements.name, email = form.elements.email;
    [name, email].forEach((f) => f.removeAttribute("aria-invalid"));
    const bad = !name.value.trim() ? name : !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.value) ? email : null;
    if (bad) { bad.setAttribute("aria-invalid", "true"); err.textContent = bad === name ? "Indiquez votre nom." : "Indiquez un courriel valide."; err.hidden = false; bad.focus(); return; }
    err.hidden = true; done.hidden = false; // TODO: POST to the CRM / form endpoint
  });
})();

// ===== Voice player =====
(() => {
  const a = document.getElementById("vaudio"), btn = document.getElementById("vplay"), wave = document.getElementById("vwave"), time = document.getElementById("vtime");
  if (!a || !btn) return;
  const bars = [...wave.children]; bars.forEach((b, i) => b.style.setProperty("--n", i % 12));
  const fmt = (s) => Math.floor(s / 60) + ":" + String(Math.floor(s % 60)).padStart(2, "0");
  const dur = () => (isFinite(a.duration) && a.duration) || 16;
  const paint = () => {
    const p = a.currentTime / dur(), n = Math.round(p * bars.length);
    bars.forEach((b, i) => b.classList.toggle("on", i < n));
    time.textContent = a.paused && a.currentTime === 0 ? fmt(dur()) : fmt(a.currentTime);
    wave.setAttribute("aria-valuenow", Math.round(a.currentTime)); wave.setAttribute("aria-valuemax", Math.round(dur()));
    wave.setAttribute("aria-valuetext", Math.round(a.currentTime) + " secondes sur " + Math.round(dur()));
  };
  const set = (on) => { btn.classList.toggle("on", on); btn.setAttribute("aria-label", on ? "Mettre l'audio en pause" : "Écouter la présentation de Kiwili (" + Math.round(dur()) + " secondes)"); };
  btn.addEventListener("click", () => { if (a.paused) a.play().catch(() => set(false)); else a.pause(); });
  a.addEventListener("play", () => set(true)); a.addEventListener("pause", () => set(false));
  a.addEventListener("ended", () => { a.currentTime = 0; set(false); paint(); });
  a.addEventListener("timeupdate", paint); a.addEventListener("loadedmetadata", paint);
  const seek = (e) => { const r = wave.getBoundingClientRect(); a.currentTime = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width)) * dur(); paint(); };
  wave.addEventListener("click", seek);
  wave.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") a.currentTime = Math.min(dur(), a.currentTime + 2);
    else if (e.key === "ArrowLeft") a.currentTime = Math.max(0, a.currentTime - 2);
    else if (e.key === " " || e.key === "Enter") { e.preventDefault(); btn.click(); } else return;
    e.preventDefault(); paint();
  });
  const wrap = document.getElementById("voice");
  if (wrap) new IntersectionObserver((es, o) => { if (es[0].isIntersecting) { wrap.classList.add("in"); o.disconnect(); } }, { threshold: 0.4 }).observe(wrap);
  paint();
})();

// ===== Claude section: example conversations =====
(() => {
  const body = document.getElementById("chat-body"); if (!body) return;
  const prompts = [...document.querySelectorAll(".prompt")];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const rows = (r) => r.map((x) => `<tr><td>${x[0]}</td><td class="late">${x[1]}</td><td class="r">${x[2]}</td></tr>`).join("");
  const confirm = (title, lines, ok, done, cancel) => `<div class="confirm"><h4>${title}</h4><dl>${lines.map((l) => `<dt>${l[0]}</dt><dd>${l[1]}</dd>`).join("")}</dl><div class="row"><button class="cbtn ok" type="button" data-done="${done}">${ok}</button><button class="cbtn" type="button" data-cancel="${cancel}">Annuler</button></div></div>`;
  const scenes = [
    { user: prompts[0]?.textContent.trim(), tool: "Kiwili · factures",
      bot: `<p>Trois factures sont en retard, pour un total de <b>8 355,50 $</b> :</p><table class="rtable"><thead><tr><th>Client</th><th>Retard</th><th class="r">Montant</th></tr></thead><tbody>${rows([["Construction Tremblay", "47 jours", "4 280,00 $"], ["Rénovation Laval", "33 jours", "2 915,50 $"], ["ACME Inc.", "12 jours", "1 160,00 $"]])}</tbody></table><p>Voulez-vous que je rédige une relance pour les factures de plus de 30 jours ?</p>` },
    { user: prompts[1]?.textContent.trim(), tool: "Kiwili · heures et factures",
      bot: `<p>Sur le projet Rénovation Laval, <b>42,5 h</b> ne sont pas encore facturées. Voici la facture que je propose :</p>` + confirm("Nouvelle facture · Rénovation Laval", [["42,5 h × 125,00 $", "5 312,50 $"], ["TPS 5 %", "265,63 $"], ["TVQ 9,975 %", "529,92 $"], ["Total", "6 108,05 $"]], "Créer la facture", "Facture 0043 créée dans Kiwili.", "Rien n'a été créé.") },
    { user: prompts[2]?.textContent.trim(), tool: "Kiwili · feuilles de temps",
      bot: `<p>Je m'apprête à inscrire cette entrée de temps :</p>` + confirm("Nouvelle entrée de temps", [["Projet", "Agrandissement Dupuis"], ["Tâche", "Plans préliminaires"], ["Date", "Hier"], ["Durée", "3 h"]], "Inscrire les heures", "3 h inscrites sur Plans préliminaires.", "Rien n'a été inscrit.") },
  ];
  let token = 0;
  const wire = (el) => {
    el.querySelectorAll("[data-done]").forEach((b) => b.addEventListener("click", () => { b.closest(".confirm").outerHTML = `<div class="ok-msg">✓ ${b.dataset.done}</div>`; }));
    el.querySelectorAll("[data-cancel]").forEach((b) => b.addEventListener("click", () => { b.closest(".confirm").outerHTML = `<p>${b.dataset.cancel}</p>`; }));
  };
  const play = async (i) => {
    const tk = ++token, s = scenes[i];
    prompts.forEach((p, k) => { p.classList.toggle("on", k === i); p.setAttribute("aria-selected", k === i); });
    body.innerHTML = "";
    const u = document.createElement("div"); u.className = "msg user"; body.appendChild(u);
    if (reduce) u.textContent = s.user; else { for (let c = 1; c <= s.user.length; c++) { if (tk !== token) return; u.textContent = s.user.slice(0, c); await sleep(16); } await sleep(350); }
    if (tk !== token) return;
    const b = document.createElement("div"); b.className = "msg bot";
    b.innerHTML = `<span class="tool${reduce ? " done" : ""}"><i></i>${s.tool}</span>` + (reduce ? s.bot : `<div class="dots"><i></i><i></i><i></i></div>`);
    body.appendChild(b);
    if (reduce) { wire(b); return; }
    await sleep(1100); if (tk !== token) return;
    b.innerHTML = `<span class="tool done"><i></i>${s.tool}</span>` + s.bot; wire(b);
  };
  prompts.forEach((p, i) => p.addEventListener("click", () => play(i)));
  let started = false;
  new IntersectionObserver((es, o) => { if (es[0].isIntersecting && !started) { started = true; play(0); o.disconnect(); } }, { threshold: 0.3 }).observe(body);
  if (reduce) play(0);
})();

// ===== Copy buttons =====
document.querySelectorAll("[data-copy]").forEach((btn) => btn.addEventListener("click", async () => {
  const el = document.getElementById(btn.dataset.copy); if (!el) return;
  const done = () => { const t = btn.textContent; btn.textContent = "Copié"; setTimeout(() => (btn.textContent = t), 1600); };
  try { await navigator.clipboard.writeText(el.textContent.trim()); done(); }
  catch (e) { const r = document.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); }
}));
