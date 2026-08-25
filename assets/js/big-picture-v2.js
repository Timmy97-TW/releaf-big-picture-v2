/* =============================================================================
   ReLeaf: the big picture, V2
   -----------------------------------------------------------------------------
   Three jobs, and no fourth.

     1  reveal      the one-shot entrance, matching .rise elsewhere on the page
     2  emphasis    pointing at something lights the run it belongs to
     3  the dial    the share at the end, and the hundred squares under it

   NOTHING OPENS. There is no panel to build, no state to remember and no route
   to change. Every word on this page is in the markup before this file runs, so
   the page is complete with scripting off. If a future edit starts storing
   content in here, the section has stopped doing its job.

   THE LIGHTING RULES, IN FULL

     a step       lights itself and the work that feeds it, and the moments in
                  the week at the end that come out of it
     a tile       lights itself, the step it feeds, every step after that one
                  and the segments between them. That is the answer to the only
                  question worth asking of a figure like this: how does my work
                  reach a farm. It also MARKS, in amber, the pieces it talks to
                  elsewhere, so the web of who-talks-to-whom shows without
                  permanent lines turning the trunk into a hairball. Cross-links
                  live in data-with.
     a moment     lights the step it came out of, so a reader who scrolls back
                  finds the part of the machine that produced it

   Segments carry data-flow rather than data-lit, because a segment belongs to
   the gap after a step rather than to the step itself.
   ========================================================================== */

