# Operating Area

## Overview

What the physical space around Spot must provide before a session
starts.

## Purpose

Spot is a legged robot with an attached manipulator arm; both move
under their own power once commanded. The operating area's job is to
make sure a command that behaves unexpectedly, or a stop that takes
longer than expected, does not put anyone or anything at risk.

## Requirements

- **Clear floor space.** Spot needs room to maneuver in any direction
  it might be commanded, including recovery movements (self-righting,
  sitting). Remove loose cables, cups, and fragile objects from the
  area, consistent with the general caution in the former ALeRT
  tutorial (`Historical procedure`).
- **A reachable E-stop.** Whoever is operating or supervising the
  session must be able to reach a physical E-stop control without
  stepping toward the robot — see [Emergency
  Stops](emergency-stops.md). The `spot_ros2_control` package's own
  README states this explicitly: "keep a safe distance from the robot
  when working with these controllers and ensure the e-stop can easily
  be pressed if needed" (source:
  `spot_ws/src/spot_ros2/spot_ros2_control/README.md`). `Verified in
  code` (the caveat exists in the shipped documentation for a component
  this system runs).
- **A supervising, trained person present.** See [Required
  Knowledge](required-knowledge.md) and [Operator
  Checklist](operator-checklist.md).
- **Awareness of the manipulator's reach.** The arm can extend beyond
  Spot's own footprint. Anyone near the robot should stay outside the
  arm's reach unless the exercise specifically requires closer
  supervision, per [Safety Principles](safety-principles.md).
- **No unrelated network traffic assumptions.** The system's software
  E-stop endpoint and driver communicate over the local network — see
  [Computers and Network](../architecture/computers-and-network.md)
  for the (anonymized) roles involved. A degraded network is a form of
  communication loss — see [Safety
  Principles](safety-principles.md#communication-loss).

## Verification

`Historical procedure` for the general caution (clear space, fragile
objects); `Verified in code` for the E-stop-distance requirement,
sourced from `spot_ros2_control`'s own README.

## Related components

[Safety Principles](safety-principles.md), [Emergency
Stops](emergency-stops.md), [Operator Checklist](operator-checklist.md).
