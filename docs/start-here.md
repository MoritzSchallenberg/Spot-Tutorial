# Start Here

## Overview

Concrete paths through this site, each ordering existing pages into a
sensible sequence. This page does not duplicate any explanation —
every step links to where that explanation actually lives. Looking to
fix something right now instead of learning the system in order? Use
the "Troubleshooting a problem" card on the [homepage](index.md)
directly.

## Purpose

A flat page list (see the homepage) is enough once you know what you
need. This page is for deciding what you need, and in what order to
read it.

## First day with Spot

**Who this is for:** a person about to operate the physical robot for
the first time.

1. [About ALeRT and Spot](about/index.md) — history
2. [Safety Principles](safety/safety-principles.md)
3. [System Architecture: At a glance](architecture/index.md) — system overview
4. [Operator Checklist](safety/operator-checklist.md)
5. [System Preparation](operating/system-preparation.md) and
   [Power-On Procedure](operating/power-on.md) — supervised startup
6. [Safe Shutdown](operating/safe-shutdown.md) — supervised shutdown

**Prior knowledge needed:** none beyond basic terminal comfort.
**Real hardware needed:** yes, from step 5 onward — steps 1–4 are
read-only and can be done anywhere.
**Read-only steps:** 1–4.
**Steps requiring supervision:** 5–6 (any step involving the physical
robot) — see [Operating Area](safety/operating-area.md).
**Expected outcome:** able to bring Spot up, drive it (see [Driving
Spot](operating/driving-spot.md), the step right after Power-On), and
shut it down safely under supervision. Manipulator operation is a
separate path below.

## Software development

**Who this is for:** someone writing or modifying ROS 2 code against
this system.

1. [System Architecture](architecture/index.md)
2. [ROS 2 Interfaces](architecture/ros2-interfaces.md)
3. [Coordinate Frames](architecture/coordinate-frames.md)
4. [Sensors and Perception](sensors-and-perception/index.md) — sensor data
5. [Simulation](simulation/index.md)
6. [Diagnostics and Testing](integration-testing/index.md)

**Prior knowledge needed:** [ROS 2](ros2/index.md) fundamentals
(nodes, topics, services, actions).
**Real hardware needed:** no — every step here is documentation, code,
and simulation; testing against the real system is covered by the
operator paths above.
**Read-only steps:** all of them — this path is entirely reading and,
optionally, writing/simulating code offline.
**Steps requiring supervision:** none.
**Expected outcome:** understand the actual topic/service/action
surface and TF tree well enough to write a node against it without
guessing a name.

## Manipulator development

**Who this is for:** someone working specifically with the Kinova arm
and gripper.

1. [Hardware Overview: Kinova Gen3 manipulator](architecture/hardware-overview.md#kinova-gen3-manipulator)
2. [Safety Principles: Manipulator (Kinova) fault handling](safety/safety-principles.md#manipulator-kinova-fault-handling)
3. [ROS 2 Interfaces](architecture/ros2-interfaces.md) — arm interfaces
4. [Manipulator and MoveIt](manipulation/index.md)
5. [Manipulator and MoveIt: Planned content](manipulation/index.md#planned-content) — planning scene; a full tutorial is not written yet, this section states what is planned and what exists today
6. [Operating the Manipulator](operating/operating-the-manipulator.md) — gripper open/close and manual control
7. [Recovery and Troubleshooting: Manipulator fault](operating/recovery-and-troubleshooting.md#manipulator-fault)

**Prior knowledge needed:** the Software development path above, plus
general MoveIt 2 concepts.
**Real hardware needed:** for steps 6–7; steps 1–5 are read-only.
**Read-only steps:** 1–5.
**Steps requiring supervision:** 6–7.
**Expected outcome:** understand the arm's actual degrees of freedom
(6, not necessarily 7 — see the Hardware Overview note), the
unresolved gripper-model and collision-checking caveats, and how to
safely open/close the gripper and recover from a fault.

## Autonomous rescue development

**Who this is for:** someone building or modifying mission-level
behavior (navigate, detect, grasp, return).

1. [Sensors and Perception](sensors-and-perception/index.md) — sensors
2. [Perception](perception/index.md)
3. [Mapping and World Models](mapping-world-models/index.md)
4. [Localization, Navigation and Exploration](navigation-exploration/index.md)
5. [Autonomous Behaviors](autonomous-behaviors/index.md)
6. [Diagnostics and Testing](integration-testing/index.md) — integration and testing

**Prior knowledge needed:** the Software development path above.
**Real hardware needed:** no for design/simulation work; yes for
validating a mission end to end (see [Operating
Spot](operating/index.md) for the supervision requirements that then
apply).
**Read-only steps:** all of them, until you actually run a mission.
**Steps requiring supervision:** none of the listed pages themselves;
running the resulting mission on the real robot does.
**Expected outcome:** understand how ALeRT's actual mission logic is
structured (YASMIN, not RAFCON, on the current real system — see
[Autonomous Behaviors](autonomous-behaviors/index.md)) well enough to
extend it.

## Related components

[Safety and Prerequisites](safety/index.md), [Operating
Spot](operating/index.md), [System Architecture](architecture/index.md),
[Recovery and Troubleshooting](operating/recovery-and-troubleshooting.md)
(linked directly from the homepage for an immediate problem, rather
than repeated here as a fifth learning path).
