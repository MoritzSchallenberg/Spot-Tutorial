# Deployment and Configuration

## Overview

How the Spot software stack is installed, configured, and run — in
simulation and, where documented, on the physical robot and its
compute — plus the hardware-design material for team-built Spot
attachments.

## Purpose

Collect the setup and environment material that does not belong on the
step-by-step operating pages: the simulation environment used for most
of this site's exercises, the platform reference that maps general
topics onto Spot's actual topics and launch files, and hardware-design
tooling for physical add-ons.

## System context

Simulation ([Webots](../simulation/index.md)) and the real system
share the same higher-level ROS 2 interfaces where the simulation is
built to match them, but topic names and available sensors differ — see
[ALeRT / Spot](../platforms/index.md) for the specific mapping, and
[System Architecture](../architecture/index.md) for the real system's
actual startup and interface set.

## Prerequisites

[ROS 2](../ros2/index.md) and [Getting Started](../getting-started/index.md)
for a working development environment before either simulating or
deploying anything.

## How it works

- **Simulation** — the Webots-based ALeRT Spot simulation, simulation
  time, and the difference between simulation and hardware behavior.
- **ALeRT / Spot** — the platform reference: how each general topic's
  concepts map onto Spot's actual topics, launch files, and RViz setup
  in simulation, plus links out to the real-hardware
  [Safety and Prerequisites](../safety/index.md) and
  [Operating Spot](../operating/index.md) sections for the physical
  robot.
- **Hardware Design with KiCad and Fusion** — electrical schematics and
  parametric mechanical design for physical add-ons. Not part of the
  site's main navigation (it is not part of Spot's core system); kept
  reachable here for anyone extending Spot's hardware. See the
  migration report for why this was demoted rather than removed.

## Verification

Each subpage carries its own verification badges.

## Related components

[System Architecture](../architecture/index.md) documents the real
system this page's simulation and platform material is checked against.

## Further learning

```{toctree}
:hidden:
:maxdepth: 2

../simulation/index
../platforms/index
```

- [Simulation](../simulation/index.md)
- [ALeRT / Spot](../platforms/index.md)
