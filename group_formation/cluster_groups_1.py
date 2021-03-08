#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 17:59:53 2020

@author: yaoli
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
# from matplotlib._png import read_png
# from matplotlib.cbook import get_sample_data
# from sklearn.cluster import DBSCAN
import math
from bisect import bisect


data_dir = "../data/Federico/dump/Hamburg_dataset.csv"
processed_dir = '../data/processed/'
sname = 'ODdata.csv'

def extractOD(data_dir, sname = 'ODdata.csv'):
    df = pd.read_csv(data_dir)
    user_id = pd.unique(df['user_id'])
    OD_data = []
    index_ = ['user_id','user_type','t_ori','x_ori','y_ori','t_des','x_des','y_des']
    for i in user_id:
        # i = 10001
        user_ori = df[df['user_id']==i].iloc[0,0:5]
        user_des = df[df['user_id']==i].iloc[-1,2:5]
        user_info = pd.concat([user_ori,user_des])        
        user_info.index = index_
        OD_data.append(user_info)
    OD_data = pd.DataFrame(OD_data)
    
    OD_data.to_csv(processed_dir + sname, index = False)
    
    return None
    
def plotODdata(data, user_type = None):
    
    if user_type:
        data = data[data['user_type']==user_type]
    
    # # visualization 3D
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(data['x_ori'], data['y_ori'], data['t_ori'], c = 'cyan')
    # # ax.scatter(data['x_des'], data['y_des'], data['t_des'], c = 'green')
    
    # ax.set_xlabel('X [m]')
    # ax.set_ylabel('Y [m]')
    # ax.set_zlabel('Time [s]')
    
    # visualization 2D
    fig, ax = plt.subplots()
    img = plt.imread("../fig/background_Bergedorf.png")
    
    xmin = min(data['x_ori'])
    xmax = max(data['x_ori'])
    ymin = min(data['y_ori'])
    ymax = max(data['y_ori'])
    
    # scat = ax.scatter(0,0)
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.imshow(img, extent=[xmin, xmax, ymin, ymax])
    ax.scatter(data['x_ori'],data['y_ori'], s=3)
    
    plt.show()
    
    return None

def initGroup(data, delta_t = 120, delta_s = 10):
    # delat_t: intervial in time [.5s*N], delta_s: interval regarding space [m]
    # test: data = ori
    range_t = [math.floor(min(data[:,2])), math.ceil(max(data[:,2]))]
    range_x = [math.floor(min(data[:,0])), math.ceil(max(data[:,0]))]
    range_y = [math.floor(min(data[:,1])), math.ceil(max(data[:,1]))]
    
    step_x = step_y = step_t = 0
    while step_x*delta_s < range_x[-1]-range_x[0]:
        step_x += 1
    while step_y*delta_s < range_y[-1]-range_y[0]:
        step_y += 1
    while step_t*delta_t < range_t[-1]-range_t[0]:
        step_t += 1
    # generate the vetex value of grid
    slice_t = np.linspace(range_t[0],delta_t*step_t+range_t[0],step_t+1)
    slice_x = np.linspace(range_x[0],delta_s*step_x+range_x[0],step_x+1)
    slice_y = np.linspace(range_y[0],delta_s*step_y+range_y[0],step_y+1)
    
    center_x = (slice_x + delta_s/2)[:-1]
    center_y = (slice_y + delta_s/2)[:-1]
    center_t = (slice_t + delta_t/2)[:-1]
    
    xx,yy,zz = np.meshgrid(center_x,center_y,center_t)
    # 2D grid visualization
    xx,yy = np.meshgrid(slice_x,slice_y)
    plt.plot(xx, yy, color='k') # use plot, not scatter
    plt.plot(np.transpose(xx), np.transpose(yy), marker='.', color='k') # add this here
    plt.show()

    # locate OD data at spatial-temporal cube (dict:{(idx,idy,idt):user_id})
    location = {}
    for count, point in enumerate(data):
        x = point[0]
        y = point[1]
        t = point[2]
        
        loc = (center_x[bisect(slice_x,x)-1],center_y[bisect(slice_y,y)-1],center_t[bisect(slice_t,t)-1])
        
        if loc in location:        
            location[loc].append(count)
        else:
            location[loc] = [count]
    # visualization - 2D
    # k = len(location)
    k = max([len(i) for i in location.values()])
    r = np.arange(k)
    ys = [i+r+(i*r)**2 for i in range(k)]    
    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for count, group in enumerate(location):
        ## SHOW THE 3D LOCATION OF INDIVIDUAL POINTS
        # idx = location[group]
        # users = data[idx]
        # ax.scatter(users[:,0], users[:,1], users[:,2], color = colors[count])    
        # SHOW THE SIZE OF A CLUSTER OF POINTS
        marker_size = len(location[group])
        ax.scatter(group[0], group[1], group[2], color = colors[marker_size%(len(colors))], s=marker_size*3)
    
    # fn = "../fig/background_Bergedorf.png"
    # arr = read_png(fn)
    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Time [s]')
    
    plt.show()
    
    return location

if __name__ == "__main__":
    
    # extractOD(data_dir, sname = 'ODdata.csv')
    data = pd.read_csv(processed_dir + sname)
    
    # cyc = df[df['user_type']=='cyclist   ']
    # ped = df[df['user_type']=='pedestrian']
    # veh = df[df['user_type']=='car       ']
    plotODdata(data,'pedestrian')
    
    ori = np.asarray(data.iloc[:,[3,4,2]])
    des = np.asarray(data.iloc[:,[6,7,5]])
    # ori[:,2] = ori[:,2]/50
    
    locO = initGroup(ori, delta_t = 900, delta_s = 10)
    locD = initGroup(des, delta_t = 900, delta_s = 10)
    
    o = [*locO]
    d = [*locD]
    
    # # Try to cluster with DBSCAN - fail
    # model = DBSCAN(eps=2, min_samples=5)
    # model.fit_predict(ori)
    # pred = model.fit_predict(ori)
    # label = model.labels_
    
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter(ori[:,0], ori[:,1], ori[:,2], c=model.labels_)
    # ax.view_init(azim=200)
    # plt.show()
    
    # print("number of cluster found: {}".format(len(set(model.labels_))))
    # print('cluster for each point: ', model.labels_)
    

