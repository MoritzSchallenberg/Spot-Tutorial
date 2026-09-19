# ALeRT Spot Tutorial

Technical documentation for the ALeRT Spot system: a Boston Dynamics
Spot quadruped fitted with a Kinova Gen3 manipulator and Robotiq
gripper, operated by the RoboCup Rescue League team at the **MASKOR
Institute, FH Aachen**. Covers safe operation, ROS 2 architecture,
perception, navigation, manipulation and autonomous rescue robotics,
grounded in the team's own code and configuration.

**Documentation:** <https://moritzschallenberg.github.io/Spot-Tutorial/>
**Repository:** <https://github.com/MoritzSchallenberg/Spot-Tutorial>

[![Build and deploy site](https://github.com/MoritzSchallenberg/Spot-Tutorial/actions/workflows/pages.yml/badge.svg)](https://github.com/MoritzSchallenberg/Spot-Tutorial/actions/workflows/pages.yml)
[![Documentation](https://img.shields.io/website?url=https%3A%2F%2Fmoritzschallenberg.github.io%2FSpot-Tutorial%2F&label=documentation)](https://moritzschallenberg.github.io/Spot-Tutorial/)
[![ROS 2](https://img.shields.io/badge/ROS%202-Humble-22314E)](https://docs.ros.org/en/humble/)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20LTS-E95420)](https://releases.ubuntu.com/22.04/)
[![Sphinx](https://img.shields.io/badge/docs-Sphinx-blue)](https://www.sphinx-doc.org/)

## Purpose

Document the ALeRT Spot system itself — safety, operation, and
architecture — grounded in the team's current code and deployment
configuration (see `maintainers/spot-code-audit.md`), not in memory or
convention. Every technical claim carries an explicit verification
level (`Verified in code`, `Verified in configuration`, `Historical
procedure`, or `Unverified on hardware`); nothing is asserted as
confirmed on real hardware without a test record backing it.

**Audience:** anyone preparing to operate the physical Spot system, or
anyone who wants to understand how it is built.

**Language:** English.

## Contents

| Section | Focus |
|---|---|
| About ALeRT and Spot | Team and RoboCup Rescue League history |
| Safety and Prerequisites | Stop states, E-stops, operating area, required knowledge |
| Operating Spot | Power-on through shutdown, driving, manipulator control, recovery |
| System Architecture | Hardware, network, software, startup order, ROS 2 interfaces, frames, data flow |
| Sensors and Perception | Cameras, LiDAR, IMU, TF2, marker/object detection |
| Navigation and Mapping | Occupancy grids, SLAM, Nav2-style planning and control |
| Manipulator and MoveIt | Arm fundamentals, MoveIt 2, grippers |
| Autonomous Behaviors | State machines, behavior trees, worked mission examples |
| Deployment and Configuration | Simulation, the platform/simulation reference, hardware-design tooling |
| Diagnostics and Testing | Startup order, configuration, systematic debugging |
| Reference | Cheat sheet, supported environment, glossary, system status |

Not sure where to start? [Start Here](https://moritzschallenberg.github.io/Spot-Tutorial/start-here.html)
lays out concrete paths by role (new operator, software developer,
manipulator developer, autonomous-rescue developer), each with its
prerequisites and expected outcome.

## Documentation structure

```text
docs/
├── index.md                      Landing page
├── start-here.md                 Role-based learning paths
├── about/                        About ALeRT and Spot
├── safety/                       Safety and Prerequisites
├── operating/                    Operating Spot (step-by-step procedures)
├── architecture/                 System Architecture (incl. Mermaid diagrams)
├── sensors-and-perception/       Hub page: sensors-frames/ + perception/
├── navigation-and-mapping/       Hub page: mapping-world-models/ + navigation-exploration/
├── manipulation/                 Manipulator and MoveIt
├── autonomous-behaviors/         Hub page: decision-making/ + rescue-projects/
├── deployment-and-configuration/ Hub page: simulation/ + platforms/
├── integration-testing/          Diagnostics and Testing
├── reference/                    Cheat sheet, supported environment, glossary
└── _static/                      CSS, JS, images, diagrams

examples/           Real, colcon-buildable starter ROS 2 packages
maintainers/         Not built, not deployed, not in any toctree — audits,
                     migration reports, and maintainers/archive/ for
                     superseded material
scripts/             verify-structure.py, verify-site.py, tutorial-preflight.sh
.github/workflows/   pages.yml — build, test, encrypt, deploy
```

`docs/` is the entire published website — everything Sphinx builds and
everything GitHub Pages serves. Nothing outside `docs/` is ever built
or deployed.

## Supported environment

Fixed to one toolchain — there is no distribution choice presented
anywhere on the site:

```text
Ubuntu 22.04 LTS
ROS 2 Humble
Python 3.10+ (3.12 used in CI)
colcon
RViz2
```

See `docs/reference/compatibility.md` ("Supported environment") for the
full detail and status legend.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Build the documentation

```bash
sphinx-build -E -a -W --keep-going \
  -b html \
  -d docs/_build/doctrees \
  docs docs/_build/html
```

`-W` turns warnings into errors — this is what CI does, so building
this way means no surprises in the pipeline. `-d docs/_build/doctrees`
keeps Sphinx's internal doctree cache outside the published output
directory; see "Password gate" below for why that specifically matters
here.

### Preview it locally

Serve it under the same subpath GitHub Pages uses, so relative links
and search behave the same as in production:

```bash
mkdir -p /tmp/spot-tutorial-preview/Spot-Tutorial
cp -r docs/_build/html/. /tmp/spot-tutorial-preview/Spot-Tutorial/

python3 -m http.server 8899 -d /tmp/spot-tutorial-preview
```

Then visit <http://localhost:8899/Spot-Tutorial/>.

### Rebuilding on save

```bash
pip install sphinx-autobuild
sphinx-autobuild docs docs/_build/html
```

> [!NOTE]
> The site is served from a repository subpath on GitHub Pages. All
> asset paths are relative, so it works both at `/` locally (via
> `sphinx-autobuild`) and at `/Spot-Tutorial/` in production. **Never
> introduce an absolute path beginning with `/`.**

## Run the tests

```bash
python scripts/verify-structure.py
python scripts/verify-site.py
```

`verify-structure.py` checks source-level structure and content rules
(navigation completeness, banned old-repository/old-course terms, no
orphaned pages) without needing a build. `verify-site.py` needs a build
served locally (see "Preview it locally" above) and a browser — it
checks JavaScript errors, mobile overflow, the light/dark toggle,
search, copy buttons, and WCAG AA contrast:

```bash
pip install playwright && playwright install chromium
python scripts/verify-site.py
```

Playwright is intentionally **not** in `requirements.txt` — building
the site itself should never need a browser download.

See `CONTRIBUTING.md` for the full pull-request checklist, including
content and security checks beyond these two scripts.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for branching, content
structure, verification-level and badge conventions, and the
pull-request checklist.

## Security

See [`SECURITY.md`](SECURITY.md) for what must never be committed, the
pre-push secret scan, and what to do if a secret is ever exposed.

> **This repository is public.** Nothing confidential is or should be
> published on it — see `SECURITY.md`.

## Deployment

Pushes to `main` trigger `.github/workflows/pages.yml`: it installs
dependencies, builds with `-W`, runs the structural checks, scans the
output for secrets, encrypts the site behind the password gate (see
"Password gate" below), checks external links, and publishes to GitHub
Pages via `actions/deploy-pages`. GitHub Pages is configured to deploy
from this workflow (Settings → Pages → Source → GitHub Actions), not
from a branch.

Live: <https://moritzschallenberg.github.io/Spot-Tutorial/> — every
push to `main` redeploys it automatically.

## Password gate

The published site is wrapped in a static password gate
([StatiCrypt](https://github.com/robinmoisson/staticrypt)) as an access
hurdle for this pre-release documentation:

- StatiCrypt encrypts the HTML pages — **this is not server-side
  authentication.** The page and its encrypted content are still
  delivered to any visitor's browser; StatiCrypt only prevents the
  content from being *readable* without the password, via client-side
  decryption.
- Images and other static assets (CSS, JavaScript) are **not**
  encrypted and remain directly fetchable at their own URL without the
  password. Nothing confidential is or should be published on this
  site regardless — see `SECURITY.md`.
- The production search index is disabled: Sphinx's built-in
  `searchindex.js` is a full-text index of effectively every word on
  every page, and being a `.js` file (not `.html`), StatiCrypt cannot
  protect it. It is removed from the published build specifically, so
  it never leaks page content unencrypted at a fixed URL. The local
  development build (see "Preview it locally") is unaffected and keeps
  full in-site search.
- The password is provided exclusively through the
  `STATICRYPT_PASSWORD` GitHub Actions secret, read directly into the
  encryption step's environment — never passed as a command-line flag,
  which would appear in a log. If the secret is missing, the deploy
  step fails loudly rather than silently publishing an unprotected
  site.
- The password value itself never appears in this repository, in any
  workflow file, or in any build log.

## License status

**Undecided.** The institute and the original rights holders have not
chosen a license for this content, so this repository ships no
`LICENSE` file and does not pick one on their behalf — see
[`LICENSES.md`](LICENSES.md) for the full context, and
[`DECISIONS_NEEDED.md`](DECISIONS_NEEDED.md) for this and every other
open decision.
