# Entwicklungsauftrag 10 report — Quality pass, merge to main, publication attempt

**Not part of the published website.** Internal working document.
Excluded from the Sphinx build (outside `docs/`), not linked from any
published toctree.

## 1. Remote state verification (Section 2)

Verified before any work, matching what the task described:

- `origin` → `git@github-carologistics:MoritzSchallenberg/Learning-Robotics-Crash-Course.git`,
  confirmed to resolve to the correct account (`ssh -T` → "Hi
  MoritzSchallenberg!").
- `origin/main` = `c91dcae2d751687eac6e5b9dca22026ef13f7906`,
  `origin/feat/alert-spot-tutorial` = `f2e906b`, 22 commits ahead of
  `main`, 0 behind — exactly as stated.
- No SSH alias change was needed; access worked throughout.

**New finding during verification, not previously known:** the GitHub
repository itself has been renamed from `Learning-Robotics-Crash-Course`
to `Spot-Tutorial` (git push/fetch over the old remote URL still work
via GitHub's redirect; confirmed via the unauthenticated REST API,
which 301-redirects `repos/.../Learning-Robotics-Crash-Course` to
`repos/.../Spot-Tutorial`). The repository's **default branch is
`feat/initial-course-website`, not `main`**, and a pull request from
`feat/alert-spot-tutorial` was already merged into that branch outside
this session (visible as merge commit `787ca80` on
`origin/feat/initial-course-website`). You confirmed proceeding with
the merge into `main` as originally instructed regardless, with both
findings flagged here rather than silently assumed resolved. Neither
finding blocked any git operation in this session; both are worth your
attention separately from this task's own scope.

## 2. Scope discipline (Section 3)

No navigation redesign, no reintroduction of course/crash-course
language, no Carologistics content, no unevidenced technical claims.
Every content change this session cites its evidence source; no
working page was rewritten without a specific reason tied to a task
section. `scripts/verify-structure.py`'s existing banned-term and
navigation checks passed after every commit, unchanged in what they
guard against.

## 3–13. Content quality work (commits `c25efec`..`6840c43`)

Summarized by section — full detail in each commit message:

- **Section 4 (homepage):** replaced the three generic entry cards with
  task-based ones ("I want to operate Spot" / "understand the system" /
  "develop for Spot"), each linking directly to its specific target
  pages. Intro kept short before them; audience/software/historical/
  verification/supervision summary moved after, condensed.
- **Section 5 (Start Here):** `docs/start-here.md`, five learning paths
  (new operator, software developer, manipulation developer,
  autonomous-systems developer, troubleshooting), each with
  prerequisites, hardware requirement, read-only vs. supervised steps,
  and expected outcome. Linked from the homepage and given its own
  toctree caption.
- **Section 6 (history vs. current):** four historical operating
  screenshots now use an explicit "Historical context / Current
  implementation / Hardware verification required" triad. The 24-image
  History gallery now serves 480px JPEG thumbnails (~1 MB total,
  generated with Pillow, originals untouched) instead of the full-
  resolution originals (~20 MB), each `loading="lazy"` with explicit
  width/height, linking through to its unmodified original.
- **Section 7 (operating procedures):** all seven operating pages
  restructured to Purpose/Required supervision/Prerequisites/Initial
  state/Procedure/Expected observations/Verification/Stop conditions/
  Recovery/Final state, with every step annotated by which
  computer/role it runs on and whether it is read-only or can trigger
  motion. `recovery-and-troubleshooting.md` rebuilt entirely as a
  ten-case decision path (the required Cases 1–10), never recommending
  an automatic restart or movement attempt as a default fix.
- **Section 8 (operator checklist):** split into the five required
  phases (Before power-on / Before enabling motion / Before
  manipulation / Before shutdown / After shutdown) with the specific
  items requested. Print CSS extended so the sidebar, mobile top bar,
  breadcrumbs, and version selector are hidden and the content column
  uses the full page width when printed.
- **Section 9 (architecture legibility):** added a single top-level
  "At a glance" diagram to `architecture/index.md`. Auditing the six
  existing diagrams found two real accuracy issues (both fixed): two
  diagrams showed navigation's `/cmd_vel_stamped` output going directly
  to `spot_driver`, contradicting each page's own prose about an
  intermediate `stamped_twist_converter` node; the safety/stop-signal
  diagram mislabeled how the software E-stop endpoint reaches
  `spot_hardware_interface`'s activation check (it queries the SDK
  directly, not via the `status/estop` topic as originally drawn).
  Added explicit legends where dashed/solid lines carry meaning.
