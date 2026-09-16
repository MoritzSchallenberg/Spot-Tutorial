# Spot code audit

**Not part of the published website.** Internal working document for
Entwicklungsauftrag 9, Section 10. Excluded from the Sphinx build
(outside `docs/`), not linked from any published toctree.

## Method

Static, read-only analysis of the current Spot code
(`Backup Ansible/workspaces/spot_ws`, `man_ws`, `alert_nav_ws`, `david_ws`)
and deployment configuration (`Backup Ansible/configs`). No launch
file, driver, Ansible playbook, or hardware-facing script was executed.
Every row below cites a concrete file path (and line number or quoted
quote where useful); nothing is included on the strength of a filename
alone. Package/workspace authority (current vs. legacy) follows
`spot-source-audit.md` §4. `go2_ws`/`omx_ws` (Unitree Go2, a different
robot) were excluded throughout.

## Repository inventory

| Repository/Pfad | Commit | Technologie | ROS-Version | Aufgabe | Aktiv/Legacy | Evidenz |
| --- | --- | --- | --- | --- | --- | --- |
| `spot_ws/src/spot_ros2` | 2025-12-10 | C++/Python | ROS 2 Humble | Spot base driver, hardware interface, description, control | Aktiv | `spot_ws/src/spot_ros2/spot_driver/package.xml` |
| `spot_ws/src/alert_ros2/spot_driver_plus` | see `spot-source-audit.md` §4 | Python/C++ | ROS 2 | Operational Spot launch wrapper (`spot_launch.py`), map_vision, E-stop process, static TF for sensors | Aktiv — this, not `spot_driver.launch.py` alone, is what a real session actually launches | `spot_ws/src/alert_ros2/spot_driver_plus/launch/spot_launch.py` |
| `spot_ws/src/frame_server`, `frame_panel` | 2026-06-25 | Python/C++ | ROS 2 | Runtime named-TF-frame authoring (RViz panel + node) | Aktiv | `spot_ws/src/frame_server/frame_server/frame_server.py` |
| `spot_ws/src/alert_dashboard_rqt` | — | Python (rqt) | ROS 2 | Operator dashboard: subsystem start/stop via tmux, Spot control tab, E-stop status display | Aktiv | `alert_dashboard_rqt/alert_dashboard_rqt/{alert_dashboard_rqt,spot_estop_rqt}.py` |
| `spot_ws/src/octomap_mapping` (`octomap_server`) | 2026-06-01 | C++ | ROS 2 | 3D occupancy mapping from point clouds | Aktiv | `octomap_server/src/octomap_server.cpp:363-374` |
| `spot_ws/src/alert_exploration` | 2026-03-09 | Python | ROS 2 | Frontier exploration, drives `move_base_flex` | Aktiv | `alert_exploration/alert_exploration/mbf_exploration.py` |
| `spot_ws/src/alert_auto_dexterity` | 2026-03-04 | Python (YASMIN) | ROS 2 | Mission state machine: navigate → sit → manipulator inspection sequence → stand, repeated for two named K-Rail waypoints | Aktiv | `alert_dexterity/alert_dexterity/auto_approach.py:38-197` |
| `spot_ws/src/kinova_stuffs` | 2026-03-19 | Python | ROS 2 Humble | Superseded Kinova integration | Legacy — own README states migration to `ros2_kortex` | `maintainers/repository-audit.md` (Entwicklungsauftrag 8) |
| `spot_ws/src/BT` (BehaviorTree.CPP/ROS2) | vendored, ~2023 | C++ | ROS 2 | Vendored behavior-tree library | Unverified — no local consumer package found | `spot-source-audit.md` §4 |
| `man_ws/src/ros2_kortex` (`kortex_driver`, `kortex_bringup`) | 2026-03-25 | C++ | ROS 2 | Kinova Gen3 hardware interface (`KortexMultiInterfaceHardware`), bring-up | Aktiv | `man_ws/src/ros2_kortex/kortex_driver/package.xml` (v0.2.3) |
| `man_ws/src/ros2_robotiq_gripper` | — | C++ | ROS 2 | Standalone Robotiq 2F-85 driver/controllers | Aktiv, but see "Open questions" — may not be the active gripper-control path in the combined robot | `robotiq_driver/package.xml`, `robotiq_controllers/config/robotiq_controllers.yaml` |
| `man_ws/src/spot_gen3_moveit` | 2026-06-19 | Python/YAML | ROS 2 | Generated MoveIt 2 config for the Kinova arm mounted on Spot | Aktiv | `spot_gen3_moveit/package.xml` (v0.3.0) |
| `man_ws/src/auto_dex_nodes` | 2026-05-07 | Python | ROS 2 | Visual servoing, direct manipulator commanding (non-YASMIN) | Aktiv | `auto_dex_nodes/auto_dex_nodes/{go_to_pose,visual_servo}.py` |
| `man_ws/src/picknik_controllers` | — | C++ | ROS 2 | `picknik_twist_controller` (forwards twist to hardware), `picknik_reset_fault_controller` (fault-clear service) | Aktiv | package.xml descriptions |
| `alert_nav_ws/src/octo_navigation` (meta-repo: `bring_up_alert_nav`, `mbf_octo_nav`, `astar_octo_planner`, `astar_2d_planner`, `octo_controller`, `graph_exploration`, `alert_rviz_plugins`) | 2026-09-08 — newest commit in the whole backup | C++/Python | ROS 2 | Octomap-based 3D navigation on `move_base_flex` | Aktiv | `bring_up_alert_nav/launch/mbf_alert_nav_server_launch.py` |
| `david_ws/src/spot_dualsense` | 2026-06-26 | Python | ROS 2 | DualSense gamepad teleop (Spot body + manipulator) | Aktiv | `controller_controls/read_dualsense.py` |

