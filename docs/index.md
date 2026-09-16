# ALeRT Spot Tutorial

A technical reference and tutorial site for the **ALeRT** (Aachen Legged
Rescue Team) Spot system: a Boston Dynamics Spot quadruped fitted with a
Kinova Gen3 manipulator and Robotiq gripper, operated by the RoboCup
Rescue League team at the **MASKOR Institute, FH Aachen**. It documents
the real system — its safety procedures, its operating procedures, and
its hardware and software architecture — grounded in the team's own
code and configuration.

:::{admonition} Safety notice
:class: danger

Spot is a heavy, fast-moving legged robot with an attached manipulator
arm. Read [Safety and Prerequisites](safety/index.md) in full before
approaching or operating the physical robot. Do not operate the
physical system without supervision from someone authorized to use it.
:::

## Three ways into this site

::::{grid} 1 1 3 3
:gutter: 3

:::{grid-item-card} Learn about ALeRT and Spot
:link: about/index
:link-type: doc

The team, the RoboCup Rescue League, and how the Spot platform came to
be ALeRT's system.
:::

:::{grid-item-card} Operate Spot safely
:link: safety/index
:link-type: doc

What to know before touching the robot, and the step-by-step procedures
for running a session.
:::

:::{grid-item-card} Understand the system
:link: architecture/index
:link-type: doc

The hardware, computers, software, and ROS 2 interfaces that make up
the Spot system.
:::

::::

## What this site covers

- [About ALeRT and Spot](about/index.md) — team and competition
  background.
- [Safety and Prerequisites](safety/index.md) — stop states, E-stops,
  operating area, required knowledge.
- [Operating Spot](operating/index.md) — power-on through shutdown,
  driving, manipulator control, recovery.
- [System Architecture](architecture/index.md) — hardware, network,
  software, startup order, ROS 2 interfaces, frames, data flow.
- [Sensors and Perception](sensors-and-perception/index.md)
- [Navigation and Mapping](navigation-and-mapping/index.md)
- [Manipulator and MoveIt](manipulation/index.md)
- [Autonomous Behaviors](autonomous-behaviors/index.md)
- [Deployment and Configuration](deployment-and-configuration/index.md)
- [Diagnostics and Testing](integration-testing/index.md)
- [Reference](reference/index.md)

## How to read this site

Every topic is marked with a difficulty level:

{{ foundation }} foundational &nbsp;
{{ intermediate }} intermediate &nbsp;
{{ advanced }} advanced &nbsp;
{{ research }} research / experimental

and, where a claim is about ALeRT's own systems specifically, a
verification status:

{{ documented }} confirmed via a repository or written documentation
&nbsp;
{{ simulation }} runs in Webots &nbsp;
{{ hardwareverified }} actually checked on running hardware &nbsp;
{{ unverified }} plausible, not checked &nbsp;
{{ historical }} no longer current, kept for context

Safety and Operating pages use a separate, plain-text verification
label per procedure step (`Verified in code`, `Verified in
configuration`, `Historical procedure`, `Unverified on hardware`) —
see Safety Principles under [Safety and Prerequisites](safety/index.md).

This site runs on one fixed toolchain — Ubuntu 22.04 LTS and ROS 2
Humble — unless a specific ALeRT repository is documented to need
something else. See [Supported environment](reference/compatibility.md)
for the exact versions and how to check them on your own machine.

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
