#!/usr/bin/env python3

import pygame as pg
import numpy as np
import rospy
from geometry_msgs.msg import Twist
import sys
from settings import *
from turtle_bot import *
from pygame.locals import *
import threading
from lds import * 
from sensor_msgs.msg import LaserScan

class Turtle_Control():
    def __init__(self):
        pg.init()
        
        #screen
        self.screen=pg.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
        pg.display.set_caption("turtlebot3 control")
        #prep sprites
        rospy.init_node("turtle_control")
        self.all_sprites = pg.sprite.Group()
        self.turtle = Turtle_leader(self.all_sprites,SCREENWIDTH/2,SCREENHEIGHT/2)

        self.ranges=np.zeros((1,360))
        self.ldss=[Lds(self.all_sprites,self.turtle,i,0) for i in range(360)]
        
        self.pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)
        self.subs_lds=rospy.Subscriber("/scan",LaserScan,self.lds_callback)
        
        self.dataSemaphore=threading.Semaphore(0)
        self.ldsLock = threading.Lock()

        self.tw = Twist()
        self.tw.linear.x=0
        self.tw.angular.z=0

        #clock
        self.clock = pg.time.Clock()

        self.sub_thread = threading.Thread(target=self.ros_subscriber)
        self.pub_thread = threading.Thread(target=self.run)

        self.sub_thread.start()
        self.pub_thread.start()



        

    
    def lds_callback(self,msg):
        with self.ldsLock:
            self.ranges=np.array(msg.ranges)
            for i in range(360):
                if self.ranges[i] == np.inf:
                    self.ranges[i]=0            
            self.dataSemaphore.release()    
                

            
    def ros_subscriber(self):
        rospy.spin()

    def event(self):
        #game_loop
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            
            self.avoidObstacle()

            self.turtle.move(v=self.tw.linear.x,a=self.tw.angular.z)

    def update(self):
        self.dataSemaphore.acquire()
        with self.ldsLock:
            for i in range(360):
                self.ldss[i].refresh(i,self.ranges[i])
            self.all_sprites.update()
            self.pub.publish(self.tw)
    
    def avoidObstacle(self):
        for r in self.ranges[-35 :35]:
            print(r)
        #     if r < THRESHOLD and r > 0.0 :
        #         self.tw.angular.z = ANGULARSPEED
        #         self.tw.linear.x = 0
        #         return
        # self.tw.linear.x = FOWARDSPEED
        return

    def run(self):
        while not rospy.is_shutdown():
            self.event()
            self.update()
            self.draw()    
            self.clock.tick(FRAME_PER_SECOND)
        self.sub_thread.join()
        self.pub_thread.join()
        sys.exit()


    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == '__main__':
    turtle_control = Turtle_Control()
    turtle_control.run()