- **Section 10 (system status page):** `docs/reference/system-status.md`,
  a ten-row matrix (Documented / Found in code / Simulation-checked /
  Hardware-checked / Open question) — built earlier in this session
  alongside Sections 4–5, since `start-here.md` already needed to link
  to it.
- **Section 11 (troubleshooting decision path):** built together with
  Section 7's rebuild of `recovery-and-troubleshooting.md` (see above)
  rather than as a separate pass.
- **Section 12 (content relevance):** audit found most content already
  correctly classified from Entwicklungsauftrag 9 (KiCad/Fusion
  demoted from primary nav; ROS 2 basics/turtlesim reachable only via
  Required Knowledge; rescue-projects already Spot-tied). One real gap:
  `decision-making/planning-approaches.md`'s RAFCON subsection lacked
  the same "this is the Webots tutorial's tool, not what the real
  deployment uses" caveat already present on `decision-making/index.md`
  — added.
- **Section 13 (editorial tone):** targeted scan of core pages for
  marketing language, humor, and vague claims found none — the content
  was written objectively from the start in Entwicklungsauftrag 9, and
  the pre-existing 13-topic content already had its own dedicated
  "objective language pass" commit (`c91dcae`, the tip of `main` before
  this session).

## 14. Password gate technical check

**Secret existence check: blocked, not performed.** `gh` CLI had no
stored credentials and no token was available in this environment to
authenticate it (`gh auth login` needs an interactive browser flow not
available here). I installed `gh` locally but could not use
`gh secret list` — this specific check (Section 14's first instruction)
was not completed. See finding in §18 below: the deploy run's failure
is consistent with this secret being unset, which is itself indirect
evidence, not a substitute for the direct check.

**Everything else in Section 14 was verified end-to-end, locally,
against a real StatiCrypt-encrypted build (test-only password,
generated fresh, never committed, removed after testing):**

- Every one of 104 HTML pages in the build was encrypted (file count
  matched exactly before/after).
- Direct root access and direct subpage access both show the password
  prompt — subpages are protected, not only the homepage.
- A wrong password does not unlock the page.
- The correct password unlocks the page and shows the real content.
- After unlocking (with "Remember me"), navigation, search (12 results
  for a real query), dark mode toggle, and copy buttons (25 found on
  one page, functional) all continue to work.
- **What stays unencrypted, checked explicitly as required:**
  `searchindex.js` (plaintext — leaks page titles and section headings,
  e.g. "3D mapping", even without the password), `objects.inv` (binary
  Sphinx inventory, also unencrypted), everything under `_static/`
  (CSS/JS), and everything under `_images/` (every migrated photo is
  directly viewable at its own URL without the password). This matches
  what StatiCrypt is documented to do — it encrypts HTML content only,
  not assets — and is stated plainly in README.md's "Access
  protection" section. Nothing confidential is or should be in this
  repository regardless, per the Entwicklungsauftrag 9 security audits,
  so this is a known, accepted, documented limitation, not a new
  problem.

**Real bug found and fixed during this testing (commit `d9185d8`):**
none of the site's 7 Mermaid diagrams rendered behind the password
gate, even after entering the correct password — sphinxcontrib-mermaid
renders once on page "load", which fires before StatiCrypt injects the
real content. Fixed with a small MutationObserver script that calls
the render function StatiCrypt-unaware sphinxcontrib-mermaid already
exposes globally (`window.runMermaid`), only when an unrendered
diagram block is actually found. Verified fixed on all diagram pages,
with no regression on the plain (non-gated) site.

**Second real bug found and fixed (commit `b405e76`):** every
`- [ ]` checklist item across the site (not just this session's new
Operator Checklist — two pre-existing pages too) rendered as literal
"[ ] " text, not a real checkbox, because MyST's `tasklist` extension
was never enabled. Fixed; 29 real checkboxes now render on the
Operator Checklist alone.

## 15. GitHub Pages configuration check

**Could not query directly** — `GET /repos/.../pages` returns 404
unauthenticated even for this public repository (Pages settings
require authentication regardless of repo visibility). **Confirmed
indirectly, with strong evidence, via the live site and the Actions
run list**: pushing to `main` triggered a **separate, GitHub-managed
"pages build and deployment" run** (id `35206659642`) alongside our
own "Build and deploy site" workflow run — this generic run only
exists when Pages is configured as "Deploy from a branch". It
completed successfully within seconds of the push, and
`https://moritzschallenberg.github.io/Spot-Tutorial/` immediately
began serving a Jekyll-rendered version of the repository's root
`README.md` (title "ALeRT Spot Tutorial | Spot-Tutorial", confirmed
via direct fetch) — not our Sphinx-built site, and with no password
protection at all, since Jekyll has no knowledge of StatiCrypt.

**Conclusion: GitHub Pages is configured to deploy from a branch
(almost certainly `main`), not from GitHub Actions.** Per the task's
own rule, I am not claiming the site is published — it is, but as an
unprotected plain README rendering, not as this tutorial.

**Required manual step:** a repository owner must go to *Settings →
Pages → Build and deployment → Source* and change it from "Deploy from
a branch" to "GitHub Actions". I could not make this change — it
requires either repository admin access via the GitHub web UI or an
authenticated `gh`/API session with admin scope, neither available in
this session.

## 16. Local final test results

- `sphinx-build -E -a -W --keep-going`: clean, run after every commit.
- `scripts/verify-structure.py`: all checks pass, run after every
  commit.
- `scripts/verify-site.py`: **313/313 checks pass** (102 pages, both
  themes) on the final build — reached only after finding and fixing a
  false failure of my own making: an interrupted background-shell
  command left `/tmp/site-serve` with an incomplete copy of the build
  (missing `start-here.html` and `reference/system-status.html`),
  which the first two run attempts correctly reported as 404s. Verified
  the copy was complete (exact file-count match) before trusting the
  next run.
- Secret scan (reusing `.github/workflows/pages.yml`'s own patterns)
  against the full built output: 0 matches in all four categories.
- Absolute-path check (`href="/`/`src="/`): 0 matches.
- Carologistics / old crash-course terms / orphaned pages: covered by
  `verify-structure.py`, all pass.
- Mobile (390px), light mode, dark mode: covered by `verify-site.py`,
  all pass.
- Historical images: all 24 + 4 migrated images re-verified by SHA-256
  against their source files — unchanged.
- All 7 Mermaid diagrams: verified rendering both on the plain site and
  (after the fix above) behind the password gate.
- Search, copy buttons: verified functional both plain and gated.
- Operator Checklist print view: verified via Playwright's print-media
  emulation — sidebar `display: none`, content margin reset to `0px`,
  29 real checkboxes present (after the tasklist fix).
- Encrypted artifact test: built and encrypted locally with a
  throwaway test password (never the real one, never committed),
  tested end-to-end, removed afterward.

## 17. Integration to main

Preconditions checked before merging, per the task's explicit list:

- Working tree clean: yes.
- All local checks passed: yes (§16).
- No secrets found: yes (§16).
- Password secret present: **not verified** — this session could not
  check it (§14); the deploy failure in §18 is consistent with it being
  absent, which is the designed, safe failure mode, not a workaround
  taken.
- GitHub Pages enabled: yes, but misconfigured (§15) — not a
  precondition failure in the sense of "is it live at all", but the
  task's spirit ("will this actually publish the tutorial") is not yet
  met, and is stated as such rather than glossed over.

Per your explicit instruction to proceed with the merge regardless,
flagging both open items in this report: `feat/alert-spot-tutorial-polish`
was pushed (`origin/feat/alert-spot-tutorial-polish`), `main` was
fast-forwarded from `c91dcae` to `b405e76` (`git merge --ff-only`, no
force-push, no reset — `main` was confirmed still at `c91dcae` and an
ancestor of the polish branch immediately before merging) and pushed
to `origin/main`.

## 18. Deployment observation

Watched via the public, unauthenticated GitHub Actions API (no `gh`
auth available; confirmed this endpoint works unauthenticated for a
public repository, which substituted for `gh run watch`):

- `pages build and deployment` (classic Pages, run `35206659642`):
  **completed, success** — this is what is now live, per §15.
- `Build and deploy site` (our own workflow, run `35206661526`):
  **completed, failure.** Job-level breakdown: `Build the Sphinx site`
  failed at the **"Encrypt the site behind a password gate" step**
  specifically — every step before it (checkout, Python setup,
  dependency install, the Sphinx build itself, the secret scan, Node.js
  setup) succeeded. `Check external links` and `Upload the Pages
  artifact` were skipped as a result; the separate `Deploy to GitHub
  Pages` job was skipped entirely (`needs: build` never satisfied).
  `Build and test the example ROS 2 packages` (the independent
  `examples` job) succeeded.

  **I could not read the raw step log** — `GET .../actions/jobs/{id}/logs`
  returned 403 "Must have admin rights to Repository" even
  unauthenticated, for this public repo. Based on the step's own logic
  (it explicitly checks for `STATICRYPT_PASSWORD` and exits with an
  `::error::` message if absent, precisely so the workflow refuses to
  deploy unprotected rather than silently succeeding — this was a
  deliberate design decision from the previous session, re-verified as
  present in the merged code) and the fact that this secret has been a
  known, unresolved, pending manual step since that session's own final
  report, **this failure is very likely the intended "no secret, no
  deploy" behavior working as designed** — not a new defect. I cannot
  fully confirm this without either the raw log or the secret actually
  being set; recommend checking the Actions tab's log directly to
  confirm the exact error line before assuming this diagnosis is
  complete.

**Not "build green"; not glossed over.** The build job failed, so per
the task's own instruction this is reported as a failure requiring a
fix, not declared done.

## 19. Live verification

`https://moritzschallenberg.github.io/Spot-Tutorial/` was checked and
is reachable (not a 404), but is currently the classic-Pages Jekyll
rendering of `README.md`, not this Sphinx site — see §15. The specific
subpage URLs requested in Section 19 (`/about/alert-and-spot.html`,
`/safety/operator-checklist.html`, etc.) were **not checked against
the live site**, because checking them now would only confirm they
404 or serve unrelated Jekyll-routed content, which is already known
and explained by §15 — a live-URL check only becomes meaningful after
the Pages source is switched to GitHub Actions and a subsequent deploy
run succeeds. All of the same checks (password gate present on
subpages, wrong/correct password behavior, navigation, search,
diagrams, dark mode, no horizontal scroll, no console errors) **were**
performed against a locally-built and locally-encrypted copy of the
exact same commit (§14, §16) and passed.

## What is required to actually finish publishing (two independent manual steps)

1. **Set the `STATICRYPT_PASSWORD` secret** — *Settings → Secrets and
   variables → Actions* on the repository (now at
   `github.com/MoritzSchallenberg/Spot-Tutorial`) — using the password
   value from your own records (not restated here).
2. **Switch the Pages source to GitHub Actions** — *Settings → Pages →
   Build and deployment → Source* → "GitHub Actions" (currently
   "Deploy from a branch").

After both: re-run the `Build and deploy site` workflow (push a no-op
commit, or use *Actions → Build and deploy site → Run workflow* if
`workflow_dispatch` access is available), then re-check the live URLs
listed in Section 19 of the task.

## Summary (first pass)

`main` now contains the full ALeRT Spot Tutorial content, all local
tests passing, two real bugs found and fixed during this session's own
testing (Mermaid-behind-the-gate, missing checkboxes) that would
otherwise have shipped silently broken. Publication is not yet live in
the form this tutorial is meant to be seen — both blockers are
GitHub-account-level admin actions outside what this session could
perform without credentials, and are reported precisely rather than
assumed away.

---

## Second pass: a more detailed re-send of the same task

The task was re-sent twice more with substantially more specific
requirements for several sections. This second pass covers that
additional work, on top of everything above (which still stands —
nothing in the first pass was reverted).

### 1. Homepage and Start Here, rebuilt to the newer spec

`docs/index.md`'s three entry cards were relabeled and restructured per
the new wording: "Who are you?" (was "What do you want to do?"), cards
"New Spot operator" / "Spot software developer" / "Troubleshooting a
problem" (was task-based phrasing from the first pass), each ending
with a "→ Full [section]" link, plus a direct GitHub Issues link for
reporting mistakes.

`docs/start-here.md` was rewritten to four named paths instead of the
first pass's five: **First day with Spot**, **Software development**,
**Manipulator development**, **Autonomous rescue development** — the
standalone "Troubleshooting" path was removed (it now lives only as
the homepage card plus a "Related components" note explaining why, so
it isn't silently missing). Each path keeps its prerequisites/hardware/
read-only/supervision/outcome summary from the first pass's format.

One process note: this edit initially landed in a stale, disconnected
copy of the working directory that had appeared alongside the real one
(the environment relocated mid-session — see the git history for
`5e2bb7a`, which is where the corrected version actually landed after
this was caught and fixed).

### 2. Workspace context added to operating commands

Per the requirement that a command's `Location:` line say which ROS 2
workspace owns the package being launched, not just which computer:
`docs/operating/power-on.md` Steps 4–5 (`spot_estop.py` /
`spot_driver_plus` → `spot_ws`) and
`docs/operating/operating-the-manipulator.md` Steps 1–2
(`kortex_bringup` / `spot_gen3_moveit` → `man_ws`) now name the
workspace explicitly.

### 3. Deployment smoke test added

`.github/workflows/pages.yml` gained a `smoke-test` job (`needs:
deploy`) that curls the live homepage with a bounded retry budget (10 ×
10s), confirms the password-gate string is present on both the
homepage and a direct subpage request (`safety/operator-checklist.html`
— chosen because it exists in every build and is not the homepage, so
this genuinely tests "is a random subpage gated", not just the root),
and confirms `_static/css/custom.css` and `_static/js/color-mode.js`
both return 200. All of its literal assumptions (the page path
existing, the gate string actually appearing in the encrypted HTML, the
two asset paths existing) were checked locally against a real encrypted
build before relying on them.

### 4. Navigation simplification and image checks

Reviewed for thin pages worth merging and dead links worth redirecting;
found none — this site has never had a prior public deploy of its own
content (every previous deploy attempt failed before the deploy job
ran, and Pages currently serves an unrelated Jekyll README — see §15
above), so there is no old bookmarked URL structure to preserve via a
redirect. Checked all 52 images under `docs/_static/images` for
byte-identical duplicates (SHA-256, none found) and non-standard EXIF
orientation (none found) — a fuller sweep than the first pass's
spot-check of two images.

### 5. A real Mermaid regression, found and fixed differently this time

Re-testing the encrypted build from scratch this round found **all 6
architecture-diagram pages rendering zero diagrams** — the fix from the
first pass (commit `d9185d8`, a `MutationObserver` calling
`window.runMermaid(false)` on every DOM mutation) had regressed:
calling that function repeatedly in quick succession corrupts mermaid's
internal per-block state without ever actually drawing an SVG, which
was not caught before because the first pass's testing did not exercise
repeated rapid mutations the way `document.write()` injecting a full
page actually does.

Two further iterations before reaching a working fix, in order:

1. A one-shot `MutationObserver` (`runMermaid(true)`, fired once on the
   first `.mermaid` element observed) worked for **manual** password
   entry but not for **"remember me" auto-unlock** — all 6 pages still
   rendered zero diagrams when navigated to directly.
2. Waiting for the window `"load"` event before a short bounded poll
   seemed like the right fix (it is the same event
   sphinxcontrib-mermaid's own script waits for) — but instrumented
   testing showed `"load"` does not reliably fire at all after
   StatiCrypt's `document.write()`. On a "remember me" auto-unlock,
   `document.readyState` does reach `"complete"`, yet **no `"load"`
   event is ever dispatched to any listener — including
   sphinxcontrib-mermaid's own**, which also never ran in that case.
   Manual password entry only appeared to work because the placeholder
   gate page's own one-time `"load"` had already started this script's
   poll loop before the user finished typing, and the loop was still
   running when the real content landed moments later.

**The actual fix** (`docs/_static/js/mermaid-after-decrypt.js`, commit
`57018b6`): poll `document.readyState` directly instead of depending on
any event, with a 900ms settle delay once it first reads `"complete"`
(mermaid's own render is `async` and explicitly not safe to call
concurrently with a second pass — the settle delay gives it room to
finish on an ordinary page before this script ever checks whether
anything is still unrendered), then call `window.runMermaid(true)`
once if any `.mermaid`/`pre.mermaid` block still lacks an `<svg>`
child.

Verified, with an instrumented console-timeline test, across: manual
password entry (`data-flow.html`, 2 diagrams), same-context "remember
me" navigation across all 6 diagram-bearing pages, a fresh reload after
"remember me", and the plain non-gated site including a light/dark
theme toggle (which an earlier iteration of this fix had regressed:
diagram count dropping from 2 to 1 after toggling) — zero console
errors and correct diagram counts in every case.

### 6. Two real, previously-undetected content leaks in the deployment pipeline itself

Found while re-verifying the password gate ahead of merging. **Both
predate this round** — they are artifacts of how `sphinx-build` and
StatiCrypt have been invoked in `.github/workflows/pages.yml` since it
was first written, not something this round's content changes
introduced — and would have affected the very first successful deploy
once the missing secret is set, not just this round's commits.

1. **`sphinx-build` never specified a doctree directory**, so Sphinx
   used its own default of `docs/_build/html/.doctrees` — *inside* the
   directory that then gets encrypted and published. Those pickle files
   hold the full parsed content of every page (103 files, 4.3MB in this
   build). StatiCrypt only wraps `.html` files in its password template;
   everything else in the directory it is pointed at is copied straight
   through unencrypted. This meant the full text of every page —
   safety procedures, operating commands, architecture details — would
   have been readable at a predictable URL regardless of the password
   gate. Fixed by adding `-d docs/_build/doctrees`, a sibling of
   `docs/_build/html`, to the build command.
2. **Sphinx's built-in search index (`searchindex.js`) ships in
   plaintext** — it is a full-text index of effectively every word used
   on every page, and being a `.js` file (not `.html`), StatiCrypt has
   no way to gate it at all. There is no configuration flag that makes
   this file protectable; the only correct fix is to not publish it.
   Added a workflow step that deletes it from the *encrypted* output
   specifically, right after encryption — local development builds are
   unaffected and keep full in-site search. **Trade-off, stated
   plainly:** the published site's search box will not return results.
   This is intentional: the task is explicit that the password gate
   must be a real access hurdle, never a partial one, and a searchable
   plaintext index of the entire site's content directly undermines
   that.

Both fixed in commit `60b6e7b`. Re-verified locally end-to-end: rebuilt,
re-encrypted with a throwaway password, confirmed zero `.doctrees`/
`.pickle`/`.doctree` files and no `searchindex.js` anywhere in the
published output, and re-ran the full password-gate test suite (direct
subpage access gated, wrong password rejected, correct password works,
"remember me" navigation, no raw `.md` sources served, no `_sources/`
directory) — all pass.

### 7. Stale repository-name references, found and fixed

The GitHub repository was renamed in place from
`Learning-Robotics-Crash-Course` to `Spot-Tutorial` at some point after
Entwicklungsauftrag 8's `maintainers/rebrand-followups.md` explicitly
decided not to rename it. `docs/conf.py`'s `html_baseurl` and
`README.md`'s published "Website:" link still pointed at the old Pages
URL — confirmed via direct fetch that the old Pages URL now **404s**
(unlike the repository page itself, which GitHub does redirect on a
rename) — a real, live broken link, not a cosmetic inconsistency.
Fixed `html_baseurl`, README's website link and local-serving
instructions, `scripts/verify-site.py`'s matching example path and
`--base-url` default, and every hard-coded
`github.com/.../Learning-Robotics-Crash-Course` link across the
`videos.md`/`continue-learning.md` pages and `LICENSES.md` (these
still redirected correctly on `github.com`, so were not broken, but
were inconsistent with the canonical name). Logged in
`maintainers/rebrand-followups.md`. Commit `e691728`.

One link I initially "fixed" incorrectly and then reverted: the
homepage's GitHub Issues link
(`github.com/MoritzSchallenberg/Spot-Tutorial/issues/new`) was already
correct — I mistakenly assumed it was wrong because the local git
remote still says `Learning-Robotics-Crash-Course`, without checking
that the remote URL redirects fine and the *actual* current repository
name (confirmed via the API) is `Spot-Tutorial`. Caught before
committing.

### 8. Full local test suite, re-run clean after all of the above

- `sphinx-build -W --keep-going -d docs/_build/doctrees`: clean.
- `scripts/verify-structure.py`: all checks pass (11 primary-nav
  sections, 10 background directories).
- `scripts/verify-site.py`: **313/313 checks pass**, 102 pages, both
  themes (JS errors, 390px overflow, light/dark toggle, search, copy
  buttons, syntax highlighting, WCAG AA contrast, dropdown/sidebar
  keyboard focus).
- Secret scan (the workflow's own four grep patterns, run manually
  against the built output): 0 matches in all four categories.
- Throwaway test password confirmed absent, in plaintext, from both
  the plain and encrypted build output.
- Absolute-path check (`href="/`, `src="/`, excluding `_static`/
  `genindex`/`search.html`): 0 matches.
- `sphinx-build -b linkcheck`: one pre-existing broken external link
  (403 on a `maskor.fh-aachen.de` PDF download, from
  `about/alert-and-spot.md`, unrelated to this round's changes) and one
  redirect (`openssh.com` → `openssh.org`) — both informational only
  per the workflow's own design (`continue-on-error: true`), neither a
  blocker.
- StatiCrypt gate, re-verified end-to-end after the leak fixes: direct
  subpage access gated (not just the homepage), wrong password
  rejected, correct password reveals real content, navigation and
  search functional after unlock, no raw `.md` source files served, no
  `_sources/` directory, no `.doctrees`/pickle files, `searchindex.js`
  correctly absent (404) from the published output.
- Mermaid: verified across manual unlock, "remember me" navigation (all
  6 diagram pages), reload-after-remember-me, and the plain site
  including a theme toggle — zero console errors throughout.

### 9. Merge, push, and deploy — same blocker as the first pass

`feat/alert-spot-tutorial-polish` (5 commits since the first pass's
report: `5e2bb7a`, `93ee70d`, `c6f5693`, `57018b6`, `e691728`, plus
`60b6e7b` for the leak fixes) was fast-forwarded into `main`
(`git merge --ff-only`; `main` confirmed to still be an ancestor
immediately before merging; no force-push, no reset) and both `main`
and the polish branch were pushed to `origin`.

The resulting `Build and deploy site` run (`35273932881`, commit
`60b6e7b`) was watched via the public Actions API to completion:
**failed**, at the exact same step as every previous push — "Encrypt
the site behind a password gate" — with everything before it
(checkout, Python setup, dependency install, the Sphinx build itself,
the secret scan, Node.js setup) succeeding, and everything after it
(including the new "Remove the unencrypted search index" step, the
external-link check, artifact upload, and the entire `deploy` and
`smoke-test` jobs) correctly skipped as a result. Raw step logs remain
inaccessible without admin auth (`403 Must have admin rights to
Repository`, confirmed again this round). This is the same failure
signature as before and, per the step's own fail-fast design, remains
most consistent with `STATICRYPT_PASSWORD` still being unset — not
provable with certainty without either the raw log or the secret
actually being set, and stated with that same qualification as before.

Live site check, repeated: `https://moritzschallenberg.github.io/Spot-Tutorial/`
still returns the classic-Pages Jekyll rendering of `README.md`
(confirmed via `<title>` match), and `GET /repos/.../pages` still 404s
unauthenticated — GitHub Pages remains on "Deploy from a branch", not
"GitHub Actions". Neither blocker has moved since the first pass's
report; both still require the same two manual, admin-only steps
listed there, which this session still cannot perform without
credentials this environment does not have.

### Second-pass summary

Everything locally verifiable now passes, including two real content
leaks in the deployment pipeline itself (not just this round's new
content) that were found and fixed before they could ever reach a
live, publicly-encrypted deploy. `main` is fast-forwarded and pushed.
Publication is still not live in its intended form — the two blockers
are exactly the ones identified in the first pass's report, unchanged
by anything in this session, and still require repository-admin access
this session was never given.
