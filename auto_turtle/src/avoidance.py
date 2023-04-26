#!/usr/bin/env python3

import rospy
import threading
import sys
import signal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np
from settings_test import *

class AvoidanceRobot():
    def __init__(self):
        self.scan_data_lock = threading.Condition()
        
        self.ranges = np.zeros(360)
        
        rospy.init_node('avoidance_robot', anonymous=True)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.ros_lds_callback)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.ros_clock = rospy.Rate(10)
        
        self.tw = Twist()
        self.tw.linear.x = 0.0
        self.tw.angular.z = 0.0
        
        self.control_thread = threading.Thread(target=self.control_loop)
        self.subscriber_thread = threading.Thread(target=self.subscriber_thread)
        
        # Register signal handler to handle Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, sig, frame):
        sys.exit()
        
    def ros_lds_callback(self, msg):
        with self.scan_data_lock:
            self.ranges = np.array(msg.ranges)
            self.ranges[np.isinf(self.ranges)] = 0       
            self.scan_data_lock.notify()
    
    def control_loop(self):
        while not rospy.is_shutdown():
            decision = self.avoid_obstacle()
            
            self.tw.linear.x = decision[0]
            self.tw.angular.z = decision[1]
            
            self.vel_pub.publish(self.tw)            
            self.ros_clock.sleep()
            
    def subscriber_thread(self):
        rospy.spin()       
        
    def avoid_obstacle(self):
        with self.scan_data_lock:
            self.scan_data_lock.wait()
            
            collision = False
            
            # check for collision
            for i in range(0, 46):
                if self.ranges[i] <= COLLISION_DISTANCE and self.ranges[i] != 0: 
                    collision = True
                    break
            
            for i in range(314, 360):
                if self.ranges[i] <= COLLISION_DISTANCE and self.ranges[i] != 0:
                    collision = True
                    break
                
            if not collision:
                return [0.2, 0.0]
       
            # normalize the ranges
            normalized_set = self.ranges.copy() / np.max(self.ranges)
            
            # negate 180-359
            for i in range(314, 360):
                normalized_set[i] = -normalized_set[i]
                
            print(np.sum(normalized_set))
                
            # get sum of the ranges
            if np.sum(normalized_set) < 0:
                return [0.0, 0.2]
            elif np.sum(normalized_set) > 0:
                return [0.0, -0.2]
            
    def start_recovery(self):
        collision_detected = True
            
        while collision_detected:
            self.tw.angular.z = 0.1
            self.vel_pub.publish(self.tw)
            

                
            self.ros_clock.sleep()
    
    def start(self):
        self.control_thread.start()
        self.subscriber_thread.start()
    


if __name__ == "__main__":
    avoidance_robot = AvoidanceRobot()
    avoidance_robot.start()
