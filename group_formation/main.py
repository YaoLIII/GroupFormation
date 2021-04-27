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
import collections

''' test with SDD dataset/deathcircle '''
sample = 'deathCircle'
file = 'video0'
path = '../data/stanford_campus_dataset/processed/'+ sample +'/'
img_path = '../data/stanford_campus_dataset/annotations/'+ sample + '/'+file+'/reference.jpg'

data = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
userType = data.type.unique() #replace string with num
userType_dict = dict(zip(userType , range(len(userType))))
data = data.replace({'type': userType_dict})
data = np.array(data.sort_values(by=['oframe']))

# userInfo = data, for visualization
userInfo = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
userInfo = userInfo.replace({'type': userType_dict})
userInfo = userInfo.sort_values(by=['oframe'])
trajsWithId = np.load(path + sample +'_' + file +'_trajsWithId.npy')

th_waiting = 900
openingcost = 200
windowsize = 10
file = '../result/result.txt'

# # with Hausdorff
# facils,mutation,belong = F.DFL(data,dimension,openingcost,5,windowsize,file,th_waiting,trajsWithId)
# with OD
facils,mutation,belong = F.DFL(data,openingcost,5,windowsize,file,th_waiting)
belong = np.vstack(belong) # [frame,userId,relativeCenterId]
facils_backup = copy.deepcopy(facils)

dt = 0.001

# print group info
mut = copy.deepcopy(mutation)
mut.append(max(userInfo['dframe']))

avgGroupSize = []
groupSize = []
compressRate = []
maxNumGroupMember = []
for i in range(len(mutation)):
    fRange = [mut[i],mut[i+1]]
    trajsInCP = belong[(belong[:,0]>=mut[i]) & (belong[:,0]<mut[i+1])] # trajs in current period
    relativeCenterId = np.unique(trajsInCP[:,2]).astype(int) #relative id of centers
    userNum = len(trajsInCP)
    maxNumGroupMember.append(max(collections.Counter(trajsInCP[:,2]).values()))
    groupSize.append(len(relativeCenterId))
    avgGroupSize.append(userNum/len(relativeCenterId))
    compressRate.append(1 - len(relativeCenterId)/userNum)
print('current average group size is: ' + str(sum(avgGroupSize)/len(mutation)))
print('current avg saving space rate is: ' + str(sum(compressRate)/len(mutation)))
print('minimum group size: ' + str(min(groupSize)))
print('maximum group size: ' + str(max(groupSize)))
print('the biggest group contains ' + str(max(maxNumGroupMember)) + ' members')

# calculate cost per update
result = pd.read_csv('../result/result.txt', header = None, delimiter = " ")
result.columns = ["updateId", "cost", "openedFacilsNum", "time"]
print('the cost per update: ' + str(result['cost'].mean()))

'''visualize'''
img = plt.imread(img_path)
lineStyle = ['solid','dotted','dashed','dashdot',(0, (3, 1, 1, 1)),(0, (5, 10))]
lineStyle_dict = dict(zip(range(len(userType)), lineStyle))
# currentFacils = copy.deepcopy(facils)
for i in range(len(mutation)):
    
    fRange = [mut[i],mut[i+1]]
    trajsInCP = belong[(belong[:,0]>=mut[i]) & (belong[:,0]<mut[i+1])] # trajs in current period
    relativeCenterId = np.unique(trajsInCP[:,2]).astype(int) #relative id of centers
    
    facilNumInCP = max(relativeCenterId) + 1  # num of facils in current period
    facilNumAll = list(map(len,facils))
    facilIdInCP = facilNumAll.index(facilNumInCP)
    facilsInCP = facils[facilIdInCP]
    facils = facils[facilIdInCP+1:]
    
    # gen color map
    x = len(facilsInCP)
    ys = [i+x+(i*x)**2 for i in range(x)]
    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    colors = np.random.permutation(colors)
    
    fLoc = np.vstack(facilsInCP)
    
    plt.title('Group results in Period '+ str(i) + ' (frame ' + str(fRange) + ')')
    plt.scatter(fLoc[:,2],fLoc[:,3], s=80, c=colors, marker='x')
    plt.imshow(img)
    
    for count,c in enumerate(relativeCenterId):
        trajGroup = trajsInCP[trajsInCP[:,2]==c][:,1]
        trajs = [trajsWithId[trajsWithId[:,0]==idx] for idx in trajGroup]
        for traj in trajs:
            idx = traj[0][0]
            userType = userInfo[userInfo['track_id']==idx].type.item()
            plt.plot(traj[:,1],traj[:,2],color=colors[c], 
                     linestyle=lineStyle_dict[userType])
    plt.pause(2)
    plt.cla()