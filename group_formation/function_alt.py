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

def isin(list1,x):
    for y in list1:
        if np.array_equal(x,y):
            return True
    return False

def inital_solution(sample_num, data, f):
    # random select sample_num pts and get first group of centers via fl
    print('random solution')
    shuffle = np.random.permutation(data)
    sample = shuffle[0:sample_num,:]
    
    plt.plot(sample[:,1],sample[:,2],'.')
    
    centers = sample
    return centers 

## Course solution: Meyerson algorithm
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

def closest_node_dist(point, centers):
    #print(node, nodes)
    distList = [OD_similarity(point,i) for i in centers]
    return min(distList)

def updateCenters(point, centers, f):
    distList = [OD_similarity(point,i) for i in centers]
    closest_center = centers[np.argwhere(distList==min(distList)).item()]
    if np.random.random_sample()*2*f < min(distList):
        centers = np.r_[centers,point.reshape((1,-1))]
    # else:
    #         #send this point to the nearest center point
    #     centers = centers
    
    # for i in range(n*math.log(n)):
    return centers

def meyerson(data, dimension, f,facil,overcount):
    data= np.random.permutation(data)
    #print(data[0:10])
    #setfacil = set(facil)
    #print('agurk')
    #print(setfacil)
    #print(type(setfacil))
    facilities= []
    cost=0
    counter=0
    numberofcenters=0
    for point in data:
        #print(point)
        counter=counter+1
        #if counter % 100==0:
            #print(counter)
        #find nearest facility
        if numberofcenters>0:
            nearest = closest_node_dist(point,facilities)
            #print(nearest)
        else:
            nearest = f+1
            #print('hej')
        if np.random.random_sample()*2*f<nearest:
            #open center at this point
            #print('agurk')
            #facilities = np.append(facilities, point)
            facilities.append(point)
            cost = cost + f
            if isin(facil,point):
                #print('already a facil')
                overcount+=1
                #print(overcount)
            else:
                numberofcenters += 1
            
        else:
            cost = cost + nearest
    #print(counter)
    #cost=actualcost(data,facilities)+f*numberofcenters
    return facilities,cost,numberofcenters,overcount

def meyersonmanytimes(data, dimension, f, times,facil,overcount):
    minimum=meyerson(data,dimension,f,facil,overcount)
    for i in range(1,times):
        run=meyerson(data,dimension,f,facil,overcount)
        if run[1]<minimum[1]:
            minimum=run
    return minimum

def DFL(data,dimension,f,n,timesrecompute,window,filename):
    filename='S'+filename
    g = open(filename,'w+')
    currentdata=data[:100]
    lastcost=0
    currentcost=0
    lasttime=0
    overcount=0
    howlong=-1
    TotalRecompute=0
    currentfacil=[]
    TotalNumberofCentersOpened=0
    start = time.time()
    for i in range(0,n-window):
        currentdata=data[i:i+window]
        if i-lasttime>howlong:
            lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount)
            howlong=4*lastcost/f
            TotalNumberofCentersOpened+=holder
            #print(howlong)
            lasttime=i
            currentcost=lastcost
            TotalRecompute+=1
            currentfacil=lastfacil
        else:
            # print(data[i-1],currentfacil)
            currentcost-=closest_node_dist(data[i-1],currentfacil)
            nearest=closest_node_dist(data[i+window-1],currentfacil)
            if nearest<f:
                currentcost=currentcost+nearest
            else:
                currentcost=currentcost+f
                TotalNumberofCentersOpened+=1
                currentfacil.append(data[i+window-1])
            
        #print(currentcost, costReMey)
        if i%100==0:
             print(i,TotalNumberofCentersOpened,currentcost, time.time()-start,howlong,overcount)
        g.write(str(i)+ " "+str(currentcost)+ " " + str(TotalNumberofCentersOpened) + " "+  str(time.time()-start)+ '\n')

if __name__ == "__main__":
    sample_num = 20
    f = 100
    
    centers = inital_solution(sample_num, data, f)
    d = OD_similarity(centers[0], centers[1])
    centers = updateCenters(data[180], centers, f)
