# -*- coding: utf-8 -*-*
"""
Created on Thu Dec 20 13:25:24 2018
Read group label

@author: cheng
"""
import pandas as pd
import time
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties

t = 100000

def main():
    # Get scale
    dis_pixel = np.sqrt(np.square(338.2 - 387.1) + np.square(1400.6 - 1000.2))
    scale = 19.04/dis_pixel
    print('dis_pixel:', dis_pixel)
    yaxis = [round(scale*y, 1) for y in [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600]]
    xaxis = [round(scale*x, 1) for x in [0, 500]]
    print(xaxis)
    print(yaxis)
    
    data_dir = 'data/userinfo_416.csv'
    label = get_label(data_dir)
    print(label)
    
    # Read the trajectory data
    df=pd.read_csv('data/UniHannover_416_original_target_coordinates.csv')
    
    # Define time counter
    time.sleep(10)   # Delays for 5 seconds. You can also use a float value.
        
    # Create the fig
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 767), ylim=(0, 1761))
    scat = ax.scatter(0, 0)
    
    def animate(i):
        global t
        t=(t+1000)
        print(t/1000)
        x=df.loc[df['time_step'] == t/1000]['x_axis'].values.tolist()
    
        y=df.loc[df['time_step'] ==t/1000]['y_axis'].values.tolist()
        
        user_type = df.loc[df['time_step']==t/1000]['user_type'].values.tolist()
    
        id=df.loc[df['time_step'] ==t/1000]['ID'].values.tolist()
    
    
        ax.clear()
        tuples=tuple([[x[k],y[k]] for k in range(len(x))])
        #
        print(tuples)
        scat.set_offsets(tuples)
        for j in range(len(tuples)):
             ax.annotate(int(id[j]),tuples[j], size=5)
        plt.xlim(0, 767)
        plt.ylim(0, 1761)
        #ax.scatter(x,y,s=10)
        ax.set_yticklabels((yaxis))
        ax.set_xticklabels((xaxis))
        
        im = plt.imread('UniHannover.png')
        plt.imshow(im)
        
        fontP = FontProperties()
        fontP.set_size('small') 
        
        # Use this to define the color for each type/group
        N = max(label.loc[:, 'group_id'])
        cmap = plt.cm.get_cmap("prism", N+1)
        markers = ['^', '^', 'o', 's']
        # markers[1]: triangle_up, pedestrians
        # markers[2]: circle, cyclists
        # markers[3]: square, vehicles
        for i, j in enumerate(id):
            group_id = label[label['object_id']==j]['group_id'].values
            c_idx = int(group_id)
            m_idx = int(user_type[i])
            if c_idx == 0:
                # single user is in balck clor
                ax.scatter(x[i], y[i], s=2.5, c='k', marker=markers[m_idx])
            else:
                #group users in different colors, each group has a dinstinct color
                ax.scatter(x[i], y[i], s=2.5, c=cmap(c_idx), marker=markers[m_idx])
            # display the legend    
        plt.scatter([], [], s=2.5, c='k', marker='^', label='ped')
        plt.scatter([], [], s=2.5, c='k', marker='o', label='cyc')
        plt.scatter([], [], s=2.5, c='k', marker='s', label='veh')
        plt.legend(loc='upper right', prop = fontP, bbox_to_anchor=(1.05, 1.02))    
            
    anim = animation.FuncAnimation(fig, animate, frames=2200, interval=100, repeat=False)


    # plt.show()
    anim.save('uni_hannover_416_fast_28012019.mp4', writer='ffmpeg', dpi=300)

def get_label(data_dir):
    '''
    This is the function to get group label
    params:
        data_dir: where the user infomation resides
    '''
    # Read data
    label_data = pd.read_csv(data_dir, sep=',')
    # Only get the object_id and group id
    label = pd.concat([label_data['object_id'], label_data['group_id']], axis=1)
    # Fill the single road user's group id as 0
    label = label.fillna(0)
    
    return label

if __name__ =="__main__":
    main()