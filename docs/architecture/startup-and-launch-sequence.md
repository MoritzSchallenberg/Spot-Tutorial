# Startup and Launch Sequence

## Overview

The order components actually come up in, and how that differs across
the system's distinct operating modes.

## Purpose

Document the real startup process — which, on the evidence available,
is not a single ROS 2 launch tree but a set of independently-started
processes — rather than presenting an idealized launch file that
doesn't exist in the current code.

## System context

This is the architectural counterpart to [Power-On
Procedure](../operating/power-on.md), which gives the same sequence as
an operator-facing step-by-step guide.

## The real bring-up mechanism

No single launch file starts the whole system. Instead, an operator
starts each subsystem as an independent process (`ros2 launch`/`ros2
run`), run inside a named `tmux` window by a custom HTTP API
(`tmux_api_server`), toggled from the operator dashboard. Source:
`alert_dashboard_rqt/window_commands.py`; see
`spot-code-audit.md` (internal) for the full table.

`Verified in code`.

## Diagram: startup sequence

:::{mermaid}
:alt: Sequence diagram showing discovery and estop processes starting first, then the Spot driver, then sensors and navigation, then the manipulator stack.

graph TD
    A["discovery + estop<br/>(software E-stop endpoint)"] --> B["spot_driver<br/>(base driver, TF, state)"]
    B --> C["Sensors<br/>(realsenses, livox_driver, thermal_cam)"]
    C --> D["Mapping<br/>(octo_livox, octo_spot)"]
    D --> E["Navigation<br/>(bring_up_alert_nav)"]
    B --> F["kinova_driver"]
    F --> G["kinova_moveit"]
:::

## Within the Spot driver window

`spot_driver_plus/launch/spot_launch.py` includes
`spot_driver/launch/spot_driver.launch.py`, whose own internal order
is: set `use_sim_time` → `spot_ros2` (main driver) →
`lease_manager_node` (if controllable) → `spot_inverse_kinematics_node`
→ `object_synchronizer_node` → `robot_state_publisher` (fed the Spot
xacro) → `state_publisher_node` → optional RViz → optional image
publishers → optional `spot_ros2_control`. `spot_launch.py` then adds
`map_vision`, `frame_server`, and static TF publishers for the sensor
frames.

`Verified in code`.

## Operating modes

```{list-table}
:header-rows: 1
:widths: 25 75

* - Mode
  - What's running (beyond `discovery` + `estop` + `spot_driver`, which every mode needs)
* - Base only
  - Nothing further — driving and body-pose control only.
* - Base with sensors
  - Add `realsenses`, `livox_driver`, `thermal_cam` as needed.
* - Base with manipulator
  - Add `kinova_driver`, `kinova_moveit`, optionally `kinova_python`,
    `kinova_vision`.
* - Mapping mode
  - Add sensors plus `octo_livox`/`octo_spot` (Octomap servers).
* - Autonomous mode
  - Add mapping plus `bring_up_alert_nav` (navigation) and, for
    frontier exploration, `alert_exploration` (run directly, no
    dedicated dashboard window found for it).
```

`Verified in code` for which processes exist; this table's grouping
into named "modes" is this documentation's own organization of the
runtime window list, not a mode switch that exists as a single control
in the code.

## Verification

`Verified in code` throughout, sourced from `window_commands.py` and
the launch files it invokes.

## Failure modes

See [Power-On Procedure](../operating/power-on.md) and [Recovery and
Troubleshooting](../operating/recovery-and-troubleshooting.md) for what
to do when a step in this sequence does not complete as expected.

## Related components

[Software Components](software-components.md), [ROS 2
Interfaces](ros2-interfaces.md).
