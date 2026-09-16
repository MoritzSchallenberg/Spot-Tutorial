# Spot Tutorial source audit

**Not part of the published website.** Internal working document for
Entwicklungsauftrag 9 (ALeRT Spot Tutorial pivot). Excluded from the Sphinx
build because the Sphinx source root is `docs/` and `maintainers/` is
outside it; not linked from any published toctree; must stay that way.

## Method

Three local source trees, plus this repository itself, were inventoried
read-only (no code executed, no playbooks run, no secrets opened) before any
content was written. Findings below are limited to what was directly
observed in file paths, README text, commit metadata, and static config —
not inferred from filenames alone, per the task's explicit warning.

## 1. Local paths

| # | Source | Path |
| - | --- | --- |
| 1 | Website repository (this repo, the migration target) | `/home/canvastino/Schreibtisch/Spot Tutorial/Learning-Robotics-Crash-Course` |
| 2 | Old Spot tutorial (scraped Sphinx/RTD static export, no git) | `/home/canvastino/Schreibtisch/Spot Tutorial/00-02 Quelle 2 Spot Tutorial/Website Code` |
| 3 | Current Spot code | `/home/canvastino/Schreibtisch/Spot Tutorial/Backup Ansible/workspaces` |
| 4 | Ansible / deployment bestand | `/home/canvastino/Schreibtisch/Spot Tutorial/Backup Ansible/ansible` + `Backup Ansible/configs` |

The full current Spot code **was found locally** (path 3 above) — the
task's contingency for a missing Spot code path ("do not invent the
system/operations section, report the missing path as a blocker") does not
apply. System and operating-procedure content in this pivot is sourced from
path 3 and cross-checked against path 4.

## 2. Git repositories and commit state

- **Website repo** (path 1): single git repository. Before branching:
  `HEAD = aef08be5012f04a67aafdc9499c466def40ed2e8` on
  `feat/alert-advanced-robotics-tutorial`, working tree clean, in sync with
  `origin/feat/alert-advanced-robotics-tutorial`. Branch
  `feat/alert-spot-tutorial` created from this commit for this task.
- **Old Spot tutorial** (path 2): not a git repository (a static scrape).
  Every page footer reads "© Copyright 2024, MASCOR Institute, FH Aachen" —
  the only date evidence for this source as a whole.
- **Current Spot code** (path 3): **no top-level git repository.** It is a
  2026-09-17 filesystem backup of one development machine (`max1@alert`,
  Ubuntu 22.04, ROS 2 Humble), taken from `workspaces/README.md`'s own
  description. Each of the 188 ROS 2 packages across 74 sub-repositories
  carries its *own* `.git` (some none at all — see §4). There is no single
  commit hash for "the Spot code"; per-package commit dates are the only
  granular evidence, cited by package in §3 and in `spot-code-audit.md`.
- **Ansible/deployment bestand** (path 4): no git repository found.

## 3. Which local source is authoritative for which part of the tutorial

| Tutorial section | Authoritative source | Notes |
| --- | --- | --- |
| History / ALeRT / RoboCup Rescue background (`docs/about/`) | Old Spot tutorial (path 2), specifically `ALeRT Team Page`, `Spot Documentation/00 General Information`, `Tutorials/01 Introduction` | Content reused per Section 5's rule: no new team history invented; Carologistics mentions stripped; time-bound statements get a "Historical snapshot" banner. |
| Safety principles (`docs/safety/`) | Current Spot code (path 3) launch files / hardware-interface packages, cross-checked against path 4 configs; old tutorial's `Spot Documentation/08 Spot Startup` used **only** for its procedural skeleton, never its wording | Old page's humour, WiFi SSID name, and personal-credit line are explicitly excluded (Section 8). |
| Operating procedures (`docs/operating/`) | Current Spot code (path 3): `spot_ws` (base driver, dashboard), `man_ws` (manipulator/gripper), Ansible/config (path 4); historical screenshots only as a last resort, labelled `Historical interface` | Per Section 9's source-priority order. |
| System architecture (`docs/architecture/`) | Current Spot code (path 3) static analysis: package manifests, launch files, URDF/Xacro, controller/MoveIt configs, udev rules; Ansible/deployment bestand (path 4) for the network/role picture | See `spot-code-audit.md` for the full evidence tables. |
| Existing 13 topic directories (ROS 2 basics, TF2, sensors, mapping, navigation, manipulation, etc.) | Website repo (path 1) as it stands after Entwicklungsauftrag 8 | Reclassified into the new nav per Section 12, not rewritten from scratch. |

## 4. Current Spot code: per-workspace inventory

Source: `Backup Ansible/workspaces/README.md` (the backup's own manifest,
dated 2026-09-17) plus direct inspection of each workspace's `src/`. Dates
are file/commit dates as observed on 2026-09-17.

