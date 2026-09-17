# ROS 2 Interfaces

## Overview

The topics, services, and actions that connect the software
components, with the message/interface type and the concrete source
file for each.

## Purpose

A reference table for anyone writing a new node against this system,
or trying to understand what a given topic name actually carries.

## System context

Assumes familiarity with [ROS 2](../ros2/index.md) concepts (topics,
services, actions). See [Software Components](software-components.md)
for which package provides each interface below.

## Prerequisites

[Required Knowledge](../safety/required-knowledge.md).

## Key interfaces

```{list-table}
:header-rows: 1
:widths: 20 12 30 38

* - Name
  - Type
  - Message/Interface
  - Source
* - `status/estop`
  - Topic
  - `spot_msgs/EStopStateArray`
  - `spot_driver` state publisher
* - `estop/hard`, `estop/gentle`, `estop/release`
  - Service
  - `std_srvs/Trigger`
  - `spot_driver`; flagged non-functional in the driver's own code comment
* - `cmd_vel`
  - Topic
  - `geometry_msgs/Twist`
  - Consumed by `spot_driver`'s `cmd_velocity_callback`
* - `power_on`, `power_off`
  - Service
  - `std_srvs/Trigger`
  - `spot_driver`
* - `navigate_to`
  - Action
  - `spot_msgs/action/NavigateTo`
  - `spot_driver`; requires goal `frame_id == "body"`
* - `/move_action`
  - Action
  - `moveit_msgs/action/MoveGroup`
  - `move_group` (`spot_gen3_moveit`)
* - `/joint_trajectory_controller/follow_joint_trajectory`
  - Action
  - `control_msgs/FollowJointTrajectory`
  - `joint_trajectory_controller` (ros2_control)
* - `/twist_controller/commands`
  - Topic
  - `geometry_msgs/TwistStamped` (frame `gen3_base_link`)
  - `picknik_twist_controller`; published by DualSense teleop and
    visual-servo nodes
* - `reset_fault/command`, `/async_success`, `/internal_fault`
  - Command/state interfaces
  - ros2_control interfaces
  - `kortex_driver`; internally calls the Kinova SDK's
    `ApplyEmergencyStop` during reset
* - `/octomap_binary`, `/octomap_full`
  - Topic
  - `octomap_msgs`
  - `octomap_server`; consumed by `bring_up_alert_nav`
* - `/cmd_vel_stamped`
  - Topic
  - `geometry_msgs/TwistStamped`
  - `move_base_flex` output (remapped), converted to `cmd_vel` by
    `alert_utils/stamped_twist_converter`
* - `joint_states`
  - Topic
  - `sensor_msgs/JointState`
  - `spot_driver` state publisher
* - `odometry`, `odometry/twist`
  - Topic
  - `nav_msgs/Odometry`, `geometry_msgs/TwistWithCovarianceStamped`
  - `spot_driver` state publisher; odometry root frame set by
    `preferred_odom_frame` (deployed config: `vision`)
```

Full inventory, including choreography/dance, sound, PTZ camera,
GraphNav, and world-object services: `spot-code-audit.md` (internal).

`Verified in code` throughout.

## Diagram: ROS 2 communication overview

:::{mermaid}
:alt: Node graph showing the operator dashboard and DualSense controller publishing commands to the Spot driver, which exposes status and state topics, and separately the Kinova driver and MoveIt exchanging joint state and trajectory actions. A stamped-twist converter node sits between navigation and the Spot driver rather than navigation publishing directly to the driver's own cmd_vel topic.

graph LR
    OpDash["Operator dashboard /<br/>DualSense teleop"] -->|"cmd_vel, body_pose"| SpotDriver["spot_driver"]
    SpotDriver -->|"status/estop, odometry,<br/>joint_states"| RViz["RViz / dashboard displays"]
    SpotDriver -->|"images, point clouds"| Octomap["octomap_server"]
    Octomap -->|"/octomap_binary,<br/>/octomap_full"| Nav["move_base_flex<br/>(bring_up_alert_nav)"]
    Nav -->|"/cmd_vel_stamped"| Conv["stamped_twist_converter<br/>(alert_utils)"]
    Conv -->|"cmd_vel"| SpotDriver
    KinovaDriver["kortex_driver"] -->|"/joint_states"| MoveIt["move_group<br/>(spot_gen3_moveit)"]
    MoveIt -->|"/move_action,<br/>FollowJointTrajectory"| KinovaDriver
    OpDash -->|"/twist_controller/commands"| KinovaDriver
:::

## Namespaces

No consistent robot-wide namespace is enforced. `spot_driver.launch.py`
parameterizes a `spot_name` namespace argument that defaults to empty
(no namespace). The only namespaces actually used in the current code
are `/nuc` and `/operator`, applied narrowly to the two-way audio
topics. `Verified in code`.

## QoS

Notably, `spot_driver`'s C++ publishers use **Reliable + Transient
Local** for all status/state/image/joint-state/odometry topics — the
opposite of the usual "sensor data → Best Effort" convention (source:
`spot_driver/include/spot_driver/api/middleware_handle_base.hpp`).
`octomap_server`'s point cloud subscriptions use Best Effort
(`rmw_qos_profile_sensor_data`), matching the usual convention.
`Verified in code`.

## Verification

`Verified in code` throughout; see `spot-code-audit.md` (internal) for
every citation.

## Related components

[Software Components](software-components.md), [Coordinate
Frames](coordinate-frames.md), [Data Flow](data-flow.md).
