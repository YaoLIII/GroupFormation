#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 13:20:54 2021
1. read SDD data: [$death circle] - generate processed data at folder 'processed/$deathCircle'
2. summerise the OD from all road users
3. calculate the mean velocity of all users
4. after process: senerio_index.csv [track_id oframe ox oy dframe ox dy av type]
@author: yaoli
"""
import os
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

sample = 'deathCircle'

path = '../data/stanford_campus_dataset/annotations/'+ sample +'/'

files = os.listdir(path)

output_dir ='../data/stanford_campus_dataset/processed/'+ sample +'/'
if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
for file in files:
        
    [annotations, background] = os.listdir(path + file)
    
    df = pd.read_csv(path+file+'/'+annotations, header=None, delimiter=' ')
    df.columns = ['track_id','xmin','ymin','xmax','ymax','frame','lost','occluded','generated','type']
    
    user_info = []
    
    for id in df['track_id'].unique():
        # 直接提取x y 含有多个重复坐标，需要根据 lost!=1/occluded/generated 进行筛选
        current_user = np.asarray(df[(df['track_id']==id) & (df['lost']!=1)])
        
        if len(current_user) > 1:   # has O&D
        
            t = current_user[0][-1]
            
            ox = (current_user[0][1] + current_user[0][3])*.5
            oy = (current_user[0][2] + current_user[0][4])*.5
            oframe = current_user[0][5]
            
            dx = (current_user[-1][1] + current_user[-1][3])*.5
            dy = (current_user[-1][2] + current_user[-1][4])*.5
            dframe = current_user[-1][5]
            
            x = (current_user[:,1] + current_user[:,3])*.5
            y = (current_user[:,2] + current_user[:,4])*.5
            # plt.plot(x,y,'o-')
            
            delta_xy = np.diff(np.asarray([x,y]).astype(float).T,axis = 0)
            traj_len = np.sum(np.sqrt((delta_xy**2).sum(axis = 1)))
            av = traj_len/(current_user[-1][5]-current_user[0][5])
            
            if av != 0:     #delete the user that never moves        
                info = [id, oframe, ox, oy, dframe, ox, dy, av, t]
                user_info.append(info)
            
    df1 = pd.DataFrame (user_info,columns=['track_id', 'oframe', 'ox', 'oy', 'dframe', 'dx', 'dy', 'av', 'type'])
    df1.to_csv(output_dir + file + '.csv', sep=',', header=True, index=False)
    
    # calculate the average speed of all types of road users
    av_table = []
    for user_type in df1['type'].unique():
        all_av = df1[df1['type']==user_type]['av']
        type_mean = all_av.mean()
        av_table.append([user_type,type_mean])
    df2 = pd.DataFrame (av_table,columns=['type','av'])
    df2.to_csv(output_dir + file + '_average_speed_' + '.csv', sep=',', header=True, index=False)
    
    # plot the OD data
    img = plt.imread( path + file + '/' + background )
    colors = {'Pedestrian':'red', 'Cart':'green', 'Biker':'blue', 'Skater':'yellow', 'Car':'grey', 'Bus':'purple'}
    
    fig, axs = plt.subplots(2)
    
    axs[0].set_title('Origin data of ' + sample + ' ' + file)
    axs[0].imshow(img)
    axs[0].scatter(df1['ox'],df1['oy'], c=df1['type'].map(colors),s = 3)
    
    axs[1].set_title('Destination data of ' + sample + ' ' + file)
    axs[1].imshow(img)
    axs[1].scatter(df1['dx'],df1['dy'], c=df1['type'].map(colors),s = 3)
    
    plt.show()
