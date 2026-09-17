# Operating the Manipulator

## Purpose

Enable the Kinova Gen3 manipulator and Robotiq gripper, and manually
control them.

## Required supervision

Continuous supervision by a trained team member for Steps 3–4 (both
command real motion); Steps 1–2 start software but do not themselves
move the arm. See [Safety Principles: Manipulator (Kinova) fault
handling](../safety/safety-principles.md#manipulator-kinova-fault-handling).

## Prerequisites

[Driving Spot](driving-spot.md); the operator understands the
manipulator has fault handling rather than the Spot-style E-stop
system — see [Safety Principles: Manipulator (Kinova) fault
handling](../safety/safety-principles.md#manipulator-kinova-fault-handling).

## Initial state

Spot driver running; manipulator not yet started.

## Procedure

### Step 1: Start the manipulator driver

Location: the operator dashboard, on the Operator Station, which
starts the driver process on the Manipulator Controller (the Kinova
Gen3's own embedded controller, reached over TCP). The launched
package (`kortex_bringup`) lives in the `man_ws` workspace.

Type: not read-only (starts the driver and clears faults), no motion
commanded.

Action: On the operator dashboard, start the `kinova_driver` window
(`ros2 launch kortex_bringup gen3.launch.py robot_ip:=$GEN3_IP dof:=6
launch_rviz:=false`). Source: `alert_dashboard_rqt/window_commands.py`.

Expected observation: The `kortex_driver` hardware interface connects to the
arm over TCP and clears any existing faults on activation (source:
`ros2_kortex/kortex_driver/src/hardware_interface.cpp`, `on_activate()`
comment "reset faults on activation").

Verification: `Verified in code`. Confirm via `ros2 topic echo
/joint_states` (run from a terminal on the Operator Station or Robot
Computer) that joint states are publishing.

Stop condition: If the connection fails or joint states do not
publish, stop.

Recovery: See [Recovery and
Troubleshooting](recovery-and-troubleshooting.md#manipulator-fault).

### Step 2: Start MoveIt

Location: the operator dashboard, on the Operator Station, which
starts `move_group` on the Robot Computer. The launched package
(`spot_gen3_moveit`) lives in the `man_ws` workspace.

Type: not read-only (starts the planning server), no motion commanded.

Action: Start the `kinova_moveit` window (`ros2 launch spot_gen3_moveit
move_group.launch.py use_rviz:=false`).

Expected observation: The `move_group` node is running, exposing the
`/move_action` action (`moveit_msgs/action/MoveGroup`). Planning
defaults to 10% of the arm's maximum velocity and acceleration (source:
`spot_gen3_moveit/config/joint_limits.yaml`,
`default_velocity_scaling_factor: 0.1`).

Verification: `Verified in code` / `Verified in configuration`.

Stop condition: If `move_group` fails to start (commonly a missing or
mismatched robot description), stop.

Recovery: Confirm Step 1 completed; restart `kinova_moveit`.

:::{admonition} Collision checking is limited
:class: warning

The MoveIt configuration disables collision checking between the arm
and most of Spot's own body/leg links (source:
`spot_gen3_moveit/config/spot.srdf`, extensive `<disable_collisions>`
entries with reason "Never"). MoveIt as configured will generally not
flag an arm-vs-body/leg self-collision. This is a real, current
limitation, not a hypothetical one — supervise manipulator motion
accordingly.
:::

### Step 3: Manual arm and gripper control

Location: RViz (Operator Station) or the DualSense controller
(Operator Station), commanding the arm on the Manipulator Controller.

Type: **not read-only — commands arm motion.**

Action: Use MoveIt's interactive markers (via RViz) to plan and execute
motions, or, on the DualSense controller, press `Options` to select
manipulator-control mode (source: `read_dualsense.py`,
`state.options -> self.mode = 1`), then use the left stick for
`linear.x`/`linear.y`, `R1`/`L1` for `linear.z`, the right stick for
angular components, and `R2`/`L2` for `angular.z` — published as
`geometry_msgs/TwistStamped` on `twist_controller/commands` (frame
`gen3_base_link`).

Expected observation: The arm moves according to the commanded
trajectory or twist.

Verification: `Verified in code` for both control paths; physical
response `Unverified on hardware`.

:::{figure} ../_static/images/historical-interface/manipulator_control.png
:alt: Historical interface. A labeled Steam Deck control schematic for manipulator control, showing Cartesian and orientation controls per stick, gripper open/close, and arm home/retract buttons.
:width: 80%
:align: center

**Historical context:** a Steam Deck manipulator-control schematic
from the former ALeRT tutorial. **Current implementation:** as with
[Driving Spot](driving-spot.md#step-1-select-the-base-control-mode)'s
control schematic, this describes the Steam Deck's own native
controls, not the DualSense mapping found in the current code.
**Hardware verification required:** yes — same caveat as the driving
schematic; confirm the active controller before relying on this
mapping.
:::

Stop condition: Any unexpected motion, or the input-lock condition
from [Driving Spot](driving-spot.md#step-2-release-the-input-lock) if
using the DualSense controller.

Recovery: Release input; if the arm does not stop, escalate per
[Safety Principles](../safety/safety-principles.md#manipulator-kinova-fault-handling).

### Step 4: Gripper open/close

Location: the operator dashboard or a terminal on the Operator
Station, calling a service on the Manipulator Controller via
`spot_driver`.

Type: **not read-only — commands gripper motion.**

Action: Call the `open_gripper`/`close_gripper` `Trigger` services
(source: `spot_driver/spot_driver/spot_ros2.py`, wrapping
`spot_wrapper.spot_arm.gripper_open()`/`gripper_close()`), or use a
`SetGripperAngle` request for a specific opening.

Expected observation: Gripper opens or closes.

Verification: `Verified in code`.

Stop condition: Unexpected gripper behavior, or an object caught
unexpectedly.

Recovery: Re-issue `open_gripper`; if unresponsive, treat as a fault —
see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md#manipulator-fault).

:::{admonition} Open question: which gripper control path is active
:class: note

Two separate gripper-control mechanisms exist in the current code: the
Kortex hardware interface's internal-bus gripper communication
(`formatted_robot.urdf`, `use_internal_bus_gripper_comm: True`) and a
standalone Robotiq driver/controller pair
(`man_ws/src/ros2_robotiq_gripper`). Static analysis of the code could
not determine which is authoritative for the combined Spot+Gen3 robot
— see `spot-code-audit.md` (internal), "Open questions". Confirm which
path is active before relying on either description.
:::

## Expected observations

The manipulator driver reports connected and fault-free; `move_group`
accepts planning requests; the arm and gripper respond to commanded
motion within the limited 10%-scaled velocity/acceleration range.

## Verification

Each step's own Verification line is authoritative. The manipulator
has no single "ready" topic equivalent to Spot's `status/estop` — use
Step 1's joint-state check plus Step 2's successful `move_group`
startup together as the readiness signal.

## Stop conditions

Any step's own Stop condition, or a reported fault
(`ARMSTATE_IN_FAULT`) at any point — stop commanding motion
immediately and go to Recovery below, rather than retrying the same
command.

## Recovery

If the arm reports a fault (`ARMSTATE_IN_FAULT`), do not attempt
further motion commands — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md#manipulator-fault).

## Final state

The manipulator responds to planned motions or manual twist commands,
and the gripper opens/closes on command.

## Related components

[Driving Spot](driving-spot.md), [Safety
Principles](../safety/safety-principles.md), [Manipulator and
MoveIt](../manipulation/index.md).
