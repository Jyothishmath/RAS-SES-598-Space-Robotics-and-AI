#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
from visualization_msgs.msg import MarkerArray, Marker
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import numpy as np

class StatePlotter(Node):
    def __init__(self):
        super().__init__('state_plotter')
        
        # Create QoS profiles
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # Subscribe to joint states and forces
        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            sensor_qos
        )
        
        self.force_sub = self.create_subscription(
            Float64,
            '/model/inverted_pendulum/joint/cart_to_base/cmd_force',
            self.force_callback,
            10
        )
        
        # Publishers for state plots
        self.state_marker_pub = self.create_publisher(
            MarkerArray,
            '/state_plots',
            10
        )
        
        self.force_marker_pub = self.create_publisher(
            MarkerArray,
            '/force_plots',
            10
        )
        
        # Initialize state history
        self.window_size = 500  # 10 seconds at 50Hz
        self.cart_pos_history = []
        self.cart_vel_history = []
        self.pole_angle_history = []
        self.pole_vel_history = []
        self.force_history = []
        self.timestamps = []
        
        self.last_force = 0.0
        self.get_logger().info('State Plotter node started')
        
    def joint_state_callback(self, msg):
        try:
            # Get current time for x-axis
            current_time = self.get_clock().now().nanoseconds / 1e9
            
            # Extract states
            cart_idx = msg.name.index('cart_to_base')
            pole_idx = msg.name.index('pole_joint')
            
            # Update histories
            self.cart_pos_history.append(msg.position[cart_idx])
            self.cart_vel_history.append(msg.velocity[cart_idx])
            self.pole_angle_history.append(msg.position[pole_idx])
            self.pole_vel_history.append(msg.velocity[pole_idx])
            self.timestamps.append(current_time)
            
            # Keep fixed window size
            if len(self.timestamps) > self.window_size:
                self.cart_pos_history.pop(0)
                self.cart_vel_history.pop(0)
                self.pole_angle_history.pop(0)
                self.pole_vel_history.pop(0)
                self.timestamps.pop(0)
            
            # Create and publish state plots
            self.publish_state_plots()
            
        except ValueError as e:
            self.get_logger().warn(f'Joint state processing error: {str(e)}')
    
    def force_callback(self, msg):
        if len(self.timestamps) > 0:  # Only record if we have timestamps
            self.force_history.append(msg.data)
            if len(self.force_history) > self.window_size:
                self.force_history.pop(0)
            self.last_force = msg.data
            self.publish_force_plots()
    
    def create_line_strip_marker(self, points, id_num, r, g, b, namespace):
        marker = Marker()
        marker.header.frame_id = "world"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = id_num
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD
        marker.scale.x = 0.02  # line width
        marker.color.r = r
        marker.color.g = g
        marker.color.b = b
        marker.color.a = 1.0
        marker.points = points
        return marker
    
    def publish_state_plots(self):
        if not self.timestamps:
            return
            
        marker_array = MarkerArray()
        base_time = self.timestamps[0]
        
        # Create points for each state variable
        for i, (data, color, label) in enumerate([
            (self.cart_pos_history, (1.0, 0.0, 0.0), "Cart Position"),  # red
            (self.cart_vel_history, (0.0, 1.0, 0.0), "Cart Velocity"),  # green
            (self.pole_angle_history, (0.0, 0.0, 1.0), "Pole Angle"),   # blue
            (self.pole_vel_history, (1.0, 1.0, 0.0), "Pole Velocity")   # yellow
        ]):
            points = []
            for t, val in zip(self.timestamps, data):
                p = Point()
                p.x = -2.5  # Start at left edge of track
                p.y = 2.0 + (i * 0.5)  # Stack plots vertically above the cart
                p.z = ((t - base_time) / 10.0) * 5.0  # Scale time to 5m length
                points.append(p)
                
                # Add the value point
                p2 = Point()
                p2.x = -2.5 + (val * 0.5)  # Scale and offset the value
                p2.y = 2.0 + (i * 0.5)     # Same height as time point
                p2.z = ((t - base_time) / 10.0) * 5.0  # Same z as time point
                points.append(p2)
            
            # Create the line strip marker
            marker = self.create_line_strip_marker(
                points, i, color[0], color[1], color[2], "state"
            )
            marker.scale.x = 0.03  # Thicker lines for better visibility
            marker_array.markers.append(marker)
            
            # Add text marker for label
            text_marker = Marker()
            text_marker.header.frame_id = "world"
            text_marker.header.stamp = self.get_clock().now().to_msg()
            text_marker.ns = "state_labels"
            text_marker.id = i
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.pose.position.x = -2.7  # Slightly left of plot
            text_marker.pose.position.y = 2.0 + (i * 0.5)
            text_marker.pose.position.z = 0
            text_marker.text = label
            text_marker.scale.z = 0.2  # Text size
            text_marker.color.r = color[0]
            text_marker.color.g = color[1]
            text_marker.color.b = color[2]
            text_marker.color.a = 1.0
            marker_array.markers.append(text_marker)
        
        self.state_marker_pub.publish(marker_array)
    
    def publish_force_plots(self):
        if not self.timestamps or not self.force_history:
            return
            
        marker_array = MarkerArray()
        base_time = self.timestamps[0]
        
        # Create points for force data
        points = []
        for t, force in zip(self.timestamps[-len(self.force_history):], self.force_history):
            p = Point()
            p.x = -2.5  # Start at left edge of track
            p.y = 0.5   # Just above the cart
            p.z = ((t - base_time) / 10.0) * 5.0  # Scale time to 5m length
            points.append(p)
            
            # Add the force value point
            p2 = Point()
            p2.x = -2.5 + (force * 0.1)  # Scale force for visibility
            p2.y = 0.5                    # Same height
            p2.z = ((t - base_time) / 10.0) * 5.0  # Same z as time point
            points.append(p2)
        
        # Create the line strip marker
        marker = self.create_line_strip_marker(
            points, 0, 1.0, 0.0, 0.0, "force"  # red for force
        )
        marker.scale.x = 0.03  # Thicker lines
        marker_array.markers.append(marker)
        
        # Add label for force plot
        text_marker = Marker()
        text_marker.header.frame_id = "world"
        text_marker.header.stamp = self.get_clock().now().to_msg()
        text_marker.ns = "force_label"
        text_marker.id = 0
        text_marker.type = Marker.TEXT_VIEW_FACING
        text_marker.action = Marker.ADD
        text_marker.pose.position.x = -2.7
        text_marker.pose.position.y = 0.5
        text_marker.pose.position.z = 0
        text_marker.text = "Applied Force"
        text_marker.scale.z = 0.2  # Text size
        text_marker.color.r = 1.0
        text_marker.color.g = 0.0
        text_marker.color.b = 0.0
        text_marker.color.a = 1.0
        marker_array.markers.append(text_marker)
        
        self.force_marker_pub.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    node = StatePlotter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main() 