# Safety and Prerequisites

## Overview

What to know and check before working with the physical Spot system:
the different kinds of stop the system supports, where the emergency
stops are and what they do, what the operating area must look like, and
what knowledge and sign-off a person needs before touching the robot.

## Purpose

Spot is a heavy, fast-moving legged robot with an attached manipulator
arm. This section states, objectively and without embellishment, what
is and is not known about how the system behaves in each kind of stop
condition, so that anyone operating it — or reading this site before
ever touching it — has an accurate picture rather than an assumed one.

## System context

This section covers the robot and its immediate operating environment.
For how to actually run a session end to end, see
[Operating Spot](../operating/index.md). For how the software
implements these stop mechanisms, see
[System Architecture](../architecture/index.md).

## Sections

- [Safety Principles](safety-principles.md) — the different stop states
  (controlled stop, software stop, motor/power-off, Spot E-stop,
  manipulator E-stop, communication loss, system fault, physical
  hazard) and what is known about each.
- [Emergency Stops](emergency-stops.md) — the physical E-stop controls,
  what they do, and when to use them.
- [Operating Area](operating-area.md) — what the physical space around
  the robot must provide before a session starts.
- [Required Knowledge](required-knowledge.md) — the background
  knowledge (ROS 2, Linux, this site's own topics) a person needs
  before operating the system, and where to get it.
- [Operator Checklist](operator-checklist.md) — a condensed, actionable
  checklist tying the rest of this section together for use immediately
  before a session.

## Verification

Every claim in this section is labeled with one of: `Verified in code`,
`Verified in configuration`, `Historical procedure`, or
`Unverified on hardware`. No claim in this section is currently labeled
`Verified on hardware` — see `spot-security-audit.md` and
`spot-code-audit.md` (internal) for why, and update these pages if and
when a specific procedure is actually tested and confirmed on the real
robot.

## Related components

[Operating Spot](../operating/index.md) is the step-by-step counterpart
to this section's principles.

```{toctree}
:hidden:
:maxdepth: 1

safety-principles
emergency-stops
operating-area
required-knowledge
operator-checklist
```
