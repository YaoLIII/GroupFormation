# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. read processed data
2. give data as a streaming
3. dynamic clustering

results:
    mutation: since frame [], facils start to change,only recompute & update
    facils: corresp to mutation
    belong: also includes 'too close' case, so has more item 

@author: yaoli
"""
import pandas as pd
import numpy as np
import random
import copy
# import function_similarity_Hausdorff as F
import function as F
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import visualize_synthetic as VS 
import visualize_SDD as VSDD 

''' test with SDD dataset/deathcircle '''
sample = 'deathCircle'
file = 'video0'
path = '../data/stanford_campus_dataset/processed/'+ sample +'/'
img_path = '../data/stanford_campus_dataset/annotations/'+ sample + '/'+file+'/reference.jpg'

data = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
userType = data.type.unique() #replace string with num
userType_dict = dict(zip(userType , range(len(userType ))))
data = data.replace({'type': userType_dict})
data = np.array(data.sort_values(by=['oframe']))

# userInfo = data, for visualization
userInfo = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
userInfo = userInfo.replace({'type': userType_dict})
userInfo = userInfo.sort_values(by=['oframe'])
trajsWithId = np.load(path + sample +'_' + file +'_trajsWithId.npy')

th_waiting = 200
openingcost = 200
windowsize = 30
file = 'result_sdd_ownMethod.txt'

# # with Hausdorff
# facils,mutation,belong = F.DFL(data,dimension,openingcost,5,windowsize,file,th_waiting,trajsWithId)
# with OD
facils,mutation,belong = F.DFL(data,openingcost,5,windowsize,file,th_waiting)
belong = np.vstack(belong) # [frame,userId,relativeCenterId]

dt = 0.001
# VSDD.plotResult(windowsize, userInfo, trajsWithId, facils, mutation, belong, dt, img_path)

# # print group info
# mut = copy.deepcopy(mutation)
# mut.append(max(userInfo['dframe']))

# avgGroupSize = []
# groupSize = []
# for i in range(len(mutation)):
#     fRange = [mut[i],mut[i+1]]
#     trajsInCP = belong[(belong[:,0]>=mut[i]) & (belong[:,0]<mut[i+1])] # trajs in current period
#     relativeCenterId = np.unique(trajsInCP[:,2]).astype(int) #relative id of centers
#     userNum = len(trajsInCP)
#     groupSize.append(len(relativeCenterId))
#     avgGroupSize.append(userNum/len(relativeCenterId))
# print('current average group size is: ' + str(sum(avgGroupSize)/len(mutation)))
# min(groupSize)
# max(groupSize)

# '''visualize with one period - sdd''
mut = copy.deepcopy(mutation)
mut.append(max(userInfo['dframe']))

img = plt.imread(img_path)

for i in range(len(mutation)):
    fRange = [mut[i],mut[i+1]]
    trajsInCP = belong[(belong[:,0]>=mut[i]) & (belong[:,0]<mut[i+1])] # trajs in current period
    relativeCenterId = np.unique(trajsInCP[:,2]).astype(int) #relative id of centers
    # gen color map    
    x = len(facils[i])
    ys = [i+x+(i*x)**2 for i in range(x)]
    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    colors = np.random.permutation(colors)
    
    fLoc = np.vstack(facils[i])[relativeCenterId] # just plot facils for new coming users
    
    plt.title('Group results in Period '+ str(i) + ' (frame ' + str(fRange) + ')')
    plt.scatter(fLoc[:,2],fLoc[:,3], s=80, c=colors[relativeCenterId], marker='x')
    plt.imshow(img)
    
    for count,c in enumerate(relativeCenterId):
        trajGroup = trajsInCP[trajsInCP[:,2]==c][:,1]
        trajs = [trajsWithId[trajsWithId[:,0]==idx] for idx in trajGroup]
        for traj in trajs:
            plt.plot(traj[:,1],traj[:,2],color=colors[c])
    plt.pause(2)
    plt.cla()


# ''' test with synthetic data'''

# path = '../data/synthetic/'

# data = pd.read_csv(path + 'synthetic_mapSize12_userInfo.csv',sep=',')
# data = np.array(data.sort_values(by=['oframe']))

# userInfo = pd.read_csv(path + 'synthetic_mapSize12_userInfo.csv', sep=',')
# trajsWithId = np.load(path + 'synthetic_mapSize12_trajsWithId.npy')

# # split data via waitting time or group member numbers
# th_waiting = 15 # max(f_t) = mapSize*8 /(opencost/2)
# openingcost = 4
# # numberofiterations = len(data)
# windowsize = 30
# file = 'result_syn'

# # # with Hausdorff
# # facils,mutation,belong = F.DFL(data,dimension,openingcost,5,windowsize,file,th_waiting,trajsWithId)
# # with OD
# facils,mutation,belong = F.DFL(data,openingcost,5,windowsize,file,th_waiting)
# belong = np.vstack(belong) # [frame,userId,relativeCenterId]
# dt = 0.3
# # VS.plotResult(windowsize, userInfo, trajsWithId, facils, mutation, belong, dt) 

# # '''visualize with one period - synthetic''
# mut = copy.deepcopy(mutation)
# mut.append(max(userInfo['dframe']))

# for i in range(len(mutation)):
#     fRange = [mut[i],mut[i+1]]
#     trajsInCP = belong[(belong[:,0]>=mut[i]) & (belong[:,0]<mut[i+1])] # trajs in current period
#     relativeCenterId = np.unique(trajsInCP[:,2]).astype(int) #relative id of centers
#     # gen color map    
#     x = len(facils[i])
#     ys = [i+x+(i*x)**2 for i in range(x)]
#     colors = cm.rainbow(np.linspace(0, 1, len(ys)))
#     colors = np.random.permutation(colors)
    
#     fLoc = np.vstack(facils[i])[relativeCenterId] # just plot facils for new coming users
    
#     plt.title('Group results in Period '+ str(i) + ' (frame ' + str(fRange) + ')')
#     plt.scatter(fLoc[:,2],fLoc[:,3], s=80, c=colors[relativeCenterId], marker='o')
    
#     for count,c in enumerate(relativeCenterId):
#         trajGroup = trajsInCP[trajsInCP[:,2]==c][:,1]
#         trajs = [trajsWithId[trajsWithId[:,0]==idx] for idx in trajGroup]
#         for traj in trajs:
#             plt.plot(traj[:,1],traj[:,2],color=colors[c])
#     plt.pause(1)
#     plt.cla()