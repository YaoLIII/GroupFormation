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
# import visualize_SDD as V 

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

## test with synthetic data
# path = '../data/synthetic/'
# data = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv',sep=',')
# data = np.array(data)
# # split data via waitting time or group member numbers
# th_waiting = 50
# th_group = 20

# dimension = 2
# openingcost = 8
# numberofiterations = 600
# windowsize = 10
# file = 'test'

# facils,mutation = F.DFL(data,dimension,openingcost,numberofiterations,5,windowsize,file,th_group,th_waiting)
# facils_loc = [np.unique((np.asarray(i)[:,2:4]),axis=0) for i in facils]




# test with synthetic dataset but dimention = 3
path = '../data/synthetic/'
data = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv',sep=',')
data = np.array(data.iloc[:,[0,2,3,5,6,7]]) #[of,ox,oy,dx,dy,av]

dimension = 6
openingcost = 6
numberofiterations = 600
windowsize = 10
file = 'test'

listofzeros = [0]*dimension
newlist=data
for x in newlist:
    for i in range(0,dimension):
        listofzeros[i]+=x[i]
averages = [0]*dimension
for i in range(0,dimension):
    averages[i]=listofzeros[i]/numberofiterations
variances = [0]*dimension
for x in newlist:
    for i in range(0,dimension):
        variances[i]+=(x[i]-averages[i])**2

for i in range(0,dimension):
    variances[i]=math.sqrt(variances[i])

for x in newlist:
    for i in range(0,dimension):
        x[i]=(x[i]-averages[i])/variances[i]
print('first two rows:',newlist[0:2])    
#print(newlist)    
array = np.asarray(newlist)

f2 = MS.DFL(array,dimension,openingcost,numberofiterations,5,windowsize,file)

# facil_info = [np.c_[facil_frames[i]*np.ones(len(facils_loc[i])).reshape((-1,1)),facils_loc[i]] for i in range(len(facils_loc))]
# facil_info = np.asarray(facil_info)



# np.save(output_dir + 'facilities_result.npy', facils)

# V.plotResult(data, facils_loc, facil_frames)

# for i in facils[600:610]:
#     j = np.asarray(i)
#     plt.plot(j[:,2],j[:,3],'.')
        
        
