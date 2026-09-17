# Operator Interface

## Purpose

Describe what the operator actually sees and controls once the system
is running: the `alert_dashboard_rqt` dashboard and RViz.

## Prerequisites

[Power-On Procedure](power-on.md) complete.

## Starting State

The Spot driver is running; the dashboard is open.

## The dashboard

`alert_dashboard_rqt` is an rqt plugin (source:
`alert_dashboard_rqt/alert_dashboard_rqt/alert_dashboard_rqt.py`,
`spot_estop_rqt.py`). It has two related parts:

**Subsystem toggles.** For every entry in a fixed table of subsystem
commands (`discovery`, `estop`, `spot_driver`, `kinova_driver`,
`kinova_moveit`, `kinova_python`, `kinova_vision`, `realsenses`,
`livox_driver`, `octo_livox`, `octo_spot`, and others — source:
`alert_dashboard_rqt/window_commands.py`), a button starts or stops
that subsystem as a named process, and a label shows its status
("✓ Running", "💥 CRASHED"). `Verified in code`.

**Spot control tab set.** Literal controls found in the source
(`spot_estop_rqt.py`), by label:

```{list-table}
:header-rows: 1
:widths: 30 70

* - Control
  - Behavior
* - "Estop" slider
  - Arms/disarms the software E-stop endpoint process — see [Safety
    Principles](../safety/safety-principles.md#the-operator-dashboards-estop-control).
* - "Start" button
  - Starts the `kinova_driver`, `kinova_vision`, and `spot_driver`
    subsystem processes via the tmux API.
* - "Frame Runner" (toggle)
  - Starts/stops the `frame_runner` subsystem window.
* - "Hazmat" button
  - Starts the hazmat-detection subsystem window.
* - "World Reset" button
  - Calls the `reset_map_frame`, `reset_travelled_path`,
    `octomap_server/reset`, and `navigation/octomap_server/reset`
    services.
* - "2WayAudio" (toggle)
  - Starts/stops the `audio_capture`/`audio_play` subsystem windows.
* - "Spot Power Off/On" button
  - Calls the `power_off` service, then the `power_on` service, in
    sequence.
* - "Lights" (toggle)
  - Calls the `arduino_lights` service.
```

Tabs are literally labeled "BASIC", "PLUS", "BW" (Blocksworld), "EXP"
(Exploration), and "NAV" (Navigation) in the source. A battery display
shows remaining percentage and estimated time from
`status/battery_states`.

`Verified in code` for every control listed above; button/tab
placement and exact visual layout are not independently reconfirmed
against a live screenshot in this documentation pass.

:::{figure} ../_static/images/historical-interface/rviz.png
:alt: Historical interface. RViz alongside the rqt dashboard, showing the BASIC/PLUS/BW/EXP/NAV tabs, the red Estop slider, a blue Start button, and a battery remaining display, plus three live camera feeds.
:width: 90%
:align: center

**Historical context:** RViz and the rqt dashboard from the former
ALeRT tutorial. **Current implementation:** the tab labels ("BASIC",
"PLUS", "BW", "EXP", "NAV"), the "Estop" slider, the "Start" button,
and the battery-remaining display visible here all match literal
strings still present in the current `spot_estop_rqt.py` source —
unusually strong agreement for a historical screenshot, which is why
it is kept rather than only described. **Hardware verification
required:** yes — the code match confirms these controls exist as
described, not that the on-screen layout is still pixel-identical
today.
:::

## RViz

`configs/rviz2/default.rviz` configures: `RobotModel`, `TF`,
`OccupancyGrid` (topic `/octomap_binary`), two `Map` displays (topics
`/mapUGV`, `/navigation/projected_map_1m`), a `Path` display (topic
`/move_base_flex/body_height/path`), a `MarkerArray` (topic
`/move_base_flex/graph_nodes`), and a `PointCloud2` display, plus the
standard `SetInitialPose`/`SetGoal`/`PublishPoint` tools.
`Verified in configuration`.

## Verification

Confirm the dashboard shows live, updating status for the subsystems
you have started, and that RViz shows the robot model and TF tree once
`robot_state_publisher` is running.

## Failure modes

A label reading "⚠️ Disconnected from API" means the dashboard cannot
reach `tmux_api_server` — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

## Related components

[Power-On Procedure](power-on.md), [Driving Spot](driving-spot.md),
[Operating the Manipulator](operating-the-manipulator.md).
