(() => {
  const $ = (id) => document.getElementById(id);
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

  // reading progress
  const fill = $("read-fill"), art = document.querySelector("article");
  const onScroll = () => {
    const r = art.getBoundingClientRect(), total = r.height - innerHeight;
    fill.style.width = (total > 0 ? Math.min(1, Math.max(0, -r.top / total)) * 100 : 0) + "%";
  };
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  // sidebar: open on desktop, closed on small screens
  const side = $("side-wrap"), mq = matchMedia("(min-width: 961px)");
  const syncSide = () => { side.open = mq.matches; };
  syncSide(); mq.addEventListener("change", syncSide);

  // catalogue: filter by text and domain
  const rights = [...document.querySelectorAll(".right")], groups = [...document.querySelectorAll(".rgroup")];
  const q = $("q"), qTop = $("q-top"), chips = [...document.querySelectorAll(".gchip")];
  const count = $("rcount"), empty = $("rempty"); let dom = "all";
  const apply = () => {
    const t = norm(q.value.trim()); let n = 0;
    rights.forEach((r) => {
      const g = r.closest(".rgroup").dataset.g;
      const show = (dom === "all" || g === dom) && (!t || norm(r.dataset.s).includes(t));
      r.hidden = !show; if (show) n++;
    });
    groups.forEach((g) => { g.hidden = ![...g.querySelectorAll(".right")].some((r) => !r.hidden); });
    count.textContent = n + (n > 1 ? " droits affichés" : " droit affiché");
    empty.hidden = n > 0;
    if (t && n > 0 && n <= 3) rights.forEach((r) => { if (!r.hidden) r.open = true; });
  };
  q.addEventListener("input", () => { if (qTop.value !== q.value) qTop.value = q.value; apply(); });
  qTop.addEventListener("input", () => { q.value = qTop.value; apply(); });
  $("help-search").addEventListener("submit", (e) => { e.preventDefault(); q.value = qTop.value; apply(); $("droits").scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); });
  chips.forEach((c) => c.addEventListener("click", () => { dom = c.dataset.g; chips.forEach((k) => k.classList.toggle("on", k === c)); apply(); }));
  const expand = $("expand");
  expand.addEventListener("click", () => {
    const open = expand.dataset.open !== "1"; expand.dataset.open = open ? "1" : "0";
    rights.forEach((r) => { if (!r.hidden) r.open = open; });
    expand.textContent = open ? "Tout replier" : "Tout déplier";
  });

  // smooth open / close
  if (!reduce) rights.forEach((d) => {
    const s = d.querySelector("summary"); let anim = null;
    s.addEventListener("click", (e) => {
      e.preventDefault();
      const closed = s.offsetHeight, opening = !d.open;
      if (anim) anim.cancel();
      if (opening) d.open = true;
      const target = opening ? d.scrollHeight : closed, from = opening ? closed : d.offsetHeight;
      d.style.overflow = "hidden";
      anim = d.animate({ height: [from + "px", target + "px"] }, { duration: 360, easing: "cubic-bezier(.2,.7,.2,1)" });
      anim.onfinish = () => { if (!opening) d.open = false; d.style.height = d.style.overflow = ""; anim = null; if (opening) history.replaceState(null, "", "#" + d.id); };
      anim.oncancel = () => { d.style.height = d.style.overflow = ""; };
    });
  });
  else rights.forEach((d) => d.addEventListener("toggle", () => { if (d.open) history.replaceState(null, "", "#" + d.id); }));

  // deep links to a right
  const openHash = () => {
    const id = decodeURIComponent(location.hash.slice(1)); if (!id) return;
    const el = document.getElementById(id);
    if (el && el.classList.contains("right")) {
      chips[0].click(); q.value = ""; qTop.value = ""; apply();
      el.open = true; setTimeout(() => el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }), 60);
    }
  };
  openHash(); addEventListener("hashchange", openHash);

  // compare tabs
  document.querySelectorAll("[data-compare]").forEach((c) => {
    const tabs = [...c.querySelectorAll(".cmp-tabs button")], imgs = [...c.querySelectorAll(".cmp-stage img")];
    tabs.forEach((t, i) => t.addEventListener("click", () => {
      tabs.forEach((k, j) => { k.classList.toggle("on", j === i); k.setAttribute("aria-selected", j === i); });
      imgs.forEach((m, j) => m.classList.toggle("on", j === i));
    }));
  });

  // feedback (front-end only)
  const fb = $("fb"), done = $("fb-done");
  fb.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
    fb.hidden = true; done.hidden = false;
    done.textContent = b.dataset.v === "yes" ? "Merci pour votre retour." : "Merci. Dites-nous ce qui manque en contactant le support.";
  }));
})();
