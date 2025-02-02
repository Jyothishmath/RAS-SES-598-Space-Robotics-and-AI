# Inverted Pendulum Optimal Control

This ROS2 package implements an LQR controller for an inverted pendulum (cart-pole) system with earthquake disturbance simulation and visualization.

## Overview

The package includes:
- Cart-pole system simulation in Gazebo
- LQR (Linear Quadratic Regulator) controller
- Earthquake force disturbance generator
- Force visualization in RViz
- State monitoring and republishing

## Prerequisites

- ROS2 Humble
- Gazebo Garden
- RViz2
- ros_gz_bridge

## Installation

1. Clone this package into your ROS2 workspace's `src` directory:
```bash
cd ~/your_ros2_workspace/src
git clone <repository_url>
```

2. Build the package:
```bash
cd ~/your_ros2_workspace
colcon build --packages-select inverted_pendulum_optimal_control
```

3. Source the workspace:
```bash
source install/setup.bash
```

## Usage

There are two ways to run the simulation:

### 1. Full Visualization (Gazebo GUI + RViz)
This launches both Gazebo GUI and RViz in separate windows:
```bash
ros2 launch inverted_pendulum_optimal_control inverted_pendulum.launch.py
```

### 2. RViz-only Visualization (Recommended)
This runs Gazebo in headless mode and shows visualization in RViz only:
```bash
ros2 launch inverted_pendulum_optimal_control inverted_pendulum_rviz.launch.py
```

The RViz visualization includes:
- Full cart-pole system visualization
- Real-time force vector display
- TF tree visualization
- Joint state monitoring

## Components

- **LQR Controller**: Stabilizes the inverted pendulum
- **Earthquake Force Generator**: Simulates disturbance forces
- **Force Visualizer**: Shows applied forces in RViz
- **State Republisher**: Ensures proper state updates for visualization

## Parameters

### Earthquake Force Generator
- `base_amplitude`: Base force amplitude in Newtons (default: 5.0)
- `frequency_range`: Frequency range in Hz (default: [0.5, 2.0])
- `update_rate`: Update rate in Hz (default: 50.0)

## Topics

### Published Topics
- `/model/inverted_pendulum/joint/cart_to_base/cmd_force`: Control force
- `/force_marker`: Force visualization marker
- `/joint_states`: Robot joint states

### Subscribed Topics
- `/world/empty/model/inverted_pendulum/joint_state`: Gazebo joint states
- `/robot_description`: URDF model description

## License

Apache License 2.0 