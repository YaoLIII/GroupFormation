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
import matplotlib.pyplot as plt
# import visualize_SDD as V 

# read processed data
sample = 'deathCircle'
output_dir ='../data/stanford_campus_dataset/processed/'+ sample +'/'

files = os.listdir(output_dir)
# test:
file = files[0]
avg_info = files[1]
print('start to deal with '+ file + '...')

data = pd.read_csv(output_dir+file, delimiter=',')
avg_info = pd.read_csv(output_dir+avg_info, delimiter=',')

## convert df to numpy array
# replace type by numbers
user_type = data.type.unique()
type_dict = dict(zip(user_type, range(len(user_type))))
data = data.replace({'type':type_dict})
# [id, oframe, ox, oy, dframe, dx, dy, avg_v, type]
data = np.asarray(data.sort_values('oframe'))

# split data via waitting time or group member numbers
th_waiting = 50
th_group = 20

dimension = 2
openingcost = 100
numberofiterations = 664
windowsize = 50
file = 'test'

facils = F.DFL(data,dimension,openingcost,numberofiterations,5,windowsize,file,th_group,th_waiting)

facils_loc = [np.asarray(i)[:,2:4] for i in facils]
facil_frames = data[:,1][:len(facils)]
facil_info = [np.c_[facil_frames[i]*np.ones(len(facils_loc[i])).reshape((-1,1)),facils_loc[i]] for i in range(len(facils_loc))]
facil_info = np.asarray(facil_info)
# np.save(output_dir + 'facilities_result.npy', facils)

# V.plotResult(data, facils_loc, facil_frames)

# for i in facils[600:610]:
#     j = np.asarray(i)
#     plt.plot(j[:,2],j[:,3],'.')
        
        
