# Operator Checklist

## Overview

A condensed, actionable checklist tying together
[Safety Principles](safety-principles.md), [Emergency
Stops](emergency-stops.md), [Operating Area](operating-area.md), and
[Required Knowledge](required-knowledge.md), organized into five
phases so you can jump to the one you actually need. Printable —
select this page and print; the site navigation is hidden
automatically in print output.

## Purpose

A single page to run through right before, during, and after a
session, rather than re-reading the full section each time.

## Before power-on

- [ ] **Work area** clear of loose cables, cups, and fragile objects,
      with room for Spot to maneuver in any direction — see [Operating
      Area](operating-area.md).
- [ ] **People**: a trained team member is present and supervising (or
      is the operator); anyone else nearby knows to stay outside the
      manipulator's reach.
- [ ] **Obstacles** in the intended operating path identified and
      cleared or noted.
- [ ] **E-stop reachability**: the physical E-stop button(s) are
      located and reachable without stepping toward the robot —
      confirm their current location with a trained team member; see
      the note in [Emergency Stops](emergency-stops.md).
- [ ] **Battery state**: Spot's battery and the operator device's
      battery are checked before starting (`Historical procedure`,
      consistent caution from the former ALeRT tutorial; specific
      charge-level guidance is not independently confirmed for the
      current hardware).
- [ ] **Visible hardware problems**: a quick visual check of Spot and
      the manipulator for anything obviously wrong (loose cabling,
      visible damage) before powering on.
- [ ] **Manipulator position**: the arm is in a position where power-on
      will not cause it to hit anything as it settles.

## Before enabling motion

- [ ] **Operator connection**: the operator device is connected and the
      dashboard is responsive — see [Operator
      Interface](../operating/operator-interface.md).
- [ ] **Robot state**: `status/estop` reports `NOT_STOPPED` and the
      driver log shows "Found estop!" — see [Power-On
      Procedure](../operating/power-on.md).
- [ ] **Software status**: the subsystem windows you need are all
      showing "✓ Running", none showing "💥 CRASHED" — see [Operator
      Interface](../operating/operator-interface.md).
- [ ] **Sensor status**: sensor topics you depend on are publishing —
      see [Recovery and Troubleshooting: Case
      5](../operating/recovery-and-troubleshooting.md#case-5-sensor-data-is-missing)
      if not.
- [ ] **Free movement zone**: the path Spot is about to move through is
      actually clear right now, not just at the start of the session.
- [ ] **Responsible operator**: it is clear, out loud, who is
      controlling the robot for this motion.
- [ ] **Abort signal**: everyone present knows the agreed signal or
      word to stop immediately, and who is watching for it.

## Before manipulation

- [ ] **Arm workspace**: the manipulator's reachable volume is clear of
      people and obstacles.
- [ ] **Gripper**: checked open/closed state matches what the next
      action expects — see [Operating the
      Manipulator](../operating/operating-the-manipulator.md).
- [ ] **Collision area**: aware that this MoveIt configuration disables
      most arm-vs-body/leg collision checking — see [Operating the
      Manipulator](../operating/operating-the-manipulator.md)'s
      collision-checking warning. MoveIt will not catch every
      collision a person would.
- [ ] **Planning scene / known obstacles**: a full planning-scene
      workflow is not yet written for this site — see [Manipulator and
      MoveIt: Planned
      content](../manipulation/index.md#planned-content). Until then,
      obstacle avoidance in the arm's workspace is the operator's
      responsibility, not the software's.
- [ ] **Supervision**: a trained team member is specifically watching
      the arm, not just the robot generally, for the duration of the
      manipulation task.

## Before shutdown

- [ ] **Stable stance**: Spot is sitting or otherwise in a stable,
      commanded stance, not mid-motion — see [Safe
      Shutdown](../operating/safe-shutdown.md).
- [ ] **Arm position**: the manipulator is retracted or otherwise in a
      safe position before motors are powered off.
- [ ] **Running missions**: any autonomous behavior or mission in
      progress is stopped deliberately, not abandoned mid-execution —
      see [Autonomous Behaviors](../autonomous-behaviors/index.md).
- [ ] **Relevant logs**: anything worth keeping (an unexpected fault, an
      unusual observation) is noted before the session's context is
      lost.
- [ ] **Controlled process order**: subsystems stopped in the order
      given in [Safe Shutdown](../operating/safe-shutdown.md) — later
      subsystems (manipulator, navigation) before the base driver, not
      the reverse.

## After shutdown

- [ ] **Motor state**: confirmed powered off, not merely commanded off
      — see [Safe Shutdown](../operating/safe-shutdown.md).
- [ ] **Manipulator state**: confirmed powered off and in a safe
      position.
- [ ] **Power supply**: Spot and the operator device physically powered
      down.
- [ ] **Detected errors**: any fault or crash observed during the
      session is noted, even if it was recovered from.
- [ ] **Documented deviations**: anything that happened differently
      from what this documentation describes is worth reporting back —
      this site is only as accurate as the code and configuration it
      was audited against.

## Verification

This page aggregates verification levels already stated on the pages
it links to; it does not introduce new claims of its own.

## Related components

[Safety Principles](safety-principles.md), [Emergency
Stops](emergency-stops.md), [Operating Area](operating-area.md),
[Required Knowledge](required-knowledge.md), [Operating
Spot](../operating/index.md).
