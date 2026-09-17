# Recovery and Troubleshooting

## Purpose

A decision path for ten specific starting symptoms, each moving from a
safe visual check toward a specific cause — not just a list of
failures. What this documentation does **not** know about a given
situation is stated as plainly as what it does.

## Required supervision

A trained team member must be present for any check beyond Step 1–2 of
any case below that involves the physical robot. No case here
recommends an automatic restart or a movement attempt as a default
fix — every "Allowed recovery" is a deliberate, supervised action.

## Prerequisites

A working knowledge of [Power-On Procedure](power-on.md), [System
Architecture](../architecture/index.md), and [Safety
Principles](../safety/safety-principles.md).

## Initial state

Something is not behaving as expected during or after a session.

## Procedure

Find the symptom below that matches what you observe, and follow its
path in order. Each path is: (1) a safe visual check, (2) a read-only
system check, (3) the expected result, (4) where to go next depending
on what you actually saw, (5) a safe condition to stop and not proceed
further, (6) a recovery action that is allowed at this point, and (7)
when to stop and get an experienced team member instead of continuing
alone.

### Case 1: Spot is not reachable

1. **Visual check:** Is Spot powered on (indicator visible per
   [Power-On Procedure](power-on.md))? Is the operator device connected
   to the robot's operating network?
2. **Read-only check:** `ros2 topic echo status/estop` (or any
   `spot_driver` topic) from a terminal on the Operator Station.
