#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 04:34:01 2024

@author: keshav
"""

import numpy as np

class Animal:
    def __init__(self, pos=np.zeros(2), theta= 0, *, speed=0.03, length):
        self.L=length
        self.pos=pos
        pos=self.set_pos(self.get_pos())
        self.th=theta
        self.speed=speed
        self.vel=self.speed*np.array([np.cos(self.th),np.sin(self.th)])
        
    
    #Getters
    
    def get_pos(self):
        return self.pos
        
    def get_vel(self):
        return self.speed*np.array([np.cos(self.th),np.sin(self.th)])
        
    def get_th(self):
        return self.th

    #Setters        

    def set_pos(self,p):
        x = p[0]
        y= p[1]
        # if np.fabs(p[0]) > self.L/2 or p[0] == self.L/2:
        #     p[0]+=self.L/2
        #     p[0]%=self.L
        #     p[0]-=self.L/2
        # if np.fabs(p[1]) > self.L/2 or p[1] == self.L/2:
        #     p[1]+=self.L/2
        #     p[1]%=self.L
        #     p[1]-=self.L/2
        
        if np.fabs(x) > self.L/2 or x == self.L/2:
            x+=self.L/2
            x%=self.L
            x-=self.L/2
        if np.fabs(y) > self.L/2 or y == self.L/2:
            y+=self.L/2
            y%=self.L
            y-=self.L/2

        self.pos=np.array([x,y])
        
    def set_th(self, theta):
        self.th=theta
        self.vel=self.speed*np.array([np.cos(self.th),np.sin(self.th)])
    
    #Other Methods
    
    def dist(self, animal2):
        p = []
        l=-self.L
        for _ in range(3):
            b=-self.L
            for _ in range(3):
                p.append(np.linalg.norm(self.pos-np.add(animal2.pos, np.array([l,b]))))
                b+=self.L
            l+=self.L
        return min(p)
    
    def dist2(self, animal2):
        return np.linalg.norm(self.pos-animal2.pos)

    def copy(self):
        return Animal(self.pos, self.th, speed = self.speed, length=self.L)