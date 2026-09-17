# Software Components

## Overview

The ROS 2 packages and nodes that make up the running system,
organized by subsystem, with authoritative-vs-legacy status where
evidence exists.

## Purpose

Give a package-level map of "what runs the system" grounded in
`spot-code-audit.md` (internal), rather than a plausible-sounding
guess based on package names alone.

## System context

See [Startup and Launch Sequence](startup-and-launch-sequence.md) for
the order these actually come up in, and [ROS 2
Interfaces](ros2-interfaces.md) for how they talk to each other.

## By subsystem

### Spot base driver

`spot_driver` (the `spot_ros2` node) is the central Spot interface:
~50 `Trigger` services, status publishers, and action servers wrapping
the Boston Dynamics SDK. `spot_hardware_interface` and
`spot_ros2_control` provide a `ros2_control`-based joint-level path,
used only when the driver is launched with `controllable:=true`.
`spot_driver_plus` (in `alert_ros2`) is the operational wrapper
actually launched in practice — it includes the base driver launch
file and adds `map_vision`, `frame_server`, and sensor static
transforms.

`Verified in code`.

### Perception and mapping

`octomap_server` builds 3D occupancy maps from point clouds (Best
Effort QoS). Two instances run in practice (`octo_livox`, `octo_spot`
runtime windows), one per LiDAR source.

`Verified in code`.

### Navigation

`bring_up_alert_nav`/`mbf_octo_nav` (in the `octo_navigation`
meta-repository) runs `move_base_flex` with a custom Octomap-derived
planner (`astar_octo_planner`) and controller (`octo_controller`).
`alert_exploration` drives `move_base_flex`'s `MoveBase` action from a
frontier-selection algorithm, consuming a 2D-projected map.

This is the most recently modified code in the entire local source
tree (see `spot-source-audit.md`, internal), and is treated as the
authoritative navigation stack throughout this site — not
`spot_ws/src/alert_ros2`'s dormant `posture_mgr` node, which is
defined but commented out of its launch file.

`Verified in code`.

### Manipulator

`man_ws/src/ros2_kortex` (`kortex_driver`) is the Kinova Gen3 hardware
interface. `spot_gen3_moveit` is the generated MoveIt 2 configuration
(one planning group, `manipulator`; joint limits scaled to 10% by
default). `auto_dex_nodes` and `alert_auto_dexterity`/`man_pkg` provide
higher-level manipulation behaviors — see [Autonomous
Behaviors](../autonomous-behaviors/index.md).

`kinova_stuffs` (in `spot_ws`) is superseded: its own README states the
team is switching to `ros2_kortex`.

:::{admonition} Open question: which gripper-control path is active
:class: note

Two separate gripper-control mechanisms exist in the current code: the
Kortex hardware interface's internal-bus gripper communication
(`configs/formatted_robot.urdf`, `use_internal_bus_gripper_comm:
True`) and a standalone Robotiq driver/controller pair
(`man_ws/src/ros2_robotiq_gripper`). Static analysis could not
determine which is authoritative for the combined robot.
:::

`Verified in code` for both paths' existence; `Unverified` for which is
active.

### Operator tools

`alert_dashboard_rqt` is the operator dashboard (subsystem toggles,
Spot control tab, E-stop status). `frame_panel`/`frame_server` provide
an RViz panel and backing node for interactively creating named TF
waypoints. `david_ws/src/spot_dualsense` provides DualSense gamepad
teleop.

`Verified in code`.

### Behavior/mission

Two frameworks coexist:

- **YASMIN** (`yasmin_ws`, and `alert_auto_dexterity`'s
  `auto_approach.py`) — actively used: an 18-state mission ("navigate
  to a K-Rail waypoint → sit → run a manipulator inspection sequence →
  stand", repeated for two named waypoints) is implemented as a YASMIN
  state machine.
- **BehaviorTree.CPP/ROS2** (`spot_ws/src/BT`) — vendored, but no local
  package was found consuming it. Its current status is `Unverified`,
  not asserted as deprecated, since absence of a found consumer is not
  proof of deprecation.

No RAFCON reference exists anywhere in the current code (the former
ALeRT tutorial's P5 topic, which covered RAFCON, is historical/general
background, not evidence of current use — see
[Autonomous Behaviors](../autonomous-behaviors/index.md)).

`Verified in code` for YASMIN's active use; `Unverified` for BT.CPP's
status.

## Verification

See each subsystem above; `spot-code-audit.md` (internal) has the full
package-by-package evidence.

## Related components

[Hardware Overview](hardware-overview.md), [Startup and Launch
Sequence](startup-and-launch-sequence.md), [ROS 2
Interfaces](ros2-interfaces.md).
