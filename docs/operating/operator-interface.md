# Operator Interface

## Purpose

Describe what the operator actually sees and controls once the system
is running: the `alert_dashboard_rqt` dashboard and RViz.

## Required supervision

None to simply observe the interface; several of its controls start
processes or command the robot — see the per-control notes below and
[Safety Principles](../safety/safety-principles.md) before using them.

## Prerequisites

[Power-On Procedure](power-on.md) complete.

## Initial state

The Spot driver is running; the dashboard is open.

## Procedure

Location for everything on this page: the Operator Station, unless
noted otherwise. The dashboard itself runs there; the processes/services
its buttons start or call run on the Robot Computer.

`alert_dashboard_rqt` is an rqt plugin (source:
`alert_dashboard_rqt/alert_dashboard_rqt/alert_dashboard_rqt.py`,
`spot_estop_rqt.py`). It has two related parts:

**Subsystem toggles** (not read-only — each starts or stops a process
on the Robot Computer). For every entry in a fixed table of subsystem
commands (`discovery`, `estop`, `spot_driver`, `kinova_driver`,
`kinova_moveit`, `kinova_python`, `kinova_vision`, `realsenses`,
`livox_driver`, `octo_livox`, `octo_spot`, and others — source:
`alert_dashboard_rqt/window_commands.py`), a button starts or stops
that subsystem as a named process, and a label shows its status
("✓ Running", "💥 CRASHED"). `Verified in code`.

**Spot control tab set.** Literal controls found in the source
(`spot_estop_rqt.py`), by label, with whether each is read-only or can
trigger motion/state changes:

```{list-table}
:header-rows: 1
:widths: 22 18 60

* - Control
  - Read-only?
  - Behavior
* - "Estop" slider
  - No
  - Arms/disarms the software E-stop endpoint process — see [Safety
    Principles](../safety/safety-principles.md#the-operator-dashboards-estop-control).
* - "Start" button
  - No
  - Starts the `kinova_driver`, `kinova_vision`, and `spot_driver`
    subsystem processes via the tmux API.
* - "Frame Runner" (toggle)
  - No
  - Starts/stops the `frame_runner` subsystem window.
* - "Hazmat" button
  - No
  - Starts the hazmat-detection subsystem window.
* - "World Reset" button
  - No
  - Calls the `reset_map_frame`, `reset_travelled_path`,
    `octomap_server/reset`, and `navigation/octomap_server/reset`
    services — clears mapping state, does not move the robot.
* - "2WayAudio" (toggle)
  - No
  - Starts/stops the `audio_capture`/`audio_play` subsystem windows.
* - "Spot Power Off/On" button
  - No
  - Calls the `power_off` service, then the `power_on` service, in
    sequence.
* - "Lights" (toggle)
  - No
  - Calls the `arduino_lights` service.
* - Battery display
  - Yes
  - Shows remaining percentage and estimated time from
    `status/battery_states`.
```

Tabs are literally labeled "BASIC", "PLUS", "BW" (Blocksworld), "EXP"
(Exploration), and "NAV" (Navigation) in the source.

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

**RViz** (read-only unless you use one of its interactive tools).
`configs/rviz2/default.rviz` configures: `RobotModel`, `TF`,
`OccupancyGrid` (topic `/octomap_binary`), two `Map` displays (topics
`/mapUGV`, `/navigation/projected_map_1m`), a `Path` display (topic
`/move_base_flex/body_height/path`), a `MarkerArray` (topic
`/move_base_flex/graph_nodes`), and a `PointCloud2` display, plus the
standard `SetInitialPose`/`SetGoal`/`PublishPoint` tools — these three
are **not** read-only, they publish a pose/point that a running
navigation stack may act on. `Verified in configuration`.

## Expected observations

Live, updating status for the subsystems you have started; RViz
showing the robot model and TF tree once `robot_state_publisher` is
running; the battery display updating from `status/battery_states`.

## Verification

Confirm the dashboard shows live, updating status for the subsystems
you have started, and that RViz shows the robot model and TF tree once
`robot_state_publisher` is running.

## Stop conditions

Do not trust a control's on-screen state if the dashboard shows "⚠️
Disconnected from API" — the tmux backend, not just that one control,
is the problem. Do not use `SetInitialPose`/`SetGoal`/`PublishPoint` in
RViz without the same supervision required for any other
motion-triggering control.

## Recovery

A label reading "⚠️ Disconnected from API" means the dashboard cannot
reach `tmux_api_server` — see [Recovery and
Troubleshooting](recovery-and-troubleshooting.md).

## Final state

The dashboard and RViz both show live, current system state, and you
know which of their controls are read-only versus which start
processes or affect the robot.

## Related components

[Power-On Procedure](power-on.md), [Driving Spot](driving-spot.md),
[Operating the Manipulator](operating-the-manipulator.md).
