#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 21:36:36 2024

@author: keshav
"""

L=3
v=0.03
eta=0.1
dt=1
N=300

import sys

sys.path.append("./outputs")

import csv
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

fig = plt.figure()

type="pairwise"
metadata = dict(title=type+" animation", author="keshav")
writer = PillowWriter(fps=20, metadata=metadata)

with writer.saving(fig, "./outputs/animations/anim_"+type+f"_L{L}_eta{eta}_v{v}.gif", 100):
    with open("./outputs/data/"+type+f"_L{L}_eta{eta}_v{v}.csv", "r", newline='') as f:
        reader = csv.reader(f, delimiter = ' ')
        for row in reader:
            plt.xlim(-L/2, L/2)
            plt.ylim(-L/2, L/2)
            xpos=[]
            ypos=[]
            xvel=[]
            yvel=[]
            for i in range(N):
                xpos.append(float(row[2*i+1]))
                ypos.append(float(row[2*i+2]))
                xvel.append(float(row[2*(N+i)+1]))
                yvel.append(float(row[2*(N+i)+2]))
            
            plt.quiver(xpos, ypos, xvel, yvel,scale=3)
            writer.grab_frame()
            plt.clf()