(function () {
  "use strict";

  var spine = document.getElementById("spine");

  /* ------------------------------------------------------------- 3  dial --- */
  /* Built first, because it is independent of the figure and must work even if
     the figure is not on the page. The hundred squares are drawn here rather
     than sitting in the markup as a hundred empty elements. */

  (function () {
    var input = document.getElementById("share");
    var grid  = document.getElementById("dial-grid");
    var val   = document.getElementById("dial-val");
    var read  = document.getElementById("dial-read");
    if (!input || !grid) return;

    var cells = [], i;
    for (i = 0; i < 100; i++) cells.push(document.createElement("i"));
    cells.forEach(function (c) { grid.appendChild(c); });

    var WORDS = ["No", "Five percent of", "A tenth of", "Fifteen percent of",
                 "A fifth of", "A quarter of", "Thirty percent of", "Thirty five percent of",
                 "A third of", "Forty five percent of", "Half", "Fifty five percent of",
                 "Three fifths of", "Sixty five percent of", "Seventy percent of",
                 "Three quarters of", "Eighty percent of", "Eighty five percent of",
                 "Ninety percent of", "Ninety five percent of", "All"];

    function paint() {
      var n = Number(input.value);
      for (var k = 0; k < 100; k++) {
        if (k < n) cells[k].setAttribute("data-on", "");
        else cells[k].removeAttribute("data-on");
      }
      if (val) val.textContent = n + "%";
      if (read) {
        read.innerHTML = "<b>What that buys, honestly</b>" + WORDS[n / 5] +
          " the small-farm land in that band, and nothing more than that yet. " +
          "The share is true by construction. The two things that would turn it into a " +
          "quantity are below, and both are ours to close.";
      }
    }
    input.addEventListener("input", paint);
    paint();
  })();

  if (!spine) return;

  var nodes   = [].slice.call(spine.querySelectorAll(".node"));
  var links   = [].slice.call(spine.querySelectorAll(".link"));
  var tasks   = [].slice.call(spine.querySelectorAll(".task"));
  var moments = [].slice.call(document.querySelectorAll(".moment"));

  /* The trajectory in the tile for "Design and docking". Forty-six frames of
     our own 30 ns run live in data attributes on the SVG, so with scripting off
     the drawing is a still frame and nothing on this page moves on its own. The
     frames are stepped here rather than by SMIL, which wedges its timeline if
     you pause it before it has ever run. It plays only while the tile it
     belongs to is pointed at or focused, which folds it into the highlight
     primitive rather than adding a third one that never stops. */
  var mdSvg   = document.querySelector(".task--md .mdanim");
  var mdOwner = document.getElementById("t-docking");
  var mdOn    = false;

  /* ---------------------------------------------------------- 1  reveal --- */

  var reduced = window.matchMedia &&
                window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var mdFrames, mdChain, mdTip, mdX, mdY, mdRaf = 0, mdT0 = 0, mdAt = -1;
  if (mdSvg && !reduced) {
    mdFrames = (mdSvg.getAttribute("data-frames") || "").split(";");
    mdX      = (mdSvg.getAttribute("data-tipx")   || "").split(";");
    mdY      = (mdSvg.getAttribute("data-tipy")   || "").split(";");
    mdChain  = mdSvg.querySelector(".md-chain");
    mdTip    = mdSvg.querySelector(".md-tip");
    if (mdFrames.length < 2 || !mdChain) mdSvg = null;
  }

  var MD_MS = 74;                        /* per frame; 46 frames is a 3.4 s loop */

  function mdStep(ts) {
    if (!mdT0) mdT0 = ts;
    var i = Math.floor((ts - mdT0) / MD_MS) % mdFrames.length;
    if (i !== mdAt) {
      mdAt = i;
      mdChain.setAttribute("d", mdFrames[i]);
      if (mdTip) { mdTip.setAttribute("cx", mdX[i]); mdTip.setAttribute("cy", mdY[i]); }
    }
    mdRaf = window.requestAnimationFrame(mdStep);
  }

  function md(run) {
    if (!mdSvg || reduced || mdOn === run) return;
    mdOn = run;
    if (run) {
      mdT0 = 0;
      mdRaf = window.requestAnimationFrame(mdStep);
    } else {
      window.cancelAnimationFrame(mdRaf);
      mdRaf = 0; mdAt = 0;
      mdChain.setAttribute("d", mdFrames[0]);          /* back to the first frame */
      if (mdTip) { mdTip.setAttribute("cx", mdX[0]); mdTip.setAttribute("cy", mdY[0]); }
    }
  }

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
    md(false);
    spine.removeAttribute("data-focus");
    nodes.forEach(function (n) { n.removeAttribute("data-lit"); });
    links.forEach(function (l) { l.removeAttribute("data-flow"); });
    tasks.forEach(function (t) { t.removeAttribute("data-lit"); t.removeAttribute("data-rel"); });
    moments.forEach(function (m) { m.removeAttribute("data-lit"); });
  }

  function at(el) { return Number(el.getAttribute("data-at") || el.getAttribute("data-node") || 0); }

  /* the quiet half. A tile names the pieces of work it talks to, usually in
     another part of the team, and pointing at it marks them. Marked, not lit,
     so the run down the trunk stays the loud thing. */
  function relate(el) {
    (el.getAttribute("data-with") || "").split(/\s+/).forEach(function (id) {
      if (!id) return;
      var t = document.getElementById(id);
      if (t && !t.hasAttribute("data-lit")) t.setAttribute("data-rel", "");
    });
  }

  /* light the trunk from one step downward, segments included */
  function runOut(from) {
    nodes.forEach(function (n) { if (at(n) >= from) n.setAttribute("data-lit", ""); });
    links.forEach(function (l) {
      if (Number(l.getAttribute("data-seg")) >= from) l.setAttribute("data-flow", "");
    });
  }

  function show(el) {
    clear();
    spine.setAttribute("data-focus", "1");

    if (el.classList.contains("moment")) {                /* a moment in the week */
      el.setAttribute("data-lit", "");
      var n = nodes[at(el) - 1];
      if (n) n.setAttribute("data-lit", "");
      return;
    }

    if (el.classList.contains("node")) {                  /* a step */
      el.setAttribute("data-lit", "");
      var here = at(el);
      tasks.forEach(function (t) { if (at(t) === here) t.setAttribute("data-lit", ""); });
      moments.forEach(function (m) { if (at(m) === here) m.setAttribute("data-lit", ""); });
      return;
    }

    if (el.classList.contains("task")) {                  /* a piece of work */
      el.setAttribute("data-lit", "");
      if (el === mdOwner) md(true);
      runOut(at(el));
      relate(el);                  /* after, so a lit step is never also marked */
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
  tasks.forEach(function (t) { wire(t, t); });
  moments.forEach(function (m) { wire(m, m); });

  spine.addEventListener("pointerleave", clear);
})();
