# Operating Spot

## Overview

Step-by-step procedures for preparing, powering on, driving, and safely
shutting down the physical Spot system, plus recovery from the most
common failure situations.

## Purpose

Where [Safety and Prerequisites](../safety/index.md) explains the
principles, this section gives the concrete sequence of actions for
each phase of a session, sourced from the current Spot code, its launch
files, and the team's deployment configuration rather than from memory
or convention.

## System context

Every procedure here assumes the safety conditions in
[Safety and Prerequisites](../safety/index.md) are already met
(supervision present, operating area clear, E-stop reachable) before
the first step is taken.

## Sections

- [System Preparation](system-preparation.md) — checking the robot,
  batteries, and workspace before power-on.
- [Power-On Procedure](power-on.md) — bringing up Spot, the operator
  device, and the base software.
- [Operator Interface](operator-interface.md) — what the operator sees
  and controls once the system is running.
- [Driving Spot](driving-spot.md) — manual driving and switching
  between operating modes.
- [Operating the Manipulator](operating-the-manipulator.md) — enabling
  and manually controlling the arm and gripper.
- [Safe Shutdown](safe-shutdown.md) — returning the system to a
  stable, powered-down state.
- [Recovery and Troubleshooting](recovery-and-troubleshooting.md) —
  what to do after an interrupted startup, a communication loss, or a
  manipulator fault.

## Verification

Every procedure step is labeled with its verification level
(`Verified in code`, `Verified in configuration`, `Historical
procedure`, or `Unverified on hardware`); see [Safety
Principles](../safety/safety-principles.md#verification-levels) for
what each label means. A small number of historical screenshots
from the previous ALeRT tutorial are used where they still illustrate a
current interface; each is marked `Historical interface`.

## Failure modes

See [Recovery and Troubleshooting](recovery-and-troubleshooting.md) for
known failure situations and their recovery steps.

## Related components

[System Architecture](../architecture/index.md) documents the software
these procedures start and interact with.

```{toctree}
:hidden:
:maxdepth: 1

system-preparation
power-on
operator-interface
driving-spot
operating-the-manipulator
safe-shutdown
recovery-and-troubleshooting
```
