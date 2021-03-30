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
data = np.array(data)
# split data via waitting time or group member numbers
th_waiting = 5
th_group = 15

dimension = 2
openingcost = 4
numberofiterations = len(data)
windowsize = 20
file = 'test'

facils,mutation = F.DFL(data,dimension,openingcost,numberofiterations,5,windowsize,file,th_group,th_waiting)
facils_loc = [np.unique((np.asarray(i)[:,2:4]),axis=0) for i in facils]

path = '../data/synthetic/'
userInfo = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv', sep=',')
trajsWithId = np.load(path + 'synthetic_mapSize10_trajsWithId.npy')

ox = userInfo['ox'].tolist()
oy = userInfo['oy'].tolist()
# dx = userInfo['dx'].tolist()
# dy = userInfo['dy'].tolist()
oframe = userInfo['oframe'].tolist()
dframe = userInfo['dframe'].tolist()

frameRange = [min(oframe),max(dframe)]

mut = np.asarray(mutation)
mut = np.insert(mut,0,0)
mut = np.insert(mut,len(mut),max(dframe))

# x = max(map(len,facils_loc))
# ys = [i+x+(i*x)**2 for i in range(x)]

# colors = cm.rainbow(np.linspace(0, 1, len(ys)))
# s_color = np.random.permutation(colors)

userPerPeriod = []
for period in range(len(facils)):
    centers = facils[period]
    existUsers = userInfo[(userInfo['oframe']>=mut[period]) & (userInfo['oframe']<mut[period+1])]
    print(len(existUsers))
    centerIds = []
    for user in np.asarray(existUsers):
        _,centerId = F.closest_node_dist(user, centers)
        centerIds.append((user[0],centers[centerId][0])) #(user_id,its_center)
    userPerPeriod.append(centerIds)

for f in np.arange(frameRange[0],frameRange[1]):
    
    existUser = userInfo[(userInfo['oframe']<=f) & (userInfo['dframe']>=f)]
    existUserId = existUser['track_id']
    existUserId = list(map(int,existUserId.tolist()))
    
    allTrajs = np.vstack(trajsWithId)
    existUserTraj = [allTrajs[allTrajs[:,0]==i] for i in existUserId]
    
    userTrajSoFar = []
    for t in existUserTraj:
        userTrajSoFar.append(t[t[:,3]<=f])            

    f_loc = facils_loc[np.where(np.asarray(mut)<=f)[0][-1]]

# extract users which has the same center
centers = []
for pt in data:
    _,centerIdx = closest_node_dist(pt, facilities)
    centers.append(centerIdx)
 
group = []
plt.figure()   
for c in np.unique(centers):
    # users belongs to same group
    groupId = np.argwhere(centers==c).ravel()
    group.append(groupId)
    for idx in groupId:
        # extract user trajectory
        user = trajsWithId[np.argwhere(trajsWithId[:,0]==idx).ravel()]
        plt.xlim(-1, 11)
        plt.ylim(-1, 11)
        plt.plot(user[:,1],user[:,2],'*-')
    plt.pause(0.5)
    plt.cla()

dt = 0.3
show_animation = True
    
VS.plotPaths(userInfo, trajsWithId, facils_loc, mutation, dt, show_animation)

# # test with synthetic dataset but dimention = 6 #[of,ox,oy,dx,dy,av]
# path = '../data/synthetic/'
# data = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv',sep=',')
# data = np.array(data.iloc[:,[1,2,3,5,6,7]]) #[of,ox,oy,dx,dy,av]
# # data = np.array(data.iloc[:,[2,3]]) 

# dimension = 6
# openingcost = 0.0001
# numberofiterations = 600
# windowsize = 10
# file = 'test'

# listofzeros = [0]*dimension
# newlist=data
# for x in newlist:
#     for i in range(0,dimension):
#         listofzeros[i]+=x[i]
# averages = [0]*dimension
# for i in range(0,dimension):
#     averages[i]=listofzeros[i]/numberofiterations
# variances = [0]*dimension
# for x in newlist:
#     for i in range(0,dimension):
#         variances[i]+=(x[i]-averages[i])**2

# for i in range(0,dimension):
#     variances[i]=math.sqrt(variances[i])

# for x in newlist:
#     for i in range(0,dimension):
#         x[i]=(x[i]-averages[i])/variances[i]
# print('first two rows:',newlist[0:2])    
# #print(newlist)    
# array = np.asarray(newlist)

# f2 = MS.DFL(array,dimension,openingcost,numberofiterations,5,windowsize,file)

# facils = []
# for i in f2:
#     facils.append([np.argwhere((array == j).all(axis=1)).ravel() for j in i])

# data = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv',sep=',')
# data = np.array(data.iloc[:,[1,2,3,5,6,7]]) #[of,ox,oy,dx,dy,av]
# t = data[np.asarray(facils).ravel()]

# plt.plot(t[:,1],t[:,2],'*')



# facil_info = [np.c_[facil_frames[i]*np.ones(len(facils_loc[i])).reshape((-1,1)),facils_loc[i]] for i in range(len(facils_loc))]
# facil_info = np.asarray(facil_info)



# np.save(output_dir + 'facilities_result.npy', facils)

# V.plotResult(data, facils_loc, facil_frames)

# for i in facils[600:610]:
#     j = np.asarray(i)
#     plt.plot(j[:,2],j[:,3],'.')
        
        
