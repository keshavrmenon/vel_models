#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 04:38:15 2024

@author: keshav
"""
import sys

L=3
v=0.03
eta=0.1
dt=1
N=300
T=1000

sys.path.append('header')

import csv
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

def find_nbrs(h,a,r=0.4):
    #finds indices of all neighbours in a given radius
    nbr=[]
    i=0
    for b in h:
        if a.dist(b)<r or a==b:
            nbr.append(i)
        i+=1
    return nbr
    
def pairwise_vel(a,b,r2=0.7):
    c=a.get_th()
    d=b.get_th()
    if np.random.rand()<r2:
        b.set_th(c)
    if np.random.rand()<r2:
        a.set_th(d)
    b.set_th(b.get_th()+np.random.normal(0,eta))
    a.set_th(a.get_th()+np.random.normal(0,eta))

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
    
t=np.linspace(0, T-1, T)


v_av=[]



with open(f"./outputs/data/pairwise_L{L}_eta{eta}_v{v}.csv", "w", newline='') as f:
    f.truncate()

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
        pairwise_vel(herd_nxt[j], herd_nxt[np.random.randint(0,len(find_nbrs(herd_nxt,herd_nxt[j]))+1)])

    #Load next iteration in as the starting point
    j=0
    for a in herd_nxt:
        herd[j]=a.copy()
        j+=1
    print(i)
    with open(f"./outputs/data/pairwise_L{L}_eta{eta}_v{v}.csv", "a", newline='') as f:
        writer = csv.writer(f,delimiter=' ')
        writer.writerow(data)
        
plt.plot(t,v_av)