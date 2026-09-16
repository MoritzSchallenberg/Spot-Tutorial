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

- **System Preparation** — checking the robot, batteries, and workspace
  before power-on.
- **Power-On Procedure** — bringing up Spot, the operator device, and
  the base software.
- **Operator Interface** — what the operator sees and controls once the
  system is running.
- **Driving Spot** — manual driving and switching between operating
  modes.
- **Operating the Manipulator** — enabling and manually controlling the
  arm and gripper.
- **Safe Shutdown** — returning the system to a stable, powered-down
  state.
- **Recovery and Troubleshooting** — what to do after an interrupted
  startup, a communication loss, or a manipulator fault.

## Verification

Every procedure step is labeled with its verification level
(`Verified in code`, `Verified in configuration`, `Historical
procedure`, or `Unverified on hardware`); see Safety Principles under
[Safety and Prerequisites](../safety/index.md) for what each label
means. A small number of historical screenshots
from the previous ALeRT tutorial are used where they still illustrate a
current interface; each is marked `Historical interface`.

## Failure modes

See **Recovery and Troubleshooting** for known failure situations and
their recovery steps.

## Related components

[System Architecture](../architecture/index.md) documents the software
these procedures start and interact with.
