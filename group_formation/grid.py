# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:08:07 2020

@author: li
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plotODdata(user_type):
    
    idx = pd.unique(user_type['user_id'])
    loc_enter = []
    loc_leave = []
    for i in idx:
        current_user = user_type[user_type['user_id']==i]
        pt_enter = (current_user['time_05'].iloc[0],current_user['x_axis'].iloc[0],current_user['y_axis'].iloc[0])
        pt_leave = (current_user['time_05'].iloc[-1],current_user['x_axis'].iloc[-1],current_user['y_axis'].iloc[-1])
        
        loc_enter.append(pt_enter)
        loc_leave.append(pt_leave)
    
    # visualization
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    t1 = np.asarray(loc_enter)
    t2 = np.asarray(loc_leave)
    
    x1 = t1[:,1]
    y1 = t1[:,2]
    t1 = t1[:,0]
    
    x2 = t2[:,1]
    y2 = t2[:,2]
    t2 = t2[:,0]
    
    ax.scatter(x1, y1, t1, c = 'cyan')
    # ax.scatter(x2, y2, t2, c = 'green')
    
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Time [s]')
    
    plt.show()
    
    return None

# read data
data_dir = "./data/Federico/dump/Hamburg_dataset.csv"
df = pd.read_csv(data_dir)

cyc = df[df['user_type']=='cyclist   ']
ped = df[df['user_type']=='pedestrian']
veh = df[df['user_type']=='car       ']

plotODdata(cyc)
plotODdata(ped)
plotODdata(veh)
