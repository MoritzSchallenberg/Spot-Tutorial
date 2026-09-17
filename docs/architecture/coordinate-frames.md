# Coordinate Frames

## Overview

The TF frame tree the system maintains, including two conventions that
coexist without being reconciled in the current code.

## Purpose

Give an accurate frame tree grounded in the actual xacro/URDF and
static-transform-publisher code, including the inconsistencies, rather
than a clean idealized tree that doesn't match the running system.

## System context

Builds on [Sensors and Perception](../sensors-and-perception/index.md)'s
general TF2 explanation with Spot-specific frame names.

## The frame tree

```{list-table}
:header-rows: 1
:widths: 20 25 20 35

* - Parent
  - Child
  - Static/Dynamic
  - Source
* - `body`
  - `base_link`, `front_rail`, `rear_rail`
  - Static
  - `spot_description`
* - `body`
  - 4× hip/upper_leg/lower_leg chains (12 joints)
  - Dynamic
  - `spot_description` + `spot_driver` dynamic broadcaster
* - `body`
  - `gen3_base_link` (Kinova root)
  - Static (unconditional include)
  - `spot_description`
* - `gen3_base_link`
  - ... `end_effector_link` (6 joints)
  - Dynamic
  - `spot_gen3_moveit` / `kortex_driver`
* - `end_effector_link`
  - `robotiq_base_link` → 10 finger links
  - Static + `finger_joint` dynamic
  - `spot_description` / `kortex_driver`
* - `body`
  - `livox` / `/livox_frame`
  - Static
  - `spot_description`, republished by `spot_driver_plus`
* - `body`
  - `ifm_front/back_plate`, `ifm_right/...`, `ifm_left/...`
  - Static
  - `spot_driver_plus`
* - `body`
  - `world`
  - Static
  - `spot_driver_plus` — note: `body` is the parent, `world` the
    child, the reverse of the usual convention
* - (SDK)
  - `vision` (odometry root)
  - Dynamic
  - `spot_driver`; `preferred_odom_frame: "vision"` in the deployed
    config
* - `graph_nav_map`
  - `body`
  - Static (published at localization)
  - `spot_driver`
* - `map`
  - `odom`
  - Defined, **inactive**
  - `bring_up_alert_nav` — commented out of the current launch file
* - `map`
  - `feet_center`
  - n/a (navigation convention)
  - `bring_up_alert_nav`'s `mbf_alert_nav.yaml` — differs from
    `alert_exploration`'s own `ROBOT_BASE_FRAME = 'body'` constant,
    not reconciled in the code
```

`Verified in code` throughout — see `spot-code-audit.md` (internal)
for exact file citations.

:::{admonition} Two coexisting robot-frame conventions
:class: warning

`bring_up_alert_nav`'s navigation config uses `feet_center` as the
robot frame; `alert_exploration`'s own Python constant uses `body`.
Both are real, current code — this is not a typo in one place, but two
different packages using different conventions. If writing a new node
that needs "the robot's frame," check which of the two conventions the
package you are integrating with actually expects.
:::

There is also a naming collision: the manipulator's local frame
constants (`auto_dex_nodes/go_to_pose.py`) define a `base_link` frame
for the arm, distinct from Spot's own `base_link` — same name, two
different frames, in different parts of the system.

## Diagram: simplified TF tree

:::{mermaid}
:alt: Simplified tree diagram of the coordinate frames, rooted at body, branching to legs, the Kinova arm chain ending at the gripper, the LiDAR and camera frames, and separately showing the map to feet_center navigation convention alongside the odometry root frame vision.

graph TD
    body --> base_link
    body --> legs["4x leg chains<br/>(12 joints)"]
    body --> gen3_base_link
    gen3_base_link --> eef["... end_effector_link<br/>(6 joints)"]
    eef --> gripper["robotiq_base_link<br/>+ finger links"]
    body --> livox
    body --> ifm["ifm_front/right/left<br/>_back_plate"]
    body --> world
    vision["vision<br/>(odometry root, SDK)"] -.-> body
    map --> feet_center["feet_center<br/>(nav robot frame,<br/>inconsistent with 'body')"]
    map -.->|"defined,<br/>currently inactive"| odom
:::

**Legend:** solid arrows are static or dynamic TF publications actually
active in the current code; dashed arrows are relationships that exist
in the code but are not a standard, always-active part of the tree —
either a reference frame used only by the SDK's odometry output
(`vision`), or a transform that is defined but currently commented out
of its launch file (`map`→`odom`).

## Verification

`Verified in code` for every frame and relationship shown; this page
does not assert a single "correct" convention where the code itself
carries two.

## Related components

[Software Components](software-components.md), [Data Flow](data-flow.md).
