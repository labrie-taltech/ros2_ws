#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class TurtlebotMappingNode(Node):
    def __init__(self):
        super().__init__("mapping_node")
        self.get_logger().info("Mapping Node has started.")
        # Publisher to send movement commands
        self._pose_publisher = self.create_publisher(
        Twist, "/cmd_vel", 10
        )
        # Subscriber to receive LiDAR data
        self._scan_listener = self.create_subscription(
        LaserScan, "/scan", self.robot_controller, 10
        )
    def robot_controller(self, scan: LaserScan):
        cmd = Twist()
        # Define the width of the range for obstacle detection
        a = 20
        # Extract directional distances
        self._front = min(scan.ranges[:a+1] + scan.ranges[-a:])
        self._left = max(scan.ranges[90-a:90+a+1])
        self._right = max(scan.ranges[270-a:270+a+1])
        # Navigation logic based on obstacle detection
        if self._front < 1.0: # Obstacle ahead
            if self._right < self._left:
                cmd.linear.x = 0.06
                cmd.angular.z = 0.7 # Turn left
            else:
                cmd.linear.x = 0.06
                cmd.angular.z = -0.7 # Turn right
        else:
            cmd.linear.x = 0.4
            cmd.angular.z = 0.0 # Move forward
        # Publish the command
        self._pose_publisher.publish(cmd)
def main(args=None):
    rclpy.init(args=args)
    node = TurtlebotMappingNode()
    rclpy.spin(node)
    rclpy.shutdown()