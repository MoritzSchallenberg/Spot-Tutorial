# ALeRT Spot Tutorial migration report (Entwicklungsauftrag 9)

**Not part of the published website.** Internal working document.
Excluded from the Sphinx build (outside `docs/`), not linked from any
published toctree. This is the final report required by Section 19 of
the task; it covers all 20 required points.

## 1. Local sources and commit states used

| Source | Path | Commit/state |
| --- | --- | --- |
| Website repository (this repo) | `Learning-Robotics-Crash-Course` | Branch created from `feat/alert-advanced-robotics-tutorial` @ `aef08be5012f04a67aafdc9499c466def40ed2e8`, working tree clean, in sync with `origin` at branch time |
| Old Spot tutorial | `00-02 Quelle 2 Spot Tutorial/Website Code` | No git; scraped Sphinx/RTD export, every page footer dated "© Copyright 2024, MASCOR Institute, FH Aachen" |
| Current Spot code | `Backup Ansible/workspaces` | No top-level git; 2026-09-17 filesystem backup of one dev machine (`max1@alert`), 12 workspaces, 188 ROS 2 packages across 74 per-package git repos |
| Ansible/deployment bestand | `Backup Ansible/ansible` + `configs` | No git; single incomplete `hosts: localhost` playbook |

Full detail, including per-workspace commit dates and which workspace
is authoritative per subsystem: `maintainers/spot-source-audit.md`.

## 2. Security scan result (no secret values)

Full detail: `maintainers/spot-security-audit.md`. Summary:

- Real credentials found and excluded from all migration:
  `configs/spot_login.yaml`, `.bashrc`'s `BOSDYN_CLIENT_PASSWORD` (the
  backup's own `restore.sh` reminds its operator to rotate this),
  vendored TLS test fixtures in `spot_wrapper`'s test suite (identified
  as mock certificates, not real secrets, by path and context).
- Real private network information found and excluded: a private IP
  and network config in `Backup Ansible/docs/system_extras.md` and
  `configs/super_client_configuration_file.xml`; a WiFi network name
  ("Alert") and a manipulator IP address visible in two old-tutorial
  screenshots (`kinova_web.png`, `kinova_faults.png`); a WiFi SSID list
  in a third screenshot (`wifi.png`). All three screenshots were
  excluded from image migration entirely.
- No secret value, password, key, token, or certificate content is
  reproduced anywhere in this branch's commits or any published page.
  All real network identifiers in the public architecture pages use
  the task's placeholder tokens (`<SPOT_IP>`, `<COMPUTE_HOST>`,
  `<OPERATOR_HOST>`, `<ROBOT_NETWORK>`).

## 3. Historical texts migrated

