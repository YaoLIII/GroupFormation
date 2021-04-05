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
from scipy.spatial.distance import directed_hausdorff

def isin(list1,x):
    for y in list1:
        if np.array_equal(x,y):
            return True
    return False

## Course solution: Meyerson algorithm
def OD_similarity(t1, t2):
    # compare the simpilarity between 2 trajectories via their OD
    # |o1-o2| + |d1-d2|
    # t1: o1(ox1,oy1),d1(dx1,dy1), t2: o2(ox2,oy2),d2(dx2,dy2)
    o1 = t1[2:4]
    d1 = t1[5:7]
    
    o2 = t2[2:4]
    d2 = t2[5:7]
    
    d = np.sqrt(sum((o1-o2)**2)) + np.sqrt(sum((d1-d2)**2))
    return d

def hausdorff(t1, t2, trajsWithId):
    # compare the simpilarity between 2 trajectories via Hausdorff distance
    id1 = t1[0]
    id2 = t2[0]
    
    u = trajsWithId[np.argwhere(trajsWithId[:,0]==id1).ravel(),1:3]
    v = trajsWithId[np.argwhere(trajsWithId[:,0]==id2).ravel(),1:3]
    
    # plt.plot(u[:,0],u[:,1])
    # plt.plot(v[:,0],v[:,1])
    
    d = max(directed_hausdorff(u, v)[0], directed_hausdorff(v, u)[0])
    
    return d
    
# # with OD
# def closest_node_dist(point, centers):
#     #print(node, nodes)
#     distList = [OD_similarity(point,i) for i in centers]
#     correspId = distList.index(min(distList))
#     return min(distList),correspId

# # with Hausdorff dist
def closest_node_dist(point, centers, trajsWithId):
    #print(node, nodes)
    distList = [hausdorff(point,i,trajsWithId) for i in centers]
    correspId = distList.index(min(distList))
    return min(distList),correspId

def meyerson(data, dimension, f,facil,overcount, trajsWithId):
    data= np.random.permutation(data)
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
            nearest,_ = closest_node_dist(point,facilities, trajsWithId)
            #print(nearest)
        else:
            nearest = f+1
            #print('hej')
        if np.random.random_sample()*f<nearest:
            #open center at this point
            #print('agurk')
            #facilities = np.append(facilities, point)
            facilities.append(point) # move from before if to avoid duplicate            
            cost = cost + f # move from before if to avoid duplicate
            if isin(facil,point):
                # print('already a facil')
                # print(point)
                # print(facilities)
                # facilities.remove(point) # if this point is already in fac, remove duplicate
                overcount+=1
                #print(overcount)
            else:
                numberofcenters += 1
                # facilities.append(point) # move from before if to avoid duplicate
                # cost = cost + f # move from before if to avoid duplicate
            
        else:
            cost = cost + nearest
    #print(counter)
    #cost=actualcost(data,facilities)+f*numberofcenters
    return facilities,cost,numberofcenters,overcount

def meyersonmanytimes(data, dimension, f, times,facil,overcount,trajsWithId):
    minimum=meyerson(data,dimension,f,facil,overcount,trajsWithId)
    for i in range(1,times):
        run=meyerson(data,dimension,f,facil,overcount,trajsWithId)
        if run[1]<minimum[1]:
            minimum=run
    return minimum

