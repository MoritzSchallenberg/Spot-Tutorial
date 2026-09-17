# Start Here

## Overview

Five concrete paths through this site, each ordering existing pages
into a sensible sequence. This page does not duplicate any
explanation — every step links to where that explanation actually
lives.

## Purpose

A flat page list (see the homepage) is enough once you know what you
need. This page is for deciding what you need, and in what order to
read it.

## New Spot operator

**Who this is for:** a person about to operate the physical robot for
the first time.

1. [Safety Principles](safety/safety-principles.md)
2. [Operator Checklist](safety/operator-checklist.md)
3. [System Preparation](operating/system-preparation.md)
4. [Power-On Procedure](operating/power-on.md)
5. [Operator Interface](operating/operator-interface.md)
6. [Driving Spot](operating/driving-spot.md)
7. [Safe Shutdown](operating/safe-shutdown.md)

**Prior knowledge needed:** none beyond basic terminal comfort.
**Real hardware needed:** yes, from step 3 onward — steps 1–2 are
read-only and can be done anywhere.
**Read-only steps:** 1, 2.
**Steps requiring supervision:** 3–7 (any step involving the physical
robot) — see [Operating Area](safety/operating-area.md).
**Expected outcome:** able to bring Spot up, drive it, and shut it
down safely under supervision. Manipulator operation is a separate
path below.

## Spot software developer

**Who this is for:** someone writing or modifying ROS 2 code against
this system.

1. [System Architecture](architecture/index.md)
2. [ROS 2 Interfaces](architecture/ros2-interfaces.md)
3. [Coordinate Frames](architecture/coordinate-frames.md)
4. [Sensors and Perception](sensors-and-perception/index.md)
5. [Navigation and Mapping](navigation-and-mapping/index.md)
6. [Diagnostics and Testing](integration-testing/index.md)

**Prior knowledge needed:** [ROS 2](ros2/index.md) fundamentals
(nodes, topics, services, actions).
**Real hardware needed:** no — every step here is documentation and
code; testing against the real system is covered by the operator paths
above.
**Read-only steps:** all of them — this path is entirely reading and,
optionally, writing code offline.
**Steps requiring supervision:** none.
**Expected outcome:** understand the actual topic/service/action
surface and TF tree well enough to write a node against it without
guessing a name.

## Manipulation developer

**Who this is for:** someone working specifically with the Kinova arm
and gripper.

1. [Safety Principles: Manipulator (Kinova) fault handling](safety/safety-principles.md#manipulator-kinova-fault-handling)
2. [Hardware Overview: Kinova Gen3 manipulator](architecture/hardware-overview.md#kinova-gen3-manipulator)
3. [Manipulator and MoveIt](manipulation/index.md)
4. [Manipulator and MoveIt: Planned content](manipulation/index.md#planned-content) — a full planning-scene tutorial is not written yet; this section states what is planned and what exists today
5. [Operating the Manipulator](operating/operating-the-manipulator.md) — gripper open/close and manual control
6. [Recovery and Troubleshooting: Manipulator fault](operating/recovery-and-troubleshooting.md#manipulator-fault)

**Prior knowledge needed:** the Spot software developer path above,
plus general MoveIt 2 concepts.
**Real hardware needed:** for steps 5–6; steps 1–4 are read-only.
**Read-only steps:** 1–4.
**Steps requiring supervision:** 5–6.
**Expected outcome:** understand the arm's actual degrees of freedom
(6, not necessarily 7 — see the Hardware Overview note), the
unresolved gripper-model and collision-checking caveats, and how to
safely open/close the gripper and recover from a fault.

## Autonomous-systems developer

**Who this is for:** someone building or modifying mission-level
behavior (navigate, detect, grasp, return).

1. [Perception](perception/index.md)
2. [Mapping and World Models](mapping-world-models/index.md)
3. [Localization, Navigation and Exploration](navigation-exploration/index.md)
4. [Manipulator and MoveIt](manipulation/index.md)
5. [Autonomous Behaviors](autonomous-behaviors/index.md)

**Prior knowledge needed:** the Spot software developer path above.
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

## Troubleshooting

**Who this is for:** something in a running session is not working as
expected.

1. [Reference: System Status](reference/system-status.md) — check
   whether the component involved is even expected to work as you
   assumed.
2. [Diagnostics and Testing](integration-testing/index.md)
3. [Startup and Launch Sequence](architecture/startup-and-launch-sequence.md)
   — confirm the affected component actually started in the right
   order.
4. [Operator Interface](operating/operator-interface.md) — check what
   the dashboard/RViz actually shows right now.
5. [Recovery and Troubleshooting](operating/recovery-and-troubleshooting.md)

**Prior knowledge needed:** whatever operator or developer path above
matches what you were doing when the problem occurred.
**Real hardware needed:** only to reproduce or fix the issue; steps
1–4 can be read anywhere.
**Read-only steps:** 1–4.
**Steps requiring supervision:** any recovery action in step 5 that
touches the physical robot.
**Expected outcome:** a specific next action or a clear escalation
point, not a guess — see [Recovery and
Troubleshooting](operating/recovery-and-troubleshooting.md)'s own
per-case Stop condition before trying anything on the real robot.

## Related components

[Safety and Prerequisites](safety/index.md), [Operating
Spot](operating/index.md), [System Architecture](architecture/index.md).
