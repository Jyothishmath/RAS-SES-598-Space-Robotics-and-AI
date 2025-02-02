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

### Core Requirements
1. Implement and tune an LQR controller to:
   - Maintain the pendulum in an upright position
   - Keep the cart within its ±2.5m physical limits
   - Achieve stable operation under earthquake disturbances
2. Document your LQR tuning approach:
   - Selection and justification of Q and R matrices
   - Analysis of performance trade-offs
   - Experimental results and observations
3. Analyze system performance:
   - Duration of stable operation
   - Maximum cart displacement
   - Pendulum angle deviation
   - Control effort analysis

### Learning Outcomes
- Understanding of LQR control design and tuning
- Experience with competing control objectives
- Practical implementation in ROS2 and Gazebo
- Analysis of system behavior under disturbances

### Extra Credit Options
Students can explore more advanced approaches for extra credit:

1. Advanced Control Strategies (up to 15 points):
   - Implement gain scheduling based on disturbance intensity
   - Design H∞ control for robust performance
   - Develop Model Predictive Control (MPC) with constraint handling
   - Create a hybrid control approach combining multiple strategies

2. Learning and Adaptation (up to 10 points):
   - Implement online parameter adaptation
   - Add disturbance learning and prediction
   - Develop adaptive gain tuning

3. Advanced Analysis (up to 5 points):
   - Frequency domain analysis of disturbance rejection
   - Robustness margin calculations
   - Comparative analysis of different control strategies

## Implementation

### Core Controller Implementation
The base implementation provides an LQR controller (`lqr_controller.py`) that students will tune. Focus areas:
- State feedback gain selection
- Q and R matrix tuning
- Balance between competing objectives:
  * Pendulum stabilization
  * Cart position constraints
  * Control effort minimization

### Extra Credit Implementation Guidelines
If pursuing extra credit options:
1. Maintain the base LQR implementation as a benchmark
2. Create separate controller variants for each approach
3. Provide comparative analysis with the base LQR solution
4. Document additional theoretical background
5. Include failure cases and limitations in analysis

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

# Launch the simulation with visualization
ros2 launch inverted_pendulum_optimal_control inverted_pendulum_rviz.launch.py
```

This will start:
- Gazebo simulation in headless mode
- RViz visualization with:
  * Cart-pole system visualization
  * Force arrows showing control and disturbance forces
  * TF frames for system state
- LQR controller
- Earthquake force generator
- Force visualizer

The visualization includes:
- Red arrows for positive forces
- Blue arrows for negative forces
- Real-time cart position and pole angle updates
- Grid for reference

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
### Core Assignment (100 points)
1. LQR Implementation and Tuning (40 points)
   - Correct implementation of LQR control
   - Well-justified Q and R matrix selection
   - Proper gain calculation and application

2. Performance Metrics (30 points)
   - Duration of stable operation
   - Maximum cart displacement
   - Average pendulum angle deviation
   - Control effort efficiency

3. Documentation and Analysis (30 points)
   - Clear explanation of tuning strategy
   - Quality of performance analysis
   - Thoroughness of implementation details
   - Professional presentation of results

### Extra Credit (up to 30 points)
- Advanced Control Implementation (15 points)
- Learning/Adaptation Features (10 points)
- Advanced Analysis (5 points)

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
1. Focus first on achieving stable LQR control
2. Start with conservative Q and R matrices
3. Systematically adjust weights based on performance
4. Document all tuning decisions and their effects
5. Only pursue extra credit after achieving solid base performance
6. Test thoroughly under various disturbance conditions

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