# Inverted Pendulum Optimal Control Assignment

## Overview
This assignment challenges students to tune and analyze an LQR controller for an inverted pendulum system subject to earthquake disturbances. The goal is to maintain the pendulum's stability while keeping the cart within its physical constraints under external perturbations.

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
- Base amplitude: 15.0N (default setting)
- Frequency range: 0.5-4.0 Hz (default setting)
- Random variations in amplitude and phase
- Additional Gaussian noise

## Assignment Objectives

### Core Requirements
1. Analyze and tune the provided LQR controller to:
   - Maintain the pendulum in an upright position
   - Keep the cart within its ±2.5m physical limits
   - Achieve stable operation under earthquake disturbances
2. Document your LQR tuning approach:
   - Analysis of the existing Q and R matrices
   - Justification for any tuning changes made
   - Analysis of performance trade-offs
   - Experimental results and observations
3. Analyze system performance:
   - Duration of stable operation
   - Maximum cart displacement
   - Pendulum angle deviation
   - Control effort analysis

### Learning Outcomes
- Understanding of LQR control parameters and their effects
- Experience with competing control objectives
- Analysis of system behavior under disturbances
- Practical experience with ROS2 and Gazebo simulation

### Extra Credit Options
Students can implement reinforcement learning for extra credit (up to 30 points):

1. Reinforcement Learning Implementation:
   - Implement a basic DQN (Deep Q-Network) controller
   - Train the agent to stabilize the pendulum
   - Compare performance with the LQR controller
   - Document training process and results
   - Create training progress visualizations
   - Analyze and compare performance with LQR

## Implementation

### Controller Description
The package includes a complete LQR controller implementation (`lqr_controller.py`) with the following features:
- State feedback control
- Configurable Q and R matrices
- Real-time force command generation
- State estimation and processing

Current default parameters:
```python
# State cost matrix Q (default values)
Q = np.diag([1.0, 1.0, 10.0, 10.0])  # [x, x_dot, theta, theta_dot]

# Control cost R (default value)
R = np.array([[0.1]])  # Control effort cost
```

### Earthquake Disturbance
The earthquake generator (`earthquake_force_generator.py`) provides realistic disturbances:
- Configurable through ROS2 parameters
- Default settings:
  ```python
  parameters=[{
      'base_amplitude': 15.0,    # Strong force amplitude (N)
      'frequency_range': [0.5, 4.0],  # Wide frequency range (Hz)
      'update_rate': 50.0  # Update rate (Hz)
  }]
  ```

## Getting Started

### Prerequisites
- ROS2 Humble
- Gazebo Garden
- Python 3.8+
- Required Python packages: numpy, scipy

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

# Launch the simulation with visualization
ros2 launch inverted_pendulum_optimal_control inverted_pendulum_rviz.launch.py
```

This will start:
- Gazebo simulation (headless mode)
- RViz visualization showing:
  * Cart-pole system
  * Force arrows (control and disturbance forces)
  * TF frames for system state
- LQR controller
- Earthquake force generator
- Force visualizer

### Visualization Features
The RViz view provides a side perspective of the cart-pole system with:

#### Force Arrows
Two types of forces are visualized:
1. Control Forces (at cart level):
   - Red arrows: Positive control force (right)
   - Blue arrows: Negative control force (left)

2. Earthquake Disturbances (above cart):
   - Orange arrows: Positive disturbance (right)
   - Purple arrows: Negative disturbance (left)

Arrow lengths are proportional to force magnitudes.

## Analysis Requirements

### Performance Metrics
Students should analyze:
1. Stability Metrics:
   - Maximum pole angle deviation
   - RMS cart position error
   - Peak control force used
   - Recovery time after disturbances

2. System Constraints:
   - Cart position limit: ±2.5m
   - Control rate: 50Hz
   - Pole angle stability
   - Control effort efficiency

### Analysis Guidelines
1. Baseline Performance:
   - Document system behavior with default parameters
   - Identify key performance bottlenecks
   - Analyze disturbance effects

2. Parameter Effects:
   - Analyze how Q matrix weights affect different states
   - Study R value's impact on control aggressiveness
   - Document trade-offs between objectives

3. Disturbance Response:
   - Characterize system response to different disturbance frequencies
   - Analyze recovery behavior
   - Study control effort distribution

## Evaluation Criteria
### Core Assignment (100 points)
1. Analysis Quality (40 points)
   - Depth of parameter analysis
   - Quality of performance metrics
   - Understanding of system behavior

2. Performance Results (30 points)
   - Stability under disturbances
   - Constraint satisfaction
   - Control efficiency

3. Documentation (30 points)
   - Clear analysis presentation
   - Quality of data and plots
   - Thoroughness of discussion

### Extra Credit (up to 30 points)
- Reinforcement Learning Implementation (30 points)

## Tips for Success
1. Start with understanding the existing controller behavior
2. Document baseline performance thoroughly
3. Make systematic parameter adjustments
4. Keep detailed records of all tests
5. Focus on understanding trade-offs
6. Use visualizations effectively

## Submission Requirements
1. Technical report including:
   - Analysis of controller behavior
   - Performance data and plots
   - Discussion of findings
2. Video demonstration of system performance
3. Any additional analysis tools or visualizations created

## License
This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/) 