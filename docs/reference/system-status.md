# System Status

## Overview

A compact, subsystem-by-subsystem status matrix, so that "documented"
is never mistaken for "hardware-verified" at a glance.

## Purpose

Every claim on this site already carries its own verification label
where it is made. This page exists purely as a fast lookup across
subsystems — it does not introduce any status not already stated, with
evidence, on the linked pages.

## Status matrix

```{list-table}
:header-rows: 1
:widths: 18 12 14 14 14 28

* - Subsystem
  - Documented
  - Found in code
  - Simulation-checked
  - Hardware-checked
  - Open question
* - Spot base driver
  - Yes
  - Yes
  - No
  - No
  - None major — see [Software Components](../architecture/software-components.md)
* - Operator interface
  - Yes
  - Yes
  - N/A
  - No
  - Current button layout not reconfirmed against a live session — see [Operator Interface](../operating/operator-interface.md)
* - Sensors
  - Yes
  - Yes
  - N/A
  - No
  - Exact RealSense unit count not confirmed — see [Hardware Overview](../architecture/hardware-overview.md)
* - Mapping
  - Yes
  - Yes
  - No
  - No
  - None major — see [Software Components](../architecture/software-components.md)
* - Navigation
  - Yes
  - Yes
  - No
  - No
  - `feet_center` vs. `body` robot-frame mismatch between packages — see [Coordinate Frames](../architecture/coordinate-frames.md)
* - Kinova arm
  - Partial
  - Yes
  - No
  - No
  - Degrees of freedom: code specifies 6, not confirmed 7 — see [Hardware Overview](../architecture/hardware-overview.md#kinova-gen3-manipulator)
* - Gripper
  - Partial
  - Yes
  - No
  - No
  - Model ambiguous (2F-140 vs. 2F-85 naming) and control path unresolved — see [Hardware Overview](../architecture/hardware-overview.md#gripper)
* - MoveIt
  - Yes
  - Yes
  - Yes (Webots)
  - No
  - Most arm-vs-body/leg collision pairs disabled in the SRDF — see [Operating the Manipulator](../operating/operating-the-manipulator.md)
* - Autonomous behaviors
  - Yes
  - Yes
  - Unclear
  - No
  - BehaviorTree.CPP status (`Unverified`, not asserted deprecated) — see [Software Components](../architecture/software-components.md#behaviormission)
* - Deployment (Ansible/systemd)
  - Partial
  - Yes
  - N/A
  - N/A
  - Provisioning playbook covers 1 of 12 non-empty workspaces — see `spot-source-audit.md` (internal)
```

`Partial` means the underlying evidence itself is incomplete or
contradictory (e.g. two sources disagree), not that this documentation
is incomplete about it — every `Partial`/`Open question` cell links to
the page that explains the ambiguity in full.

## Verification

This page is a summary view; every cell traces back to a verification
level already stated on the linked page. Nothing here is
`Verified on hardware` — see [Safety
Principles](../safety/safety-principles.md#verification-levels).

## Related components

[System Architecture](../architecture/index.md), [Safety
Principles](../safety/safety-principles.md).
