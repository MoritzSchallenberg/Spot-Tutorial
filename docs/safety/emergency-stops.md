# Emergency Stops

## Overview

The physical and software controls available to stop the system, and
when to use each one.

## Purpose

State, in order of how forcefully each one stops the system, what is
available — without inventing button locations, timings, or physical
outcomes that are not evidenced in the current code or configuration.

## System context

See [Safety Principles](safety-principles.md) for what each mechanism
actually is at the software level; this page is the quick-reference for
use during a session.

## Available controls, from least to most forceful

1. **Controlled stop** (`stop`/`sit` services) — commands the robot to
   stop or sit through its normal command interface. Use for a routine
   pause. `Verified in code`.
2. **Motor power off** (`power_off` service, or the dashboard's "Spot
   Power Off/On" button) — commands the robot to cut motor power
   through the normal command interface. `Verified in code`.
3. **Software E-stop endpoint** (the dashboard's "Estop" slider) —
   arms or disarms the software E-stop endpoint process the driver
   requires before it will command the robot at all. Disarming it
   (sliding back) stops that process, which the driver's own startup
   logic treats as equivalent to the robot being E-stopped. `Verified
   in code`.
4. **Physical E-stop button(s)** — a hardware-level control, described
   by the former ALeRT tutorial as two separate buttons: one for Spot,
   one for the manipulator arm. Their exact location and labeling are
   not confirmed against current hardware in this documentation pass —
   see the note below. `Historical procedure` for their existence and
   general purpose; `Unverified on hardware` for exact location,
   color, and labeling.

:::{admonition} Physical E-stop button locations: historical procedure, not verified
:class: warning

The former ALeRT tutorial described two physical E-stop buttons on the
robot and controller, with specific colors and press-and-hold timings.
This documentation pass could not independently confirm those exact
details against the current hardware or a current photograph, and does
not repeat them as fact. Confirm the actual physical location and
behavior of both E-stop buttons with a trained team member before any
session, rather than relying on this page alone.
:::

## What each button does, precisely

For the **software** mechanisms above, see [Safety
Principles](safety-principles.md) for the exact code-level behavior
and its verification level.

For the **physical** E-stop buttons: this documentation does not assert
a specific physical outcome (for example, whether Spot's legs go limp
or the robot sits automatically) beyond what Boston Dynamics' own SDK
calls are documented, in this codebase, to request — see [Safety
Principles: Spot E-stop](safety-principles.md#spot-e-stop-physical-button).
Do not assume a specific behavior beyond that documentation.

## Failure modes

If a physical E-stop button does not appear to have the expected effect,
treat the situation as a physical hazard and follow your team's
in-person emergency procedure — do not attempt to diagnose the system
in the moment.

## Verification

`Historical procedure` / `Unverified on hardware` — see the admonition
above. This page will be upgraded to `Verified on hardware` once a
concrete, supervised test confirms the current physical button
locations and behavior.

## Related components

[Safety Principles](safety-principles.md), [Operating Area](operating-area.md),
and Recovery and Troubleshooting under [Operating Spot](../operating/index.md).
