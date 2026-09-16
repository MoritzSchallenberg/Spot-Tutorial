# Computers and Network

## Overview

Which conceptual roles exist in the system, what runs where, and how
they communicate — using role placeholders throughout, since the local
sources are a single development machine's backup, not a documented
multi-host production inventory (see `spot-source-audit.md`, internal).

## Purpose

Give an anonymized, accurate picture of the compute/network
architecture without publishing any real hostname, IP address, or
credential.

## System context

This page complements [Hardware Overview](hardware-overview.md) (what
the physical components are) with where the software that drives them
actually runs.

## Roles

```{list-table}
:header-rows: 1
:widths: 25 75

* - Role
  - What runs here (evidence)
* - Operator Station
  - `alert_dashboard_rqt` (operator dashboard), RViz, audio playback
    (`audio_play`, namespace `/operator`)
* - Robot Computer
  - `tmux-api-server.service`, `zenoh-router.service` (both persistent
    systemd services), the Spot driver stack (`spot_driver`,
    `frame_server`, `map_vision`), Octomap servers, the navigation
    stack (`bring_up_alert_nav`/`mbf_octo_nav`), `alert_exploration`,
    audio capture (namespace `/nuc`), MoveIt (`kinova_moveit`), and the
    software E-stop endpoint process (`spot_estop.py`)
* - Spot Base
  - Boston Dynamics' own onboard compute; reached only through the
    `bosdyn` SDK/gRPC connection inside `spot_driver` — not otherwise
    visible to this codebase
* - Manipulator Controller
  - The Kinova Gen3's own embedded controller, reached over TCP
    (`kortex_driver`'s `KortexMultiInterfaceHardware` plugin) via an
    IP referenced as `$GEN3_IP` in the runtime window commands
* - Sensors
  - RealSense, Livox Mid-360, Seek Thermal, and IFM O3P devices,
    connected to the Robot Computer via USB (per the udev rules that
    target them)
```

`Verified in configuration` for the role assignments (source:
`spot-code-audit.md` §"Runtime components", internal); no real
hostnames or IP addresses are reproduced here — use `<SPOT_IP>`,
`<COMPUTE_HOST>`, `<OPERATOR_HOST>`, and `<ROBOT_NETWORK>` as
placeholders for anything a real deployment needs to fill in.

## Diagram

:::{mermaid}
:alt: Role diagram showing the Operator Station connected to the Robot Computer, which connects to Spot Base, the Manipulator Controller, and Sensors.

graph LR
    OP["Operator Station<br/>(dashboard, RViz)"]
    RC["Robot Computer<br/>(spot_driver, nav stack,<br/>MoveIt, E-stop endpoint)"]
    SB["Spot Base<br/>(Boston Dynamics SDK/gRPC)"]
    MC["Manipulator Controller<br/>(Kinova Gen3, TCP)"]
    SE["Sensors<br/>(RealSense, Livox, Seek Thermal, O3P)"]

    OP -->|"ROS 2 / tmux API<br/>&lt;ROBOT_NETWORK&gt;"| RC
    RC -->|"bosdyn SDK/gRPC<br/>&lt;SPOT_IP&gt;"| SB
    RC -->|"Kortex TCP<br/>&lt;COMPUTE_HOST&gt; to arm"| MC
    SE -->|"USB"| RC
:::

## Communication middleware

Two middleware approaches are configured in the local sources, and the
evidence does not resolve which is actually live:

- **Zenoh** (`rmw_zenoh_cpp`) — run as a persistent systemd service
  (`zenoh-router.service`, `Restart=always`), listening on TCP port
  7447. This looks like the more "production" setup, being
  systemd-managed rather than ad hoc.
- **Fast-DDS discovery server** — started as one of the ad hoc runtime
  windows (`fastdds discovery --server-id 0`), with a corresponding
  Fast-DDS client XML profile in the configuration.

`Verified in configuration` for both existing; `Unverified` for which
is the actual live choice at any given time — see Software Components,
later in this section, and the open questions in `spot-code-audit.md`
(internal).

## What happens on connection loss

Not found in the current code — see [Recovery and
Troubleshooting](../operating/recovery-and-troubleshooting.md#communication-loss).

## Verification

`Verified in configuration` throughout this page; no real network
identifiers are published, consistent with `spot-security-audit.md`.

## Related components

[Hardware Overview](hardware-overview.md), Software Components
(later in this section), [Safety and Prerequisites](../safety/index.md).