From the former ALeRT tutorial's `ALeRT Team Page`,
`Spot Documentation/00 General Information`,
`Spot Documentation/07 Challenges`, and `Tutorials/01 Introduction`,
into `docs/about/{index,alert-and-spot,robocup-rescue,rescue-challenges,
historical-gallery}.md`. Content and order preserved from source;
spelling ("Challengens"→"Challenges", "Discription"→"Description",
"resuce"→"rescue") and the institute name ("MASCOR"→"MASKOR", matching
this site's established spelling) corrected. Time-bound statements
(e.g. "tasks for 2022 not published yet") carry a "Historical snapshot"
admonition rather than appearing as current fact.

## 4. Images migrated, excluded, and replaced

**24 historical images** migrated byte-for-byte into
`docs/_static/images/history/`, every checksum verified equal to its
source; 2 duplicate top-level copies (`award_ceremony.jpg`,
`spot_gravel_sitting.jpg`) not re-migrated (byte-identical to the
`..._files/` copy already migrated). Full table:
`maintainers/historical-asset-migration.md`.

**4 historical operating-interface screenshots**
(`spot_buttons.jpg`, `rviz.png`, `spot_control.png`,
`manipulator_control.png`) migrated into
`docs/_static/images/historical-interface/`, each visually reviewed
(no sensitive content) and labeled `Historical interface` on the page
that uses it. `spot_control.png`/`manipulator_control.png` carry an
explicit note that they describe Steam Deck native controls, which do
not match the DualSense mapping found in the current teleop code —
kept for historical reference, not presented as current.

**3 images excluded entirely** (not on the task's requested list, and
showing real network information): `wifi.png`, `kinova_web.png`,
`kinova_faults.png`.

No image was replaced with a newly-created screenshot — no
supervised access to the live interface was available in this pass.

## 5. Content deviations from the old history section

- Excluded: two Carologistics/Logistics League video references on the
  old Introduction page (explicit task requirement).
- Excluded: course-organizational material on the same page ("invites
  you to support us... deepening knowledge in these topics", the
  "Course Structure" pointer) — old course organization, not history,
  per the task's own rule.
- Excluded: the `course_structure.png` image referenced at the very end
  of the old Introduction page, since the section it illustrated
  (course structure) was excluded.
- No new team history, year, or competition result was invented.
  Where the old tutorial named no individual, none was added (see
  `historical-asset-migration.md`'s note on `award_ceremony.jpg` /
  `rrl_eindhoven_group.png`).

## 6. Final navigation

```text
Home
About ALeRT and Spot
├── ALeRT and Spot
├── RoboCup Rescue
├── Rescue Challenges
└── Historical Gallery
Safety and Prerequisites
├── Safety Principles
├── Emergency Stops
├── Operating Area
├── Required Knowledge
└── Operator Checklist
Operating Spot
├── System Preparation
├── Power-On Procedure
├── Operator Interface
├── Driving Spot
├── Operating the Manipulator
├── Safe Shutdown
└── Recovery and Troubleshooting
System Architecture
├── Hardware Overview
├── Computers and Network
├── Software Components
├── Startup and Launch Sequence
├── ROS 2 Interfaces
├── Coordinate Frames
└── Data Flow
Sensors and Perception   (hub -> sensors-frames/, perception/)
Navigation and Mapping   (hub -> mapping-world-models/, navigation-exploration/)
Manipulator and MoveIt   (-> manipulation/, direct)
Autonomous Behaviors     (hub -> decision-making/, rescue-projects/)
Deployment and Configuration  (hub -> simulation/, platforms/)
Diagnostics and Testing  (-> integration-testing/, direct)
Reference                (-> reference/, direct)
```

Matches the task's Section 6 structure exactly (verified by
`scripts/verify-structure.py`'s `check_full_navigation`). Ten
pre-existing topic directories (`getting-started`, `ros2`, `simulation`,
`platforms`, `sensors-frames`, `perception`, `mapping-world-models`,
`navigation-exploration`, `decision-making`, `rescue-projects`) remain
at their original paths and are reachable transitively through the hub
pages above, rather than being independent top-level nav entries.

## 7. Hardware components identified

Boston Dynamics Spot (base platform, BD's own optional arm present in
the URDF but disabled in every located deployment config); Kinova Gen3
manipulator — **6 degrees of freedom confirmed** (`dof:=6` in the
actual bring-up command), not 7 as might be assumed; a Robotiq
2-finger gripper of **ambiguous model** (2F-140 vs. 2F-85 naming
disagree between two local sources, not resolved); Livox Mid-360
LiDAR; RealSense depth/color cameras; 3× IFM O3P 3D cameras; a Seek
Thermal camera; an operator device (Steam Deck per historical
screenshots, a Sony DualSense per the current, more recently modified
teleop code — not reconciled); an onboard/payload compute unit
("NUC" per its own provisioning playbook). Full detail:
`docs/architecture/hardware-overview.md`, `maintainers/spot-code-audit.md`.

## 8. Computer and network roles identified

Operator Station, Robot Computer, Spot Base, Manipulator Controller,
Sensors — see `docs/architecture/computers-and-network.md`. No real
hostname, IP address, or WiFi SSID appears in any published page. Two
middleware configurations coexist in the local sources (Zenoh via a
persistent systemd service; Fast-DDS discovery as an ad hoc runtime
window) with no evidence resolving which is actually live — stated as
such, not asserted either way.

## 9. ROS packages, nodes, topics, services, and actions

Full inventory with file:line citations: `maintainers/spot-code-audit.md`
(Repository inventory, ROS package inventory, Runtime components,
Interfaces, TF frames tables) and `docs/architecture/ros2-interfaces.md`
(public-facing key-interfaces table). Notable findings:

- The ROS-level `estop/hard`/`estop/gentle`/`estop/release` services
  are flagged as apparently non-functional in the driver's own code
  comment.
- The operator dashboard's "Estop" slider arms/disarms a background
  software-E-stop-endpoint process, not a direct trigger.
- No single ROS 2 launch tree starts the system — a ~19-process
  tmux-window orchestration does.
- Two robot-frame conventions coexist unreconciled (`feet_center` vs.
  `body`).

## 10. Documented start and shutdown sequence

Startup: `discovery` + `estop` (software E-stop endpoint) → `spot_driver`
→ sensors → mapping (Octomap) → navigation, with the manipulator stack
(`kinova_driver` → `kinova_moveit`) brought up independently. Five
operating modes documented (Base only / Base with sensors / Base with
manipulator / Mapping mode / Autonomous mode). Shutdown: command Spot
to sit → power off motors → stop subsystem windows in reverse order →
power off devices, with the driver's own `destroy_node()` behavior
(conditionally sits the robot) documented explicitly rather than relied
upon silently. Full detail: `docs/architecture/startup-and-launch-sequence.md`,
`docs/operating/{power-on,safe-shutdown}.md`.

## 11. Legacy components identified

`spot_ws/src/kinova_stuffs` (superseded by `ros2_kortex`, per its own
README); `france_sensor_ws`, `cpp_spot_ws` (dormant since 2023);
`spot_ws/src/BT` (BehaviorTree.CPP/ROS2, vendored, no local consumer
found — status `Unverified`, not asserted as deprecated); the
`alert_nav_ws`'s `posture_mgr` node (defined but commented out of its
launch file); `go2_ws`/`omx_ws` (a different robot, Unitree Go2, not
legacy Spot code — excluded from all Spot-system claims throughout).

