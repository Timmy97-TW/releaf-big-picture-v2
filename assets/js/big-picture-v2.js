/* =============================================================================
   ReLeaf: the big picture, V2
   -----------------------------------------------------------------------------
   Two jobs, and no third.

     1  reveal      the one-shot entrance, matching .rise elsewhere on the page
     2  emphasis    pointing at something lights the run it belongs to

   NOTHING OPENS. There is no panel to build, no state to remember and no route
   to change. Every word on this page is in the markup before this file runs, so
   the page is complete with scripting off. If a future edit starts storing
   content in here, the section has stopped doing its job.

   THE LIGHTING RULES, IN FULL

     a node       lights itself and the work that feeds it
     a card       lights itself, the node it feeds, every node after that one,
                  the segments between them, and the map at the end. That is
                  the answer to the only question worth asking of a figure like
                  this: how does my work reach a farm. It also MARKS, in amber,
                  the pieces it talks to elsewhere, so the web of who-talks-to
                  -whom shows without permanent lines turning the trunk into a
                  hairball. Cross-links live in data-with.
     the map      lights itself and marks what feeds it
     a zone       in the key, lights every card that belongs to it
     a moment     in the week at the end, lights the node it came out of, so a
                  reader who scrolls back finds the verb that produced it

   Segments carry data-flow rather than data-lit, because a segment belongs to
   the gap after a node rather than to the node itself.
   ========================================================================== */

(function () {
  "use strict";

  var spine = document.getElementById("spine");
  if (!spine) return;

  var bridge  = document.getElementById("bridge");
  var nodes   = [].slice.call(spine.querySelectorAll(".node"));
  var links   = [].slice.call(spine.querySelectorAll(".link"));
  var chips   = [].slice.call(spine.querySelectorAll(".chip"));
  var moments = [].slice.call(document.querySelectorAll(".moment"));
  var keys    = [].slice.call(spine.querySelectorAll(".key__item"));

  /* ---------------------------------------------------------- 1  reveal --- */

  var reduced = window.matchMedia &&
                window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!reduced && "IntersectionObserver" in window) {
    spine.classList.add("will-rise");
    new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("in");
        obs.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -12% 0px" }).observe(spine);

    /* Belt and braces. If the observer never fires, because the tab was in the
       background at load or because a browser we have not tested does not run
       it, the figure must still appear. It is never allowed to stay hidden. */
    window.setTimeout(function () { spine.classList.add("in"); }, 1400);
  }

  /* -------------------------------------------------------- 2  emphasis --- */

  function clear() {
    spine.removeAttribute("data-focus");
    nodes.forEach(function (n) { n.removeAttribute("data-lit"); });
    links.forEach(function (l) { l.removeAttribute("data-flow"); });
    chips.forEach(function (c) { c.removeAttribute("data-lit"); c.removeAttribute("data-rel"); });
    keys.forEach(function (k) { k.removeAttribute("data-lit"); });
    moments.forEach(function (m) { m.removeAttribute("data-lit"); });
    if (bridge) { bridge.removeAttribute("data-lit"); bridge.removeAttribute("data-rel"); }
  }

  function at(el) { return Number(el.getAttribute("data-at") || el.getAttribute("data-node") || 0); }

  /* the quiet half. A card names the pieces of work it talks to, usually in
     another zone, and pointing at it marks them. Marked, not lit, so the run
     down the trunk stays the loud thing. */
  function relate(el) {
    (el.getAttribute("data-with") || "").split(/\s+/).forEach(function (id) {
      if (!id) return;
      var t = document.getElementById(id);
      if (t && !t.hasAttribute("data-lit")) t.setAttribute("data-rel", "");
    });
  }

  /* light the trunk from one node downward, segments included */
  function runOut(from) {
    nodes.forEach(function (n) {
      if (at(n) >= from) n.setAttribute("data-lit", "");
    });
    links.forEach(function (l) {
      if (Number(l.getAttribute("data-seg")) >= from) l.setAttribute("data-flow", "");
    });
    if (bridge) bridge.setAttribute("data-lit", "");
  }

  function show(el) {
    clear();
    spine.setAttribute("data-focus", "1");

    if (el === bridge) {                                  /* the map */
      bridge.setAttribute("data-lit", "");
      relate(el);
      return;
    }

    if (el.classList.contains("moment")) {                /* a moment in the week */
      el.setAttribute("data-lit", "");
      var n = nodes[at(el) - 1];
      if (n) n.setAttribute("data-lit", "");
      return;
    }

    if (el.classList.contains("node")) {                  /* a node */
      el.setAttribute("data-lit", "");
      var here = at(el);
      chips.forEach(function (c) { if (at(c) === here) c.setAttribute("data-lit", ""); });
      moments.forEach(function (m) { if (at(m) === here) m.setAttribute("data-lit", ""); });
      return;
    }

    if (el.classList.contains("key__item")) {             /* a whole zone */
      el.setAttribute("data-lit", "");
      var zone = el.getAttribute("data-zone");
      chips.forEach(function (c) {
        if (c.getAttribute("data-feeds") === zone) c.setAttribute("data-lit", "");
      });
      return;
    }

    if (el.classList.contains("chip")) {                  /* a piece of work */
      el.setAttribute("data-lit", "");
      runOut(at(el));
      relate(el);                  /* after, so a lit node is never also marked */
    }
  }

  /* Pointer and keyboard reach the same code path. Touch lands on pointerenter
     in every browser we have, and because nothing is hidden behind the
     emphasis, a device that never fires it loses nothing. */
  function wire(el, target) {
    el.addEventListener("pointerenter", function () { show(target); });
    el.addEventListener("pointerleave", clear);
    el.addEventListener("focus", function () { show(target); });
    el.addEventListener("blur", clear);
  }

  nodes.forEach(function (n) { wire(n.querySelector(".node__core"), n); });
  chips.forEach(function (c) { wire(c, c); });
  moments.forEach(function (m) { wire(m, m); });
  keys.forEach(function (k) { wire(k, k); });
  if (bridge) wire(bridge, bridge);

  spine.addEventListener("pointerleave", clear);
})();
