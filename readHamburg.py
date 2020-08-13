# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:54:35 2020

@author: li
"""
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt

path = "Federico/dump/"
df = read_csv(path + "Hamburg_dataset.csv")

print(list(df.columns))
print(np.unique(df.user_type)) #'car       ', 'cyclist   ', 'pedestrian'

# dups_user_type = df.pivot_table(index=['user_type'], aggfunc='size')
# print(dups_user_type)

car_id = np.unique(df.user_id[df['user_type'] == 'car       '].values)
cyc_id = np.unique(df.user_id[df['user_type'] == 'cyclist   '].values)
ped_id = np.unique(df.user_id[df['user_type'] == 'pedestrian'].values)

user_id = np.unique(df['user_id'].values)

# extract t,x,y,v,a of same user
data = [df.loc[df['user_id'] == id].iloc[:,2:].values for id in user_id]
# the order of user is its id-10001
tpdata = [data[i] for i in ped_id-10001]

for i in tpdata:
    plt.plot(i[:,1],i[:,2])
