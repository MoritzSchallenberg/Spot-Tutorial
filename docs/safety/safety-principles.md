# Safety Principles

## Overview

Spot can be stopped in several distinct ways, at several distinct
levels of the system. This page states what each one actually does,
based on the current Spot code, and explicitly marks what is not
knowable from that code alone.

## Purpose

An operator, or anyone reading this site before ever approaching the
robot, needs to know which stop mechanism applies to which situation,
and what each one does and does not guarantee. Conflating them is a
real risk: the wrong control for a given situation may not stop the
robot fast enough, or may stop it in a way that requires a longer
recovery.

## System context

This page describes mechanisms; [Emergency Stops](emergency-stops.md)
describes the physical controls and when to use them, and [Operating
Spot](../operating/index.md) shows them in the context of a real
session.

(verification-levels)=
## Verification levels

Every claim on this page and on the Operating Spot pages carries one of
these labels:

`Verified in code`
: The behavior is directly implemented in the current Spot codebase —
  cite the file.

`Verified in configuration`
: The behavior follows from a deployment configuration file (a YAML
  parameter, a launch default) rather than from logic in the code
  itself.

`Historical procedure`
: The claim comes from the former ALeRT tutorial and has not been
  independently confirmed against the current code.

`Unverified on hardware`
: No test record exists confirming this behavior was actually observed
  on the physical robot. This includes every claim on this site at the
  time of writing — see `spot-security-audit.md` and
  `spot-code-audit.md` (internal) for why no `Verified on hardware`
  claim is made anywhere in this section yet.

## The stop mechanisms

### Controlled stop

A command telling Spot to come to a stop and/or sit down through its
normal command interface, rather than cutting power. The `spot_driver`
node exposes this as the `stop` and `sit` `Trigger` services (source:
`spot_driver/spot_driver/spot_ros2.py`, service registration block).
The robot remains under software control throughout — this is not a
safety stop, it is a commanded motion.

`Verified in code`

### Software stop (E-stop endpoint release/assert via ROS)

The `spot_driver` node also exposes `estop/hard` (severe), `estop/gentle`,
and `estop/release` as `Trigger` services, wrapping the Boston Dynamics
SDK's `EstopKeepAlive.stop()` / `.settle_then_cut()` / `.allow()`
calls respectively (source: `spot_driver/spot_driver/spot_ros2.py`,
service registration block; `spot_wrapper/spot_wrapper/wrapper.py`,
`assertEStop`/`disengageEStop`).

:::{admonition} Known issue in the current code
:class: warning

A comment in `spot_driver/spot_driver/spot_ros2.py`, next to the
`estop/hard`/`estop/gentle` service registrations, states these calls
did not appear to be functional at the time it was written ("Neither
estop call appears to be functional atm (functions called in wrapper
return a 'no attribute' error)"). Do not rely on these ROS services as
a working stop mechanism without first confirming, on the actual
deployed code, that this is fixed.
:::

`Verified in code` (services exist and are registered) —
`Unverified on hardware` (whether they currently work)

### The operator dashboard's "Estop" control

The `alert_dashboard_rqt` operator dashboard has a labeled "Estop"
slider (source: `alert_dashboard_rqt/alert_dashboard_rqt/spot_estop_rqt.py`).
Sliding it past its midpoint does **not** call a ROS stop service — it
starts two background processes (`fastdds discovery` and
`spot_driver_plus/spot_estop.py`, the software E-stop endpoint) that
the rest of the driver requires to be present before it will command
the robot at all (see [Emergency Stops](emergency-stops.md)). Sliding it
back kills those processes. Treat this control as **arming or
disarming the software E-stop endpoint**, not as an emergency-stop
button in the usual sense.

`Verified in code`

### Motor power on/off

`power_on` and `power_off` are separate `Trigger` services on the same
`spot_driver` node (source: `spot_driver/spot_driver/spot_ros2.py`,
service registration block), also exposed as a single "Spot Power
Off/On" button on the operator dashboard that calls both in sequence
(source: `alert_dashboard_rqt/alert_dashboard_rqt/spot_estop_rqt.py`,
`spot_power_off_on_command`). `power_on()` in `spot_wrapper` explicitly
checks the software E-stop endpoint before attempting to power on: "Enable
the motor power if e-stop is enabled" (source:
`spot_wrapper/spot_wrapper/wrapper.py`, `power_on()` docstring and
logic).

`Verified in code`

### Spot E-stop (physical button)

