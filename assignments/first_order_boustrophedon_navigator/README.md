# Boustrophedon Pattern with PD Controller

# SETTING UP THE PROJECT - 

Step 1: Fork and Clone the Repository

Since the assignment is hosted in a GitHub repository, started by forking it:

    DREAMS-lab/RAS-SES-598-Space-Robotics-and-AI.
    Click Fork (top-right) to create a personal copy of the repository.
    Cloned the forked repository:
    git clone https://github.com/YOUR_USERNAME/RAS-SES-598-Space-Robotics-and-AI.git


Step 2: Setting up the ROS2 Environment

Since I already installed ROS2(Humble) proceeding to create a symlink -

    cd ~/ros2_ws/src
    ln -s ~/RAS-SES-598-Space-Robotics-and-AI/assignments/first_order_boustrophedon_navigator 


Step 3: Building the package-
         
    colcon build --packages-select first_order_boustrophedon_navigator
    
    source install/setup.bash

This documentation provides an overview of the tuning process, performance analysis, and lessons learned.

## Tuning Process

### Initial Parameters
The initial parameters were:
- `Kp_linear = 1.0`
- `Kd_linear = 0.0`
- `Kp_angular = 2.0`
- `Kd_angular = 0.0`

These values caused:
- Significant overshooting while following straight lines.
- Unstable turning behavior at corners.

## Final PD Controller Parameters

The following parameters were used after tuning:
- **Kp_linear:** 1.2  
  - Justification: Improves straight-line tracking performance without overshooting.
- **Kd_linear:** 0.03  
  - Justification: Reduces oscillations in velocity for smoother motion.
- **Kp_angular:** 7.0  
  - Justification: Ensures sharper turns and precise cornering.
- **Kd_angular:** 0.03  
  - Justification: Damps angular overshooting during turns.
- **Spacing:** 1.2  
  - Justification: Achieves even coverage while balancing efficiency.


### Final Tuned Parameters
The final parameters were:
- `Kp_linear = 1.2`
- `Kd_linear = 0.03`
- `Kp_angular = 7.0`
- `Kd_angular = 0.03`
- `spacing = 1.2`

This project aims to implement a boustrophedon motion pattern using a TurtleBot in ROS2. The primary objective was to tune a PD controller to minimize the cross-track error while ensuring smooth motion and efficient area coverage. The final tuned parameters allowed the robot to achieve:
- **Average Cross-Track Error:** 0.112 units
- **Maximum Cross-Track Error:** 0.297 units
  ![Screenshot from 2025-01-27 20-19-32](https://github.com/user-attachments/assets/fc1fc4f4-b904-4500-8b9b-ed65c76dc7b0)

# Plotting Values -
Graphs for -

    /turtle1/pose/x
    /turtle1/pose/y
    /turtle1/cmd_vel/linear/x
    /turtle1/cmd_vel/angular/z
    /cross_track_error

### Trajectory Visualization
The TurtleSim trajectory shows a clean boustrophedon pattern with even line spacing and efficient coverage.
![Screenshot from 2025-01-27 20-19-15](https://github.com/user-attachments/assets/c8baddd1-12cd-4a0b-8ca4-f5317ec2c832)

### Velocity Profiles
Velocity profiles illustrate how the TurtleBot's linear and angular velocities change over time during the simulation. These profiles are crucial for understanding the robot's movement dynamics, such as how smoothly it accelerates, maintains speed, and decelerates.
![Screenshot from 2025-01-27 20-20-05](https://github.com/user-attachments/assets/6ca93661-a728-4216-b8ff-4e12aa910da7)
![Screenshot from 2025-01-27 20-20-18](https://github.com/user-attachments/assets/e61bf146-80fb-42c4-997b-498cb9474801)

### Cross Track Error over time
Cross-track error (CTE) measures the lateral deviation of the TurtleBot from the desired trajectory. It is a critical metric to evaluate how well the robot follows the planned path.

In this project, minimizing cross-track error was a primary objective. A low average CTE indicates the robot stayed close to the desired trajectory, while a low maximum CTE ensures that deviations were controlled even in challenging turns or transitions.
![Screenshot from 2025-01-27 20-35-39](https://github.com/user-attachments/assets/580a2b16-04b6-4e16-8bea-cb70d87afb57)

### TurtleBot1 Pose (X and Y)

The TurtleBot1 pose represents the robot's position in the simulation environment. It includes two key coordinates:

    X: The horizontal position of the TurtleBot along the X-axis.
    Y: The vertical position of the TurtleBot along the Y-axis.
 ![Screenshot from 2025-01-27 20-41-37](https://github.com/user-attachments/assets/76fad584-0570-490a-a1e2-743f20d399d3)

### Challenges and Solutions

Challenge 1: Overshooting in Straight Lines

    Problem: Initially, the robot was overshooting the desired trajectory, especially in straight-line segments. The robot would move too fast and then oscillate back and forth trying to correct itself.
    Solution:
        Reduced Kp_linear to avoid excessive acceleration.
        Introduced Kd_linear to dampen oscillations and create smoother corrections.
        The final tuning helped the robot stay closer to the desired trajectory without excessive corrections.

Challenge 2: Poor Cornering Performance

    Problem: The robot struggled to make sharp turns and often deviated significantly at waypoints.
    Solution:
        Increased Kp_angular to make the robot turn more aggressively at waypoints.
        Adjusted Kd_angular to prevent excessive angular corrections.
        These adjustments improved cornering behavior, reducing drift and ensuring the robot transitioned smoothly between rows.

Challenge 3: Uneven Coverage of the Target Area

    Problem: The spacing between adjacent rows in the boustrophedon pattern was inconsistent, leading to inefficient coverage.
    Solution:
        Adjusted the spacing parameter to optimize coverage.
        Tuned Kp_linear to control speed and ensure the robot reached waypoints without excessive deviation.
        This led to a more uniform pattern with even spacing between rows.

### Step-by-Step Parameter Adjustments

    Initial Values (Kp_linear = 1.0, Kd_linear = 0.0, Kp_angular = 2.0, Kd_angular = 0.0)
        Observation:
            The robot oscillated significantly in straight lines.
            Cornering was slow, causing the robot to take wide turns.
        Reason for Change:
            Introduced Kd_linear to reduce oscillations and overshooting.
            Increased Kp_angular to make turns sharper.

    Second Iteration (Kp_linear = 1.2, Kd_linear = 0.03, Kp_angular = 5.0, Kd_angular = 0.08)
        Observation:
            The robot followed straight paths more accurately.
            Turns were sharper, but there was still some instability in transitions.
        Reason for Change:
            Reduced Kd_angular to smooth out transitions.
            Slightly increased Kd_linear for finer straight-line corrections.

    Final Values (Kp_linear = 1.2, Kd_linear = 0.03, Kp_angular = 7.0, Kd_angular = 0.03)
        Observation:
            The cross-track error was minimized (~0.1 units on average).
            The robot moved smoothly with controlled speed and cornering.
            The boustrophedon pattern had even coverage.
        Final Adjustment:
            Increased Kp_angular further to refine cornering.
            Balanced Kd_linear and Kd_angular for minimal oscillations.
