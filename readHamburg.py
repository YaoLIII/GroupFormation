# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:54:35 2020

@author: li
"""
import numpy as np
import pandas as pd
from pandas import read_csv

import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties

def readData(path="Federico/dump/"):

    df = read_csv(path + "Hamburg_dataset.csv")

    print(list(df.columns))
    data = pd.concat([df['user_id'], df['time_05']], axis=1)
    # data = data.fillna(0)
    print(np.unique(df.user_type)) #'car       ', 'cyclist   ', 'pedestrian'

    # dups_user_type = df.pivot_table(index=['user_type'], aggfunc='size')
    # print(dups_user_type)

    # car_id = np.unique(df.user_id[df['user_type'] == 'car       '].values)
    # cyc_id = np.unique(df.user_id[df['user_type'] == 'cyclist   '].values)
    # ped_id = np.unique(df.user_id[df['user_type'] == 'pedestrian'].values)
    
    # user_id = np.unique(df['user_id'].values)

    # # extract t,x,y,v,a of same user
    # data = [df.loc[df['user_id'] == id].iloc[:,[0,2,3,4,5,6]].values for id in user_id]
    # # the order of user is its id-10001
    # data_ped = [data[i] for i in ped_id-10001]
    # data_car = [data[i] for i in car_id-10001]
    # data_cyc = [data[i] for i in cyc_id-10001]
    
    return data

def main():
    print("enter main()")
    
    # read data
    data_dir = "Federico/dump/Hamburg_dataset.csv"
    df = pd.read_csv(data_dir)
    
    #
    # time.sleep(10)
    
    # create a figure
    fig, ax = plt.subplots()
    ax.set(xlim = (min(df['x_axis']),max(df['x_axis'])), \
           ylim = (min(df['y_axis']),max(df['y_axis'])))
    scat = ax.scatter(0,0)
    
    def animate(t):
        print("enter animate()")
        # global t
        t = (t+1000)
        print(t/1000)
        
        x = df.loc[df['time_05']==t/1000]['x_axis'].values.tolist()
        y = df.loc[df['time_05']==t/1000]['y_axis'].values.tolist()
        user_type = df.loc[df['time_05']==t/1000]['user_type'].values.tolist()        
        user_id = df.loc[df['time_05']==t/1000]['user_id'].values.tolist()
        
        ax.clear()
        tuples = tuple([x[k],y[k]] for k in range(len(x)))
        scat.set_offsets(tuples)
        
        for j in range(len(tuples)):
            ax.annotate(int(id[j]),tuples[j], size = 5)
            
        fontP = FontProperties()
        fontP.set_size('small')
            
        # define colormap and markers
        cmap = plt.cm.get_cmap("prism",len(np.unique(df['user_id'])))
        markers = ['^', 'o', 's']
        # markers[1]: triangle_up, pedestrians
        # markers[2]: circle, cyclists
        # markers[3]: square, vehicles
        
        for i,j in enumerate(user_id):
            if user_type[i] == 'pedestrian':
                m_idx = 0
            elif  user_type[i] == 'cyclist':
                m_idx = 1
            else:
                m_idx = 2
            ax.scatter(x[i],y[i],s = 50, c = cmap(i), marker = markers[m_idx])
        # display legend
        plt.scatter([], [], s=2.5, color='k', marker='^', label='ped')
        plt.scatter([], [], s=2.5, color='k', marker='o', label='cyc')
        plt.scatter([], [], s=2.5, color='k', marker='s', label='veh')
        plt.legend(loc='upper right', bbox_to_anchor=(1.05, 1.02))
        
    anim = animation.FuncAnimation(fig = ax, func = animate, frames = range(len(np.unique(df['time_05']))), \
                            interval = 100, repeat = False)
    plt.show()

if __name__ == "__main__":
    main()



