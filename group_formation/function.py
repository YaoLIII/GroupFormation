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
    
    d = np.sqrt(sum((o1-o2)**2)) + np.sqrt(sum((d1-d2)**2))
    return d

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
        if np.random.random_sample()*2*f<nearest:
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

def DFL(data,dimension,f,n,timesrecompute,window,filename,th_group,th_waiting):
    
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
    mutation = []
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
            mutation.append(data[lowerbound,1])
            
            lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount)
            howlong=4*lastcost/f
            TotalNumberofCentersOpened+=holder
            #print(howlong)
            lasttime=i
            currentcost=lastcost
            TotalRecompute+=1
            currentfacil=lastfacil
            lowerbound = upperbound
            upperbound = upperbound + window
            i += 1
                      
        else:
            currentdata=data[lowerbound:upperbound]        
            if i-lasttime>howlong:
                print('recompute because reach cost update criteria')
                mutation.append(data[lowerbound,1])
                
                lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount)
                howlong=4*lastcost/f
                TotalNumberofCentersOpened+=holder
                #print(howlong)
                lasttime=i
                currentcost=lastcost
                TotalRecompute+=1
                currentfacil=lastfacil
                
            else:                
                mutation.append(data[lowerbound,1])
                
                currentcost-=closest_node_dist(data[lowerbound-1],currentfacil)[0]
                nearest,_=closest_node_dist(data[upperbound],currentfacil) # or ub+1?
                if nearest<f:
                    print('update')
                    currentcost=currentcost+nearest
                else:
                    print('too close to open new facil')
                    currentcost=currentcost+f
                    TotalNumberofCentersOpened+=1
                    currentfacil.append(data[upperbound])
                
            i += 1
            upperbound += 1
            lowerbound += 1
        
        facils.append(list(currentfacil))
        #print(currentcost, costReMey)
        if i%100==0:
             print(i,TotalNumberofCentersOpened,currentcost, time.time()-start,howlong,overcount)
        g.write(str(i)+ " "+str(currentcost)+ " " + str(TotalNumberofCentersOpened) + " "+  str(time.time()-start)+ '\n')
        
    # filename='S'+filename
    # g = open(filename,'w+')
    # # currentdata=data[:100]
    # lastcost=0
    # currentcost=0
    # lasttime=0
    # overcount=0
    # howlong=-1
    # TotalRecompute=0
    # currentfacil=[]
    # facils = []
    # TotalNumberofCentersOpened=0
    # start = time.time()
    
    # flag = 0
    # i = 0
    # mutation = []
    
    # while flag < len(data):
        
    #     print(flag) # start idx
        
    #     waiting_period = data[:,1]-data[flag,1]
    #     # print(waiting_period)
    #     if np.where(waiting_period>th_waiting)[0].size >0:
    #         # print(np.where(waiting_period>th_waiting)[0].size)
    #         waiting_bound = np.where(waiting_period>th_waiting)[0][0] #idx: waiting time over th_waiting
    #         mutation.append(waiting_bound)
    #         print('reach the maximum waitting time!')
    #         currentdata = data[flag:waiting_bound]
    #         if len(currentdata) > th_group:
    #             print('reach the maximum person num!')
    #             currentdata = currentdata[:th_group] # reach th_group can start moving
    #         flag += len(currentdata)
    #     else:
    #         currentdata = data[flag:]
    #         flag += len(currentdata)
        
    #     print(flag) #end idx
        
    #     if i-lasttime>howlong:
    #         print('recompute')
    #         lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount)
    #         howlong=4*lastcost/f
    #         TotalNumberofCentersOpened+=holder
    #         #print(howlong)
    #         lasttime=i
    #         currentcost=lastcost
    #         TotalRecompute+=1
    #         currentfacil=lastfacil
    #     else:
    #         currentcost-=closest_node_dist(data[i-1],currentfacil)[0]
    #         nearest,_=closest_node_dist(data[i+window-1],currentfacil)
    #         if nearest<f:
    #             currentcost=currentcost+nearest
    #         else:
    #             currentcost=currentcost+f
    #             TotalNumberofCentersOpened+=1
    #             currentfacil.append(data[i+window-1])
                
    #     facils.append(list(currentfacil))
    #     # print(len(currentfacil))
        
    #     #print(currentcost, costReMey)
    #     if i%100==0:
    #           print(i,TotalNumberofCentersOpened,currentcost, time.time()-start,howlong,overcount)
    #     g.write(str(i)+ " "+str(currentcost)+ " " + str(TotalNumberofCentersOpened) + " "+  str(time.time()-start)+ '\n')
        
    #     i = i + 1
        
    return facils,mutation

# def DFL_():        
#     for i in range(0,n-window):
#         currentdata=data[i:i+window]
        
#         if i-lasttime>howlong:
#             lastfacil,lastcost,holder,overcount=meyersonmanytimes(currentdata,dimension,f,timesrecompute,currentfacil,overcount)
#             howlong=4*lastcost/f
#             TotalNumberofCentersOpened+=holder
#             #print(howlong)
#             lasttime=i
#             currentcost=lastcost
#             TotalRecompute+=1
#             currentfacil=lastfacil
#         else:
#             # print(data[i-1],currentfacil)
#             currentcost-=closest_node_dist(data[i-1],currentfacil)
#             nearest=closest_node_dist(data[i+window-1],currentfacil)
#             if nearest<f:
#                 currentcost=currentcost+nearest
#             else:
#                 currentcost=currentcost+f
#                 TotalNumberofCentersOpened+=1
#                 currentfacil.append(data[i+window-1])
                
#         facils.append(list(currentfacil)) 
#         # print(len(currentfacil))
#         #print(currentcost, costReMey)
#         if i%100==0:
#               print(i,TotalNumberofCentersOpened,currentcost, time.time()-start,howlong,overcount)
#         g.write(str(i)+ " "+str(currentcost)+ " " + str(TotalNumberofCentersOpened) + " "+  str(time.time()-start)+ '\n')
        
        
#     return facils

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