def DFL(data,dimension,f,n,timesrecompute,window,filename,th_waiting, trajsWithId):
    
    filename='S'+filename
    g = open(filename,'w+')

    lastcost=0
    currentcost=0
    lasttime=0
    overcount=0
    howlong=-1
    TotalRecompute=0
    currentfacil=[]
    facils=[]
    TotalNumberofCentersOpened=0
    start = time.time()
    
    i = 0
    lowerbound = 0 #index of vary-length sliding window
    upperbound = lowerbound + window
    mutation = [] # when facil number change
    belong = []
    # flag = 0 # start of window
    # window_wid = window # vary window length
    
    while upperbound < len(data):
        delta_t = data[upperbound,1] - data[lowerbound,1] #enter one point per step
        if delta_t > th_waiting: # waiting time exceed th_waiting
            # print('reach the maximum waiting time!')
            waiting_period = data[:,1] - data[lowerbound,1] 
            newbound = np.where(waiting_period>th_waiting)[0][0] # idx: where exceed th_waiting
            upperbound = newbound
            currentdata = data[lowerbound:upperbound]
            
            print('recompute because exceed waiting time')
            mutation.append(data[upperbound,1])
            
            lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount,trajsWithId)
            howlong=4*lastcost/f
            TotalNumberofCentersOpened+=holder
            #print(howlong)
            lasttime=i
            currentcost=lastcost
            TotalRecompute+=1
            currentfacil=lastfacil
            
            # decide which facil users belongs to (relative id of currentfacils)
            correspIds = [closest_node_dist(point, currentfacil, trajsWithId)[1] for point in currentdata]
            bel = np.c_[currentdata[:,0],np.asarray(correspIds)] #[traj_id, corresp_center]
            belong.append(bel)
            
            lowerbound = upperbound
            upperbound = upperbound + window
            i += 1
                      
        else:
            currentdata=data[lowerbound:upperbound]        
            if i-lasttime>howlong:
                print('recompute because reach cost update criteria')
                mutation.append(data[upperbound,1])
                
                lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount,trajsWithId)
                howlong=4*lastcost/f
                TotalNumberofCentersOpened+=holder
                #print(howlong)
                lasttime=i
                currentcost=lastcost
                TotalRecompute+=1
                currentfacil=lastfacil

		# decide which fail users belongs to (relative id of currentfacils)
                correspIds = [closest_node_dist(point, currentfacil,trajsWithId)[1] for point in currentdata]
                bel = np.c_[currentdata[:,0],np.asarray(correspIds)] #[traj_id, corresp_center]
                belong.append(bel)
                
            else:                
                # mutation.append(data[upperbound,1])
                
                currentcost-=closest_node_dist(data[lowerbound-1],currentfacil, trajsWithId)[0]
                nearest,cid=closest_node_dist(data[upperbound],currentfacil, trajsWithId) # or ub+1?
                if nearest<f:
                    print('too close to open new facil')
                    currentcost=currentcost+nearest
                    bel = np.array([data[upperbound,0],cid])
                    belong.append(bel)
                else:
                    print('update')
                    mutation.append(data[upperbound,1])
                    currentcost=currentcost+f
                    TotalNumberofCentersOpened+=1
                    bel = np.array([data[upperbound,0],len(currentfacil)]) # 是否加上所有的取值，而不只是新加的这个点
                    belong.append(bel)
                    
                    currentfacil.append(data[upperbound])
                    
                
            i += 1
            upperbound += 1
            lowerbound += 1
        
        facils.append(list(currentfacil))
        #print(currentcost, costReMey)
        if i%100==0:
             print(i,TotalNumberofCentersOpened,currentcost, time.time()-start,howlong,overcount)
        g.write(str(i)+ " "+str(currentcost)+ " " + str(TotalNumberofCentersOpened) + " "+  str(time.time()-start)+ '\n')
        
    return facils,mutation, belong

if __name__ == "__main__":
    
    # test Meyerson with synthetic data
    path = '../data/synthetic/'
    userInfo = pd.read_csv(path + 'synthetic_mapSize10_userInfo.csv', sep=',')
    trajsWithId = np.load(path + 'synthetic_mapSize10_trajsWithId.npy')
    
    num = 300
    
    # # plot sample users Origins
    # x = userInfo['ox'].iloc[0:num].tolist()
    # y = userInfo['oy'].iloc[0:num].tolist()
    # plt.plot(x,y,'.')
    
    # extract sample users
    data = userInfo.iloc[0:num,:].to_numpy()
    # facilities,cost,numberofcenters,overcount = meyerson(data,2,20,[],0)   
    
    '''check multi Meyerson fun with sample data''' 
    facilities,cost,numberofcenters,overcount = meyersonmanytimes(data,2, 6, 5,[],0,trajsWithId)
    
    # extract users which has the same center
    centers = []
    for pt in data:
        _,centerIdx = closest_node_dist(pt, facilities, trajsWithId)
        centers.append(centerIdx)
     
    group = []
    plt.figure()   
    for c in np.unique(centers):
        # users belongs to same group
        groupId = np.argwhere(centers==c).ravel()
        group.append(groupId)
        for idx in groupId:
            # extract user trajectory
            user = trajsWithId[np.argwhere(trajsWithId[:,0]==idx).ravel()]
            plt.xlim(-1, 11)
            plt.ylim(-1, 11)
            plt.plot(user[:,1],user[:,2],'*-')
        plt.pause(0.5)
        plt.cla()
        
    
    # f_loc = np.asarray(facilities)[:,2:4]
    # plt.plot(f_loc[:,0],f_loc[:,1],'*')

