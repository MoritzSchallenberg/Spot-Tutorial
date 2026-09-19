# Decisions needed

Open decisions for the ALeRT Spot Tutorial that this repository's own
development work cannot make on its own — either because they are a
rights-holder call, or because they need confirmation against the
physical robot rather than its code. Every page that depends on one of
these says so explicitly (an `Unverified on hardware` label, an "Open
question" admonition, or a link back to this file) and degrades
gracefully rather than guessing.

For the repository's earlier, general multi-team "crash course" era
decisions (course sessions, hackathon logistics, room planning), see
[`maintainers/archive/course-era/decisions-needed-course-era.md`](maintainers/archive/course-era/decisions-needed-course-era.md) —
archived, not active.

---

## 1. Final content license

**Status:** undecided. The institute and the original rights holders
have not chosen a license for this content, so the repository
deliberately ships no `LICENSE` file and `LICENSES.md` does not pick
one on their behalf. Until a decision is made, no terms of reuse are
granted beyond what applies by default under copyright law. See
`LICENSES.md` for the full context and the available options.

## 2. Rights to the historical images

**Status:** unestablished. The photographs and diagrams under
`docs/_static/images/history/` and `historical-interface/`, migrated
from the former ALeRT Spot tutorial, carry no asserted license — see
`maintainers/historical-asset-migration.md` for the full
provenance/checksum table. They were reviewed for sensitive content
(no visible credentials, no readable network information) before
migration, but rights ownership itself was not established and needs
the same institute-level decision as item 1.

## 3. Sign-off on the safety instructions

**Status:** written from the current Spot/Kinova code and
configuration (see `maintainers/spot-code-audit.md`), not from a live
session on the robot. Every safety and operating page states its
verification level per step, but a trained team member has not signed
off on the procedures as a whole against the physical system. Needed
before treating this site as the sole reference during an actual
power-on or operation, rather than one input alongside direct
supervision.

## 4. Hardware verification of the operating procedures

**Status:** every command across `docs/operating/` and `docs/safety/`
is labeled `Verified in code`, `Verified in configuration`, `Historical
procedure`, or `Unverified on hardware` — nothing on the site claims
`Verified on hardware`, because no hardware-test record exists in the
sources this documentation was built from (see
`docs/safety/safety-principles.md#verification-levels`). Confirming
each procedure step-by-step against the real robot, and upgrading the
labels that pass, is unfinished work — not a defect in what exists
today, but a real gap between "the code says this happens" and "this
was seen happening."

## 5. The manipulator's actual gripper-control path

**Status:** open question, `docs/architecture/software-components.md`.
Two separate gripper-control mechanisms exist in the current code — the
Kortex hardware interface's internal-bus gripper communication
(`use_internal_bus_gripper_comm: True`) and a standalone Robotiq
driver/controller pair (`man_ws/src/ros2_robotiq_gripper`). Static
analysis could not determine which is authoritative for the combined
Spot + Gen3 robot. Needs a team member who has run the manipulator to
confirm.

## 6. The manipulator's actual degrees of freedom

**Status:** open question, `docs/architecture/hardware-overview.md`.
The URDF in the current code specifies 6 degrees of freedom; confirm
whether the physical arm in use is genuinely the 6-DOF Gen3 variant
before any documentation or planning assumes a 7-DOF arm.

## 7. The current operator input device

**Status:** open question, `docs/architecture/hardware-overview.md` and
throughout `docs/operating/`. The former ALeRT tutorial's screenshots
show a Steam Deck; the current teleop code (`read_dualsense.py`)
targets a Sony DualSense controller over `pydualsense`. Both are
documented — the Steam Deck as historical context, the DualSense as the
code-confirmed current mapping — but which one (or both) is actually in
use has not been reconfirmed against a live session.

## 8. The production ROS 2 middleware

**Status:** open question, `docs/architecture/computers-and-network.md`.
Both Zenoh (`rmw_zenoh_cpp`, run as a persistent systemd service) and
Fast-DDS are configured in the local sources. Which one is authoritative
for the current production deployment — or whether both are genuinely
in concurrent use for different purposes — needs a team member's
confirmation.

## 9. The active TF coordinate-frame convention

**Status:** open question, `docs/architecture/coordinate-frames.md`.
Two coexisting robot-frame conventions appear in the current code, with
different packages apparently using different conventions (including
one parent/child relationship that is the reverse of the usual TF
convention). A node written against "the robot's frame" without
checking which convention its target package expects can silently pick
the wrong one; this needs resolving at the code level, not just
documenting.

## 10. A later transfer to an `RRL-ALeRT` organisation repository

**Status:** not started; the repository was already renamed in place
once, to its current name, still under `MoritzSchallenberg`, rather
than transferred to another owner. See
`maintainers/rebrand-followups.md` for the full checklist a genuine
transfer to an `RRL-ALeRT`-organisation repository would still require
— organisation-owner permission, re-enabling Pages, updating
`html_baseurl` and every hard-coded repository link again, and
re-setting the `STATICRYPT_PASSWORD` secret on the destination
repository, since GitHub secrets do not carry over automatically.
