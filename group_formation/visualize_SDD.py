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

def plotData(userInfo, trajsWithId, dt):

    ox = userInfo['ox'].tolist()
    oy = userInfo['oy'].tolist()

    oframe = userInfo['oframe'].tolist()
    dframe = userInfo['dframe'].tolist()
    
    frameRange = [min(oframe),max(dframe)]
    
    for f in np.arange(frameRange[0],frameRange[1]):
        
        existUser = userInfo[(userInfo['oframe']<=f) & (userInfo['dframe']>=f)]
        existUserId = existUser['track_id']
        existUserId = list(map(int,existUserId.tolist()))        
        existUserTraj = [trajsWithId[trajsWithId[:,0]==i] for i in existUserId]
        
        userTrajSoFar = []
        for t in existUserTraj:
            userTrajSoFar.append(t[t[:,3]<=f])            

        plt.cla()
        # plt.scatter(existUser['ox'].tolist(), existUser['oy'].tolist(), 
        #             color='g', marker='^')
        
        for subt in userTrajSoFar:
            # print(subt[0,0])
            plt.plot(subt[-3:,1], subt[-3:,2], 'b--')
            plt.scatter(subt[-1,1], subt[-1,2], s=10, color='r', marker='X')
            plt.annotate(str(int(subt[0,0])),
                         (subt[-1,1], subt[-1,2]),
                         textcoords="offset points",
                         xytext=(0,5),
                         ha='right')
    
        plt.xlim(min(ox)-2, max(ox)+2)
        plt.ylim(min(oy)-2, max(oy)+2)
        plt.title( "Before grouping - Movements at frame " + str(int(f)) )
    
        plt.pause(dt)
            
def plotResult_(windowsize, userInfo, trajsWithId, facils_loc, mut_frame, dt):

    ox = userInfo['ox'].tolist()
    oy = userInfo['oy'].tolist()
    # dx = userInfo['dx'].tolist()
    # dy = userInfo['dy'].tolist()
    oframe = userInfo['oframe'].tolist()
    dframe = userInfo['dframe'].tolist()
    
    frameRange = [min(oframe),max(dframe)]
    
    mut_frame.insert(0,windowsize)

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
        
        if f > frameRange[0]+windowsize and f<= mut_frame[-1]: # after historical data, start to have facils
            f_idx = np.argwhere(f>np.asarray(mut_frame)).ravel()[-1] - 1
            existFacils = facils_loc[f_idx]
            plt.scatter(existFacils[:,0], existFacils[:,1], 
                    s=100, color='orange', marker='o')
            
        plt.scatter(existUser['ox'].tolist(), existUser['oy'].tolist(), 
                    s = 10, color='g', marker='^')
        
        for subt in userTrajSoFar:
            # print(subt[0,0])
            plt.plot(subt[-3:,1], subt[-3:,2], 'b--')
            plt.scatter(subt[-1,1], subt[-1,2], s=10, color='r', marker='X')
            plt.annotate(str(int(subt[0,0])),
                          (subt[-1,1], subt[-1,2]),
                          textcoords="offset points",
                          xytext=(0,5),
                          ha='right')
    
        plt.xlim(min(ox)-2, max(ox)+2)
        plt.ylim(min(oy)-2, max(oy)+2)
        plt.title( "Movements at frame " + str(int(f)) )
    
        plt.pause(dt)
        
def plotResult(windowsize, userInfo, trajsWithId, facils, mutation, belong, dt, img_path):

    ox = userInfo['ox'].tolist()
    oy = userInfo['oy'].tolist()

    oframe = userInfo['oframe'].tolist()
    dframe = userInfo['dframe'].tolist()
    
    frameRange = [min(oframe),max(dframe)]
    
    # mutation.insert(len(mutation),max(dframe))

    # x = int(max(map(len,facils))) #use relatiev center number - center per period
    # # x = len(userInfo) # absolute center number: id-color
    # ys = [i+x+(i*x)**2 for i in range(x)]    
    # colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    # colors = np.random.permutation(colors)
    
    img = plt.imread(img_path)
    
    for f in np.arange(frameRange[0],frameRange[1],20):
        
        existUser = userInfo[(userInfo['oframe']<=f) & (userInfo['dframe']>=f)]
        existUserId = existUser['track_id']
        existUserId = list(map(int,existUserId.tolist()))        
        existUserTraj = [trajsWithId[trajsWithId[:,0]==i] for i in existUserId]
        
        userTrajSoFar = []
        for t in existUserTraj:
            userTrajSoFar.append(t[t[:,3]<=f])
            
        # start to plot
        plt.cla()
        plt.imshow(img)
        
        mut = np.asarray(mutation,dtype=int)
        period = np.argwhere(mut <= f).ravel()
        if len(period)>0:
            periodIdx = period[-1] # which period of facils 
            existFacils = np.vstack(facils[periodIdx])
            plt.scatter(existFacils[:,2], existFacils[:,3], 
                        s=80, color='orange', marker='o')            
            # plt.scatter(existUser['ox'].tolist(), existUser['oy'].tolist(), 
            #             s = 10, color='g', marker='^')
        
        for subt in userTrajSoFar:
            # print(subt[0,0])
            plt.plot(subt[-100:,1], subt[-100:,2], 'b--')
            plt.scatter(subt[-1,1], subt[-1,2], s=10, color='r', marker='X')
            plt.annotate(str(int(subt[0,0])),
                          (subt[-1,1], subt[-1,2]),
                          textcoords="offset points",
                          xytext=(0,5),
                          ha='right')
    
        plt.xlim(min(ox)-2, max(ox)+2)
        plt.ylim(min(oy)-2, max(oy)+2)
        plt.title( "Movements at frame " + str(int(f)) )
    
        plt.pause(dt)
        
        # mut = np.asarray(mutation,dtype=int)
        # period = np.argwhere(mut <= f).ravel()
        # if len(period)>0:
        #     periodIdx = period[-1] # which period of facils 
        #     existFacils = np.vstack(facils[periodIdx])
        #     plt.scatter(existFacils[:,2], existFacils[:,3], 
        #                 s=80, color='orange', marker='o')            
        #     # plt.scatter(existUser['ox'].tolist(), existUser['oy'].tolist(), 
        #     #             s = 10, color='g', marker='^')
        
        # for subt in userTrajSoFar:
        #     # print(subt[0,0])
        #     plt.plot(subt[-100:,1], subt[-100:,2], 'b--')
        #     plt.scatter(subt[-1,1], subt[-1,2], s=10, color='r', marker='X')
        #     plt.annotate(str(int(subt[0,0])),
        #                   (subt[-1,1], subt[-1,2]),
        #                   textcoords="offset points",
        #                   xytext=(0,5),
        #                   ha='right')
    
        # plt.xlim(min(ox)-2, max(ox)+2)
        # plt.ylim(min(oy)-2, max(oy)+2)
        # plt.title( "Movements at frame " + str(int(f)) )
    
        # plt.pause(dt)
            
if __name__ == "__main__":
    
    # synthetic data
    path = '../data/synthetic/'
    userInfo = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv', sep=',')
    trajsWithId = np.load(path + 'synthetic_mapSize10_trajsWithId.npy')
    dt = 0.3
    show_animation = True
    
    # # sdd - death circle - vido0
    # sample = 'deathCircle'
    # file = 'video0'
    # path = '../data/stanford_campus_dataset/processed/'+ sample +'/'    
    # userInfo = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
    # trajsWithId = np.load(path + sample +'_' + file +'_trajsWithId.npy')
    # dt = 0.01
    # show_animation = True   

    plotData(userInfo, trajsWithId, dt)
