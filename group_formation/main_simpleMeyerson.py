#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run Meyerson for all datapoints

@author: yaoli
"""

import pandas as pd
import numpy as np
import time

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

def meyerson(data,f,facil,overcount,filename): #facil is the current existing facil
    g = open(filename,'w+')
    
    # data= np.random.permutation(data)
    facilities= []
    cost=0
    counter=0
    numberofcenters=0
    start = time.time()
    
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
            nearest = f + 1
        if np.random.random_sample()*f<nearest: # should multi 2 or not?
            #open center at this point
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
            
        numberofcenters = len(facilities)
        
        if counter%100==0:
              print(counter,numberofcenters,cost, time.time()-start,overcount)
        g.write(str(counter)+ " "+str(cost)+ " " + str(numberofcenters) + " "+  str(time.time()-start)+ '\n')
         
    #print(counter)
    #cost=actualcost(data,facilities)+f*numberofcenters
    return facilities,cost,numberofcenters,overcount

# def meyerson(data,f,facil,overcount,filename): #facil is the current existing facil

#     g = open(filename,'w+')
    
#     # data= np.random.permutation(data)
#     # facilities= []
#     cost=0
#     counter=0
#     numberofcenters = len(facil)
#     start = time.time()
#     TotalNumberofCentersOpened=0
    
#     for point in data:
#         #print(point)
#         counter=counter+1
#         #if counter % 100==0:
#             #print(counter)
#         #find nearest facility
#         if numberofcenters>0: 

#             nearest,_ = closest_node_dist(point,facil) # if there is a facil nearby
#             if nearest > f: # point is far away
#                 if np.random.random_sample()*f<nearest: 
                    
#                     TotalNumberofCentersOpened += 1
                    
#                     if isin(facil,point):
#                         # print('already a facil')
#                         overcount+=1
#                         # print(overcount)
#                     else:
#                         facil.append(point) #open center at this point 
#                         numberofcenters += 1
#                         cost = cost + f
#             else: # close to a facil, cost increase the transport fee
#                 cost += nearest
            
#         else: # if there's no facil yet
#             nearest = 0 
#             cost += f # create a new facil, and without transport fee
#             facil.append(point)
#             TotalNumberofCentersOpened += 1
        
#         numberofcenters = len(facil)
        
#         if counter%100==0:
#               print(counter,TotalNumberofCentersOpened,cost, time.time()-start,overcount)
#         g.write(str(counter)+ " "+str(cost)+ " " + str(TotalNumberofCentersOpened) + " "+  str(time.time()-start)+ '\n')
            
#     return facil,cost,numberofcenters,overcount

if __name__ == "__main__":
    
    ''' test with SDD dataset/deathcircle '''
    sample = 'deathCircle'
    file = 'video0'
    path = '../data/stanford_campus_dataset/processed/'+ sample +'/'
    img_path = '../data/stanford_campus_dataset/annotations/'+ sample + '/'+file+'/reference.jpg'
    
    data = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
    userType = data.type.unique() #replace string with num
    userType_dict = dict(zip(userType , range(len(userType ))))
    data = data.replace({'type': userType_dict})
    data = np.array(data.sort_values(by=['oframe']))
    
    # userInfo = data, for visualization
    userInfo = pd.read_csv(path + sample +'_' + file + '_userInfo.csv', sep=',')
    userInfo = userInfo.replace({'type': userType_dict})
    userInfo = userInfo.sort_values(by=['oframe'])
    trajsWithId = np.load(path + sample +'_' + file +'_trajsWithId.npy')
    
    f = 200
    file = 'result_sdd_simpleMeyerson_1.txt'
    facil = []
    overcount = 0
    
    facil,cost,numberofcenters,overcount = meyerson(data,f,facil,overcount,file)