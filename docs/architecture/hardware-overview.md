# Hardware Overview

## Overview

The physical components that make up the Spot system, limited to what
is actually evidenced in the current code and configuration.

## Purpose

Give a new reader an accurate parts list before going into software —
without repeating unconfirmed technical specifications from memory.

## System context

Every component below feeds into [System
Architecture](index.md)'s later pages: how it's networked (Computers
and Network), what software drives it (Software Components), what
interfaces it exposes (ROS 2 Interfaces), and what frame it occupies
(Coordinate Frames).

## Components

### Boston Dynamics Spot (base platform)

A quadruped: 4 legs, each with hip, upper-leg, and lower-leg joints
(12 leg joints total). Carries the onboard sensors and compute
described below, and the manipulator. Boston Dynamics' own optional
"Spot Arm" is present in the URDF but conditional on an `arm:=true`
xacro argument; every located deployment configuration sets
`has_arm: False`, so this codebase's Spot does not use Boston
Dynamics' own arm — the manipulator described below is a separately
mounted Kinova arm.

`Verified in code` (source: `spot_description/spot_description/urdf/spot_macro.xacro`;
`spot_driver_plus/config/spot_params.yaml`).

Safety relevance: see [Safety and Prerequisites](../safety/index.md) —
Spot's motors, E-stop, and fault reporting are all specific to this
platform.

### Kinova Gen3 manipulator

Mounted on Spot via a fixed joint (`spot_to_kinova`), unconditionally
included in the robot description. The actual bring-up command found
in the current code specifies **6 degrees of freedom**
(`kortex_bringup gen3.launch.py ... dof:=6`), and the MoveIt joint
limits configuration defines exactly 6 joints (`joint_1`..`joint_6`).

:::{admonition} Confirm degrees of freedom before assuming 7-DOF
:class: warning

Kinova's Gen3 family is available in both 6-DOF and 7-DOF variants.
This codebase's own launch command and joint configuration are
specific to 6 joints — do not assume a 7-DOF arm without confirming it
against the actual physical unit, since the code evidence here points
to 6-DOF.
:::

`Verified in code` (source: `man_ws/src/alert_dashboard_rqt/window_commands.py`
line launching `kortex_bringup gen3.launch.py ... dof:=6`;
`spot_gen3_moveit/config/joint_limits.yaml`).

Software: `man_ws/src/ros2_kortex` (`kortex_driver`), MoveIt 2 config
in `spot_gen3_moveit`. See [Manipulator and MoveIt](../manipulation/index.md)
and [Software Components](software-components.md).

### Gripper

A Robotiq 2-finger gripper is present, but the exact model is not
consistent between two located sources: the combined robot description
(`configs/formatted_robot.urdf`) names its links `robotiq_140_base_link`
(consistent with a 2F-140), while a separate standalone gripper
controller configuration
(`man_ws/src/ros2_robotiq_gripper/robotiq_description/config/robotiq_controllers.yaml`)
names a joint `robotiq_85_left_knuckle_joint` (consistent with a
2F-85). This documentation does not assert one model over the other —
confirm the physical gripper model directly. This is also tied to the
open question of which gripper-control path is active, covered under
[Software Components](software-components.md).

`Verified in code` for both naming conventions existing; `Unverified`
for which is correct.

### Sensors

```{list-table}
:header-rows: 1
:widths: 25 45 30

* - Sensor
  - Evidence
  - Notes
* - Livox Mid-360 LiDAR
  - `spot_macro.xacro` mounts a `livox` frame with the Mid-360 mesh;
    `livox_ros_driver2 msg_MID360_launch.py` in the runtime window list
  - `Verified in code`
* - RealSense depth/color cameras
  - `realsenses` runtime window (`rrl_launchers realsenses_launch.py`);
    RealSense udev rules present
  - Number of units not confirmed
* - IFM O3P 3D cameras (×3: front, right, left)
  - `spot_launch.py` static TF publishers for `ifm_front/back_plate`,
    `ifm_right/back_plate`, `ifm_left/back_plate`; udev rule
    `11-o3p.rules`
  - `Verified in code`
* - Seek Thermal camera
  - `thermal_cam` runtime window; udev rule `10-seekthermal.rules`
  - `Verified in code`
* - Spot's own body cameras
  - Published via `spot_driver`'s per-camera image topics
  - Provided by the Spot platform itself, not a separately mounted
    sensor
```

### Operator device

Two distinct pieces of evidence exist and are not reconciled in the
codebase:

- The former ALeRT tutorial's screenshots (see [Operating
  Spot](../operating/index.md)) show a **Steam Deck** running RViz and
  the operator dashboard.
- The current, actively maintained teleop code (`david_ws/src/spot_dualsense`,
  most recently modified workspace after `man_ws`) targets a **Sony
  DualSense** controller directly via `pydualsense`, not the Steam
  Deck's own native input.

Treat the Steam Deck as the historical operator device and the
DualSense as the current, code-confirmed input device; which one (or
both) is in actual current use is not resolved by static analysis.

### Compute

An onboard/payload compute unit (referred to in the deployment
configuration's own provisioning playbook as a "NUC") runs the
persistent `tmux-api-server` and `zenoh-router` systemd services and
the majority of the ROS 2 software stack. See [Computers and
Network](computers-and-network.md) for the full role breakdown.
`Verified in configuration`.

## Verification

See each component's own line above; nothing here is marked
`Verified on hardware`.

## Failure modes

Not applicable to a hardware inventory; see [Safety and
Prerequisites](../safety/index.md) and [Operating
Spot](../operating/index.md).

## Related components

[Computers and Network](computers-and-network.md), and [Software
Components](software-components.md).