## 12. Hardware-verified statements

**None.** Per your decision at the start of this task, no claim on
this site is labeled `Verified on hardware` in this pass, since no
test record for any procedure exists in the local sources. This is
stated explicitly on every safety/operating page rather than left
implicit.

## 13. Statements that remain unconfirmed

- Physical E-stop button exact locations, colors, and press-and-hold
  timings (`Historical procedure`, not independently reconfirmed).
- What physically happens to Spot's motors/posture at the moment of an
  E-stop (only the SDK call's own docstring — "cut power" vs. "settle"
  — is cited; no independent physical confirmation).
- Whether the ROS `estop/*` services currently work (flagged broken in
  a code comment; not retested).
- Which gripper-control path is active (Kortex internal-bus vs.
  standalone Robotiq driver).
- Which middleware is actually live (Zenoh vs. Fast-DDS discovery).
- Whether BD's own Spot Arm (`has_arm: True`) is ever used.
- Whether `bring_up_alert_nav/srv/StartNav.srv` is advertised anywhere.
- What happens on communication loss (no code found implementing this
  for either driver).
- Whether the current operator device is the Steam Deck, the DualSense,
  or both.

## 14. Removed old course content

None removed outright in this pass — the existing 13 topics were
reclassified (see point 6) rather than deleted. Two pre-existing pages
were corrected where they conflicted with new code-audit evidence
(`decision-making/index.md`'s RAFCON claim, `manipulation/index.md`'s
7-DOF/2F-85 claim — see commit `1b06d3f`), not removed. The KiCad/Fusion
hardware-design content was demoted from the main navigation (no longer
a top-level caption) per the task's explicit rule, but kept reachable
under Deployment and Configuration, not deleted.

