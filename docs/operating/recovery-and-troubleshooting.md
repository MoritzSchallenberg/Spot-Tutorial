# Recovery and Troubleshooting

## Purpose

What to do after an interrupted startup, a communication loss, or a
manipulator fault — and, just as importantly, what this documentation
does **not** know about each situation.

## Prerequisites

A working knowledge of [Power-On Procedure](power-on.md) and [Safety
Principles](../safety/safety-principles.md).

## Interrupted startup

If the `spot_driver` node was started before the software E-stop
endpoint was present, it blocks in a wait loop, repeatedly logging
"Waiting for estop to be released..." (source:
`spot_driver/spot_driver/spot_ros2.py`). This is expected behavior, not
a fault.

Action: Confirm the `estop` window/process is running on the operator
dashboard (see [Power-On Procedure, Step
4](power-on.md#step-4-arm-the-software-e-stop-endpoint)). Once it is,
the driver proceeds on its own — no restart is needed.

Verification: Driver log changes from "Waiting for estop..." to "Found
estop!". `Verified in code`.

If the driver was started, then the estop process was stopped and
restarted, `Unverified on hardware` whether the driver recovers without
a restart — restart the `spot_driver` window if it does not.

(communication-loss)=
## Communication loss

No code in the current Spot codebase implements a specific,
documented "lost connection" behavior (for example, an automatic
failsafe stop after a communication timeout) for either the Spot
driver or the Kinova driver — this was searched for directly and not
found. `Unverified` (not just unverified on hardware — unverified in
code as well).

Action: If communication is lost, do not assume the robot has stopped
moving on its own. Use the physical E-stop if there is any doubt about
the robot's state — see [Emergency Stops](../safety/emergency-stops.md).

Recovery: Once communication is restored, re-run [Power-On
Procedure](power-on.md) from the step that failed, rather than
assuming prior state is still valid.

(manipulator-fault)=
## Manipulator fault

If the Kinova arm reports a fault (`ARMSTATE_IN_FAULT`), the
`reset_fault` command interface, exposed via the
`picknik_reset_fault_controller`, runs a fixed sequence: switch to
single-level servoing, call the Kinova SDK's `ApplyEmergencyStop`
**twice** (an in-code comment notes this was found necessary because a
single call was unreliable in testing), call `ClearFaults()`, then
restore the previous servoing mode. Source:
`ros2_kortex/kortex_driver/src/hardware_interface.cpp`.

Action: Trigger the fault-reset via the `reset_fault` command interface
(exposed through whatever controller/UI path is wired up in the
current deployment — this documentation confirms the interface exists
in code, not a specific button for it on the dashboard).

Expected state: Fault cleared, arm returns to its prior servoing mode.

Verification: `Verified in code` for the sequence itself;
`Unverified on hardware` for whether it reliably clears every fault
condition in practice.

Stop condition: If the fault recurs immediately after reset, stop and
consult a trained team member rather than repeating the reset
indefinitely.

Recovery: Re-run [Operating the Manipulator](operating-the-manipulator.md)
from Step 1 once the fault is cleared.

## Software E-stop endpoint crashed or disconnected

If the operator dashboard shows "💥 E-Stop CRASHED" or "⚠️ Disconnected
from API" (literal strings from `spot_estop_rqt.py`'s
`check_estop_status()`):

Action: Disengage and re-engage the dashboard's "Estop" control (see
[Safety Principles: the operator dashboard's "Estop"
control](../safety/safety-principles.md#the-operator-dashboards-estop-control)).
If the tmux API itself is unreachable, confirm `tmux-api-server.service`
is running on the robot computer.

Verification: Status label returns to "✓ E-Stop Running".

## Verification

Every claim on this page states its own verification level inline,
since the honest answer differs sharply between "interrupted startup"
(well understood from code) and "communication loss" (not documented
anywhere in the current codebase).

## Related components

[Safety Principles](../safety/safety-principles.md), [Power-On
Procedure](power-on.md), [Safe Shutdown](safe-shutdown.md).