## ROS package inventory (selected, safety/architecture-relevant)

| Paket | Typ | Aufgabe | Startpunkt | Abhängigkeiten | Hardwarebezug | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `spot_driver` | ament_python/C++ | Main Spot driver node, ~50 Trigger services, status publishers, action servers | executable `spot_ros2` | `bosdyn`, `bosdyn_msgs`, `spot_wrapper`, `spot_msgs`, `spot_description` | Real Spot (gRPC/SDK) | Aktiv |
| `spot_hardware_interface` | ament_cmake | `ros2_control` hardware component `SpotSystem`, estop-gated activation | plugin `hardware_interface::SystemInterface` | `bosdyn`, `bosdyn_api_msgs`, `hardware_interface` | Real Spot joint control API | Aktiv |
| `spot_ros2_control` | ament_cmake | ros2_control bring-up, controllers | `ros2_control_node` via launch | `spot_hardware_interface`, `spot_controllers` | Real Spot | Aktiv |
| `spot_description` | ament_python | URDF/xacro (Spot body, optional BD arm, unconditional Kinova+gripper include) | n/a (description only) | `xacro`, `robot_state_publisher` | n/a | Aktiv |
| `kortex_driver` | ament_cmake (v0.2.3) | Kinova Gen3 hardware interface, fault management | plugin `KortexMultiInterfaceHardware` | `kortex_api`, `hardware_interface` | Real Kinova Gen3 (TCP) | Aktiv |
| `spot_gen3_moveit` | ament_python (v0.3.0) | MoveIt 2 config: 1 planning group (`manipulator`), joint limits at 10% default scaling | `move_group.launch.py`, `demo.launch.py` | `moveit_configs_utils`, `moveit_ros_move_group` | Real or simulated Kinova | Aktiv |
| `octomap_server` | ament_cmake | 3D occupancy mapping | node, Best Effort point cloud subscription | `octomap`, PCL | Real LiDAR/depth sensors | Aktiv |
| `bring_up_alert_nav` / `mbf_octo_nav` | ament_cmake/python | `move_base_flex`-based navigation on Octomap-derived costmaps | node `move_base_flex` (executable `mbf_octo_nav`) | `move_base_flex`, custom `astar_octo_planner`, `octo_controller` | Real/sim | Aktiv |
| `alert_exploration` | ament_python | Frontier-based autonomous exploration | run directly (`ros2 run`), no launch file found | `mbf_msgs`, `nav_msgs` (undeclared in package.xml — manifest gap) | n/a | Aktiv, with a documented manifest gap |
| `alert_dashboard_rqt` | ament_python (rqt plugin) | Operator dashboard: subsystem toggle, Spot control tab, E-stop status | rqt plugin, `plugin.xml` | `rqt_gui`, `rqt_gui_py` | n/a | Aktiv |
| `spot_dualsense` | ament_python | DualSense gamepad teleop | `read_dualsense.py`, `pydualsense` (non-ROS `joy`) | none declared beyond ROS basics | Real Spot + manipulator via cmd_vel/twist topics | Aktiv |

