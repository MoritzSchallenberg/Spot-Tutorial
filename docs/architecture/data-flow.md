# Data Flow

## Overview

How data moves from sensors, through processing, to actions — for the
navigation pipeline and the manipulation pipeline.

## Purpose

Tie together [Hardware Overview](hardware-overview.md), [Software
Components](software-components.md), and [ROS 2
Interfaces](ros2-interfaces.md) into an end-to-end picture of what
happens between a sensor reading and a commanded action.

## System context

This is the most integrative of the architecture pages — every arrow
below is backed by a topic named in [ROS 2
Interfaces](ros2-interfaces.md).

## Navigation pipeline

1. LiDAR/depth sensors publish point clouds (Best Effort QoS).
2. `octomap_server` builds a 3D occupancy map (`/octomap_binary`,
   `/octomap_full`).
3. `bring_up_alert_nav`'s `move_base_flex` consumes the octomap plus
   odometry, plans with `astar_octo_planner`, and controls with
   `octo_controller`, in the `feet_center` robot frame.
4. Output is `/cmd_vel_stamped`, converted to `cmd_vel` and sent to
   `spot_driver`.
5. Separately, `alert_exploration` consumes a 2D-projected map
   (`/projected_map_1m`) and drives goals into the same
   `move_base_flex` server via its `MoveBase` action, in the `body`
   frame — see the frame-convention mismatch noted in [Coordinate
   Frames](coordinate-frames.md).

`Verified in code`.

## Manipulation pipeline

1. Perception (camera/marker detection, covered generally in
   [Perception](../perception/index.md)) or a fixed named-frame
   waypoint (via `frame_server`) provides a target pose.
2. `move_group` (`spot_gen3_moveit`) plans a trajectory via `/move_action`
   or a mission node calls `/joint_trajectory_controller/follow_joint_trajectory`
   directly.
3. `kortex_driver` executes the trajectory on the Kinova Gen3.
4. Gripper open/close is commanded via `spot_driver`'s
   `open_gripper`/`close_gripper` services or `SetGripperAngle`.
5. On a fault, the `reset_fault` interface runs its fixed recovery
   sequence (see [Safety Principles](../safety/safety-principles.md#manipulator-kinova-fault-handling)).

`Verified in code`.

## Diagram: sensor-to-action data flow

:::{mermaid}
:alt: Flow diagram showing sensors feeding octomap_server, which feeds navigation, which outputs velocity commands back to the Spot driver; and separately perception feeding MoveIt, which commands the Kinova driver.

graph LR
    Sensors["LiDAR / depth sensors"] --> Octomap["octomap_server"]
    Octomap --> Nav["move_base_flex<br/>(bring_up_alert_nav)"]
    Nav -->|"/cmd_vel_stamped"| SpotDriver["spot_driver"]
    SpotDriver -->|"motor commands"| SpotBase["Spot Base"]

    Cameras["Cameras / markers"] --> Perception["Perception<br/>(detection, frame_server waypoints)"]
    Perception --> MoveIt["move_group<br/>(spot_gen3_moveit)"]
    MoveIt --> KinovaDriver["kortex_driver"]
    KinovaDriver --> Arm["Kinova Gen3 + gripper"]
:::

## Diagram: safety and stop signal chain

:::{mermaid}
:alt: Flow diagram showing the physical E-stop button, the software E-stop endpoint process, and the power/motor services, and how each relates to the Spot driver's activation checks. The manipulator's separate fault-reset path is shown alongside, not merged with Spot's E-stop chain.

graph TD
    PhysicalEstop["Physical E-stop button(s)<br/>(hardware-level, outside this codebase)"] -.->|"Unverified on hardware:<br/>exact physical effect"| SpotFirmware["Spot's own firmware/SDK"]
    SoftEstop["Software E-stop endpoint<br/>(spot_estop.py process)"] -->|"status/estop"| SpotDriverActivate["spot_hardware_interface<br/>on_activate(): check_estop()"]
    SoftEstop -.->|"required present<br/>before driver commands robot"| SpotDriverMain["spot_driver main node"]
    RosEstopServices["estop/hard, estop/gentle,<br/>estop/release (ROS services)"] -.->|"flagged non-functional<br/>in driver code comment"| SoftEstop
    PowerServices["power_on / power_off<br/>services"] --> SpotDriverMain

    KinovaFault["Kinova fault detected<br/>(ARMSTATE_IN_FAULT)"] --> ResetFault["reset_fault sequence:<br/>ApplyEmergencyStop x2, ClearFaults"]
    ResetFault --> KinovaDriver["kortex_driver"]
:::

## Verification

`Verified in code` for every arrow above; the safety diagram
deliberately shows the two systems (Spot E-stop, Kinova fault
handling) as separate chains rather than implying they share a single
mechanism, consistent with [Safety
Principles](../safety/safety-principles.md).

## Related components

[Software Components](software-components.md), [ROS 2
Interfaces](ros2-interfaces.md), [Coordinate Frames](coordinate-frames.md).