3. **Expected result:** Topic data arrives.
4. **Next branch:** No power → see [Power-On
   Procedure](power-on.md). Powered but no network → this is
   [Communication loss](#communication-loss) below. Network present but
   no topic data → go to [Case 2](#case-2-ros-2-nodes-are-missing).
5. **Safe abort condition:** Do not attempt to physically approach or
   power-cycle Spot solely to "fix" a network issue — the robot itself
   may be fine.
6. **Allowed recovery:** Reconnect the operator device to the network;
   re-run [Power-On Procedure, Step 2](power-on.md#step-2-power-on-the-operator-device-and-connect).
7. **Escalation:** If reconnecting does not restore topic data within
   a few attempts, stop and get a trained team member — this may be a
   deeper network or middleware issue (see [Computers and
   Network](../architecture/computers-and-network.md)'s Zenoh/Fast-DDS
   note).

(communication-loss)=
### Communication loss

No code in the current Spot codebase implements a specific, documented
"lost connection" behavior (e.g. an automatic failsafe stop after a
timeout) for either the Spot driver or the Kinova driver — this was
searched for directly and not found. `Unverified` (unverified in code,
not only unverified on hardware).

**Allowed recovery:** do not assume the robot has stopped moving on
its own. Use the physical E-stop if there is any doubt about the
robot's state — see [Emergency Stops](../safety/emergency-stops.md).
Once communication is restored, re-run [Power-On
Procedure](power-on.md) from the step that failed, rather than
assuming prior state is still valid.

### Case 2: ROS 2 nodes are missing

1. **Visual check:** Which subsystem windows does the operator
   dashboard show as running?
2. **Read-only check:** `ros2 node list` from a terminal, compared
   against [Startup and Launch
   Sequence](../architecture/startup-and-launch-sequence.md)'s node
   list for the operating mode you intended to run.
3. **Expected result:** Every node the intended operating mode requires
   is present.
4. **Next branch:** A specific subsystem window shows "💥 CRASHED" →
   go to [Case 10](#case-10-a-process-exited-during-startup). All
   windows show running but a node is still missing → escalate (this
   is not a documented failure mode).
5. **Safe abort condition:** Do not command motion or manipulation
   while a required node for that function is missing.
6. **Allowed recovery:** Start the missing subsystem window from the
   operator dashboard, in the order given in [Startup and Launch
   Sequence](../architecture/startup-and-launch-sequence.md).
7. **Escalation:** If a node required by the operating mode never
   appears after a correctly-ordered start, stop and get a trained
   team member.

### Case 3: The operator interface shows no data

1. **Visual check:** Does the dashboard show "⚠️ Disconnected from
   API" or "💥 E-Stop CRASHED" (literal strings from
   `spot_estop_rqt.py`'s `check_estop_status()`)?
2. **Read-only check:** none needed if Step 1 already shows one of
   those labels — they are the read-only check.
3. **Expected result:** Labels showing "✓ Running" / "✓ E-Stop
   Running".
4. **Next branch:** "⚠️ Disconnected from API" → the tmux backend
   itself is the problem, not any one control — confirm
   `tmux-api-server.service` is running on the Robot Computer. "💥
   E-Stop CRASHED" → go to [Case
   4](#case-4-spot-cannot-be-enabled).
5. **Safe abort condition:** Do not trust any other on-screen control
   state while "Disconnected from API" is shown.
6. **Allowed recovery:** Disengage and re-engage the dashboard's
   "Estop" control (see [Safety Principles: the operator dashboard's
   "Estop" control](../safety/safety-principles.md#the-operator-dashboards-estop-control)).
7. **Escalation:** If the label does not return to "✓ E-Stop Running"
   after one re-attempt, stop and get a trained team member —
   restarting the underlying systemd service requires direct access to
   the Robot Computer.

### Case 4: Spot cannot be enabled

1. **Visual check:** Driver log window — is it repeating "Waiting for
   estop to be released..."?
2. **Read-only check:** Dashboard's E-stop status label.
3. **Expected result:** Log changes to "Found estop!"; label shows "✓
   E-Stop Running". `Verified in code` (source:
   `spot_driver/spot_driver/spot_ros2.py`) — this waiting behavior
   itself is expected, not a fault.
4. **Next branch:** Estop window not started → see [Power-On
   Procedure, Step 4](power-on.md#step-4-arm-the-software-e-stop-endpoint).
   Estop window running but driver still waiting → go to [Case
   3](#case-3-the-operator-interface-shows-no-data). `spot_hardware_interface`
   specifically refuses to activate while Spot reports itself
   E-stopped (source: `spot_hardware_interface.cpp`, `check_estop()`)
   — if using the `ros2_control` path, confirm `status/estop` directly
   rather than only the dashboard label.
5. **Safe abort condition:** Do not repeatedly restart the driver
   hoping it resolves on its own — confirm the E-stop endpoint state
   first.
6. **Allowed recovery:** Start or re-arm the software E-stop endpoint
   per [Power-On Procedure, Step 4](power-on.md#step-4-arm-the-software-e-stop-endpoint);
   the driver proceeds on its own once it is present — no driver
   restart needed if you only just fixed the endpoint.
7. **Escalation:** If the driver was started, then the estop process
   was stopped and restarted, whether the driver recovers without a
   restart is `Unverified on hardware` — if it does not, restart the
   `spot_driver` window; if that also fails, get a trained team member.

### Case 5: Sensor data is missing

1. **Visual check:** Is the sensor's subsystem window (`realsenses`,
   `livox_driver`, `thermal_cam`) running on the dashboard?
2. **Read-only check:** `ros2 topic hz <topic>` for the specific
   sensor's topic (see [Hardware
   Overview](../architecture/hardware-overview.md) for which sensor
   maps to which subsystem window; exact topic names are not all
   literal strings in the driver and vary by sensor — confirm with
   `ros2 topic list` first).
3. **Expected result:** Data publishing at a steady rate.
4. **Next branch:** Window not running → start it from the dashboard.
   Window running but no data → this is not a documented failure mode
   in the current code — escalate rather than guess at a USB/driver
   cause.
5. **Safe abort condition:** Do not proceed with mapping, navigation,
   or perception tasks that depend on this sensor until data is
   confirmed flowing.
6. **Allowed recovery:** Restart the specific sensor's subsystem
   window from the dashboard.
7. **Escalation:** If restarting the window does not restore data,
   stop and get a trained team member — sensor hardware issues (loose
   USB connection, power) are outside what this documentation can
   diagnose from code alone.

### Case 6: TF is incomplete

1. **Visual check:** In RViz, does the `TF` display show a broken tree
   (disconnected frames, or frames present but not updating)?
2. **Read-only check:** `ros2 run tf2_tools view_frames` or `ros2 topic
   echo /tf_static` compared against [Coordinate
   Frames](../architecture/coordinate-frames.md)'s frame table.
3. **Expected result:** Every frame relevant to your current operating
   mode present and updating (static frames appear once; dynamic
   frames update continuously).
4. **Next branch:** A whole subsystem's frames missing (e.g. all arm
   frames) → the corresponding driver likely is not running — see
   [Case 2](#case-2-ros-2-nodes-are-missing). Frames present but stale
   (not updating) → the publishing node is running but not producing
   data — treat like [Case 5](#case-5-sensor-data-is-missing) for that
   subsystem.
5. **Safe abort condition:** Do not trust a navigation goal, a
   manipulation target, or any RViz-displayed pose while TF is known
   incomplete for the frames involved.
6. **Allowed recovery:** Restart the specific subsystem window whose
   frames are missing or stale.
7. **Escalation:** If frames remain missing after a restart, stop —
   this codebase has two coexisting, unreconciled robot-frame
   conventions (`feet_center` vs. `body`; see [Coordinate
   Frames](../architecture/coordinate-frames.md)), so a "missing frame"
   may also be a naming mismatch between packages rather than a
   crashed node. Get a trained team member rather than guessing which.

### Case 7: Navigation does not start

1. **Visual check:** Is the `octo_livox`/`octo_spot` (Octomap) window
   running, and is the navigation stack's own window running?
2. **Read-only check:** `ros2 topic echo /octomap_binary` and `ros2
   action list` for `move_base_flex`'s action server (see [Data
   Flow](../architecture/data-flow.md) for the pipeline this depends
   on).
3. **Expected result:** Octomap data present; the navigation action
   server listed.
4. **Next branch:** No octomap data → go to [Case
   5](#case-5-sensor-data-is-missing) for the underlying LiDAR/depth
   sensor. Octomap present but no navigation action server → the
   `bring_up_alert_nav` window itself likely did not start — restart
   it. Both present but a goal is still rejected → check the robot
   frame used in the goal against [Coordinate
   Frames](../architecture/coordinate-frames.md)'s `feet_center`/`body`
   note.
5. **Safe abort condition:** Do not send a navigation goal while
   Octomap data is stale or absent — the planner will be working from
   an outdated or empty map.
6. **Allowed recovery:** Restart the mapping window, then the
   navigation window, in that order.
7. **Escalation:** If navigation still does not start with both
   confirmed running and publishing, stop and get a trained team
   member — this documentation cannot distinguish a planner-parameter
   issue from a deeper fault without a live session.

### Case 8: The manipulator does not respond

1. **Visual check:** Is the `kinova_driver` window running, and does
   it show connected (not crashed)?
2. **Read-only check:** `ros2 topic echo /joint_states`.
3. **Expected result:** Joint states publishing.
4. **Next branch:** Window not running → see [Operating the
   Manipulator, Step 1](operating-the-manipulator.md#step-1-start-the-manipulator-driver).
   Window running, joint states publishing, but the arm still does not
   move on command → this is likely a fault state, go to [Manipulator
   fault](#manipulator-fault) below, not a connectivity problem.
5. **Safe abort condition:** Do not repeat a motion command that had
   no visible effect — confirm joint-state data and fault status
   first.
6. **Allowed recovery:** Restart the `kinova_driver` window.
7. **Escalation:** If joint states publish but the arm still does not
   respond to any command and is not reporting a fault, stop and get a
   trained team member.

(manipulator-fault)=
### Manipulator fault

If the Kinova arm reports a fault (`ARMSTATE_IN_FAULT`), the
`reset_fault` command interface, exposed via the
`picknik_reset_fault_controller`, runs a fixed sequence: switch to
single-level servoing, call the Kinova SDK's `ApplyEmergencyStop`
**twice** (an in-code comment notes this was found necessary because a
single call was unreliable in testing), call `ClearFaults()`, then
restore the previous servoing mode. Source:
`ros2_kortex/kortex_driver/src/hardware_interface.cpp`.
`Verified in code` for the sequence; `Unverified on hardware` for
whether it reliably clears every fault condition in practice.

**Safe abort condition:** if the fault recurs immediately after reset,
stop and consult a trained team member rather than repeating the reset
indefinitely.

**Allowed recovery:** trigger the fault-reset via the `reset_fault`
command interface, then re-run [Operating the
Manipulator](operating-the-manipulator.md) from Step 1.

### Case 9: MoveIt cannot plan

1. **Visual check:** Does RViz's MoveIt plugin show a specific planning
   error, or does "Plan" simply do nothing?
2. **Read-only check:** Confirm `move_group` is running (see [Operating
   the Manipulator, Step 2](operating-the-manipulator.md#step-2-start-moveit))
   and that `/joint_states` is publishing (Case 8, Step 2).
3. **Expected result:** A valid trajectory is returned for a reachable
   target.
4. **Next branch:** `move_group` not running → see [Operating the
   Manipulator, Step 2](operating-the-manipulator.md#step-2-start-moveit).
   Running but planning still fails → the target may be outside the
   arm's reachable workspace, or — since this configuration disables
   most arm-vs-body/leg collision checking (see [Operating the
   Manipulator](operating-the-manipulator.md)'s collision-checking
   warning) — a target that MoveIt accepts as collision-free may still
   be physically unreachable for reasons collision checking here would
   not catch.
5. **Safe abort condition:** Do not switch to manual twist control to
   "push through" a planning failure without first understanding why
   planning failed.
6. **Allowed recovery:** Choose a different, confirmed-reachable
   target; restart `move_group` if it appears unresponsive rather than
   simply erroring.
7. **Escalation:** If a target that should clearly be reachable
   consistently fails to plan, stop and get a trained team member —
   this may indicate a planning-scene or joint-limit configuration
   issue beyond what this documentation can diagnose from code alone.

### Case 10: A process exited during startup

1. **Visual check:** Which dashboard label shows "💥 CRASHED"?
2. **Read-only check:** None beyond the dashboard label itself —
   accessing the process's own log requires the Robot Computer
   directly (outside the dashboard's scope).
3. **Expected result:** The label shows "✓ Running" instead.
4. **Next branch:** If the crashed process is `estop` → treat as
   [Case 4](#case-4-spot-cannot-be-enabled). If `spot_driver` → treat
   as [Case 1](#case-1-spot-is-not-reachable) once restarted. If a
   sensor/perception window → treat as [Case
   5](#case-5-sensor-data-is-missing) once restarted.
5. **Safe abort condition:** Do not start a dependent subsystem (e.g.
   navigation) while an upstream one it needs shows "💥 CRASHED".
6. **Allowed recovery:** Restart the specific crashed window from the
   dashboard, in the order given in [Startup and Launch
   Sequence](../architecture/startup-and-launch-sequence.md) if it
   depends on another subsystem also being up.
7. **Escalation:** If the same process crashes again immediately after
   restart, stop and get a trained team member rather than restarting
   it repeatedly — this documentation has no code-level evidence for
   why a specific process would crash on startup.

## Expected observations

For any case above: a specific next check to run, a specific place to
route to next depending on what that check shows, and a specific point
at which to stop and escalate — never an instruction to "just restart
and see."

## Verification

Every case states its own verification level inline, since the honest
answer differs sharply between well-understood code paths (e.g. Case 4)
and genuinely undocumented behavior (e.g. Communication loss).

## Stop conditions

Any case's own "Safe abort condition" — in general, do not command
motion or manipulation while the specific data or state that command
depends on is confirmed missing, stale, or faulted.

## Recovery

Each case's own "Allowed recovery" is the authoritative answer for that
specific symptom. There is no page-level catch-all recovery beyond
working through the matching case above.

## Final state

The specific fault is either resolved (the expected result in the
matching case is observed) or explicitly escalated to a trained team
member — not left as an unresolved retry loop.

## Related components

[Safety Principles](../safety/safety-principles.md), [Power-On
Procedure](power-on.md), [Safe Shutdown](safe-shutdown.md), [System
Architecture](../architecture/index.md).
