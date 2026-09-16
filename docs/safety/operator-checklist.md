# Operator Checklist

## Overview

A condensed, actionable checklist tying together
[Safety Principles](safety-principles.md), [Emergency
Stops](emergency-stops.md), [Operating Area](operating-area.md), and
[Required Knowledge](required-knowledge.md), for use immediately
before a session.

## Purpose

A single page to run through right before touching the robot, rather
than re-reading the full section each time.

## Before every session

- [ ] A trained team member is present and supervising (or is the
      operator).
- [ ] The operating area is clear of loose cables, cups, and fragile
      objects, with room for Spot to maneuver in any direction.
- [ ] The physical E-stop button(s) are located and reachable without
      stepping toward the robot — confirm their current location with
      a trained team member; see the note in [Emergency
      Stops](emergency-stops.md).
- [ ] Anyone near the robot understands the manipulator's reach and
      stays outside it unless the exercise requires closer supervision.
- [ ] Spot's battery and the operator device's battery are checked
      before starting (`Historical procedure`, consistent caution from
      the former ALeRT tutorial; specific charge-level guidance is not
      independently confirmed for the current hardware).
- [ ] The operator knows the difference between a controlled stop,
      motor power off, the software E-stop endpoint control, and a
      physical E-stop button — see [Safety
      Principles](safety-principles.md).

## During the session

- [ ] Confirm the driver reports the E-stop endpoint present ("Found
      estop!" in the driver's log — see [Power-On
      Procedure](../operating/power-on.md)) before issuing any motion
      command.
- [ ] Keep the abort condition for the current step in mind — see the
      relevant [Operating Spot](../operating/index.md) procedure.

## After the session

- [ ] Follow [Safe Shutdown](../operating/safe-shutdown.md) rather than
      simply disconnecting power.

## Verification

This page aggregates verification levels already stated on the pages
it links to; it does not introduce new claims of its own.

## Related components

[Safety Principles](safety-principles.md), [Emergency
Stops](emergency-stops.md), [Operating Area](operating-area.md),
[Required Knowledge](required-knowledge.md), [Operating
Spot](../operating/index.md).
