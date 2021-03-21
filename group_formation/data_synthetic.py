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
    
if __name__ == "__main__":
    
    mapSize = 30
    trajNum = 20
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

    xmin = min(data[:,1]-2)
    xmax = max(data[:,1]+2)
    ymin = min(data[:,2]-2)
    ymax = max(data[:,2]+2)
    
    # create canvas
    fig, ax = plt.subplots()    
    scat = ax.scatter(0,0)
    # flag = 0

    def update(t):
    
        x = data[data[:,3]==t][:,1].tolist()
        y = data[data[:,3]==t][:,2].tolist()
        # user_type = data[data[:,3]==t][:,-1].tolist()     
        user_id = data[data[:,3]==t][:,0].tolist()
        
        ax.clear()
        ax.set_title("Movements at frame " + str(t))
        ax.set_xlim(xmin,xmax)
        ax.set_ylim(ymin,ymax)
        tuples = tuple([x[k],y[k]] for k in range(len(x)))        
        scat.set_offsets(tuples)
            
        for j in range(len(tuples)):
            ax.annotate(int(user_id[j]),tuples[j], size = 10)
            
        # define colormap and markers
        # cmap = plt.cm.get_cmap("prism",len(np.unique(df['user_id'])))
        markers = ['^', 'o', 's','p','d','P']
        # markers[1]: triangle_up, pedestrians
        # markers[2]: circle, cyclists
        # markers[3]: square, vehicles
        
        for i,j in enumerate(user_id):
            ax.scatter(x[i],y[i],s = 50)
        
    anim = animation.FuncAnimation(fig, update, frames = len(np.unique(data[:,3])), \
                            interval = 200, repeat = True)
    plt.show()