## Runtime components (how the system is actually started)

**No single ROS 2 launch tree starts the whole system.** The real
bring-up is a set of ~19 independently-started processes, each run as
a named `tmux` window through a custom HTTP API
(`tmux_api_server`, `spot_ws/src/alert_dashboard_rqt/tmux_api_server/main.py`,
started by `configs/systemd/tmux-api-server.service`), toggled from the
`alert_dashboard_rqt` operator dashboard. The window→command table
(`spot_ws/src/alert_dashboard_rqt/alert_dashboard_rqt/window_commands.py:13-46`):

| Komponente | Host-Rolle | Prozess/Node | Startmechanismus | Eingaben | Ausgaben | Evidenz |
| --- | --- | --- | --- | --- | --- | --- |
| `discovery` | Robot Computer | `fastdds discovery --server-id 0` | tmux window via dashboard | — | DDS discovery service | `window_commands.py:15` |
| `estop` | Robot Computer | `spot_driver_plus/spot_estop.py` | tmux window via dashboard (Estop slider) | operator slider input | Spot software E-stop endpoint (SDK `EstopKeepAlive`) | `window_commands.py:16`; `spot_estop_rqt.py:637-651` |
| `spot_driver` | Robot Computer | `spot_driver_plus spot_launch.py` (includes `spot_driver.launch.py` + map_vision + frame_server + static TF) | tmux window via dashboard | Spot SDK/gRPC connection | `cmd_vel`, `status/*`, `odometry`, TF, images | `spot_launch.py` |
| `kinova_driver` | Manipulator Controller | `kortex_bringup gen3.launch.py robot_ip:=$GEN3_IP dof:=6` | tmux window via dashboard | Kinova Gen3 TCP connection | joint states, `/joint_states` | `window_commands.py:20` |
| `kinova_moveit` | Robot Computer | `spot_gen3_moveit move_group.launch.py use_rviz:=false` | tmux window via dashboard | joint states, planning requests | `/move_action`, `FollowJointTrajectory` | `window_commands.py:21` |
| `kinova_python` | Robot Computer | `kortex_controller_py manipulator_launch.py` | tmux window via dashboard | — | manipulator command interface | `window_commands.py:19` |
| `kinova_vision` | Manipulator Controller | `kinova_vision kinova_vision.launch.py` | tmux window via dashboard | wrist camera | image topics | `window_commands.py:22` |
| `realsenses` | Sensors | `rrl_launchers realsenses_launch.py` | tmux window via dashboard | RealSense USB | depth/color images | `window_commands.py:23` |
| `livox_driver` | Sensors | `livox_ros_driver2 msg_MID360_launch.py` | tmux window via dashboard | Livox Mid-360 LiDAR | point cloud | `window_commands.py:24` |
| `octo_livox`/`octo_spot` | Robot Computer | `octomap_server octomap_{livox,spot}_launch.py` | tmux window via dashboard | point clouds (Best Effort QoS) | `/octomap_binary`, `/octomap_full` | `window_commands.py:25-26`; `octomap_server.cpp:363-374` |
| (nav stack) | Robot Computer | `bring_up_alert_nav`/`mbf_octo_nav` (not itself in the dashboard's dict — started separately, evidenced by its own launch files) | `ros2 launch bring_up_alert_nav alert_nav_launch.py` | Octomap, odometry | `/cmd_vel_stamped` velocity commands | `mbf_alert_nav_server_launch.py` |
| Operator dashboard/RViz | Operator Station | `alert_dashboard_rqt`, RViz | manual (operator device) | tmux API, ROS topics | operator control input | `alert_dashboard_rqt.py` |

The Spot driver's own internal startup order (within the `spot_driver`
window), from `spot_driver.launch.py`: set `use_sim_time` → `spot_ros2`
(main driver) → `lease_manager_node` (if controllable) →
`spot_inverse_kinematics_node` → `object_synchronizer_node` →
`robot_state_publisher` (fed the Spot xacro) → `state_publisher_node`
→ optional RViz → optional image publishers → optional
`spot_ros2_control`.

