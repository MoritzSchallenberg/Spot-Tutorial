# Power-On Procedure

## Purpose

Bring up Spot, establish the operator connection, and start the base
software stack far enough that the ROS 2 system is reachable.

## Required supervision

A trained team member must be present throughout — this procedure ends
with the robot's motors powered and the driver able to accept motion
commands, even though no step here commands motion itself. See
[Safety Principles](../safety/safety-principles.md) and [Operating
Area](../safety/operating-area.md).

## Prerequisites

[System Preparation](system-preparation.md) complete.

## Initial state

Spot and the operator device are off. No ROS 2 nodes for this system
are running.

## Procedure

### Step 1: Power on Spot

Location: the physical robot — no computer or terminal involved.

Type: not read-only (applies power to the robot's own systems), but
does not command movement.

Action: Power on the robot using its own physical power control.

Expected observation: Robot completes its own boot sequence.

Verification: Historical procedure describes specific buttons and LED
colors for this step; this documentation does not repeat those details
as current fact — see the note in [Emergency
Stops](../safety/emergency-stops.md). Confirm the current procedure
with a trained team member.

Stop condition: If the robot does not complete its boot sequence,
stop and consult [Recovery and Troubleshooting](recovery-and-troubleshooting.md).

Recovery: Power cycle per the manufacturer's own procedure if
available; otherwise consult a trained team member.

`Historical procedure`

:::{figure} ../_static/images/historical-interface/spot_buttons.jpg
:alt: Historical interface. A labeled photograph of Spot's rear panel showing a power button and a separate motor cut-off button.
:width: 70%
:align: center

**Historical context:** a labeled photograph from the former ALeRT
tutorial showing the power button and motor cut-off button locations.
**Current implementation:** no current code or configuration describes
Spot's physical power panel (it is outside the ROS 2 stack this site
otherwise audits), so there is nothing in the codebase to compare this
photograph against. **Hardware verification required:** yes — confirm
the button locations shown here are still correct on the physical unit
before relying on this photograph alone.
:::

### Step 2: Power on the operator device and connect

Location: the operator device (Operator Station role — see [Computers
and Network](../architecture/computers-and-network.md)).

Type: not read-only (powers a device and joins a network), no motion
commanded.

Action: Power on the operator device and connect it to the robot's
operating network.

Expected observation: Operator device connected.

Verification: `Unverified on hardware` for the exact connection
method on the current system — no code in this repository documents a
specific client-side connection step; the driver and dashboard assume
the network is already reachable.

Stop condition: If the connection cannot be established, stop.

Recovery: See [Recovery and
Troubleshooting](recovery-and-troubleshooting.md#communication-loss).

### Step 3: Start the process orchestration backend

Location: the Robot Computer role, via `systemctl status` in a
terminal on that machine (or, indirectly, by observing whether the
operator dashboard in Step 4 can reach it at all).

Type: read-only (a status check; these services are normally already
running, not started per-session).

Action: Confirm `tmux-api-server.service` and `zenoh-router.service`
are running on the robot computer (these are systemd services,
`Restart=always`).

Expected observation: Both services active.

Verification: `Verified in configuration` — source:
`Backup Ansible/configs/systemd/{tmux-api-server,zenoh-router}.service`
(internal; see `spot-code-audit.md`).

Stop condition: If the dashboard cannot reach the tmux API, the
subsystem toggles will not work — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

Recovery: Restart the affected systemd service (requires access to the
robot computer directly — not read-only).

### Step 4: Arm the software E-stop endpoint

Location: the operator dashboard, on the Operator Station, which
starts processes on the Robot Computer via the tmux API.

Type: not read-only (starts background processes), no robot motion
commanded.

Action: On the operator dashboard, engage the "Estop" control.

Expected observation: This starts the `discovery` and `estop`
background processes (`fastdds discovery --server-id 0` and
`spot_driver_plus/spot_estop.py`) — source:
`alert_dashboard_rqt/alert_dashboard_rqt/window_commands.py`,
`spot_estop_rqt.py`.

Verification: The dashboard's E-stop status label shows "✓ E-Stop
Running" (a literal string in `spot_estop_rqt.py`'s
`check_estop_status()`). `Verified in code`.

Stop condition: If the label shows "💥 E-Stop CRASHED" or "⚠️
Disconnected from API", do not proceed — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

Recovery: Disengage and re-engage the control; if it still fails,
consult a trained team member before proceeding.

### Step 5: Start the Spot driver

Location: the operator dashboard, on the Operator Station, which
starts the driver process on the Robot Computer.

Type: not read-only (starts the main driver), but starting the driver
does not itself command movement.

Action: On the operator dashboard, start the `spot_driver` window
(`ros2 launch spot_driver_plus spot_launch.py`).

Expected observation: The driver logs "Waiting for estop to be
released..." until the software E-stop endpoint is present, then logs
"Found estop!" and proceeds (source:
`spot_driver/spot_driver/spot_ros2.py`). Internally this also starts
`robot_state_publisher`, the Spot-specific state publisher,
`map_vision`, `frame_server`, and static TF publishers for the sensor
frames (source: `spot_driver.launch.py`,
`spot_driver_plus/launch/spot_launch.py`).

Verification: Driver log shows "Found estop!"; `status/estop` topic
reports `STATE_NOT_ESTOPPED`. `Verified in code`.

Stop condition: If the driver remains stuck waiting for the estop, or
logs an authentication/connection error, stop.

Recovery: Confirm Step 4 completed successfully; see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

### Step 6: Confirm ROS 2 communication

Location: a terminal with ROS 2 sourced, anywhere on the same
network/middleware domain as the Robot Computer — commonly the
Operator Station.

Type: read-only.

Action: Confirm topics are publishing — for example `ros2 topic echo
status/estop` or observing the operator dashboard's live status
fields.

Expected observation: Status topics update; the dashboard's E-stop and
battery displays are live.

Verification: `Verified in code` (the topics exist and are published
by the driver, per `spot-code-audit.md`'s interface table).

Stop condition: If topics are not publishing, treat this as a
communication or driver problem — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

Recovery: Restart the `spot_driver` window; if that fails, escalate to
a trained team member.

## Expected observations

By the end of this procedure: Spot has completed its boot sequence,
the operator device is connected, both backend services are active,
the software E-stop endpoint shows "✓ E-Stop Running", the driver log
shows "Found estop!", and ROS 2 topics are visibly live.

## Verification

Each step's own Verification line is authoritative; taken together,
the strongest single overall check is `status/estop` reporting
`STATE_NOT_ESTOPPED` combined with live topic traffic (Step 6).

## Stop conditions

Do not proceed past a step whose own Stop condition was hit. In
particular, do not attempt Step 5 before Step 4's E-stop status label
confirms "✓ E-Stop Running" — this is the single most common failure
mode of this whole procedure (see Recovery below).

## Recovery

The driver waiting indefinitely for the E-stop almost always means
Step 4 did not complete — confirm the dashboard's E-stop status label
before re-attempting Step 5, rather than restarting the driver
repeatedly. For anything not covered by a step's own Recovery line,
see [Recovery and Troubleshooting](recovery-and-troubleshooting.md).

## Final state

The Spot driver is running, the software E-stop endpoint is present
and shows `NOT_STOPPED`, and ROS 2 topics are live. The system is ready
for [Operator Interface](operator-interface.md) and [Driving
Spot](driving-spot.md); the manipulator is not yet enabled — see
[Operating the Manipulator](operating-the-manipulator.md).

## Related components

[System Preparation](system-preparation.md), [Operator
Interface](operator-interface.md), [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).
