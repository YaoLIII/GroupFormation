#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. read processed data
2. give data as a streaming
3. dynamic clustering

@author: yaoli
"""
import pandas as pd
import numpy as np
import os
import time
import random
# import function_similarity_Hausdorff as F
import function as F
import MeyersonS as MS
import matplotlib.pyplot as plt
import math
import visualize_synthetic as VS 

''' test with SDD dataset/deathcircle '''
sample = 'deathCircle'
file = 'video0'
path = '../data/stanford_campus_dataset/processed/'+ sample +'/'

data = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
userType = data.type.unique() #replace string with num
userType_dict = dict(zip(userType , range(len(userType ))))
data = data.replace({'type': userType_dict})
data = np.array(data.sort_values(by=['oframe']))

userInfo = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
trajsWithId = np.load(path + sample +'_' + file +'_trajsWithId.npy')

th_waiting = 200

dimension = 2
openingcost = 200
numberofiterations = len(data)
windowsize = 30
file = 'test'


# ''' test with synthetic data'''

# path = '../data/synthetic/'

# data = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv',sep=',')
# data = np.array(data.sort_values(by=['oframe']))

# userInfo = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv', sep=',')
# trajsWithId = np.load(path + 'synthetic_mapSize10_trajsWithId.npy')

# # split data via waitting time or group member numbers
# th_waiting = 15
# dimension = 2 # max(f_t) = mapSize*8 /(opencost/2)
# openingcost = 8
# numberofiterations = len(data)
# windowsize = 30
# file = 'test'

facils,mutation,belong = F.DFL(data,dimension,openingcost,numberofiterations,5,windowsize,file,th_waiting)
# facils,mutation,belong = F.DFL(data,dimension,openingcost,numberofiterations,5,windowsize,file,th_waiting,trajsWithId)

# # mutation is the frame f each time facils update
# mutation.insert(0,data[windowsize-1,1]) # at windowsize, the first set of facils appear
# mutation = np.unique(mutation)
# mut_frame = list(map(int,mutation))

# mutation = list(map(int,mutation))
# mut_frame = [data[i,1] for i in mutation] # find the frame according to data order
# !!! 这里报错，肯定是mutation的idx和内容弄混了，需要重新检查可视化逻辑。另外，sdd数据库非常分散，可能效果不如synthetic好

# # 每次变化对应的 facil 
# len_facil = list(map(len,facils))
# len_facil.insert(0,0)
# mut_facil = np.argwhere(np.diff(len_facil)!=0).ravel() # facils[mut_facil] when new facils are introduced
# # mut_facil = np.insert(mut_facil,0,0)
# # mut = np.insert(mut,len(mut),max(userInfo['dframe']))

# 每次变化对应的从属关系 belong
lenf = np.asarray(list(map(len,belong)))
recompute = list(np.argwhere(lenf>2).ravel())
split = [belong[i:j] for i, j in zip([0]+recompute, recompute+[None])]

period = [] # list of [id, relative center id]
colornum = 0 # max number of centers for all period
for i in split:
    if len(i)>0:
        period.append(np.vstack(i))
        cnum = len(np.unique(np.vstack(i)[:,1]))
        if cnum > colornum:
            colornum = cnum
        
for i in period: # each recompute to next recompute is called period
    plt.figure()
    for j in np.unique(i[:,1]): # j is group index in current period
        currentgroupid = [i[k][0] for k in np.argwhere(i[:,1]==j).ravel()]
        trajs = [trajsWithId[trajsWithId[:,0]==idx][:,1:3] for idx in currentgroupid]
        for t in trajs:
            plt.plot(t[:,0],t[:,1])
            plt.xlim(-1, 11)
            plt.ylim(-1, 11)
        plt.pause(1)
        plt.cla()

facils_dedup = [facils[i] for i in mut_facil]
facils_loc = [np.unique((np.asarray(i)[:,2:4]),axis=0) for i in facils_dedup]

dt = 0.3
# VS.plotResult(windowsize, userInfo, trajsWithId, facils_loc, mut_frame, dt)
        
        
