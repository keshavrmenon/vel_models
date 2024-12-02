#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 04:38:15 2024

@author: keshav
"""

import sys

L=3
v=0.03
eta=2
dt=1
N=300

sys.path.append('header')

import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
from animal import Animal

def find_nn(h, a):
    #Returns the two nearest neighbours to an animal a in a given herd h
    d1, d2 = 2*L, 2*L
    nn, nnn=Animal(),Animal()
    for b in h:
        if a==b:
            continue
        if a.dist(b)<d1:
            d1=a.dist(b)
            nn=b
            continue
        if a.dist(b)<d2:
            d2=a.dist(b)
            nnn=b
    return nn, nnn
        
def triplet_vel(a, b, c, r3=0.3):
    th1=a.get_th()
    th2=b.get_th()
    th3=c.get_th()
    x=np.array([np.fabs(th1-th2), np.fabs(th2-th3),np.fabs(th3-th1)])
    i=np.argmin(x)
    th=x[i]+x[(i+1)%3]
    a.set_th(th)
    b.set_th(th)
    c.set_th(th)

def anv(h):
    #average normalised velocity of the herd
    va=np.zeros(2)
    for a in h:
        va+=a.get_vel()
    va=np.linalg.norm(va)/(N*v)
    return va

#Creating the main herd and a copy for the next iteration
herd=[]
herd_nxt = []
for i in range(N):
    herd.append(Animal(L*random.rand(2)-(L/2)*np.ones(2), theta= 2*np.pi*random.rand()-np.pi,speed=v, length=L))
    temp=herd[i].copy()
    herd_nxt.append(temp)
    
t=np.linspace(0, 49, 50)


v_av=[]


for i in range(50):
    v_av.append(anv(herd))
    for j in range(len(herd)):
        #Update Position with PBC
        herd_nxt[j].set_pos((herd[j].get_pos()+herd[j].get_vel()*dt))
        #update velocity according to triplet scheme
        #add code
        
    j=0
    
    #Load next iteration in as the starting point
    for a in herd_nxt:
        herd[j]=a.copy()
        j+=1
    print(i)

plt.plot(t,v_av)