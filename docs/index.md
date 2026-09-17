# ALeRT Spot Tutorial

The technical reference for **ALeRT**'s Spot system — a Boston Dynamics
Spot quadruped fitted with a Kinova Gen3 manipulator and Robotiq
gripper, operated by the RoboCup Rescue League team at the **MASKOR
Institute, FH Aachen** — grounded in the team's own code and
configuration.

:::{admonition} Safety notice
:class: danger

Spot is a heavy, fast-moving legged robot with an attached manipulator
arm. Read [Safety and Prerequisites](safety/index.md) in full before
approaching the physical robot, and never move the real system without
supervision from someone authorized to operate it.
:::

## What do you want to do?

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item}
### I want to operate Spot

- [Safety Principles](safety/safety-principles.md)
- [Operator Checklist](safety/operator-checklist.md)
- [System Preparation](operating/system-preparation.md)
- [Power-On Procedure](operating/power-on.md)
- [Driving Spot](operating/driving-spot.md)
- [Safe Shutdown](operating/safe-shutdown.md)
:::

:::{grid-item}
### I want to understand the system

- [Hardware Overview](architecture/hardware-overview.md)
- [Computers and Network](architecture/computers-and-network.md)
- [Software Components](architecture/software-components.md)
- [Startup and Launch Sequence](architecture/startup-and-launch-sequence.md)
- [ROS 2 Interfaces](architecture/ros2-interfaces.md)
- [Coordinate Frames](architecture/coordinate-frames.md)
- [Data Flow](architecture/data-flow.md)
:::

:::{grid-item}
### I want to develop for Spot

- [ROS 2](ros2/index.md)
- [Sensors and Perception](sensors-and-perception/index.md)
- [Navigation and Mapping](navigation-and-mapping/index.md)
- [Manipulator and MoveIt](manipulation/index.md)
- [Autonomous Behaviors](autonomous-behaviors/index.md)
- [Diagnostics and Testing](integration-testing/index.md)
:::

::::

Not sure where to start, or want a guided order through one of these
rather than a flat list? See [**Start Here**](start-here.md) for five
concrete learning paths, each with its prerequisites, whether it needs
real hardware, and what you should be able to do by the end of it.

## About this site

**Covers:** the real ALeRT Spot system — safety, operation, and
architecture — not a general robotics course.
**Written for:** anyone preparing to operate the physical robot, or
anyone who wants to understand how it is built.
**Software:** Ubuntu 22.04 LTS, ROS 2 Humble, unless a specific ALeRT
repository is documented to need something else — see [Supported
environment](reference/compatibility.md).
**Historical content:** the [About ALeRT and Spot](about/index.md)
section and some operating-page screenshots document the team's past,
not the current system — every such page or image says so explicitly.
**Verification:** most claims on this site are `Verified in code` or
`Verified in configuration`, not `Verified on hardware` — see [Safety
Principles](safety/safety-principles.md#verification-levels) for what
each label means and why. [Reference: System
Status](reference/system-status.md) gives the same picture at a glance,
subsystem by subsystem.

## How to read this site

Background/development topics carry a difficulty level ({{ foundation }}
{{ intermediate }} {{ advanced }} {{ research }}) and, where a claim is
about ALeRT's own systems, a verification status ({{ documented }}
{{ simulation }} {{ hardwareverified }} {{ unverified }} {{ historical }}).
Safety and Operating pages use the separate plain-text labels described
above instead. See [Supported environment](reference/compatibility.md)
for what "documented" assumes about your own setup.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Start Here

start-here
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: About ALeRT and Spot

about/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Safety and Prerequisites

safety/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Operating Spot

operating/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: System Architecture

architecture/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Sensors and Perception

sensors-and-perception/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Navigation and Mapping

navigation-and-mapping/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Manipulator and MoveIt

manipulation/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Autonomous Behaviors

autonomous-behaviors/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Deployment and Configuration

deployment-and-configuration/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Diagnostics and Testing

integration-testing/index
```

```{toctree}
:hidden:
:maxdepth: 2
:caption: Reference

reference/index
```
