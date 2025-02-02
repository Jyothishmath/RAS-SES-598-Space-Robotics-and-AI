# Inverted Pendulum Robust Control Assignment

## Overview
This assignment challenges students to implement and tune a robust controller for an inverted pendulum system subject to earthquake disturbances. The goal is to maintain the pendulum's stability while keeping the cart within its physical constraints under external perturbations.

## System Description

### Physical Setup
- Inverted pendulum mounted on a cart
- Cart traversal range: ±2.5m (total range: 5m)
- Base platform: 5m long, matching cart width
- Pole length: 1m
- Cart mass: 1.0 kg
- Pole mass: 1.0 kg

### Disturbance Generator
The system includes an earthquake force generator that introduces external disturbances:
- Generates continuous, earthquake-like forces using superposition of sine waves
- Base amplitude: 5.0N (configurable)
- Frequency range: 0.5-2.0 Hz (configurable)
- Random variations in amplitude and phase
- Additional Gaussian noise

## Assignment Objectives

### Primary Goals
1. Implement and tune a controller to:
   - Maintain the pendulum in an upright position
   - Keep the cart within its ±2.5m physical limits
   - Maximize the duration of stable operation under disturbances
2. Understand and apply robust control principles
3. Analyze the trade-offs between performance and robustness

### Learning Outcomes
- Understanding of robust control in the presence of external disturbances
- Experience with LQR tuning for competing objectives
- Practical implementation of control systems in ROS2 and Gazebo
- Analysis of system stability under perturbations

## Implementation

### Controller
The base implementation provides an LQR controller (`lqr_controller.py`) that students will tune. Key aspects:
- State feedback control
- Adjustable gains for different state variables
- Balance between pendulum stability and cart position constraints

### Earthquake Disturbance
The earthquake generator (`earthquake_force_generator.py`) provides realistic disturbances:
- Configurable through ROS2 parameters
- Continuous perturbation forces
- Variable frequency and amplitude components

## Getting Started

### Prerequisites
- ROS2 Humble
- Gazebo Garden
- Python 3.8+
- Required Python packages: numpy, control

### Installation
```bash
# Clone the repository
cd ~/ros2_ws/src
git clone <repository_url>

# Build the package
cd ~/ros2_ws
colcon build --packages-select inverted_pendulum_optimal_control
```

### Running the Simulation
```bash
# Source ROS2
source ~/ros2_ws/install/setup.bash

# Launch the simulation with controller and earthquake generator
ros2 launch inverted_pendulum_optimal_control inverted_pendulum.launch.py
```

### Tuning Parameters
1. Controller parameters can be adjusted in the LQR implementation
2. Earthquake disturbance parameters can be modified in the launch file:
   ```python
   parameters=[{
       'base_amplitude': 5.0,  # Force amplitude (N)
       'frequency_range': [0.5, 2.0],  # Frequency range (Hz)
       'update_rate': 50.0  # Update rate (Hz)
   }]
   ```

## Evaluation Criteria
1. Duration of stable operation under disturbances
2. Maximum cart displacement from center
3. Average pendulum angle deviation from vertical
4. Quality of controller implementation and tuning strategy

## Why This is Robust Control
This assignment exemplifies robust control because:
1. The controller must maintain stability despite unknown, time-varying disturbances
2. The system has physical constraints (cart position limits) that must be respected
3. Multiple competing objectives must be balanced:
   - Pendulum stabilization
   - Position constraint satisfaction
   - Disturbance rejection
4. The controller must work across a range of disturbance frequencies and amplitudes

## Tips for Success
1. Start with conservative controller gains
2. Analyze the system's natural frequencies
3. Consider the trade-off between tight position control and disturbance rejection
4. Test the controller with different disturbance parameters
5. Document your tuning strategy and results

## Submission Requirements
1. Implemented controller code
2. Technical report including:
   - Controller design approach
   - Tuning methodology
   - Performance analysis
   - Discussion of challenges and solutions
3. Video demonstration of the system under disturbance

## References
- [LQR Control Theory]
- [Inverted Pendulum Dynamics]
- [Robust Control Principles]
- [ROS2 Control Documentation]

## License
This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/) 