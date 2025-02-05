#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    """Generate launch description for terrain mapping with camera bridge."""
    
    # Get the path to the terrain model
    pkg_share = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    model_path = os.path.join(pkg_share, 'models')
    
    # Set Gazebo model path
    os.environ['GZ_SIM_RESOURCE_PATH'] = model_path
    
    # Launch PX4 SITL with x500_gimbal
    px4_sitl = ExecuteProcess(
        cmd=['make', 'px4_sitl', 'gz_x500_gimbal'],
        cwd='/home/jdas/PX4-Autopilot',
        output='screen'
    )
    
    # Spawn the terrain model
    spawn_terrain = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-file', os.path.join(model_path, 'terrain', 'model.sdf'),
            '-name', 'terrain',
            '-x', '0',
            '-y', '0',
            '-z', '0'
        ],
        output='screen'
    )
    
    # Bridge node for gimbal topics - start after a delay to ensure PX4 is up
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='bridge',
        arguments=[
            '/model/x500_gimbal_0/command/gimbal_roll@std_msgs/msg/Float64@gz.msgs.Double',
            '/model/x500_gimbal_0/command/gimbal_pitch@std_msgs/msg/Float64@gz.msgs.Double',
            '/model/x500_gimbal_0/command/gimbal_yaw@std_msgs/msg/Float64@gz.msgs.Double'
        ],
        output='screen'
    )

    # Launch the spiral trajectory controller with a delay
    controller_node = Node(
        package='terrain_mapping_drone_control',
        executable='spiral_trajectory',
        name='spiral_trajectory',
        output='screen'
    )

    # Add delays to ensure proper startup sequence
    delayed_terrain = TimerAction(
        period=2.0,  # 2 second delay
        actions=[spawn_terrain]
    )

    delayed_bridge = TimerAction(
        period=5.0,  # 5 second delay
        actions=[bridge]
    )

    delayed_controller = TimerAction(
        period=10.0,  # 10 second delay
        actions=[controller_node]
    )

    return LaunchDescription([
        px4_sitl,
        delayed_terrain,
        delayed_bridge,
        delayed_controller
    ])