## Interfaces (selected safety- and architecture-relevant)

| Name | Typ | Nachricht/Interface | Anbieter | Verbraucher | Namespace | Evidenz |
| --- | --- | --- | --- | --- | --- | --- |
| `status/estop` | Topic | `spot_msgs/EStopStateArray` | `spot_driver` (`state_publisher_node`) | dashboard, any monitor | none (default) | `state_middleware_handle.cpp:28,75` |
| `estop/hard` | Service (`std_srvs/Trigger`) | severe E-stop (`assertEStop(severe=True)`) | `spot_driver` (`spot_ros2` node) | operator/scripted caller | none | `spot_ros2.py:1278-1323`; **flagged in-code as apparently non-functional at time of writing** (`spot_ros2.py` comment near line 1318/1319) |
| `estop/gentle` | Service (`std_srvs/Trigger`) | gentle E-stop (`assertEStop(severe=False)`) | `spot_driver` | operator/scripted caller | none | same as above |
| `estop/release` | Service (`std_srvs/Trigger`) | `disengageEStop()` | `spot_driver` | operator/scripted caller | none | same as above |
| `cmd_vel` | Topic | `geometry_msgs/Twist` | operator input (dashboard/gamepad) | `spot_driver` (`cmd_velocity_callback`) | none | `spot_ros2.py:619, 2643` |
| `power_on` / `power_off` | Service (`std_srvs/Trigger`) | motor power on/off | `spot_driver` | dashboard "Spot Power Off/On" button, `.bashrc spot()` helper | none | `spot_ros2.py:1278-1323`; `spot_estop_rqt.py:576-589` |
| `/move_action` | Action | `moveit_msgs/action/MoveGroup` | `move_group` (spot_gen3_moveit) | dashboard `moveit_action_client.py`, `auto_dex_node.py` | none | `moveit_action_client.py:9,14` |
| `/joint_trajectory_controller/follow_joint_trajectory` | Action | `control_msgs/FollowJointTrajectory` | `joint_trajectory_controller` (ros2_control) | `auto_dex_node.py` | none | `auto_dex_node.py:42-45` |
| `/twist_controller/commands` | Topic | `geometry_msgs/TwistStamped` (frame `gen3_base_link`) | DualSense teleop, visual servo nodes | `picknik_twist_controller` | none | `read_dualsense.py:229-239`; `picknik_controllers` package description |
| `reset_fault/command`, `reset_fault/async_success`, `reset_fault/internal_fault` | Command/state interfaces (ros2_control) | Kinova fault clear (internally calls SDK `ApplyEmergencyStop` ×2, then `ClearFaults`) | `kortex_driver` write() | `picknik_reset_fault_controller` | none | `kortex_driver/kortex_driver/src/hardware_interface.cpp:927-964` |
| `navigate_to` | Action | `spot_msgs/action/NavigateTo` | `spot_driver`, requires `frame_id=="body"` | operator/mission code | none | `spot_ros2.py:981-987, 2529-2533` |
| `/octomap_binary`, `/octomap_full` | Topic | `octomap_msgs` | `octomap_server` | `bring_up_alert_nav`/`mbf_octo_nav` | none | `mbf_alert_nav.yaml:` `octo_mapping_server.octomap_topic` |
| `/cmd_vel_stamped` | Topic | `geometry_msgs/TwistStamped` | `move_base_flex` (remapped) | `alert_utils/stamped_twist_converter` → `cmd_vel` | none | `mbf_alert_nav_server_launch.py:18-28` |

## TF frames