`maintainers/instructors/*.md` (pre-existing staleness from
Entwicklungsauftrag 8, linking to a `docs/course/` path that no longer
exists) was identified but not corrected in this pass — it is outside
`docs/` already, not published, and out of this task's explicit scope;
flagged here for a future pass.

## 15. Build and browser check results

- `sphinx-build -E -a -W --keep-going -b html docs docs/_build/html`:
  clean, 0 warnings, after every commit in this branch.
- `python scripts/verify-structure.py`: all checks pass, including the
  full set of new Section 16 checks added in this pass.
- `python scripts/verify-site.py` (Playwright, Chromium, 100 pages,
  both light and dark theme): **307/307 checks passed** — no JS errors,
  no mobile horizontal overflow, working theme toggle, working search,
  working copy buttons, correct syntax highlighting, WCAG AA contrast
  (including every dropdown and the sidebar) with visible keyboard
  focus, in both themes.
- Manual absolute-path check (`href="/`/`src="/` at the build root):
  0 matches.
- All 24 + 4 migrated image checksums re-verified against their source
  files after every image-touching commit.

## 16. Secret scan result

Reused `.github/workflows/pages.yml`'s own patterns (signed/tokenised
URLs, private key material, credential-shaped strings, known internal
hosts) against the full built `docs/_build/html`: **0 matches** in all
four categories. See point 2 above for the source-level scan.

## 17. Password protection status

**Implemented and validated locally end-to-end** (see commit `955b789`):
StatiCrypt wired into the deploy workflow, reading the password from
the `STATICRYPT_PASSWORD` GitHub Actions secret via the environment
(never a command-line argument), encrypting every HTML page recursively
(direct subpages protected, not only the root), and failing the build
loudly if the secret is absent rather than deploying unprotected. A
local dry run against the real site output with the requested initial
password confirmed: subpages show the password prompt, and the
password value does not appear anywhere in the encrypted output.

**Not yet exercised in real CI** — that requires the manual secret
step below and an actual GitHub Actions run, neither of which this
local session can perform.

## 18. Required manual GitHub secret step

A repository owner must set the `STATICRYPT_PASSWORD` secret under
*Settings → Secrets and variables → Actions* on the
`Learning-Robotics-Crash-Course` repository before the first deploy
under the updated workflow can succeed. This report does not state the
password value; see the task's own requested initial password in your
records. See README.md's "Access protection" section for the same
instruction in the public-facing (but not user-facing) documentation.

## 19. Commit list

```text
4f5f5cf docs: audit local Spot sources and code
a6893c0 refactor: pivot site to ALeRT Spot Tutorial
7927a95 docs: migrate ALeRT and RoboCup history
0c7dc40 assets: migrate and document historical images
e8741f2 docs: add Spot safety and prerequisites
698ba5a docs: rebuild Spot operating procedures
2ddaf7b docs: document Spot hardware and network architecture
eeafccf docs: document ROS interfaces and startup sequence
1b06d3f refactor: migrate existing content into Spot topics
955b789 feat: protect published tutorial with static password gate
2c6160a test: extend Spot tutorial verification
<this commit> docs: update README and migration report
```

Every commit builds and passes `verify-structure.py` individually
(re-verified, not just at HEAD).

## 20. Branch and push status

Branch `feat/alert-spot-tutorial`, created from
`feat/alert-advanced-robotics-tutorial` @ `aef08be5012f04a67aafdc9499c466def40ed2e8`.
`main` untouched throughout. No force-push used. Ready to push to
`origin` for review — **not merged to `main`**, per your instruction,
pending your content and security review.
