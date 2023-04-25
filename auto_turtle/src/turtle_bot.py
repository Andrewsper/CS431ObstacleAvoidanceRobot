import pygame as pg
import numpy as np
import rospy
from geometry_msgs.msg import Twist
import sys
from settings import *
from turtle_bot import *
import tf


class Turtle_bot(pg.sprite.Sprite):
    def __init__(self,group,x,y) -> None:
        super().__init__(group)
  
        img = pg.image.load("tank.png")
        self.image0 = pg.transform.scale(img,(img.get_rect().width / TANKSCALE,img.get_rect().height/ TANKSCALE))
        
        self.image = self.image0
        self.rect=self.image.get_rect()
        self.y=y
        self.x= x
        self.dir =0
    
    def move(self,v=0,a=0):
        self.dir += a*DT
        dl = np.array([v * DT,0,0])
        rotz= tf.transformations.rotation_matrix(self.dir,(0,0,1)) [:3,:3]
        dw= rotz.dot(dl)
        self.x -=dw[1] * PIXPERM
        self.y -=dw[0] * PIXPERM

    def update(self):
        self.rect.centerx=self.x
        self.rect.centery=self.y
        self.image = pg.transform.rotate(self.image0,np.rad2deg(self.dir))
        self.rect=self.image.get_rect(center=self.rect.center)

class Turtle_leader(Turtle_bot):
    def move(self,v=0,a=0):
        pass
    