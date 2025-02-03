from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    """Generate launch description for spiral trajectory demonstration."""
    
    # Get the path to this package's share directory
    pkg_share = FindPackageShare(package='terrain_mapping_drone_control').find('terrain_mapping_drone_control')
    
    # Launch spiral trajectory controller
    controller_node = Node(
        package='terrain_mapping_drone_control',
        executable='terrain_mapping_controller',
        name='spiral_trajectory_controller',
        output='screen',
        parameters=[os.path.join(pkg_share, 'config', 'spiral_params.yaml')]
    )
    
    # Create and return launch description
    return LaunchDescription([
        controller_node
    ]) 