# Sensors and Perception

## Overview

How Spot senses its environment, and how raw sensor data becomes
usable information — detected objects, markers, and calibrated camera
geometry.

## Purpose

Bring together the two topics a working perception pipeline needs:
what a sensor publishes and how it relates to the robot's frames
([Sensors and Coordinate Frames](../sensors-frames/index.md)), and what
is done with that data once published
([Perception](../perception/index.md)).

## System context

Sensor data flows from drivers into TF-aware consumers (RViz, mapping,
navigation) and into perception nodes (object detection, marker
detection) whose output in turn feeds navigation and manipulation. See
Data Flow under [System Architecture](../architecture/index.md) for
where this fits in the full Spot pipeline.

## Prerequisites

[ROS 2](../ros2/index.md) topics and messages; ROS 2 fundamentals are
covered under [Required Knowledge](../safety/required-knowledge.md).

## How it works

- **Sensors and Coordinate Frames** — cameras, LiDAR, IMU, and how TF2
  relates every sensor's data to the robot body and the world.
- **Perception** — camera calibration, OpenCV, fiducial markers
  (ArUco/AprilTag), object detection (including YOLO-based detection),
  and data labeling for training a custom detector.

## Verification

Each subpage carries its own verification badges; nothing on this hub
page itself makes a hardware claim.

## Related components

[Navigation and Mapping](../navigation-and-mapping/index.md) consumes
LiDAR/point-cloud data placed in TF frames here. [Manipulator and
MoveIt](../manipulation/index.md) consumes detected objects and marker
poses for pick targets.

## Further learning

```{toctree}
:hidden:
:maxdepth: 2

../sensors-frames/index
../perception/index
```

- [Sensors and Coordinate Frames](../sensors-frames/index.md)
- [Perception](../perception/index.md)
