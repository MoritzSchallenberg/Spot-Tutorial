# Contributing

## Branching

Branch from `main`. Name it `<scope>/<description>` — for example
`jdoe/fix-nav2-params`. No force-push, no reset, and no rewriting
another contributor's history — fast-forward or an ordinary merge only.

## Content structure

All content is **MyST Markdown** under `docs/`. Keep the general/specific
split: shared concepts on the general topic pages (`docs/ros2/`,
`docs/perception/`, etc.), Spot-specific detail under `docs/architecture/`,
`docs/operating/` and `docs/safety/`, linking back rather than repeating.
Explain each thing once — if you find yourself writing something that
already exists elsewhere, link to it instead.

**Never invent** a command, topic name or package name. If you are
unsure, add a `TODO-REVIEW` block rather than a plausible guess:

```markdown
:::{admonition} TODO-REVIEW
:class: todo-review
What needs checking, and why.
:::
```

### Verification levels

Every technical claim about the Spot system states how it was checked —
`Verified in code`, `Verified in configuration`, `Historical procedure`,
or `Unverified on hardware`. See
`docs/safety/safety-principles.md#verification-levels` for the full
definitions. Nothing on this site is currently marked `Verified on
hardware`; see `DECISIONS_NEEDED.md` items 3–4.

### Badges

Write the substitution and it renders as a styled badge:

```markdown
{{ alert }}  {{ simulation }}  {{ documented }}  {{ hardwareverified }}
{{ unverified }}  {{ hwverificationrequired }}  {{ experimental }}  {{ historical }}
{{ foundation }}  {{ intermediate }}  {{ advanced }}  {{ research }}
```

See `docs/reference/compatibility.md`'s "Status legend" for what each
one means. Badges are defined in `docs/conf.py` and styled in
`custom.css`. The whole site is fixed to one toolchain — Ubuntu 22.04
LTS, ROS 2 Humble — so there is deliberately no distribution badge.

> [!WARNING]
> Do **not** put a badge inside a heading. It becomes part of the
> generated anchor and breaks links to that section. Put it on its own
> line underneath.

### Screenshots and historical images

Historical photographs and screenshots (`docs/_static/images/history/`,
`historical-interface/`) are kept for context, but must be labeled as
historical wherever they appear, and paired with an explicit note on
whether the current code confirms or contradicts what they show — see
any figure in `docs/operating/` for the pattern (`Historical context` /
`Current implementation` / `Hardware verification required`). Never
present a historical screenshot as current fact. New screenshots showing
real network information, credentials, or identifiable people must not
be added — see `SECURITY.md`.

## Building and testing

Build with `-W` before you push. CI rejects warnings:

```bash
sphinx-build -E -a -W --keep-going \
  -b html \
  -d docs/_build/doctrees \
  docs docs/_build/html
```

Then run the structural checks (no build required beyond the one
above) and the browser-level checks:

```bash
python scripts/verify-structure.py
python scripts/verify-site.py
```

`scripts/verify-site.py` needs Playwright, intentionally **not** in
`requirements.txt` — building the site itself should never need a
browser download:

```bash
pip install playwright && playwright install chromium
```

See `README.md`'s "Run the tests" for the full local-serving setup
`verify-site.py` expects, and "Password gate" for testing a local
StatiCrypt-encrypted build.

## Status badges in pull requests

`.github/workflows/pages.yml` runs on every push and pull request:
the Sphinx build, a structural verification pass, and a secret scan
always run; encryption and deployment only run on `main`. A pull
request only needs the build/structure/secret-scan checks green —
encryption and deploy are expected to be skipped on a branch.

## Pull request checklist

- [ ] Built locally with `-W` and no warnings.
- [ ] `scripts/verify-structure.py` passes.
- [ ] Every new technical claim has an explicit verification level.
- [ ] No invented commands, topics or package names.
- [ ] No secrets, internal IPs, hostnames, or personal data (see
      `SECURITY.md`).
- [ ] Historical images are labeled as such, not presented as current.
