# Driving Spot

## Purpose

Manually drive Spot's base and switch between operating modes.

## Prerequisites

[Operator Interface](operator-interface.md); the operator understands
[Safety Principles](../safety/safety-principles.md).

## Starting State

The Spot driver is running and the software E-stop endpoint is
present (`status/estop` reports `NOT_STOPPED`).

## Steps

### Step 1: Select the base control mode

Action: On the DualSense controller, press `Share` to select Spot
base-control mode (source:
`workspaces/david_ws/src/spot_dualsense/controller_controls/read_dualsense.py`,
`state.share -> self.mode = 0`). A separate joystick path also exists
using a generic `joy_node` plus a dedicated C++ controller node
(source: `spot_ws/src/alert_ros2/spot_driver_plus/launch/controller_launch.py`,
`spot_kinova_controller.cpp`) for Xbox-style, "Backterra", or "Steam
Deck" controller variants.

Expected state: Controller in base-control mode.

Verification: `Verified in code` for the DualSense mapping; which
physical controller is actually used in a given session is not
asserted here.

:::{figure} ../_static/images/historical-interface/spot_control.png
:alt: Historical interface. A labeled Steam Deck control schematic showing left-stick walk/stance controls, right-stick rotation, and named buttons for speed, mode, waypoints and height.
:width: 80%
:align: center

**Historical context:** a Steam Deck control schematic from the former
ALeRT tutorial. **Current implementation:** the actively maintained
teleop code (`read_dualsense.py`) targets a Sony DualSense controller
with a different button/stick mapping entirely — the two controllers
are not interchangeable, and this schematic does not describe the
current code path. **Hardware verification required:** yes — confirm
which controller (Steam Deck, DualSense, or both) is actually in use
in a given session before relying on either mapping.
:::

Stop condition: Confirm mode before commanding any motion.

Recovery: Re-press the mode-select control.

### Step 2: Release the input lock

Action: The DualSense mapping treats holding `L2` and `R2`
simultaneously as a toggle for a `locked_mode` flag; while locked, no
commands are published (source: `read_dualsense.py`,
`ControllerReader`, lines defining `locked_mode`). Confirm the
controller is not in this locked state before attempting to drive.

Expected state: Unlocked — commands will be published.

Verification: `Verified in code`. This is a software input gate, not a
robot-level safety stop — do not treat it as an E-stop substitute; see
[Safety Principles](../safety/safety-principles.md).

Stop condition: If unsure whether the controller is locked, hold
`L2`+`R2` again and re-confirm before proceeding.

Recovery: Toggle the lock again.

### Step 3: Drive

Action: Use the left stick for translation and the right stick's `X`
axis for rotation. Source (`read_dualsense.py`): `linear.x` from `LY`,
`linear.y` from `LX`, `angular.z` from `RX`, published as
`geometry_msgs/Twist` on `cmd_vel`, with a 0.1 deadzone. `R1`/`L1`
increment/decrement a speed scale factor.

Expected state: Spot moves according to the commanded `Twist`.

Verification: `Verified in code` for the mapping; the robot's physical
response is `Unverified on hardware` in this documentation.

Stop condition: Any unexpected motion, obstacle, or person entering
the operating area — release the stick to zero the command, or use the
next stop mechanism per [Emergency Stops](../safety/emergency-stops.md).

Recovery: Release input to stop commanded motion; if the robot does
not stop as expected, escalate per [Emergency
Stops](../safety/emergency-stops.md).

### Step 4: Body pose adjustments (optional)

Action: `Triangle` resets height/pitch/roll and gait mode; `Square`
commands a sit (`send_sit_request()`); `Cross` toggles body-pose mode
(right stick controls roll/pitch, published on `body_pose`); D-pad
up/down adjusts height. Source: `read_dualsense.py`.

Expected state: Spot's body pose changes accordingly.

Verification: `Verified in code`.

Stop condition: Same as Step 3.

Recovery: `Triangle` to reset to a known pose.

## Successful End State

Spot responds to drive commands within the operating area, under
continuous supervision.

## Common Problems

If Spot does not respond to stick input, confirm the controller is not
in the locked-input state (Step 2) and that `status/estop` still shows
`NOT_STOPPED` before assuming a deeper fault.

## Related components

[Operating the Manipulator](operating-the-manipulator.md), [Safety
Principles](../safety/safety-principles.md), [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).
