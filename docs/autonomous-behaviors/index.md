# Autonomous Behaviors

## Overview

How Spot sequences individual capabilities (navigate, detect, grasp,
return) into a complete autonomous mission.

## Purpose

Bring together the general decision-making concepts
([Autonomous Decision-Making](../decision-making/index.md): state
machines, behavior trees, RAFCON, PlanSys2, Golog++) with worked,
mission-scale examples
([Rescue Applications and Projects](../rescue-projects/index.md)) that
combine several topics into one run.

## System context

An autonomous behavior sits above navigation, perception and
manipulation, calling each as a step and reacting to their outcomes
(success, failure, timeout). On the current Spot system, the active
state-machine framework for this kind of mission logic is YASMIN (see
`spot-code-audit.md`, internal, for the evidence trail); a vendored
BehaviorTree.CPP/ROS2 integration also exists in the codebase but no
local package was found consuming it, so its current status is
recorded as unverified rather than asserted either way.

## Prerequisites

[Navigation and Mapping](../navigation-and-mapping/index.md) and
[Manipulator and MoveIt](../manipulation/index.md), since a mission
behavior calls into both.

## How it works

- **Autonomous Decision-Making** — general state-machine and
  behavior-tree concepts, RAFCON basics, PlanSys2, Golog++.
- **Rescue Applications and Projects** — worked examples: an autonomous
  rescue mission, a mission-monitoring setup, and platform-specific
  notes tying a mission back to the concrete robot it ran on.

## Verification

Each subpage carries its own verification badges. No claim on this hub
page itself is asserted as hardware-verified.

## Failure modes

A mission behavior's failure handling is only as good as the recovery
behavior of the steps it calls — see Recovery and Troubleshooting under
[Operating Spot](../operating/index.md) and each subpage's own
failure-mode notes.

## Related components

[Navigation and Mapping](../navigation-and-mapping/index.md),
[Manipulator and MoveIt](../manipulation/index.md),
[Sensors and Perception](../sensors-and-perception/index.md).

## Further learning

```{toctree}
:hidden:
:maxdepth: 2

../decision-making/index
../rescue-projects/index
```

- [Autonomous Decision-Making](../decision-making/index.md)
- [Rescue Applications and Projects](../rescue-projects/index.md)
