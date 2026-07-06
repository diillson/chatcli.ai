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

  // Matching is by language stem on the element's own text, because Mintlify
  // renders variant labels ("Brazilian Portuguese", "Português (Brasil)") and
  // may nest icons (e.g. the selected-item check) beside the label.
  function flagFor(label) {
    var t = label.toLowerCase();
    if (t.indexOf("portug") !== -1) return "🇧🇷";
    if (t.indexOf("english") !== -1) return "🇺🇸";
    return null;
  }

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
        // Decorate the element's OWN text node, so labels sitting next to
        // nested icons (selected-item check, chevrons) still match.
        var textNode = null;
        for (var c = 0; c < el.childNodes.length; c++) {
          var n = el.childNodes[c];
          if (n.nodeType === 3 && n.data && n.data.trim().length > 1) {
            textNode = n;
            break;
          }
        }
        if (!textNode) continue;
        var label = textNode.data.replace(/\s+/g, " ").trim();
        var flag = flagFor(label);
        if (!flag || label.indexOf(flag) !== -1) continue;
        el.setAttribute("data-lang-flag", "1");
        textNode.data = textNode.data.replace(label, flag + " " + label);
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
