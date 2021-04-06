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
    
# with OD
def closest_node_dist(point, centers):
    #print(node, nodes)
    distList = [OD_similarity(point,i) for i in centers]
    correspId = distList.index(min(distList))
    return min(distList),correspId

def meyerson(data, dimension, f,facil,overcount):
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
            nearest,_ = closest_node_dist(point,facilities)
            #print(nearest)
        else:
            nearest = f+1
            #print('hej')
        if np.random.random_sample()*f<nearest: # should multi 2 or not?
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

def meyersonmanytimes(data, dimension, f, times,facil,overcount):
    minimum=meyerson(data,dimension,f,facil,overcount)
    for i in range(1,times):
        run=meyerson(data,dimension,f,facil,overcount)
        if run[1]<minimum[1]:
            minimum=run
    return minimum

def DFL(data,dimension,f,n,timesrecompute,window,filename,th_waiting):
    
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
            # print(lowerbound)
            mut = data[upperbound-1,1]
            mutation.append(mut)
            
            lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount)
            howlong=4*lastcost/f
            TotalNumberofCentersOpened+=holder
            #print(howlong)
            lasttime=i
            currentcost=lastcost
            TotalRecompute+=1
            currentfacil=lastfacil
            facils.append(list(currentfacil))
            
            # decide which facil users belongs to (relative id of currentfacils)
            correspIds = [closest_node_dist(point, currentfacil)[1] for point in currentdata]
            bel = np.c_[np.ones((len(currentdata),))*mut, currentdata[:,0],np.asarray(correspIds)] #[traj_id, corresp_center]
            belong.append(bel)
            
            lowerbound = upperbound
            upperbound = upperbound + window
            i += 1
                      
        else:
            currentdata=data[lowerbound:upperbound]        
            if i-lasttime>howlong:
                print('recompute because reach cost update criteria')
                mut = data[upperbound-1,1]
                mutation.append(mut)
                
                lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount)
                howlong=4*lastcost/f
                TotalNumberofCentersOpened+=holder
                #print(howlong)
                lasttime=i
                currentcost=lastcost
                TotalRecompute+=1
                currentfacil=lastfacil
                facils.append(list(currentfacil))
                
                # decide which fail users belongs to (relative id of currentfacils)
                correspIds = [closest_node_dist(point, currentfacil)[1] for point in currentdata]
                bel = np.c_[np.ones((len(currentdata),))*mut, currentdata[:,0],np.asarray(correspIds)] #[mutation,traj_id, corresp_center]
                belong.append(bel)
                
            else:
                
                currentcost-=closest_node_dist(data[lowerbound-1],currentfacil)[0] # delete passed lowerbound-1 from facil?
                nearest,cid=closest_node_dist(data[upperbound],currentfacil)
                if nearest<f:
                    print('too close to open new facil')
                    currentcost=currentcost+nearest
                    bel = np.array([data[upperbound-1,1],data[upperbound-1,0],cid])
                    belong.append(bel)
                else:
                    print('update')
                    mut = data[upperbound-1,1]
                    mutation.append(mut)
                    currentcost=currentcost+f
                    TotalNumberofCentersOpened+=1
                    bel = np.array([data[upperbound-1,1],data[upperbound-1,0],len(currentfacil)]) # 是否加上所有的取值，而不只是新加的这个点
                    belong.append(bel)
                    
                    currentfacil.append(data[upperbound])
                    facils.append(list(currentfacil))
                    
                
            i += 1
            upperbound += 1
            lowerbound += 1
        
        # facils.append(list(currentfacil))
        # print(currentcost, costReMey)
        if i%100==0:
             print(i,TotalNumberofCentersOpened,currentcost, time.time()-start,howlong,overcount)
        g.write(str(i)+ " "+str(currentcost)+ " " + str(TotalNumberofCentersOpened) + " "+  str(time.time()-start)+ '\n')
        
    return facils,mutation,belong

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
    facilities,cost,numberofcenters,overcount = meyersonmanytimes(data,2, 6, 5,[],0)
    
    # extract users which has the same center
    centers = []
    for pt in data:
        _,centerIdx = closest_node_dist(pt, facilities)
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

