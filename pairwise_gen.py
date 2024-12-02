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
    
def pairwise_vel(a,b,r2=0.7):
    c=a.get_th()
    d=b.get_th()
    if np.random.rand()<r2:
        b.set_th(c)
    if np.random.rand()<r2:
        a.set_th(d)
        

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
    herd.append(Animal(L*np.random.rand(2)-(L/2)*np.ones(2), theta= 2*np.pi*np.random.rand()-np.pi,speed=v, length=L))
    temp=herd[i].copy()
    herd_nxt.append(temp)
    
t=np.linspace(0, 49, 50)


v_av=[]

for i in range(50):
    v_av.append(anv(herd))
    for j in range(len(herd)):
        #Update Position with PBC
        herd_nxt[j].set_pos((herd[j].get_pos()+herd[j].get_vel()*dt))
        #update velocity according to pairwise scheme
        #add code
    
    #Load next iteration in as the starting point
    j=0
    for a in herd_nxt:
        herd[j]=a.copy()
        j+=1
    print(i)

plt.plot(t,v_av)