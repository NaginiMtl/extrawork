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

// ===== Hero product loop: counters, cursor click, status change, toast =====
(() => {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const $ = (id) => document.getElementById(id);
  const fmt = (n, d = 0) => new Intl.NumberFormat("fr-CA", { minimumFractionDigits: d, maximumFractionDigits: d }).format(n);
  const tween = (el, to, { suffix = "", dec = 0, from = 0, ms = 1400 } = {}) => {
    const t0 = performance.now();
    const step = (t) => {
      const p = Math.min((t - t0) / ms, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(from + (to - from) * e, dec) + suffix;
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const kpis = { k1: [1626583, " $", 0], k2: [3487238, " $", 0], k3: [70600, " $", 0], k4: [208.5, " h", 1] };
  Object.entries(kpis).forEach(([id, [v, s, d]]) => tween($(id), v, { suffix: s, dec: d }));

  const shot = $("shot"), cur = $("cursor"), tag = $("live-tag"), row = $("row-live"), toast = $("toast");
  if (!shot || !cur || !tag) return;
  let paid = false, k2 = 3487238;

  const loop = async () => {
    const sr = shot.getBoundingClientRect(), tr = tag.getBoundingClientRect();
    const x = tr.left - sr.left + tr.width / 2, y = tr.top - sr.top + tr.height / 2;
    cur.style.opacity = 1;
    await cur.animate([{ transform: `translate(${sr.width * 0.55}px,${sr.height * 0.85}px)` }, { transform: `translate(${x}px,${y}px)` }],
      { duration: 1400, easing: "cubic-bezier(.2,.7,.2,1)", fill: "forwards" }).finished;
    await cur.animate([{ scale: 1 }, { scale: 0.8 }, { scale: 1 }], { duration: 260 }).finished;
    paid = !paid;
    tag.className = "tag " + (paid ? "ok" : "wait");
    tag.textContent = paid ? "Payée" : "En attente";
    row.classList.remove("flash"); void row.offsetWidth; row.classList.add("flash");
    if (paid) {
      toast.classList.add("on");
      const next = k2 + 8912.5; tween($("k2"), next, { suffix: " $", from: k2, ms: 900 }); k2 = next;
      setTimeout(() => toast.classList.remove("on"), 2600);
    }
    await new Promise((r) => setTimeout(r, 900));
    await cur.animate({ opacity: [1, 0] }, { duration: 400, fill: "forwards" }).finished;
    setTimeout(loop, 2600);
  };
  setTimeout(loop, 2600);

  // gentle parallax tilt that follows the pointer
  const wrap = shot.parentNode;
  wrap.addEventListener("pointermove", (e) => {
    const r = wrap.getBoundingClientRect();
    shot.style.setProperty("--ry", ((e.clientX - r.left) / r.width - 0.5) * 4 + "deg");
    shot.style.setProperty("--rx", (0.5 - (e.clientY - r.top) / r.height) * 2 + "deg");
  });
  wrap.addEventListener("pointerleave", () => { shot.style.setProperty("--rx", "0deg"); shot.style.setProperty("--ry", "0deg"); });
})();
