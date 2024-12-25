#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 04:38:15 2024

@author: keshav
"""
import sys

L=25
v=0.03
eta=0.1
dt=1
N=300
T=1000
sys.path.append('./header')

import csv
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

t=np.linspace(0, T-1, T)


v_av=[]

with open(f"./outputs/data/vicsek_L{L}_eta{eta}_v{v}.csv", "w", newline='') as f:
    f.truncate()

# print(find_nbrs(herd, herd[3]))
# print(find_nbrs2(herd, herd[3]))
    
for i in range(T):
    #empty list to hold pos and vel values for the csv file
    data = []
    v_av.append(anv(herd))
    #add anv to the list for 
    data.append(v_av[i])
    for j in range(len(herd)):
        #add position data to the data list
        data.append(herd[j].get_pos()[0])
        data.append(herd[j].get_pos()[1])
        #Update Position with PBC
        herd_nxt[j].set_pos((herd[j].get_pos()+herd[j].get_vel()*dt))
    for j in range(len(herd)):
        #add position data to the list to the data list        
        data.append(herd[j].get_vel()[0])
        data.append(herd[j].get_vel()[1])
        #update velocity according to pairwise scheme
        herd_nxt[j].set_th(vicsek_vel(herd, herd[j]))

    #Load next iteration in as the starting point
    j=0
    for a in herd_nxt:
        herd[j]=a.copy()
        j+=1
    print(i)
    with open(f"./outputs/data/vicsek_L{L}_eta{eta}_v{v}.csv", "a", newline='') as f:
        writer = csv.writer(f,delimiter=' ')
        writer.writerow(data)


plt.plot(t,v_av)