A physical E-stop button, described by the former ALeRT tutorial as
one of two big red buttons on Spot's rear. Boston Dynamics' Spot has a
dedicated hardware/software E-stop system (`spot_msgs/EStopStateArray`,
published on `status/estop`, with `TYPE_HARDWARE` and `TYPE_SOFTWARE`
estop entries — source: `spot_driver/src/conversions/robot_state.cpp`,
`spot_driver/src/robot_state/state_middleware_handle.cpp`). The
`spot_hardware_interface` component explicitly checks this state and
**refuses to activate** if the robot reports itself E-stopped (source:
`spot_hardware_interface/src/spot_hardware_interface.cpp`,
`check_estop()`, called from `on_activate()`).

What physically happens to Spot's motors and posture at the moment this
button is pressed is not implemented in this codebase — that behavior
lives in Boston Dynamics' own robot firmware and SDK, which this
codebase only calls into. The SDK-level distinction this codebase does
carry: a "severe" stop is documented (in this code's own docstring) as
cutting motor power immediately, while a "gentle" stop is documented as
attempting to settle the robot on the ground first (source:
`spot_wrapper/spot_wrapper/wrapper.py`, `assertEStop` docstring). This
codebase does not independently confirm what "settle" or "cut power"
looks like on the physical robot.

`Verified in code` (that the system checks and reacts to this state) —
`Unverified on hardware` (the robot's physical response)

### Manipulator (Kinova) fault handling

The Kinova arm has no "E-stop" concept in this codebase's terminology —
it has **fault** handling instead. `kortex_driver`'s fault-reset routine
(triggered via the `reset_fault` command interface, exposed by the
`picknik_reset_fault_controller`) switches the arm to single-level
servoing, calls the Kinova SDK's `ApplyEmergencyStop` **twice** — an
in-code comment notes this was found necessary because calling it once
was unreliable in testing — then calls `ClearFaults()`, then restores
the previous servoing mode (source:
`ros2_kortex/kortex_driver/src/hardware_interface.cpp`, the fault-reset
block in `write()`).

There is no separate, user-facing "stop the arm now" control in this
codebase outside of this fault-reset sequence. Whatever physical E-stop
button the former tutorial described for "the arm" is, on the evidence
available, a hardware-level control outside this codebase's software —
not a ROS service or topic this repository defines.

`Verified in code` (the fault-reset sequence and its internal use of
`ApplyEmergencyStop`) — `Unverified on hardware` (what an operator
pressing a physical arm E-stop button actually triggers)

### Communication loss

No code in this repository implements a specific "lost connection"
behavior (a documented failsafe timeout, for example) for either the
Spot driver or the Kinova driver. `Unverified on hardware` and, for the
software side, `Unverified` more generally — this is a gap this
documentation cannot fill without either further code (not found) or
Boston Dynamics'/Kinova's own SDK documentation (not quoted in this
codebase, so not cited here as fact).

### System fault

Distinguish two unrelated things that both use the word "fault":

- Spot's own `status/system_faults` and `status/behavior_faults` topics
  (source: `spot_driver`'s state publisher) — Spot-level fault
  reporting, read-only from this codebase's perspective.
- The Kinova arm's fault state (`ARMSTATE_IN_FAULT`, checked in
  `kortex_driver`'s `write()`) and its reset routine, described above.

`Verified in code` for both being reported/handled at the software
level; no claim is made here about what a specific fault means
physically.

### Physical hazard (general)

Not a software mechanism at all: a person, object, or terrain feature
that could be harmed by, or interfere with, the robot's movement. See
[Operating Area](operating-area.md) for how to set up the physical
space before a session.

## Failure modes

If a stop mechanism does not behave as expected during a session, stop
attempting further commands and use the next-more-forceful stop
available (see [Emergency Stops](emergency-stops.md) for the ordering)
rather than repeating the same command.

## Safety notes

The `spot_ros2_control` package's own README states, verbatim: "there
is no safety mechanism in place to ensure smooth motion... the robot
can move in unpredictable and dangerous ways if this is not set
correctly. Make sure to keep a safe distance from the robot when
working with these controllers and ensure the e-stop can easily be
pressed if needed" (source:
`spot_ws/src/spot_ros2/spot_ros2_control/README.md`). This applies
whenever `spot_ros2_control` is active (the `controllable:=true` launch
path), not only during exercises explicitly labeled as such.

## Related components

[Emergency Stops](emergency-stops.md), [Operating Spot](../operating/index.md).
