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
data = np.asarray(data)

# split data via waitting time
waiting = 20
f = 5


