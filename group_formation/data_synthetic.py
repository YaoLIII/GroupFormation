#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[aim] 
    generate synthetic data with [track_id ot ox oy dt dx dy av(1) type(1)]
[continuity] 
    - genTrajSet() are continuous in time, i.e. after each frame add one more 
        traj to scene
    - for distinct trajectories, generate then independently [firstFrame], 
        then combine all trajSet, finally add idx


@author: yaoli
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties

def genSingleTraj(mapSize):
    
    top = np.asarray([np.random.randint(mapSize), mapSize])
    bottom = np.asarray([np.random.randint(mapSize), 0])
    left = np.asarray([0, np.random.randint(mapSize)])
    right = np.asarray([mapSize, np.random.randint(mapSize)])
    
    start, end = np.random.permutation(np.asarray([top,bottom, left, right]))[0:2]
    # print(start)
    # print(end)
    
    path = []
    
    # waypoints in x direction
    if start[0] > end[0]:
        diff = start[0] - end[0]
        path = path + [ [i,start[1]] for i in range(end[0],end[0]+diff)[::-1] ]
    elif start[0] < end[0]:
        diff = end[0] - start[0]
        path = path + [ [i,start[1]] for i in range(start[0],start[0]+diff+1) ]
        
    # waypoints in y direction
    if start[1] > end[1]:
        diff = start[1] - end[1] 
        path = path + [ [end[0],i] for i in range(end[1],end[1]+diff)[::-1] ]
    elif start[1] < end[1]:
        diff = end[1] - start[1] 
        path = path + [ [end[0],i] for i in range(start[1],start[1]+diff+1) ]
    
    # insert start and end points
    path.insert(0,start)
    path.insert(len(path),end)
    
    # drop duplicates
    df = pd.DataFrame(path)
    path = np.asarray(df.drop_duplicates())
    
    # print(path)    
    
    return path

def genTrajSet(mapSize,trajNum, firstFrame):
    
    trajs = []
    
    for i in range(trajNum): 
        t = genSingleTraj(mapSize)
        frame = np.arange(firstFrame,(firstFrame+len(t)))
        trajs.append(np.c_[t,frame])
        firstFrame += 1
        
    return trajs

# [track_id ot ox oy dt dx dy av(1) type(1)]

# trajs: list of vari-length traj [idx,x,y,frame]
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
        av = 1 #default value
        ty = 0 #default value
        userInfo.append([idx,oframe,ox,oy,dframe,dx,dy,av,ty])
        
    df = pd.DataFrame (userInfo,columns=['track_id', 'oframe', 'ox', 'oy', 'dframe', 'dx', 'dy', 'av', 'type'])
    
    return df

def plotPaths(userInfo, trajsWithId):

    ox = userInfo['ox'].tolist()
    oy = userInfo['oy'].tolist()
    dx = userInfo['dx'].tolist()
    dy = userInfo['dy'].tolist()
    oframe = userInfo['oframe'].tolist()
    dframe = userInfo['dframe'].tolist()
    
    frameRange = [min(oframe),max(dframe)]
    
    for f in np.arange(frameRange[0],frameRange[1]):
        
        existUser = userInfo[(userInfo['oframe']<=f) & (userInfo['dframe']>=f)]
        existUserId = existUser['track_id']
        existUserId = list(map(int,existUserId.tolist()))
        
        allTrajs = np.vstack(trajsWithId)
        existUserTraj = [allTrajs[allTrajs[:,0]==i] for i in existUserId]
        
        userTrajSoFar = []
        for t in existUserTraj:
            userTrajSoFar.append(t[t[:,3]<=f])
            
        if show_animation:  # pragma: no cover
            plt.cla()
            plt.scatter(existUser['ox'].tolist(), existUser['oy'].tolist(), 
                        color='g', marker='^')
            # plt.scatter(existUser['dx'].tolist(), existUser['dy'].tolist(), 
            #             color='r', marker='X')
            
            for subt in userTrajSoFar:
                plt.plot(subt[:,1], subt[:,2], 'b--')
                plt.plot(subt[-1,1], subt[-1,2], color='r', marker='X')
                plt.annotate(str(int(subt[0,0])),
                             (subt[-1,1], subt[-1,2]),
                             textcoords="offset points",
                             xytext=(0,5),
                             ha='right')
        
            plt.xlim(min(ox)-2, max(ox)+2)
            plt.ylim(min(oy)-2, max(oy)+2)
            plt.title( "Movements at frame " + str(int(f)) )
        
            plt.pause(dt)
    
if __name__ == "__main__":
    
    output_dir ='../data/synthetic/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    mapSize = 10
    trajNum = 600
    firstFrame = 0
    trajs = genTrajSet(mapSize,trajNum,firstFrame) #list of [x,y,t]
    
    # # multi traj sets examples - for discrete group
    # t1 = genTrajSet(mapSize,3,0)
    # t2 = genTrajSet(mapSize,5,10)
    # t3 = genTrajSet(mapSize,4,20)
    # trajs = t1 + t2 +t3
    
    trajsWithId = [ np.c_[ (np.ones((len(trajs[i]),1))*i), trajs[i] ] for i in range(len(trajs))]
    userInfo = genInput(trajsWithId)
    
    # trajs: list of vari-length traj [idx,x,y,frame]
    data = np.vstack(trajsWithId)
    
    np.save(output_dir+'synthetic_mapSize'+str(mapSize)+'_trajsWithId'+'.npy', data)
    userInfo.to_csv(output_dir+'synthetic_mapSize'+str(mapSize)+'_userInfo'+'.csv',index=False)   
    
    dt = 0.3
    show_animation = True
    
    # plotPaths(userInfo, trajsWithId)
