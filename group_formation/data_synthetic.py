#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
trajsWithId - np.array [idx,x,y,frame]
userInfo - pd.dataframe ['track_id', 'oframe', 'ox', 'oy', 'dframe', 'dx', 'dy', 'av', 'type']
"""

import matplotlib.pyplot as plt
import numpy as np
from random import uniform
import pandas as pd
import os

# simulation parameters
Kp_rho = 9
Kp_alpha = 15
Kp_beta = -3
dt = 0.01
    
def genSingleTraj(mapSize):
    
    minRoadWidth = mapSize/2 - 4
    maxRoadWidth = mapSize/2 + 4
    
    top = np.asarray([uniform(minRoadWidth,maxRoadWidth), mapSize])
    bottom = np.asarray([uniform(minRoadWidth,maxRoadWidth), 0])
    left = np.asarray([0, uniform(minRoadWidth,maxRoadWidth)])
    right = np.asarray([mapSize, uniform(minRoadWidth,maxRoadWidth)])
    
    start, end = np.random.permutation(np.asarray([top,bottom, left, right]))[0:2]
    
    x_start = start[0]
    y_start = start[1]
    if x_start == 0 and y_start != 0: # come from left
        theta_start = 0
    elif x_start != 0 and y_start == mapSize: # come from top
        theta_start = -0.5 * np.pi
    elif x_start != 0 and y_start == 0: # come from bottom
        theta_start = 0.5 * np.pi
    elif x_start == mapSize and y_start != 0: # come from right
        theta_start = np.pi
        
    x_goal = end[0]
    y_goal = end[1]
    if x_goal == 0 and y_goal != 0: # go to left
        theta_goal = np.pi
    elif x_goal != 0 and y_goal == mapSize: # go to top
        theta_goal = 0.5 * np.pi
    elif x_goal != 0 and y_goal == 0: # go to bottom
        theta_goal = -0.5 * np.pi
    elif x_goal == mapSize and y_goal != 0: # go to right
        theta_goal = 0
        
    x = x_start
    y = y_start
    theta = theta_start

    x_diff = x_goal - x
    y_diff = y_goal - y

    x_traj, y_traj = [], []

    rho = np.hypot(x_diff, y_diff)
    
    while rho > 0.001:
        x_traj.append(x)
        y_traj.append(y)

        x_diff = x_goal - x
        y_diff = y_goal - y

        rho = np.hypot(x_diff, y_diff)
        alpha = (np.arctan2(y_diff, x_diff)
                 - theta + np.pi) % (2 * np.pi) - np.pi
        beta = (theta_goal - theta - alpha + np.pi) % (2 * np.pi) - np.pi

        v = Kp_rho * rho
        w = Kp_alpha * alpha + Kp_beta * beta

        if alpha > np.pi / 2 or alpha < -np.pi / 2:
            v = -v

        theta = theta + w * dt
        x = x + v * np.cos(theta) * dt
        y = y + v * np.sin(theta) * dt

    traj = np.asarray([np.asarray(x_traj),np.asarray(y_traj)]).T
    
    return traj

def genTrajSet(mapSize,trajNum, firstFrame):
    
    trajs = []
    
    for i in range(trajNum): 
        t = genSingleTraj(mapSize)
        frame = np.arange(firstFrame,(firstFrame+len(t)))
        trajs.append(np.c_[t,frame])
        firstFrame += 1
        
    return trajs

def genInput(trajsWithId):
    
    userInfo = []
    for t in trajsWithId:
        ox = t[0,1]
        oy = t[0,2]
        dx = t[-1,1]
        dy = t[-1,2]
        idx = t[0,0]
        oframe = t[0,3]
        dframe = t[-1,3]
        av = (4 - 0.5) * np.random.random_sample() + 0.5 #default value
        ty = 0 #default value
        userInfo.append([idx,oframe,ox,oy,dframe,dx,dy,av,ty])
        
    df = pd.DataFrame (userInfo,columns=['track_id', 'oframe', 'ox', 'oy', 'dframe', 'dx', 'dy', 'av', 'type'])
    
    return df

if __name__ == '__main__':
    
    output_dir ='../data/synthetic/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    mapSize = 12
    # trajNum = 600
    # firstFrame = 0
    # trajs = genTrajSet(mapSize,trajNum,firstFrame) #list of [x,y,t]
    
    # multi traj sets examples - for discrete group
    # genTrajSet(mapSize,trajNum, firstFrame)
    t1 = genTrajSet(mapSize,100,100)
    t2 = genTrajSet(mapSize,200,50)
    t3 = genTrajSet(mapSize,300,300)
    trajs = t1 + t2 +t3
    
    trajsWithId = [ np.c_[ (np.ones((len(trajs[i]),1))*i), trajs[i] ] for i in range(len(trajs))]
    userInfo = genInput(trajsWithId)
    userInfo = userInfo.sort_values(by=['oframe']) # reorder by starting frame
    
    # trajs: list of vari-length traj [idx,x,y,frame]
    data = np.vstack(trajsWithId)
    
    np.save(output_dir+'synthetic_mapSize'+str(mapSize)+'_trajsWithId'+'.npy', data)
    userInfo.to_csv(output_dir+'synthetic_mapSize'+str(mapSize)+'_userInfo'+'.csv',index=False) 

