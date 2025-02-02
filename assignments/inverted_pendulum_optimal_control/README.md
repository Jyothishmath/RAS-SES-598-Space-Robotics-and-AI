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

### Branch Information
- `main`: Primary development branch with:
  * Basic LQR controller (requires tuning)
  * Strong earthquake disturbances
  * Force visualization (control and disturbance forces)
  * Side-view RViz configuration
  * Intentionally challenging default parameters

- `baseline`: Backup branch with verified working implementation
  * Use this as reference if needed
  * Contains stable parameters and tuned controller
  * Maintained by instructors

For extra credit implementations, create new branches from `main`.

### Default Parameters
The main branch comes with intentionally challenging controller parameters while maintaining realistic disturbance conditions:

1. Earthquake Disturbances (Realistic Setting):
   ```python
   parameters=[{
       'base_amplitude': 15.0,    # Strong force amplitude (N)
       'frequency_range': [0.5, 4.0],  # Wide frequency range (Hz)
       'update_rate': 50.0  # Update rate (Hz)
   }]
   ```
   These parameters create significant disturbances that reflect real-world conditions:
   - Forces up to 15N (15x the cart mass)
   - Wide frequency spectrum (0.5-4.0 Hz)
   - Random variations in amplitude and phase
   - Continuous perturbation

2. LQR Controller (Requires Tuning):
   Current settings in main branch:
   ```python
   self.Q = np.diag([0.1, 0.1, 1.0, 1.0])  # State cost matrix
   self.R = np.array([[1.0]])               # Control cost
   ```
   These values are intentionally conservative and need tuning:
   - Low weights on cart position (0.1) → Large position deviations
   - Low weights on cart velocity (0.1) → Slow response
   - Moderate weights on pole angle (1.0) → Insufficient stabilization
   - High control cost (1.0) → Too conservative control action

### Tuning Requirements

Students must tune the LQR gains to achieve:

1. Primary Objectives:
   - Keep pole angle within ±15 degrees
   - Maintain cart position within ±2.0m
   - Achieve stable operation under earthquake forces
   - Minimize control effort while meeting above constraints

2. Tuning Strategy:
   - Adjust Q matrix weights to balance:
     * Cart position control (Q[0,0])
     * Cart velocity damping (Q[1,1])
     * Pole angle stabilization (Q[2,2])
     * Pole angular velocity damping (Q[3,3])
   - Tune R value to balance:
     * Control effort (higher R = less aggressive)
     * Response speed (lower R = faster response)
     * Disturbance rejection (lower R = better rejection)

3. Performance Metrics:
   - Maximum pole angle deviation
   - RMS cart position error
   - Peak control force used
   - Time to recover from disturbances

4. Physical Constraints:
   - Cart position limit: ±2.5m
   - Cart motor force: Limited by controller
   - Pole angle: Unconstrained (but should be minimized)
   - Control rate: 50Hz

### Tips for Tuning
1. Start with baseline branch parameters to understand good performance
2. Methodically adjust one weight at a time
3. Consider the following sequence:
   - First stabilize pole angle (Q[2,2] and Q[3,3])
   - Then improve cart position control (Q[0,0] and Q[1,1])
   - Finally, balance control effort (R)
4. Test with different initial conditions:
   - Small pole angle disturbances
   - Large cart position offsets
   - Combined angle and position errors
5. Validate against earthquake disturbances:
   - Check steady-state behavior
   - Verify disturbance rejection
   - Ensure constraints are met

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
  * Force arrows showing both control and disturbance forces
  * TF frames for system state
- LQR controller
- Earthquake force generator
- Force visualizer

### Visualization Details
The RViz view shows a side perspective of the cart-pole system with force visualizations:

#### Force Arrows
Two types of forces are visualized:
1. Control Forces (at cart level):
   - Red arrows: Positive control force (pushing right)
   - Blue arrows: Negative control force (pushing left)

2. Earthquake Disturbances (slightly above cart):
   - Orange arrows: Positive disturbance force (pushing right)
   - Purple arrows: Negative disturbance force (pushing left)

The arrow length is proportional to the force magnitude.

#### RViz View Settings
- Side view perspective (looking along Y-axis)
- Clean interface with only 3D viewport visible
- Grid for reference
- Cart-pole system with:
  * Blue base platform (5m long)
  * Red cart
  * Blue pole

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

## Reinforcement Learning Implementation (Baseline Branch)

The baseline branch includes a complete RL implementation using Deep Q-Learning (DQN):

### Prerequisites
Additional requirements for RL:
```bash
pip install torch numpy
```

### RL Architecture
1. Neural Network:
   - Input: 4D state vector [x, x_dot, theta, theta_dot]
   - Hidden layers: 2 layers of 128 units with ReLU
   - Output: Q-values for 11 discretized force actions

2. Training Parameters:
   - Episodes: 1000
   - Max steps per episode: 1000
   - Batch size: 64
   - Learning rate: 0.001
   - Discount factor (gamma): 0.99
   - Epsilon decay: 0.995 (1.0 → 0.01)
   - Memory buffer size: 10000 transitions

3. Reward Structure:
   ```python
   # Rewards:
   - Staying upright: +cos(theta)  # +1 when vertical, decreasing as it falls
   - Position penalty: -|x|        # Penalize cart displacement
   - Control penalty: -0.1|force|  # Encourage smooth control
   - Living bonus: +0.1           # Encourage longer episodes
   - Failure: -100                # |theta| > 15° or |x| > 2.0m
   ```

### Running RL Training
```bash
# Source ROS2
source ~/ros2_ws/install/setup.bash

# Launch RL training
ros2 launch inverted_pendulum_optimal_control inverted_pendulum_rl.launch.py
```

### Training Metrics
The RL controller publishes metrics every second:
- Episode number
- Total steps
- Current exploration rate (epsilon)
- Episode reward
- Best reward achieved

### Monitoring Progress
1. Console Output:
   ```bash
   ros2 topic echo /rl_controller/metrics
   ```

2. Training Visualization:
   - RViz shows cart-pole system
   - Force arrows indicate control actions
   - Real-time performance monitoring

### Saving and Loading Models
- Models auto-save every 100 episodes
- Saved in `trained_models` directory
- Best model preserved based on reward

### Performance Comparison
The RL implementation can achieve:
- Stability in presence of strong disturbances
- Cart position maintained within ±1.0m
- Pole angle within ±10 degrees
- Smooth control actions 