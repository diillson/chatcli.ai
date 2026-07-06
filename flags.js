/*
 * Language-selector flags for the Mintlify chrome.
 *
 * Mintlify's current frontend ships a language→flag map but no longer renders
 * it (dead code in their bundle), so the selector shows bare language names.
 * This script decorates the selector with the flags again. It is deliberately
 * defensive: scoped to chrome containers only (never page content), idempotent
 * via a data attribute, resilient to re-renders through a throttled
 * MutationObserver, and a silent no-op if Mintlify changes its markup.
 */
(function () {
  "use strict";

  var FLAGS = {
    "English": "🇺🇸",
    "Portuguese": "🇧🇷",
    "Brazilian Portuguese": "🇧🇷",
    "Português": "🇧🇷",
    "Português (Brasil)": "🇧🇷"
  };

  // Only decorate inside chrome containers: the site header and floating
  // dropdown/popover portals. Never touch article/page content.
  var SCOPES = [
    "header",
    "[role='listbox']",
    "[role='menu']",
    "[data-radix-popper-content-wrapper]"
  ].join(",");

  function decorate() {
    var candidates;
    try {
      candidates = document.querySelectorAll(
        "button, [role='option'], [role='menuitem'], a, span"
      );
    } catch (_) {
      return;
    }
    for (var i = 0; i < candidates.length; i++) {
      var el = candidates[i];
      try {
        if (el.getAttribute("data-lang-flag")) continue;
        if (!el.closest || !el.closest(SCOPES)) continue;
        var label = (el.textContent || "").trim();
        var flag = FLAGS[label];
        if (!flag) continue;
        // Innermost match only: skip wrappers whose child carries the label.
        if (el.children.length > 0) continue;
        el.setAttribute("data-lang-flag", "1");
        el.textContent = flag + " " + label;
      } catch (_) {
        /* markup changed — degrade to plain labels */
      }
    }
  }

  var scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () {
      scheduled = false;
      decorate();
    });
  }

  function start() {
    decorate();
    try {
      new MutationObserver(schedule).observe(document.body, {
        childList: true,
        subtree: true
      });
    } catch (_) {
      /* no observer — first paint decoration only */
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
