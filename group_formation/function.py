#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: yaoli
"""
import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt

def inital_solution(sample_num, data, f):
    # random select sample_num pts and get first group of centers via fl
    print('random solution')
    shuffle = np.random.permutation(data)
    sample = shuffle[0:sample_num,:]
    
    plt.plot(sample[:,1],sample[:,2],'.')
    
    centers = sample
    return centers 

# Course solution: Meyerson algorithm
def OD_similarity(t1, t2):
    # compare the simpilarity between 2 trajectory via their OD
    # |o1-o2| + |d1-d2|
    # t1: o1(ox1,oy1),d1(dx1,dy1), t2: o2(ox2,oy2),d2(dx2,dy2)
    o1 = t1[2:4]
    d1 = t1[5:7]
    
    o2 = t2[2:4]
    d2 = t2[5:7]
    
    # plt.plot(o1[0],o1[1],'ro')
    # plt.plot(d1[0],d1[1],'r*')
    # plt.plot(o2[0],o2[1],'go')
    # plt.plot(d2[0],d2[1],'g*')
    
    d = np.sqrt(sum((o1-o2)**2)) + np.sqrt(sum((d1-d2)**2))
    return d

def updateCenters(point, centers, f):
    distList = [OD_similarity(point,i) for i in centers]
    closest_center = centers[np.argwhere(distList==min(distList)).item()]
    if np.random.random_sample()*2*f < min(distList):
        centers = np.r_[centers,point.reshape((1,-1))]
    # else:
    #         #send this point to the nearest center point
    #     centers = centers
    
    for i in range(n*math.log(n)):
    return centers

if __name__ == "__main__":
    sample_num = 20
    f = 100
    
    centers = inital_solution(sample_num, data, f)
    d = OD_similarity(centers[0], centers[1])
    centers = updateCenters(data[180], centers, f)
