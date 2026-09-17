# Navigation and Mapping

## Overview

How Spot builds a model of its surroundings and moves through it
without collisions.

## Purpose

Bring together map-building
([Mapping and World Models](../mapping-world-models/index.md)) and
using a map to move and explore
([Localization, Navigation and Exploration](../navigation-exploration/index.md))
under one entry point.

## System context

Mapping and localization sit between perception (sensor data placed in
TF frames) and navigation (planners and controllers that consume a map
and a pose). On the real Spot system, the currently active navigation
stack builds on `move_base_flex` with Octomap-derived 3D/2D
representations — see [Software
Components](../architecture/software-components.md) for the concrete
package names and evidence.

## Prerequisites

[Sensors and Perception](../sensors-and-perception/index.md) for TF and
point cloud/LiDAR data; [ROS 2](../ros2/index.md) fundamentals.

## How it works

- **Mapping and World Models** — occupancy grids, SLAM Toolbox, 3D
  mapping, saving and loading maps.
- **Localization, Navigation and Exploration** — AMCL, Nav2, costmaps,
  planners, controllers, recovery behavior, and frontier-based
  exploration.

## Verification

Each subpage carries its own verification badges. Statements about the
currently active navigation stack on real Spot hardware are grounded in
`spot-code-audit.md` (internal) and cited by evidence there; nothing on
this hub page itself makes a hardware claim.

## Failure modes

See each subpage's own failure-mode/troubleshooting content, and
[Recovery and Troubleshooting](../operating/recovery-and-troubleshooting.md)
for what to do when navigation stalls or the robot cannot reach a goal
during an operating session.

## Related components

[Sensors and Perception](../sensors-and-perception/index.md) supplies
the data this stack consumes. [Autonomous Behaviors](../autonomous-behaviors/index.md)
sequences navigation goals as part of a larger mission.

## Further learning

```{toctree}
:hidden:
:maxdepth: 2

../mapping-world-models/index
../navigation-exploration/index
```

- [Mapping and World Models](../mapping-world-models/index.md)
- [Localization, Navigation and Exploration](../navigation-exploration/index.md)
