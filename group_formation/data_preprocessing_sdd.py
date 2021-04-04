#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. read SDD data: [$death circle] - generate processed data at folder 'processed/$deathCircle'
2. summerise the OD from all road users
3. calculate the mean velocity of all users
4. after process: senerio_index.csv [track_id oframe ox oy dframe ox dy av type]

trajsWithId - np.array [idx,x,y,frame]
userInfo - pd.dataframe ['track_id', 'oframe', 'ox', 'oy', 'dframe', 'dx', 'dy', 'av', 'type']

@author: yaoli
"""
import os
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

sample = 'deathCircle'
path = '../data/stanford_campus_dataset/annotations/'+ sample +'/'
output_dir ='../data/stanford_campus_dataset/processed/'+ sample +'/'
if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
files = os.listdir(path)
      
for file in files:
        
    [dataName, bgImg] = os.listdir(path + file)
    
    df = pd.read_csv(path+file+'/'+dataName, header=None, delimiter=' ')
    df.columns = ['track_id','xmin','ymin','xmax','ymax','frame','lost','occluded','generated','type']
    
    userInfo = []
    trajsWithId = []
    
    for idx in df['track_id'].unique():
        # x, y include several repeated coordinates，filter: lost!=1/occluded/generated!=0 
        current_user = df[(df['track_id']==idx) & (df['lost']!=1) & (df['generated']!=0)]
        
        if len(current_user) > 1:   # has O&D
        
            userType = current_user['type'].iloc[0]
            
            ox = (current_user['xmin'].iloc[0] + current_user['xmax'].iloc[0])*.5
            oy = (current_user['ymin'].iloc[0] + current_user['ymax'].iloc[0])*.5
            oframe = current_user['frame'].iloc[0]
            
            dx = (current_user['xmin'].iloc[-1] + current_user['xmax'].iloc[-1])*.5
            dy = (current_user['ymin'].iloc[-1] + current_user['ymax'].iloc[-1])*.5
            dframe = current_user['frame'].iloc[-1]
            
            x = ((current_user['xmin'] + current_user['xmax'])*.5).to_numpy(dtype=float)
            y = ((current_user['ymin'] + current_user['ymax'])*.5).to_numpy(dtype=float)
            frame = current_user['frame'].to_numpy()
            n = len(x)
            # plt.plot(x,y,'o-')
            # plt.axis('equal')
            
            delta_xy = np.diff(np.asarray([x,y]).astype(float).T,axis = 0)
            traj_len = np.sum(np.sqrt((delta_xy**2).sum(axis = 1)))
            av = traj_len/(dframe-oframe)
            
            if av != 0:     #delete the user that never moves        
                info = [idx, oframe, ox, oy, dframe, ox, dy, av, userType]
                userInfo.append(info)
                trajsWithId.append(np.c_[np.ones(n)*idx,x,y,frame])
            
    userInfo = pd.DataFrame(userInfo,columns=['track_id', 'oframe', 'ox', 'oy', 'dframe', 'dx', 'dy', 'av', 'type'])
    userInfo.to_csv(output_dir + sample +'_' + file + '_userInfo.csv', sep=',', header=True, index=False)
    
    trajsWithId = np.vstack(trajsWithId)
    np.save(output_dir + sample +'_' + file +'_trajsWithId.npy', trajsWithId)
    
    # # calculate the average speed of all types of road users
    # av_table = []
    # for user_type in userInfo['type'].unique():
    #     all_av = userInfo[userInfo['type']==user_type]['av']
    #     type_mean = all_av.mean()
    #     av_table.append([user_type,type_mean])
    # df2 = pd.DataFrame (av_table,columns=['type','av'])
    # df2.to_csv(output_dir + file + '_average_speed_' + '.csv', sep=',', header=True, index=False)
    
    # # plot the OD data
    # img = plt.imread( path + file + '/' + bgImg )
    # colors = {'Pedestrian':'red', 'Cart':'green', 'Biker':'blue', 'Skater':'yellow', 'Car':'grey', 'Bus':'purple'}
    
    # fig, axs = plt.subplots(2)
    
    # axs[0].set_title('Origin data of ' + sample + ' ' + file)
    # axs[0].imshow(img)
    # axs[0].scatter(userInfo['ox'],userInfo['oy'], c=userInfo['type'].map(colors),s = 3)
    
    # axs[1].set_title('Destination data of ' + sample + ' ' + file)
    # axs[1].imshow(img)
    # axs[1].scatter(userInfo['dx'],userInfo['dy'], c=userInfo['type'].map(colors),s = 3)
    
    # plt.show()
