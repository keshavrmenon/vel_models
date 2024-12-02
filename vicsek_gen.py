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

def find_nbrs(h,a,r=0.4):
    #finds indices of all neighbours in a given radius
    nbr=[]
    i=0
    for b in h:
        if a.dist(b)<r or a==b:
            nbr.append(i)
        i+=1
    return nbr

# def find_nbrs2(h,a,r=0.2):
#     #finds indices of all neighbours in a given radius
#     nbr=[]
#     i=0
#     for b in h:
#         if a.dist2(b)<r or a==b:
#             nbr.append(i)
#         i+=1
#     return nbr

def vicsek_vel(h,a):
    #updates velocities according to the vicsek scheme
    th_av=0
    nbrs=find_nbrs(h, a)
    for i in nbrs:
        th_av+=h[i].get_th()
        if th_av>0:
            th_av%=np.pi
        else:
            th_av%=-np.pi
    th_av/=len(nbrs)
    th_av+=(eta*random.rand()-eta/2)
    return th_av
    
def pairwise_vel(a,b,r2=0.7):
    c=a.get_th()
    d=b.get_th()
    if random.rand()<r2:
        b.set_th(c)
    if random.rand()<r2:
        a.set_th(d)
        
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

print(find_nbrs(herd, herd[3]))
# print(find_nbrs2(herd, herd[3]))

for i in range(50):
    v_av.append(anv(herd))
    for j in range(len(herd)):
        #Update Position with PBC
        herd_nxt[j].set_pos((herd[j].get_pos()+herd[j].get_vel()*dt))
        #update velocity according to vicsek scheme
        herd_nxt[j].set_th(vicsek_vel(herd, herd[j]))
    j=0
    
    #Load next iteration in as the starting point
    for a in herd_nxt:
        herd[j]=a.copy()
        j+=1
    print(i)

plt.plot(t,v_av)