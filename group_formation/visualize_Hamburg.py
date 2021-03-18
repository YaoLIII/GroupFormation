# -*- coding: utf-8 -*-
"""

@author: li
"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties

# read data
data_dir = "../data/Federico/dump/Hamburg_dataset.csv"
df = pd.read_csv(data_dir)

print('column names are: '+str(list(df.columns)))
print('Types of agents are: ' + str([i.replace(' ','') for i in np.unique(df.user_type)]))

xmin = min(df['x_axis'])
xmax = max(df['x_axis'])
ymin = min(df['y_axis'])
ymax = max(df['y_axis'])

# create canvas
fig, ax = plt.subplots()
img = plt.imread("../fig/background_Bergedorf.png")
# img = plt.imread("../fig/background_map.png")

scat = ax.scatter(0,0)

def update(t):

    x = df.loc[df['time_05']==t]['x_axis'].values.tolist()
    y = df.loc[df['time_05']==t]['y_axis'].values.tolist()
    user_type = df.loc[df['time_05']==t]['user_type'].values.tolist()        
    user_id = df.loc[df['time_05']==t]['user_id'].values.tolist()
    
    ax.clear()
    ax.set_title("Movements at time " + str(t))
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.imshow(img, extent=[xmin, xmax, ymin, ymax])
    tuples = tuple([x[k],y[k]] for k in range(len(x)))
    scat.set_offsets(tuples)
        
    for j in range(len(tuples)):
        ax.annotate(int(user_id[j]-10000),tuples[j], size = 10)
        
    fontP = FontProperties()
    fontP.set_size('large')
        
    # define colormap and markers
    # cmap = plt.cm.get_cmap("prism",len(np.unique(df['user_id'])))
    markers = ['^', 'o', 's']
    # markers[1]: triangle_up, pedestrians
    # markers[2]: circle, cyclists
    # markers[3]: square, vehicles
    
    for i,j in enumerate(user_id):
        if user_type[i] == 'pedestrian':
            m_idx = 0
            c = 'orange'
        elif  user_type[i] == 'cyclist':
            m_idx = 1
            c = 'red'
        else:
            m_idx = 2
            c = 'cyan'
        ax.scatter(x[i],y[i],s = 50, color = c, marker = markers[m_idx])
    # display legend
    plt.scatter([], [], s=40, color='k', marker='^', label='ped')
    plt.scatter([], [], s=40, color='k', marker='o', label='cyc')
    plt.scatter([], [], s=40, color='k', marker='s', label='veh')
    plt.legend(loc='lower right')
    
anim = animation.FuncAnimation(fig, update, frames = len(np.unique(df['time_05'])), \
                        interval = 200, repeat = False)
plt.show()

# if __name__ == "__main__":
#     main()

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