| Workspace | Packages | Own git per-package? | Most recent activity | Role |
| --- | --- | --- | --- | --- |
| `spot_ws` | 42 (72 incl. nested) | Yes | 2026-06-25 (`frame_server`) | Spot base driver, dashboard, exploration, perception, simulation (Webots) |
| `man_ws` | 14 | Yes | 2026-08-03 (`kortex_ros2_python`) — **newest workspace in the backup** | Kinova Gen3 manipulator + Robotiq gripper, MoveIt config |
| `alert_nav_ws` | 4 | Yes | 2026-09-08 (`octo_navigation`) — **newest single commit in the backup** | Octomap-based 3D navigation on `move_base_flex` |
| `yasmin_ws` | 2 (+4 sub-packages) | Yes | 2025-06-28 | YASMIN state-machine framework + deliberation glue |
| `go2_ws` | 19 | Yes | 2025-07-11 | **Different robot** (Unitree Go2) — not Spot, must not be conflated |
| `omx_ws` | 5 | Yes | 2025-07-15 | OpenMANIPULATOR-X on Dynamixel — tied to the Go2 platform (`go2_omx_moveit`), not Spot |
| `oliver_ws` | 2 | Partial | 2026-04-14 | Audio subsystem |
| `david_ws` | 1 | Yes | 2026-06-26 | DualSense gamepad teleop for Spot |
| `france_sensor_ws` | 4 | Mostly none | 2023-05-18 | Dormant since 2023 — likely legacy |
| `cpp_spot_ws` | 1 | No | n/a (dir mtime 2023-06-09) | Stale/unused C++ Spot node |
| `livox_ws` | 1 | Yes | 2024-09-11 (repo), 2026 (dir) | Ambiguous — new addition or dormant, not resolved from evidence alone |
| `rtabmap_ws` | 0 | n/a | n/a | Empty |

**Superseded-in-place evidence** (a package's own README states it is
legacy): `spot_ws/src/kinova_stuffs` explicitly states the team is
switching to `ros2_kortex` (now in `man_ws`) — used as the authoritative
manipulator integration throughout this tutorial; `kinova_stuffs` is
referenced only as historical background where relevant.

**Ambiguous, flagged rather than guessed:** whether `spot_ws/src/BT`
(vendored BehaviorTree.CPP/ROS2) is abandoned or simply not yet wired to a
demo package — no local consumer package was found, but absence of a
consumer is not proof of deprecation. Documented as `Unverified` status in
`spot-code-audit.md`, not asserted either way in public content.

## 5. Ansible / deployment bestand structure

No formal multi-host inventory, `group_vars`, or `host_vars` structure
exists. The only Ansible content is a single, self-contained playbook
(`Backup Ansible/other_code/ansible_spot_nuc-main/spot_nuc.yaml`) targeting
`hosts: localhost` — a local bootstrap script for one NUC, not a
role-based deployment across named hosts. It covers 3 of 74 repositories
and 1 of 12 non-empty workspaces (`spot_ws`, partially), and is documented
as incomplete by its own accompanying `ansible/README.md`. `configs/`
supplies real udev rules (Kinova arm, Seek Thermal, O3P, RealSense), RViz
layout, Zenoh/Fast-DDS middleware config, and rosdep sources for the
Boston Dynamics message bundle — used as evidence for the hardware and
network architecture pages, with any real host/IP/SSID values replaced by
the neutral placeholders specified in Section 4 of the task
(`<SPOT_IP>`, `<COMPUTE_HOST>`, `<OPERATOR_HOST>`, `<ROBOT_NETWORK>`).

Section 11.2's "Computer and Network Architecture" page is therefore
written as a **role diagram** (Operator Station / Robot Computer / Spot
Base / Manipulator Controller / Sensors) grounded in what the code and
configs actually show is deployed to one development machine — not as a
multi-host production inventory, because no such inventory exists in the
local sources.

## 6. Cross-reference to prior audits in this repository

`maintainers/repository-audit.md` (Entwicklungsauftrag 8) already audited
the GitHub-hosted versions of several of these same packages
(`alert_ros2`, `spot_gen3_moveit`, `ros2_kortex`, `kinova_stuffs`,
`alert_auto_dexterity`, and others) via the GitHub API and capped every
finding at "Repository exists" / "Repository documented" because no build,
simulation, or hardware test was performed. This audit reaches the same
packages from the other direction (local backup, not GitHub) and adds
concrete local evidence (commit dates, in-repo README statements, launch
files, configs) but does not change that prior audit's conclusion: nothing
here rises to "Build verified" or "Hardware verified" either, for the same
reason — static analysis of source and config was performed, not
execution.
