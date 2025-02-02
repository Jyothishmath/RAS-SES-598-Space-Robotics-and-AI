#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from sensor_msgs.msg import JointState
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import numpy as np

class ForceVisualizer(Node):
    def __init__(self):
        super().__init__('force_visualizer')
        
        # Create QoS profiles
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # Subscribe to force command
        self.force_sub = self.create_subscription(
            Float64,
            '/model/inverted_pendulum/joint/cart_to_base/cmd_force',
            self.force_callback,
            10)
            
        # Subscribe to joint states using the republished topic
        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',  # Standard ROS2 joint states topic
            self.joint_state_callback,
            sensor_qos)
            
        # Publisher for force marker
        self.marker_pub = self.create_publisher(Marker, '/force_marker', 10)
        
        self.cart_position = 0.0
        self.get_logger().info('Force Visualizer node started')
        
    def joint_state_callback(self, msg):
        # Get cart position from joint states
        try:
            cart_idx = msg.name.index('cart_to_base')
            self.cart_position = msg.position[cart_idx]
        except ValueError:
            self.get_logger().warn('cart_to_base joint not found in joint states')
            
    def force_callback(self, msg):
        # Create marker for force visualization
        marker = Marker()
        marker.header.frame_id = "world"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "force"
        marker.id = 0
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        
        # Set the start point at the cart's position
        start = Point()
        start.x = self.cart_position
        start.y = 0.0
        start.z = 0.15  # Slightly above cart center
        
        # Set end point based on force magnitude (scaled for visualization)
        end = Point()
        scale = 0.1  # Scale factor to make force visible
        end.x = self.cart_position + msg.data * scale
        end.y = 0.0
        end.z = 0.15
        
        marker.points = [start, end]
        
        # Set the arrow properties
        marker.scale.x = 0.02  # shaft diameter
        marker.scale.y = 0.04  # head diameter
        marker.scale.z = 0.1   # head length
        
        # Color based on force direction (red for positive, blue for negative)
        marker.color.a = 1.0
        if msg.data > 0:
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
        else:
            marker.color.r = 0.0
            marker.color.g = 0.0
            marker.color.b = 1.0
            
        self.marker_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = ForceVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 