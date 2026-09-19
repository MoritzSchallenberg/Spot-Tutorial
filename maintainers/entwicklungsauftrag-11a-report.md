# Entwicklungsauftrag 11A report — Repository finalization

**Not part of the published website.** Internal working document.
Excluded from the Sphinx build (outside `docs/`), not linked from any
published toctree.

## 1. Start and end commit

- Start: `main` at `6079f55` ("docs: document the second, more detailed
  Entwicklungsauftrag 10 pass") — the commit named in the task as the
  last publicly visible one, confirmed current via `git fetch` before
  any work began.
- Branch: `fix/finalize-spot-tutorial-repository`, created from
  `6079f55`, 6 commits, fast-forwarded into `main`.
- End: `main` at `5240863` ("ci: harden encrypted Pages artifact
  validation"), pushed to `origin`.

## 2. New README structure

Rewritten in full (commit `40ebfb4`) to the prescribed section order:
title/description/documentation link/badges, Purpose, Contents,
Documentation structure, Supported environment, Local setup, Build the
documentation, Run the tests, Contributing, Security, Deployment,
Password gate, License status. Developer-facing detail (content
conventions, PR checklist, the full security policy) moved out to
`CONTRIBUTING.md` and `SECURITY.md` (commit `36cf597`), which the
README now links to rather than repeating. 512 lines → 173 lines net
(counting the new files separately).

## 3. Updated root documents

- `README.md` — full rewrite (§2).
- `CONTRIBUTING.md`, `SECURITY.md` — new files, split out of the old
  README's "Editing the content"/"Contributing"/"Security" sections.
- `DECISIONS_NEEDED.md` — full rewrite (§4).
- `CONTENT_MAP.md`, `CONTENT_REVIEW.md`, `SECURITY_REVIEW.md` —
  reviewed, left unchanged: all three are explicitly dated snapshots
  (`Date: 2026-09-01` / `Analysed: 2026-09-01`) of the original
  three-source migration audit, already read as historical record
  rather than a live claim about the project's current state, and a
  scan for forward-looking course-planning language
  (`will run|upcoming|next session|...`) found none.
- `LICENSES.md` — reviewed, left unchanged: its "Course content"
  section accurately describes the actual historical origin of the
  material and the two rewrites that removed event/facilitator framing
  from it — accurate provenance, not a claim that the project is still
  a planned course.

## 4. Archived course-era records

`DECISIONS_NEEDED.md`'s original content (course sessions, room
planning, participant numbers, hackathon logistics and scoring, plus
three sign-off items that reference platform pages confirmed no longer
to exist — `platforms/alert-spot.md`, `platforms/carologistics-robotino.md`)
moved to `maintainers/archive/course-era/decisions-needed-course-era.md`
(commit `a0b035b`), with a header explaining what it is and why it is
archived rather than deleted.

The new `DECISIONS_NEEDED.md` lists 10 items, all still genuinely open
against the site as it exists today: the content license; rights to
the historical images; sign-off on the safety instructions; hardware
verification of the operating procedures; five specific open technical
questions already documented with evidence in the architecture/safety
pages (gripper-control path, manipulator DOF, operator input device,
production middleware, TF convention); and the still-unperformed
`RRL-ALeRT` organisation transfer.

## 5. Rebranding search results

`rg -i` search for `Learning-Robotics-Crash-Course` /
`github.io/Learning-Robotics-Crash-Course` /
`MoritzSchallenberg/Learning-Robotics-Crash-Course` /
`/Learning-Robotics-Crash-Course/` / `Entwicklungsauftrag` across
`README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/`, `scripts/`,
`.github/`, `requirements.txt`, `LICENSES.md`, `DECISIONS_NEEDED.md`
found real occurrences in three files, all fixed:

- `docs/conf.py` and `scripts/verify-structure.py`: every
  "Entwicklungsauftrag N" mention across their source comments (12
  total, confirmed by recount after editing), reworded to describe
  what each check/badge scheme does and why without the internal
  task-numbering.
- `DECISIONS_NEEDED.md` (this round's own new draft, written before
  this search ran): one mention of the literal old repository name
  while explaining the earlier rename — reworded to describe the
  rename without repeating the retired name, since this file is itself
  one of the files the new automated check scans.

A closer manual read of `scripts/tutorial-preflight.sh` (prompted by
the task's own separate instruction to check that script specifically
for `docs/course/` links and old workspace names, not by the rg search
above) found four more real, if differently-patterned, issues: three
`docs/course/02-ros2/...` links pointing at a path that no longer
exists (fixed to `docs/ros2/installation.md`, the real current path),
one `docs/platforms/simulation.md` reference (fixed to
`docs/simulation/index.md`), the stale header name "ALeRT Advanced
Robotics Tutorial", and the workspace-candidate list — this one needed
more than a rename: `~/course_ws` was genuinely stale and dropped, but
a check of the actual published `docs/ros2/installation.md` and three
other content pages found they already, consistently, instruct a
reader to create `~/robot_ws` (13 real usages found via grep) — so the
fix kept `~/robot_ws` as the primary candidate rather than replacing it
with the task's suggested `~/spot_tutorial_ws`, which no actual page
anywhere references.

Final state: `rg` against the same pattern set and file list returns
zero matches except the intentional banned-phrase list entry inside
`scripts/verify-structure.py` itself (the detector's own data, not a
leak). Verified live: injected a throwaway file containing the old
repository name, confirmed `verify-structure.py` caught it, then
removed the file and reran to confirm a clean pass.

## 6. Repository description

Changed via the GitHub API (`gh api repos/.../-X PATCH`) from *"This is
the tutorial for every new guy at the different Teams of the Maskor
Institut."* to *"Technical documentation for the ALeRT Spot system:
safe operation, ROS 2 architecture, perception, navigation,
manipulation and autonomous rescue robotics."* — confirmed via a
follow-up `GET`. Homepage set to
`https://moritzschallenberg.github.io/Spot-Tutorial/`. Topics set to
`alert, documentation, robocup-rescue, robotics, ros2, sphinx, spot`.

## 7. Default branch

**Was `feat/initial-course-website`, not `main`** — confirmed via
`gh api repos/.../ --jq .default_branch` before any change, matching
what an earlier report had already flagged as unresolved. Switched to
`main` via the API; confirmed with a follow-up read.

## 8. Pages source

**Was `"build_type": "legacy"`** (classic "Deploy from a branch",
source `main` / `/`) — confirmed via `GET repos/.../pages` before any
change. Switched to `"build_type": "workflow"` (GitHub Actions) via
`PUT repos/.../pages -f build_type=workflow`; confirmed with a
follow-up read. **This is a real, verified configuration change, not
an assumption** — the previous report could only infer the
misconfiguration indirectly (a separate classic "pages build and
deployment" Actions run appearing on every push); this round read and
changed the actual setting directly.

## 9. Secret status (name only, never the value)

**`STATICRYPT_PASSWORD` does not exist.** Confirmed directly and with
certainty this round, for the first time — `GET
repos/.../actions/secrets` returns `{"total_count":0,"secrets":[]}`.
Every previous report could only infer this indirectly from the deploy
step's own fail-fast log line, without admin access to confirm it
outright. **This is the one item from Section 13's hard preconditions
that is not met**, and this report does not claim otherwise. Setting
it requires the password value, which this session does not have and
should not have — it must be added by a repository owner under
*Settings → Secrets and variables → Actions → New repository secret →
name `STATICRYPT_PASSWORD`*.

## 10. Workflow run ID

`35451753103`, triggered automatically by the `main` push (fast-forward
merge of the branch above), on commit `5240863`. Watched to completion
via `gh run watch 35451753103 --exit-status`.

## 11. Results of every workflow job

- **Build the Sphinx site** — **failed**, at the "Encrypt the site
  behind a password gate" step, with the *exact* log line now
  confirmed directly (not inferred): `STATICRYPT_PASSWORD secret is
  not set -- refusing to deploy an unprotected site.` Every step before
  it succeeded, including the two new ones added this round: "Run
  structural checks" (`scripts/verify-structure.py`, not previously run
  in CI at all) and, further down, the "Validate the encrypted artifact
  before upload" step never got a chance to run because the job had
  already failed earlier — correct, expected behavior given the
  encryption step itself failed first.
- **Build and test the example ROS 2 packages** — succeeded,
  independent of the Sphinx build/deploy as designed.
- **Deploy to GitHub Pages** — skipped (`needs: build` not satisfied).
- **Smoke test the deployed site** — skipped (`needs: deploy` not
  satisfied).

## 12. Live URL

`https://moritzschallenberg.github.io/Spot-Tutorial/` returns HTTP 200
but **still serves the old classic-Pages Jekyll rendering of
`README.md`** (confirmed via `<title>ALeRT Spot Tutorial |
Spot-Tutorial</title>`, matching the README's own top heading, not this
site's real homepage). This is expected, not a new problem: switching
Pages' `build_type` to `"workflow"` (§8) changes which *source* future
deploys use, but does not retroactively replace whatever was last
*successfully* deployed — and no workflow-based deploy has ever
succeeded, because of §9. The live content will not actually change
until a `Build and deploy site` run succeeds end-to-end.

## 13. Tested subpages

**Not tested against the live site** — doing so now would only confirm
they 404 or continue serving the unrelated Jekyll content, which §12
already explains. All of the following were tested against a local
build of the exact commit that is now on `main` (`5240863`), encrypted
locally with a throwaway test password, generated fresh and never
committed:

- `about/alert-and-spot.html` (as `index.html`'s equivalent check, plus
  navigation to it after unlock) — loads, password-gated, real content
  after unlock.
- `safety/operator-checklist.html` — direct subpage access correctly
  shows the password gate, not real content; real content after
  unlock.
- `operating/power-on.html`, `architecture/index.html`,
  `reference/system-status.html` — covered by the 102-page
  `verify-site.py` sweep (§16) and, for the four `architecture/*`
  diagram pages among them, the dedicated Mermaid test (§15).

## 14. Password-gate test

Against the local encrypted build (throwaway password
`throwaway-test-pw-5678`, never committed):

- Direct subpage request (`safety/operator-checklist.html`) shows the
  password prompt, not real content — subpages are protected, not only
  the homepage.
- A wrong password does not unlock the page.
- The correct password unlocks the page and shows real content
  (homepage's "Who are you?" heading confirmed present).
- After unlock: navigation (>5 links found), search box present.
- `searchindex.js` returns 404 — confirmed absent, not just
  unreferenced.
- A raw `.md` source file (`safety/operator-checklist.md`) returns 404
  — not served.
- No `_sources/` directory in the encrypted output.
- No `.doctrees/` directory, and no `.pickle`/`.doctree` file anywhere
  in the encrypted output (a full walk, not a spot check) — the fix
  from the previous round holds.
- The three workflow-level validation checks added this round
  (§§10-11 of the workflow itself) were also run manually against this
  exact local output and all pass: no `_sources/`, no `searchindex.js`,
  no doctree/pickle file.

## 15. Mermaid test

Re-verified against this round's fresh build and re-encryption (the
previous round's fix — polling `document.readyState` rather than
depending on the `"load"` event — was not touched this round, per the
task's "confirm by testing, don't rebuild" instruction):

- Manual password entry, `architecture/data-flow.html` (2 diagrams):
  `svg_count=2`, zero console errors.
- "Remember me" navigation across all 6 diagram-bearing architecture
  pages: every page's diagram count matches its actual diagram count,
  zero console errors.
- Reload after "remember me": `data-flow.html` still `svg_count=2`.
- Plain (non-gated) site: `data-flow.html` `svg_count=2`, zero console
  errors, and a light/dark theme toggle correctly keeps `svg_count=2`
  (the specific regression an earlier iteration of the fix had
  introduced, now confirmed stable).

## 16. Checklist and mobile checks

Covered by the full `scripts/verify-site.py` run against the current
build: **313/313 checks pass**, 102 pages, both themes — JavaScript
errors, 390px mobile overflow, the light/dark toggle, search, copy
buttons, syntax highlighting, WCAG AA contrast (including every
`sphinx-design` dropdown and the sidebar's expanded-branch links) in
both themes. Real checkboxes (MyST `tasklist`, fixed in an earlier round) confirmed
directly this round: 29 `type="checkbox"` elements still present on
`safety/operator-checklist.html`'s built output, same count as before
— `verify-site.py` itself has no dedicated checkbox assertion, so this
was checked separately rather than claimed on the strength of that
sweep alone.

## 17. Remaining technical uncertainties

Unchanged from the previous report, still genuinely open (see
`DECISIONS_NEEDED.md` for the full detail on each): content license;
image rights; safety-instruction sign-off; hardware verification of
the operating procedures; which gripper-control path is active; the
manipulator's actual DOF; which operator input device (Steam Deck vs.
DualSense) is in current use; which middleware (Zenoh vs. Fast-DDS) is
production-authoritative; which of the two coexisting TF conventions
applies where. None of these were resolved or newly discovered this
round — this round's own new finding is organisational/infrastructure
(§§7-9), not about the robot itself.

**New this round, informational only:** a full `sphinx-build -b
linkcheck` pass found substantially more broken external links than
the previous report's single item — roughly a dozen `docs.nav2.org`
URLs now 404 (that project appears to have restructured its own docs
site since these links were written) and five `fh-aachen.sciebo.de`
share links in `about/alert-and-spot.md` now 404 (cloud-storage share
links with an expiry, most likely). None of this is a regression from
this round's own changes — the affected pages
(`navigation-exploration/`, `decision-making/`, `rescue-projects/`,
`mapping-world-models/`, `simulation/`, `about/alert-and-spot.md`)
were not touched. Not fixed in this pass — replacing ~17 external URLs
needs actual research into each one's current equivalent, which is
outside this task's scope, but flagged here rather than silently
noticed and dropped. The workflow's own linkcheck step remains
`continue-on-error: true` by design, so this does not block anything.

## 18. Commit list

On `fix/finalize-spot-tutorial-repository`, fast-forwarded into `main`:

1. `40ebfb4` — docs: rewrite README for the Spot Tutorial repository
2. `36cf597` — docs: add current contributing and security guidance
3. `a0b035b` — docs: archive obsolete course-era project records
4. `234e9d3` — fix: remove stale repository names and paths
5. `8e7e6e1` — test: enforce Spot-Tutorial repository identity
6. `5240863` — ci: harden encrypted Pages artifact validation

(This report itself is commit 7, added after the above per the task's
own recommended sequence, since it needed to describe the merge/push/
workflow-watch outcome above.)

## 19. Force-push confirmation

**No force-push, no reset, at any point.** `main` was advanced only via
`git merge --ff-only` (twice: once locally verified as an ancestor
relationship before merging, matching the established pattern from
every previous round) and `git push origin main` with no `--force`.
The working branch was pushed with a plain `git push -u origin
fix/finalize-spot-tutorial-repository`, no force flag. `git log
--oneline --decorate --graph --all` was run before any change (§2 of
the task) and showed no branch this session had any reason to touch
other than `main` and the new working branch.

## 20. What is still required to actually finish publishing

**One item, not two, this time** — the Pages-source misconfiguration
identified in every previous report is now fixed (§8):

1. **Set the `STATICRYPT_PASSWORD` secret** — *Settings → Secrets and
   variables → Actions → New repository secret*, name
   `STATICRYPT_PASSWORD`, using the password value from your own
   records (not restated here, and not knowable to this session).

That is the only remaining blocker. Once it is set, the next push to
`main` (or a manual `workflow_dispatch` run) will encrypt and publish
the real site — no further configuration change is needed on either
side. This report does not claim publication is complete, per the
task's own explicit instruction not to end on "you still need to flip
the setting" as if it were a success — the setting is already flipped;
only the secret itself remains outside this session's ability to
provide.
