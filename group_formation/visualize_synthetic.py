# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:05:20 2021

@author: li
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# import matplotlib.animation as animation
# from matplotlib.font_manager import FontProperties

def plotData(userInfo, trajsWithId, dt, show_animation):

    ox = userInfo['ox'].tolist()
    oy = userInfo['oy'].tolist()

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
            
        if show_animation:
            plt.cla()
            plt.scatter(existUser['ox'].tolist(), existUser['oy'].tolist(), 
                        color='g', marker='^')
            
            for subt in userTrajSoFar:
                # print(subt[0,0])
                plt.plot(subt[:,1], subt[:,2], 'b--')
                plt.plot(subt[-1,1], subt[-1,2], color='r', marker='X')
                plt.annotate(str(int(subt[0,0])),
                             (subt[-1,1], subt[-1,2]),
                             textcoords="offset points",
                             xytext=(0,5),
                             ha='right')
        
            plt.xlim(min(ox)-2, max(ox)+2)
            plt.ylim(min(oy)-2, max(oy)+2)
            plt.title( "Before grouping - Movements at frame " + str(int(f)) )
        
            plt.pause(dt)
            
def plotResult(userInfo, trajsWithId, facils_loc, mut, dt):

    ox = userInfo['ox'].tolist()
    oy = userInfo['oy'].tolist()
    # dx = userInfo['dx'].tolist()
    # dy = userInfo['dy'].tolist()
    oframe = userInfo['oframe'].tolist()
    dframe = userInfo['dframe'].tolist()
    
    frameRange = [min(oframe),max(dframe)]

    # x = int(max(map(len,facils_loc))) #use relatiev center number - center per period
    # # x = len(userInfo) # absolute center number: id-color
    # ys = [i+x+(i*x)**2 for i in range(x)]
    
    # colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    # colors = np.random.permutation(colors)
    
    for f in np.arange(frameRange[0],frameRange[1]):
        
        existUser = userInfo[(userInfo['oframe']<=f) & (userInfo['dframe']>=f)]
        existUserId = existUser['track_id']
        existUserId = list(map(int,existUserId.tolist()))
        
        allTrajs = np.vstack(trajsWithId)
        existUserTraj = [allTrajs[allTrajs[:,0]==i] for i in existUserId]
        
        userTrajSoFar = []
        for t in existUserTraj:
            userTrajSoFar.append(t[t[:,3]<=f])
            
        # start to plot
        plt.cla()
        plt.scatter(existUser['ox'].tolist(), existUser['oy'].tolist(), 
                    color='g', marker='^')
        
        for subt in userTrajSoFar:
            print(subt[0,0])
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
    
    path = '../data/synthetic/'
    userInfo = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv', sep=',')
    trajsWithId = np.load(path + 'synthetic_mapSize10_trajsWithId.npy')
    
    dt = 0.3
    show_animation = True
    
    plotData(userInfo, trajsWithId, dt, show_animation)
