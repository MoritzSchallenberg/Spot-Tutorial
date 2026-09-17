# System Architecture

## Overview

How the Spot system is put together: the physical hardware, the
computers and network it runs on, the software components on top of
that hardware, the order they start in, the ROS 2 interfaces between
them, the coordinate frames the system maintains, and how data flows
from sensors to actions.

## Purpose

Take a new reader from the whole system down to individual components,
grounded in the actual Spot code and deployment configuration rather
than a generic robotics description. Every component and interface
listed here has a concrete source reference in `spot-code-audit.md`
(internal); nothing is included on the basis of a filename or a guess.

## System context

This section describes the system as found in the current Spot
codebase and deployment configuration at the time of writing (see
`spot-source-audit.md`, internal, for exactly which workspaces and
packages were treated as authoritative per subsystem, and which were
excluded as legacy or a different platform).

## Sections

- [Hardware Overview](hardware-overview.md) — the physical components:
  Spot itself, the Kinova Gen3 manipulator, the gripper, sensors, and
  the operator device.
- [Computers and Network](computers-and-network.md) — the compute
  roles involved and how they communicate, using role placeholders
  instead of real host or network identifiers.
- [Software Components](software-components.md) — the ROS 2 packages
  and nodes that make up the running system, organized by subsystem.
- [Startup and Launch Sequence](startup-and-launch-sequence.md) — the
  order components come up in, for each of the system's distinct
  operating modes.
- [ROS 2 Interfaces](ros2-interfaces.md) — the topics, services, and
  actions that connect the software components.
- [Coordinate Frames](coordinate-frames.md) — the TF frame tree the
  system maintains.
- [Data Flow](data-flow.md) — how data moves from sensors, through
  processing, to actions.

## Verification

Every component and interface is labeled with its verification level.
Diagrams are provided as accessible Mermaid diagrams, checked for
legibility in both light and dark mode.

## Related components

[Operating Spot](../operating/index.md) is the procedural counterpart —
this section explains what the system is, that section explains how to
run it.

```{toctree}
:hidden:
:maxdepth: 1

hardware-overview
computers-and-network
software-components
startup-and-launch-sequence
ros2-interfaces
coordinate-frames
data-flow
```
