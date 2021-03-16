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

df = pd.read_csv(output_dir+file, delimiter=',')
df2 = pd.read_csv(output_dir+avg_info, delimiter=',')

# split data via waitting time
waiting = 20
f = 5


