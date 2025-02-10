#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class FeatureTracker(Node):
    def __init__(self):
        super().__init__('feature_tracker')
        
        # Create QoS profile for better image streaming
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        # Initialize CV bridge
        self.bridge = CvBridge()
        
        # Initialize feature detector and tracker
        self.feature_params = dict(
            maxCorners=100,
            qualityLevel=0.3,
            minDistance=7,
            blockSize=7
        )
        
        # Initialize ORB for descriptor computation
        self.orb = cv2.ORB_create(
            nfeatures=1000,
            scaleFactor=1.2,
            nlevels=8
        )
        
        # Initialize FLANN matcher
        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH,
                          table_number=6,
                          key_size=12,
                          multi_probe_level=1)
        search_params = dict(checks=50)
        self.matcher = cv2.FlannBasedMatcher(index_params, search_params)
        
        # Store latest images and camera info
        self.left_image = None
        self.right_image = None
        self.left_camera_info = None
        self.right_camera_info = None
        self.prev_left_image = None
        self.prev_left_points = None
        
        # Create subscribers
        self.left_sub = self.create_subscription(
            Image,
            '/zed/zed_node/left_gray/image_rect_gray',
            self.left_image_callback,
            qos_profile
        )
        self.right_sub = self.create_subscription(
            Image,
            '/zed/zed_node/right_gray/image_rect_gray',
            self.right_image_callback,
            qos_profile
        )
        self.left_info_sub = self.create_subscription(
            CameraInfo,
            '/zed/zed_node/left/camera_info',
            self.left_camera_info_callback,
            qos_profile
        )
        self.right_info_sub = self.create_subscription(
            CameraInfo,
            '/zed/zed_node/right/camera_info',
            self.right_camera_info_callback,
            qos_profile
        )
        
        # Create publisher for visualization
        self.vis_pub = self.create_publisher(
            Image,
            '/dreams_stereo/tracked_features',
            qos_profile
        )
        
        # Create timer for processing
        self.create_timer(0.1, self.process_features)  # 10Hz processing
        
        self.get_logger().info('Feature Tracker Node initialized')
    
    def left_image_callback(self, msg):
        try:
            self.left_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        except Exception as e:
            self.get_logger().error(f'Error converting left image: {str(e)}')
    
    def right_image_callback(self, msg):
        try:
            self.right_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        except Exception as e:
            self.get_logger().error(f'Error converting right image: {str(e)}')
    
    def left_camera_info_callback(self, msg):
        self.left_camera_info = msg
    
    def right_camera_info_callback(self, msg):
        self.right_camera_info = msg
    
    def draw_epipolar_lines(self, img1, img2, pts1, pts2, F):
        """Draw epipolar lines and their corresponding points."""
        h, w = img1.shape[:2]
        lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
        lines1 = lines1.reshape(-1, 3)
        lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
        lines2 = lines2.reshape(-1, 3)
        
        img1_with_lines = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        img2_with_lines = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        
        for pt1, pt2, line1, line2 in zip(pts1, pts2, lines1, lines2):
            # Draw points
            color = tuple(np.random.randint(0, 255, 3).tolist())
            x0, y0 = map(int, [pt1[0], pt1[1]])
            x1, y1 = map(int, [pt2[0], pt2[1]])
            cv2.circle(img1_with_lines, (x0, y0), 5, color, -1)
            cv2.circle(img2_with_lines, (x1, y1), 5, color, -1)
            
            # Draw epipolar lines
            # Line equation: ax + by + c = 0
            a, b, c = line1
            if abs(b) > 1e-6:  # Avoid division by zero
                x0, y0 = map(int, [0, -c/b])
                x1, y1 = map(int, [w, -(a*w + c)/b])
                cv2.line(img1_with_lines, (x0, y0), (x1, y1), color, 1)
            
            a, b, c = line2
            if abs(b) > 1e-6:  # Avoid division by zero
                x0, y0 = map(int, [0, -c/b])
                x1, y1 = map(int, [w, -(a*w + c)/b])
                cv2.line(img2_with_lines, (x0, y0), (x1, y1), color, 1)
        
        return img1_with_lines, img2_with_lines
    
    def process_features(self):
        if (self.left_image is None or self.right_image is None or 
            self.left_camera_info is None or self.right_camera_info is None):
            return
            
        try:
            # Detect features in left image if no previous points
            if self.prev_left_points is None:
                p = cv2.goodFeaturesToTrack(self.left_image, mask=None, **self.feature_params)
                if p is not None:
                    self.prev_left_points = p
                    self.prev_left_image = self.left_image.copy()
                return
            
            # Calculate optical flow
            curr_left_points, status, err = cv2.calcOpticalFlowPyrLK(
                self.prev_left_image, self.left_image, 
                self.prev_left_points, None
            )
            
            # Filter out points where tracking failed
            good_curr = curr_left_points[status == 1]
            good_prev = self.prev_left_points[status == 1]
            
            if len(good_curr) < 8:  # Need at least 8 points for essential matrix
                self.prev_left_points = None
                return
            
            # Get camera matrices
            K1 = np.array(self.left_camera_info.k).reshape(3, 3)
            K2 = np.array(self.right_camera_info.k).reshape(3, 3)
            
            # Find essential matrix
            E, mask = cv2.findEssentialMat(
                good_curr.reshape(-1, 2), 
                good_prev.reshape(-1, 2), 
                K1,
                method=cv2.RANSAC, 
                prob=0.999, 
                threshold=1.0
            )
            
            if E is None:
                self.prev_left_points = None
                return
            
            # Filter points using the essential matrix mask
            good_curr = good_curr[mask.ravel() == 1]
            good_prev = good_prev[mask.ravel() == 1]
            
            # Calculate fundamental matrix
            F = np.linalg.inv(K2.T) @ E @ np.linalg.inv(K1)
            
            # Draw visualization
            img1_lines, img2_lines = self.draw_epipolar_lines(
                self.left_image, self.right_image,
                good_curr, good_prev, F
            )
            
            # Create side-by-side visualization
            h1, w1 = img1_lines.shape[:2]
            h2, w2 = img2_lines.shape[:2]
            vis_img = np.zeros((max(h1, h2), w1 + w2, 3), dtype=np.uint8)
            vis_img[0:h1, 0:w1] = img1_lines
            vis_img[0:h2, w1:w1+w2] = img2_lines
            
            # Draw connecting lines between matches
            for pt1, pt2 in zip(good_curr, good_prev):
                x1, y1 = map(int, [pt1[0], pt1[1]])
                x2, y2 = map(int, [pt2[0], pt2[1]])
                cv2.line(vis_img, (x1, y1), (x2 + w1, y2), (0, 255, 0), 1)
            
            # Update previous frame info
            self.prev_left_points = good_curr.reshape(-1, 1, 2)
            self.prev_left_image = self.left_image.copy()
            
            # Convert visualization to ROS message and publish
            vis_msg = self.bridge.cv2_to_imgmsg(vis_img, encoding='bgr8')
            self.vis_pub.publish(vis_msg)
            
        except Exception as e:
            self.get_logger().error(f'Error processing features: {str(e)}')
            self.prev_left_points = None

def main(args=None):
    rclpy.init(args=args)
    node = FeatureTracker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 