| Parent | Child | Quelle | Statisch/Dynamisch | Verantwortliches Paket | Verifiziert |
| --- | --- | --- | --- | --- | --- |
| `body` | `base_link`, `front_rail`, `rear_rail` | `spot_macro.xacro:26-64` | Static (fixed joints) | `spot_description` | Verified in code |
| `body` | 4× hip/upper_leg/lower_leg chains | `spot_macro.xacro:67-543` | Dynamic (revolute) | `spot_description` + `spot_driver` dynamic broadcaster | Verified in code |
| `body` | `gen3_base_link` (Kinova root) | `spot_macro.xacro:59-64`, fixed joint `spot_to_kinova`, unconditional include | Static | `spot_description` | Verified in code |
| `gen3_base_link` | ... | `end_effector_link` | 6 Kinova joints (joint_1..6) | Dynamic | `spot_gen3_moveit`/`kortex_driver` |
| `end_effector_link` | `robotiq_base_link` → 10 finger links | `formatted_robot.urdf` | Static + `finger_joint` dynamic | `spot_description`/`kortex_driver` (internal bus gripper comm) | Verified in code |
| `body` | `livox` / `/livox_frame` | `spot_macro.xacro:83-102`; also republished by `spot_launch.py:59-68` | Static | `spot_description`, `spot_driver_plus` | Verified in code |
| `body` | `ifm_front/back_plate`, `ifm_right/...`, `ifm_left/...` | `spot_launch.py:78-120` | Static | `spot_driver_plus` | Verified in code |
| `body` | `world` | `spot_launch.py:70-76` | Static — note: `body` is the parent, `world` the child, opposite of the usual convention | `spot_driver_plus` | Verified in code, flagged as non-standard |
| — | `vision` (odom root) | SDK kinematic snapshot, `preferred_odom_frame: "vision"` | Dynamic | `spot_driver`; config `spot_driver_plus/config/spot_params.yaml:12` | Verified in configuration |
| `graph_nav_map` | `body` | `StaticTransformBroadcaster`, `spot_ros2.py:603` | Static (published at GraphNav localization) | `spot_driver` | Verified in code |
| `map` | `odom` | `alert_nav_launch.py:53-58` | Defined but **commented out** — not active in the current launch | `bring_up_alert_nav` | Verified in code as present-but-inactive |
| `map` (`global_frame`) | `feet_center` (`robot_frame`) | `mbf_alert_nav.yaml:3-4` | n/a (navigation frame convention) | `bring_up_alert_nav` | Verified in configuration — note: differs from `alert_exploration`'s own `ROBOT_BASE_FRAME = 'body'` constant; not reconciled in the codebase |
| `base_link` (manipulator-local) | `tool_tip` | `auto_dex_nodes/go_to_pose.py:23-24` | n/a | `auto_dex_nodes` | Verified in code — note: name collides with Spot's own `base_link`; distinct frame, same name, a real ambiguity in the system |

## Open questions (not resolved by static analysis — do not assert either way in public docs)

1. Whether Boston Dynamics' own Spot Arm (`has_arm: True`) is used in any real deployment — every located deployment config sets `has_arm: False`.
2. Which gripper-control path is authoritative for the combined robot: Kortex's internal-bus gripper comm (`formatted_robot.urdf`) or the standalone Robotiq driver/controllers (`man_ws/src/ros2_robotiq_gripper`) — both exist in the repository.
3. Zenoh (`rmw_zenoh_cpp`, persistent systemd service) vs. Fast-DDS discovery server (`fastdds discovery`, an ad-hoc tmux window) as the actual live middleware — both are configured; no single definitive answer found.
4. Whether `bring_up_alert_nav/srv/StartNav.srv` is advertised by any node — the service is defined but no advertising code was located.
5. Whether a `spot_name` namespace is ever set at deployment (default is empty/no namespace) — not found in any located config.
6. Whether `spot_ws/src/BT` (BehaviorTree.CPP/ROS2) is genuinely deprecated or simply unused so far — no local consumer package found either way.

## Cross-reference

TF frame and package findings above complement, and in a few places
correct or add nuance to, the GitHub-level audit in
`maintainers/repository-audit.md` (Entwicklungsauftrag 8) — e.g. that
audit could not determine `spot_gen3_moveit`'s purpose beyond its name
(no README on GitHub); this audit confirms it from the actual config
files (one planning group `manipulator`, joint limits at 10% default
scaling, named states `nuc_rest`/`front_inspection`).
