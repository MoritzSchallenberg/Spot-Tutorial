# Safe Shutdown

## Purpose

Return the system to a stable, powered-down state at the end of a
session.

## Prerequisites

An active session, per [Power-On Procedure](power-on.md).

## Starting State

Spot and/or the manipulator are active and under operator control.

## Steps

### Step 1: Command Spot to sit

Action: Command a sit, either via the `sit` `Trigger` service or the
DualSense `Square` button (`send_sit_request()`).

Expected state: Spot sits.

Verification: `Verified in code` for the command path; physical
response `Unverified on hardware`.

Stop condition: If Spot does not sit as commanded, do not proceed to
power-off — treat as a fault.

Recovery: Retry once; if unsuccessful, consult a trained team member
before proceeding.

### Step 2: Power off motors

Action: Call the `power_off` service (directly, or via the dashboard's
"Spot Power Off/On" button, which calls `power_off` then `power_on` in
sequence — if only powering off is intended, use the direct service
instead of that button).

Expected state: Motors powered off.

Verification: `Verified in code`.

Stop condition: n/a.

Recovery: n/a.

### Step 3: Stop the software stack

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

Expected state: All subsystem windows stopped.

Verification: Dashboard labels show each window as stopped;
`Verified in code` for `destroy_node()`'s conditional sit-before-disconnect
behavior.

Stop condition: n/a.

Recovery: n/a.

### Step 4: Power off the robot and operator device

Action: Power off Spot using its own physical control, then the
operator device.

Expected state: Both devices off.

Verification: `Historical procedure` — the exact physical control
sequence is not independently reconfirmed in this documentation pass;
see the note in [Emergency Stops](../safety/emergency-stops.md).

Stop condition: n/a.

Recovery: n/a.

## Successful End State

Spot is sitting with motors powered off, the software stack is
stopped, and both devices are powered down.

## Common Problems

Powering off the `spot_driver` process without first sitting and
power-cycling the robot explicitly (Steps 1–2) relies on
`destroy_node()`'s conditional behavior, which does not sit the robot
if the software E-stop endpoint is owned externally — do not assume
the driver will always sit the robot for you.

## Related components

[Recovery and Troubleshooting](recovery-and-troubleshooting.md).
