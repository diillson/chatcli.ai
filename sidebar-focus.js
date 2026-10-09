/*
 * Section focus for the Mintlify sidebar.
 *
 * Opening a page inside one of the Documentation sections (Coder, Agents,
 * Tools, ...) narrows the sidebar to that section: the other sections and
 * the Get started group slide away and a "‹ Section" header takes their
 * place. Clicking the header brings the full list back; clicking a section
 * in the list narrows to it again. Pages outside the sections (the home
 * page, Get started) keep the full list.
 *
 * Mintlify renders a section as an <li data-title> without an id whose
 * first child is the expand <button aria-expanded>, directly under the
 * group's <ul class="sidebar-group">; pages are <li id="/path">, and the
 * section holding the current page carries data-active="true". The script
 * only adds data-* attributes and one button, so every rule it relies on
 * lives in style.css. It is idempotent, survives React re-renders through
 * a throttled MutationObserver, and is a silent no-op if Mintlify changes
 * its markup: the sidebar then simply stays as Mintlify draws it.
 */
(function () {
  "use strict";

  var focused = null; // title of the focused section, or null for the list
  var exitedOn = null; // pathname where the reader chose the full list
  var lastPath = null;

  function sections(nav) {
    var out = [];
    var items = nav.querySelectorAll("ul.sidebar-group > li[data-title]");
    for (var i = 0; i < items.length; i++) {
      var li = items[i];
      if (li.id) continue; // a page, not a section
      var btn = li.firstElementChild;
      if (btn && btn.tagName === "BUTTON" && btn.hasAttribute("aria-expanded")) {
        out.push(li);
      }
    }
    return out;
  }

  // The section holding the current page: the one Mintlify marks active,
  // or the one containing the page's <li id="/path">.
  function activeSection(nav, path) {
    var list = sections(nav);
    for (var i = 0; i < list.length; i++) {
      if (list[i].getAttribute("data-active") === "true") return list[i];
    }
    var clean = path.replace(/\/+$/, "") || "/";
    for (var j = 0; j < list.length; j++) {
      var pages = list[j].querySelectorAll("li[id]");
      for (var k = 0; k < pages.length; k++) {
        if (pages[k].id === clean) return list[j];
      }
    }
    return null;
  }

  function isPortuguese() {
    return /^\/pt(\/|$)/.test(window.location.pathname);
  }

  // The header sits right before the section list, outside the elements
  // React renders the list into.
  function backButton(nav) {
    var b = nav.previousElementSibling;
    if (b && b.classList.contains("cc-nav-back")) return b;
    b = document.createElement("button");
    b.type = "button";
    b.className = "cc-nav-back";
    b.innerHTML =
      '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" ' +
      'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="m15 18-6-6 6-6"/></svg><span class="cc-nav-back-label"></span>';
    b.addEventListener("click", function () {
      focused = null;
      exitedOn = window.location.pathname;
      collapseAll(nav);
      apply(true, false);
    });
    b.hidden = true;
    nav.parentElement.insertBefore(b, nav);
    return b;
  }

  // The full list shows section names only, as on first load: any section
  // left open by the focus is collapsed on the way back.
  var collapsing = false;
  function collapseAll(nav) {
    var list = sections(nav);
    collapsing = true;
    try {
      for (var i = 0; i < list.length; i++) {
        var btn = list[i].firstElementChild;
        if (btn && btn.getAttribute("aria-expanded") === "true") btn.click();
      }
    } finally {
      collapsing = false;
    }
  }

  // Mintlify opens the section of the current page by itself; this only
  // catches the case where it did not. It waits for Mintlify to settle and
  // stands down if the reader clicked in the meantime, since a click on an
  // opening section would close it.
  var lastClick = 0;
  function expandLater(li) {
    var title = li.getAttribute("data-title");
    window.setTimeout(function () {
      try {
        if (Date.now() - lastClick < 1500 || focused !== title || !li.isConnected) return;
        var btn = li.firstElementChild;
        if (btn && btn.getAttribute("aria-expanded") === "false") btn.click();
      } catch (_) {
        /* ignore */
      }
    }, 600);
  }

  function animate(nav, dir) {
    nav.classList.remove("cc-nav-in", "cc-nav-out");
    // restart the animation
    void nav.offsetWidth;
    nav.classList.add(dir === "in" ? "cc-nav-in" : "cc-nav-out");
  }

  // expand: open the focused section if it is collapsed. Only for focus
  // that follows a navigation; after the reader's own click Mintlify is
  // already opening it, and a second click would close it again.
  function apply(animated, expand) {
    var navs = document.querySelectorAll("#navigation-items");
    for (var n = 0; n < navs.length; n++) {
      var nav = navs[n];
      try {
        var list = sections(nav);
        if (!list.length) {
          nav.removeAttribute("data-cc-focus");
          continue;
        }
        var target = null;
        for (var i = 0; i < list.length; i++) {
          if (focused && list[i].getAttribute("data-title") === focused) target = list[i];
        }
        var was = nav.hasAttribute("data-cc-focus");
        for (var j = 0; j < list.length; j++) {
          if (list[j] === target) list[j].setAttribute("data-cc-focused", "1");
          else list[j].removeAttribute("data-cc-focused");
        }
        var back = backButton(nav);
        if (!target) {
          back.hidden = true;
          nav.removeAttribute("data-cc-focus");
          if (animated && was) animate(nav, "out");
          continue;
        }
        back.querySelector(".cc-nav-back-label").textContent = focused;
        back.setAttribute(
          "aria-label",
          isPortuguese() ? "Voltar para todas as seções" : "Back to all sections"
        );
        back.hidden = false;
        nav.setAttribute("data-cc-focus", "1");
        var btn = target.firstElementChild;
        if (expand && btn && btn.getAttribute("aria-expanded") === "false") expandLater(target);
        if (animated && !was) animate(nav, "in");
      } catch (_) {
        /* markup changed — leave the sidebar as Mintlify draws it */
      }
    }
  }

  // On every navigation, follow the section that holds the current page,
  // unless the reader just asked for the full list on this same page.
  function sync() {
    var path = window.location.pathname;
    // Same page: keep the reader's choice. A page with no focus yet tries
    // again, since the sidebar may not have rendered on the first pass.
    if (path === lastPath && (focused !== null || exitedOn !== null)) {
      apply(false, false);
      return;
    }
    lastPath = path;
    if (exitedOn !== path) exitedOn = null;
    if (exitedOn === null) {
      focused = null;
      var navs = document.querySelectorAll("#navigation-items");
      for (var n = 0; n < navs.length && !focused; n++) {
        var active = activeSection(navs[n], path);
        if (active) focused = active.getAttribute("data-title");
      }
    }
    apply(false, true);
  }

  // A click on a section in the full list narrows to it. An expanded section
  // would collapse on that click, so the click is kept from reaching it.
  document.addEventListener(
    "click",
    function (ev) {
      try {
        if (collapsing) return;
        lastClick = Date.now();
        var btn = ev.target && ev.target.closest && ev.target.closest("button[aria-expanded]");
        if (!btn) return;
        var li = btn.parentElement;
        var nav = li && li.closest("#navigation-items");
        if (!nav || nav.hasAttribute("data-cc-focus")) return;
        if (sections(nav).indexOf(li) < 0) return;
        focused = li.getAttribute("data-title");
        exitedOn = null;
        if (btn.getAttribute("aria-expanded") === "true") {
          ev.preventDefault();
          ev.stopPropagation();
        }
        window.requestAnimationFrame(function () {
          apply(true, false);
        });
      } catch (_) {
        /* ignore */
      }
    },
    true
  );

  var scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () {
      scheduled = false;
      sync();
    });
  }

  function start() {
    sync();
    try {
      new MutationObserver(schedule).observe(document.body, {
        childList: true,
        subtree: true
      });
    } catch (_) {
      /* no observer — first paint only */
    }
    window.addEventListener("popstate", schedule);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
