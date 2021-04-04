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
import function as F
import MeyersonS as MS
import matplotlib.pyplot as plt
import math
import visualize_synthetic as VS 

# # test with SDD dataset/deathcircle
# sample = 'deathCircle'
# output_dir ='../data/stanford_campus_dataset/processed/'+ sample +'/'

# files = os.listdir(output_dir)
# # test:
# file = files[0]
# avg_info = files[1]
# print('start to deal with '+ file + '...')

# data = pd.read_csv(output_dir+file, delimiter=',')
# avg_info = pd.read_csv(output_dir+avg_info, delimiter=',')

# ## convert df to numpy array
# # replace type by numbers
# user_type = data.type.unique()
# type_dict = dict(zip(user_type, range(len(user_type))))
# data = data.replace({'type':type_dict})
# # [id, oframe, ox, oy, dframe, dx, dy, avg_v, type]
# data = np.asarray(data.sort_values('oframe'))

# test with synthetic data
path = '../data/synthetic/'

data = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv',sep=',')
data = np.array(data.sort_values(by=['oframe']))

userInfo = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv', sep=',')
trajsWithId = np.load(path + 'synthetic_mapSize10_trajsWithId.npy')

# split data via waitting time or group member numbers
th_waiting = 40

# 可以根据 mapSize*8 /(opencost/2) 算出大概同时存在最多fac数目
dimension = 2
openingcost = 20
numberofiterations = len(data)
windowsize = 30
file = 'test'

facils,mutation,belong = F.DFL(data,dimension,openingcost,numberofiterations,5,windowsize,file,th_waiting)
# mutation is every upperbound for data index
mutation.insert(0,windowsize) # at windowsize, the first set of facils appear
mutation = list(map(int,mutation))
mut_frame = [data[i,1] for i in mutation] # find the frame according to data order

mut_facil = np.argwhere(np.diff(list(map(len,facils)))!=0).ravel() # when new facils are introduced
# mut_facil = np.insert(mut_facil,0,0)
# mut = np.insert(mut,len(mut),max(userInfo['dframe']))
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
        
# for i in period: # each recompute to next recompute is called period
#     plt.figure()
#     for j in np.unique(i[:,1]): # j is group index in current period
#         currentgroupid = [i[k][0] for k in np.argwhere(i[:,1]==j).ravel()]
#         trajs = [trajsWithId[trajsWithId[:,0]==idx][:,1:3] for idx in currentgroupid]
#         for t in trajs:
#             plt.plot(t[:,0],t[:,1])
#             plt.xlim(-1, 11)
#             plt.ylim(-1, 11)
#         plt.pause(1)
#         plt.cla()


facils_dedup = [facils[i] for i in mut_facil]
facils_loc = [np.unique((np.asarray(i)[:,2:4]),axis=0) for i in facils_dedup]

dt = 0.3
VS.plotResult(windowsize, userInfo, trajsWithId, facils_loc, mut_frame, dt)
        
        
