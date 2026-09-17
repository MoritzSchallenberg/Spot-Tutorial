/* ==========================================================================
   Re-run Mermaid after a StatiCrypt decrypt.

   sphinxcontrib-mermaid renders every `.mermaid`/`pre.mermaid` block once,
   on the page's "load" event, and exposes that render function globally as
   `window.runMermaid` (see its own default.js.j2 template). StatiCrypt
   protects the whole page by replacing the visible document with a
   password form and only writing the real page content in afterwards
   (via `document.write`) once the password is confirmed -- which happens
   *after* "load" has already fired once, on the password-prompt version of
   the page. Mermaid's own diagram blocks do not exist in the DOM yet at
   that point, so its one-time render pass finds nothing to draw, and
   nothing on either side re-triggers it once the real content lands.

   This never touches mermaid's own rendering logic -- it only calls the
   function that library already exposes, and only when there is
   demonstrably a diagram block sitting unrendered in the DOM.
   ========================================================================== */

(function () {
  'use strict';

  function hasUnrenderedMermaid() {
    var blocks = document.querySelectorAll('.mermaid, pre.mermaid');
    for (var i = 0; i < blocks.length; i++) {
      if (blocks[i].getAttribute('data-processed') !== 'true') {
        return true;
      }
    }
    return false;
  }

  var triggering = false;

  function maybeRerun() {
    if (triggering) return;
    if (typeof window.runMermaid !== 'function') return;
    if (!hasUnrenderedMermaid()) return;

    triggering = true;
    try {
      var result = window.runMermaid(false);
      if (result && typeof result.finally === 'function') {
        result.finally(function () {
          triggering = false;
        });
      } else {
        triggering = false;
      }
    } catch (e) {
      /* Nothing on this page needed it, or mermaid itself is not present
         (e.g. a page with no diagrams) -- not an error worth surfacing. */
      triggering = false;
    }
  }

  /* Pages without a password gate render mermaid diagrams on "load" as
     normal; this observer simply finds nothing to do on them. Pages behind
     the gate get their real content spliced in well after "load", which is
     exactly what this watches for. */
  var observer = new MutationObserver(function () {
    maybeRerun();
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });

  /* Also try once directly, in case the content is already present by the
     time this script runs (e.g. no password gate on this deployment). */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', maybeRerun);
  } else {
    maybeRerun();
  }
})();
