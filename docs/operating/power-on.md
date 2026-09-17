# Power-On Procedure

## Purpose

Bring up Spot, establish the operator connection, and start the base
software stack far enough that the ROS 2 system is reachable.

## Prerequisites

[System Preparation](system-preparation.md) complete.

## Starting State

Spot and the operator device are off. No ROS 2 nodes for this system
are running.

## Steps

### Step 1: Power on Spot

Action: Power on the robot using its own physical power control.

Expected state: Robot completes its own boot sequence.

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

**Historical interface.** A labeled photograph from the former ALeRT
tutorial showing the power button and motor cut-off button locations.
Not independently reconfirmed against the current hardware in this
documentation pass.
:::

### Step 2: Power on the operator device and connect

Action: Power on the operator device and connect it to the robot's
operating network.

Expected state: Operator device connected.

Verification: `Unverified on hardware` for the exact connection
method on the current system — no code in this repository documents a
specific client-side connection step; the driver and dashboard assume
the network is already reachable.

Stop condition: If the connection cannot be established, stop.

Recovery: See [Recovery and
Troubleshooting](recovery-and-troubleshooting.md#communication-loss).

### Step 3: Start the process orchestration backend

Action: Confirm `tmux-api-server.service` and `zenoh-router.service`
are running on the robot computer (these are systemd services,
`Restart=always`, normally already running rather than started
per-session).

Expected state: Both services active.

Verification: `Verified in configuration` — source:
`Backup Ansible/configs/systemd/{tmux-api-server,zenoh-router}.service`
(internal; see `spot-code-audit.md`).

Stop condition: If the dashboard cannot reach the tmux API, the
subsystem toggles will not work — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

Recovery: Restart the affected systemd service (requires access to the
robot computer directly).

### Step 4: Arm the software E-stop endpoint

Action: On the operator dashboard, engage the "Estop" control.

Expected state: This starts the `discovery` and `estop` background
processes (`fastdds discovery --server-id 0` and
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

Action: On the operator dashboard, start the `spot_driver` window
(`ros2 launch spot_driver_plus spot_launch.py`).

Expected state: The driver logs "Waiting for estop to be released..."
until the software E-stop endpoint is present, then logs "Found
estop!" and proceeds (source: `spot_driver/spot_driver/spot_ros2.py`).
Internally this also starts `robot_state_publisher`, the Spot-specific
state publisher, `map_vision`, `frame_server`, and static TF publishers
for the sensor frames (source: `spot_driver.launch.py`,
`spot_driver_plus/launch/spot_launch.py`).

Verification: Driver log shows "Found estop!"; `status/estop` topic
reports `STATE_NOT_ESTOPPED`. `Verified in code`.

Stop condition: If the driver remains stuck waiting for the estop, or
logs an authentication/connection error, stop.

Recovery: Confirm Step 4 completed successfully; see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

### Step 6: Confirm ROS 2 communication

Action: Confirm topics are publishing — for example `ros2 topic echo
status/estop` or observing the operator dashboard's live status
fields.

Expected state: Status topics update; the dashboard's E-stop and
battery displays are live.

Verification: `Verified in code` (the topics exist and are published
by the driver, per `spot-code-audit.md`'s interface table).

Stop condition: If topics are not publishing, treat this as a
communication or driver problem — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

Recovery: Restart the `spot_driver` window; if that fails, escalate to
a trained team member.

## Successful End State

The Spot driver is running, the software E-stop endpoint is present
and shows `NOT_STOPPED`, and ROS 2 topics are live. The system is ready
for [Operator Interface](operator-interface.md) and [Driving
Spot](driving-spot.md); the manipulator is not yet enabled — see
[Operating the Manipulator](operating-the-manipulator.md).

## Common Problems

The driver waiting indefinitely for the E-stop almost always means
Step 4 did not complete — confirm the dashboard's E-stop status label
before re-attempting Step 5, rather than restarting the driver
repeatedly.

## Related components

[System Preparation](system-preparation.md), [Operator
Interface](operator-interface.md), [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).
