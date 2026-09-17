# System Preparation

## Purpose

Prepare the robot, the operator device, and the physical workspace
before powering anything on.

## Required supervision

A trained team member must be present for this entire procedure — see
[Operator Checklist](../safety/operator-checklist.md). No step here
powers or moves anything, but Step 3 requires a second person to
confirm E-stop access.

## Prerequisites

[Safety and Prerequisites](../safety/index.md) read in full, and the
[Operator Checklist](../safety/operator-checklist.md) available for
reference during this procedure.

## Initial state

Spot and the manipulator are powered off. The operator device (the
former ALeRT tutorial describes a Steam Deck; not independently
reconfirmed for the current system — `Historical procedure`) is
available but not yet on.

## Procedure

### Step 1: Prepare the physical area

Location: the physical operating area — no computer or terminal
involved.

Type: read-only (visual inspection and manual tidying; no motion
triggered).

Action: Clear the operating area per [Operating
Area](../safety/operating-area.md) — remove loose cables, cups, and
fragile objects, and confirm there is room for Spot to maneuver in any
direction.

Expected observation: An open area with a clear line of sight to the
robot from the operating position.

Verification: Visual inspection.

Stop condition: Do not proceed if the area cannot be cleared
adequately.

Recovery: Clear the area before continuing.

### Step 2: Check batteries

Location: Spot's own battery indicator and the operator device's own
battery indicator — no computer or terminal involved yet.

Type: read-only.

Action: Check Spot's battery and the operator device's battery.

Expected observation: Both sufficiently charged for the planned
session.

Verification: Battery level as shown by each device's own indicator.
Once the driver is running, Spot's battery is also visible on the
operator dashboard's battery display, which subscribes to
`status/battery_states` (source: `alert_dashboard_rqt/alert_dashboard_rqt/spot_estop_rqt.py`,
running on the Robot Computer). `Verified in code` for the dashboard
display; `Historical procedure` for the general "charge before
starting" guidance itself.

Stop condition: Do not start a session on a battery too low to
complete it safely.

Recovery: Charge before continuing.

### Step 3: Confirm the physical E-stop button(s) are reachable

Location: the physical operating area — no computer or terminal
involved.

Type: read-only (a verbal confirmation, not a system check).

Action: Locate and confirm access to the physical E-stop control(s) —
see [Emergency Stops](../safety/emergency-stops.md).

Expected observation: A trained team member can identify and reach the
E-stop without approaching the robot.

Verification: Confirmed verbally with a trained team member present.

Stop condition: Do not proceed without a confirmed, reachable E-stop.

Recovery: Locate the E-stop, or postpone the session.

## Expected observations

A clear operating area, two charged devices, and one confirmed,
reachable E-stop — nothing here yet depends on any software being
running.

## Verification

Every step in this procedure is a direct visual or verbal check; none
depends on the ROS 2 stack being up yet (that starts in [Power-On
Procedure](power-on.md)).

## Stop conditions

Do not proceed to [Power-On Procedure](power-on.md) unless all three
steps above completed without a stop condition being hit.

## Recovery

If battery status cannot be confirmed before the driver is running,
rely on each device's own hardware indicator rather than proceeding on
an assumption. There is no software-level recovery for this page — every
recovery here is physical (clear the area, charge a device, locate the
E-stop).

## Final state

The area is clear, batteries are checked, and the E-stop is confirmed
reachable — ready to proceed to [Power-On
Procedure](power-on.md).

## Related components

[Power-On Procedure](power-on.md), [Safety and Prerequisites](../safety/index.md).
