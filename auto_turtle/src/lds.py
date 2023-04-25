
import pygame as pg
import numpy as np
from settings import *
import tf
class Lds(pg.sprite.Sprite):
    def __init__(self, group,leader,deg,r):
        super().__init__(group)
        img = pg.image.load("lds.png")
        
        self.image=pg.transform.scale(img,(img.get_rect().width / LDS_SCALE,img.get_rect().height/ LDS_SCALE))

        self.rect=self.image.get_rect()
        self.leader=leader
        self.refresh(deg,r)

    def refresh(self,deg,r):
        dl = np.array([r,0,0])
        rotz = tf.transformations.rotation_matrix(np.radians(deg),(0,0,1))[:3,:3]
        dw=rotz.dot(dl)

        self.x = -dw[1] * PIXPERM + self.leader.rect.centerx
        self.y = -dw[0] * PIXPERM + self.leader.rect.centery
    
    def update(self):
        self.rect.centerx=self.x
        self.rect.centery=self.y
