# Safe Shutdown

## Purpose

Return the system to a stable, powered-down state at the end of a
session.

## Required supervision

Continuous supervision by a trained team member until Step 1 confirms
Spot is sitting — Step 1 itself commands motion. Steps 2–4 do not move
the robot.

## Prerequisites

An active session, per [Power-On Procedure](power-on.md).

## Initial state

Spot and/or the manipulator are active and under operator control.

## Procedure

### Step 1: Command Spot to sit

Location: the operator dashboard or DualSense controller, on the
Operator Station, commanding Spot on the Robot Computer/Spot Base.

Type: **not read-only — commands robot motion.**

Action: Command a sit, either via the `sit` `Trigger` service or the
DualSense `Square` button (`send_sit_request()`).

Expected observation: Spot sits.

Verification: `Verified in code` for the command path; physical
response `Unverified on hardware`.

Stop condition: If Spot does not sit as commanded, do not proceed to
power-off — treat as a fault.

Recovery: Retry once; if unsuccessful, consult a trained team member
before proceeding.

### Step 2: Power off motors

Location: the operator dashboard, on the Operator Station.

Type: not read-only (powers off motors), no motion commanded.

Action: Call the `power_off` service (directly, or via the dashboard's
"Spot Power Off/On" button, which calls `power_off` then `power_on` in
sequence — if only powering off is intended, use the direct service
instead of that button).

Expected observation: Motors powered off.

Verification: `Verified in code`.

Stop condition: n/a.

Recovery: n/a.

### Step 3: Stop the software stack

Location: the operator dashboard, on the Operator Station, stopping
processes on the Robot Computer.

Type: not read-only (stops processes), no motion commanded.

Action: Note what actually happens when the `spot_driver` process is
stopped: `spot_ros2.py`'s `destroy_node()` sits the robot
(`sit_blocking()`) before disconnecting, **but only if** the robot is
powered on and the driver itself owns the software E-stop endpoint
(`start_estop` is true); if the endpoint is owned externally, the
driver only disconnects without sitting the robot first. Source:
`spot_driver/spot_driver/spot_ros2.py`, `destroy_node()`. This is why
Step 1 and Step 2 above are performed explicitly rather than relying
on shutdown alone.

Stop the `kinova_moveit` and `kinova_driver` windows, then the
`spot_driver` window, then (if no further session is planned) the
`estop` and `discovery` windows, via the operator dashboard.

Expected observation: All subsystem windows stopped.

Verification: Dashboard labels show each window as stopped;
`Verified in code` for `destroy_node()`'s conditional sit-before-disconnect
behavior.

Stop condition: n/a.

Recovery: n/a.

### Step 4: Power off the robot and operator device

Location: the physical robot and the physical operator device — no
computer or terminal involved.

Type: not read-only (physically powers off both devices).

Action: Power off Spot using its own physical control, then the
operator device.

Expected observation: Both devices off.

Verification: `Historical procedure` — the exact physical control
sequence is not independently reconfirmed in this documentation pass;
see the note in [Emergency Stops](../safety/emergency-stops.md).

Stop condition: n/a.

Recovery: n/a.

## Expected observations

Spot sitting with motors off, every subsystem window stopped on the
dashboard, and both physical devices powered down at the end.

## Verification

Each step's own Verification line is authoritative; there is no single
combined "shutdown complete" signal beyond working through all four
steps in order.

## Stop conditions

Do not proceed past Step 1 if Spot does not sit as commanded — treat
that as a fault requiring a trained team member, not something to
route around by powering off anyway.

## Recovery

Powering off the `spot_driver` process without first sitting and
power-cycling the robot explicitly (Steps 1–2) relies on
`destroy_node()`'s conditional behavior, which does not sit the robot
if the software E-stop endpoint is owned externally — do not assume
the driver will always sit the robot for you. That is precisely why
this procedure performs Steps 1–2 explicitly rather than only stopping
the driver.

## Final state

Spot is sitting with motors powered off, the software stack is
stopped, and both devices are powered down.

## Related components

[Recovery and Troubleshooting](recovery-and-troubleshooting.md).
