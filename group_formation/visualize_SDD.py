# -*- coding: utf-8 -*-
"""
visualizing result of dynamic facility location.

@author: li
"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties

# read data
# [id, oframe, ox, oy, dframe, dx, dy, avg_v, type]
data = data

xmin = min(data[:,2])
xmax = max(data[:,2])
ymin = min(data[:,3])
ymax = max(data[:,3])

# create canvas
fig, ax = plt.subplots()
# img = plt.imread("../fig/background_Bergedorf.png")
# img = plt.imread("../fig/background_map.png")
img = plt.imread('../data/stanford_campus_dataset/annotations/deathCircle/' + 'video0' + '/' + 'reference.jpg' )

scat = ax.scatter(0,0)

def update(t):

    x = data[data[:,1]==t][:,2].tolist()
    y = data[data[:,1]==t][:,3].tolist()
    user_type = data[data[:,1]==t][:,-1].tolist()     
    user_id = data[data[:,1]==t][:,0].tolist()
    
    ax.clear()
    ax.set_title("Movements at time " + str(t))
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.imshow(img, extent=[xmin, xmax, ymin, ymax])
    tuples = tuple([x[k],y[k]] for k in range(len(x)))
    scat.set_offsets(tuples)
        
    for j in range(len(tuples)):
        ax.annotate(int(user_id[j]),tuples[j], size = 10)
        
    fontP = FontProperties()
    fontP.set_size('large')
        
    # define colormap and markers
    # cmap = plt.cm.get_cmap("prism",len(np.unique(df['user_id'])))
    markers = ['^', 'o', 's','p','d','P']
    # markers[1]: triangle_up, pedestrians
    # markers[2]: circle, cyclists
    # markers[3]: square, vehicles
    
    for i,j in enumerate(user_id):
        if user_type[i] == 0:
            m_idx = 0
            c = 'orange'
        elif  user_type[i] == 1:
            m_idx = 1
            c = 'red'
        elif  user_type[i] == 2:
            m_idx = 2
            c = 'yellow'
        elif  user_type[i] == 3:
            m_idx = 3
            c = 'green'
        elif  user_type[i] == 4:
            m_idx = 4
            c = 'blue'
        else:
            m_idx = 5
            c = 'cyan'
        ax.scatter(x[i],y[i],s = 50, color = c, marker = markers[m_idx])
    # # display legend
    # plt.scatter([], [], s=40, color='k', marker='^', label='ped')
    # plt.scatter([], [], s=40, color='k', marker='o', label='cyc')
    # plt.scatter([], [], s=40, color='k', marker='s', label='veh')
    # plt.legend(loc='lower right')
    
anim = animation.FuncAnimation(fig, update, frames = len(data[:,1]), \
                        interval = 2, repeat = False)
plt.show()

if __name__ == "__main__":
    
    sample = 'deathCircle'    
    output_dir = '../data/stanford_campus_dataset/processed/'+ sample +'/'
    
    f = np.load(output_dir + 'facilities_result.npy',allow_pickle=True)



