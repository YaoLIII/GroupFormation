#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot the comparision of three methods
"""

import numpy as np
import matplotlib.pyplot as plt
import statistics 
import pylab

X = 0
with open('../result/result_sdd_ownMethod.txt') as f:
    liste = f.readlines()
    A1=[]
    A2=[]
    A3=[]
    avg=0
    for line in liste:
        line=line.split()
        X=X+1
        A1.append(float(line[1]))
        A2.append(float(line[2]))
        A3.append(float(line[3]))
        
with open('../result/result_sdd_simpleMeyerson.txt') as f:
    liste = f.readlines()
    B1=[]
    B2=[]
    B3=[]
    avg=0
    for line in liste:
        line=line.split()
        #print(line)
        B1.append(float(line[1]))
        B2.append(float(line[2]))
        B3.append(float(line[3]))
        #avg=float(line[1])
        
with open('../result/result_sdd_cohen_added.txt') as f:
    liste = f.readlines()
    C1=[]
    C2=[]
    C3=[]
    avg=0
    for line in liste:
        line=line.split()
        #print(line[2])
        C1.append(float(line[1]))
        C2.append(float(line[2]))
        C3.append(float(line[3]))
        
S=0
count=0
'''for x in C3[0:500000]:
    count+=1
    if x>1000:
        print(x,count)'''

plt.figure(1)
plt.ylabel('Cost')
plt.plot(A1[S:X],label = 'Our Alg')
plt.plot(B1[S:X],label = 'Meyerson')
plt.plot(C1[S:X],label = 'Cohen-Addad')
pylab.legend(loc='upper left')
plt.xlabel('Number of updates')
plt.show()

plt.figure(2)
plt.ylabel('Clusters opened (log scale)')
plt.semilogy(A2[S:X],label = 'Our Alg')
plt.semilogy(B2[S:X],label = 'Meyerson')
plt.semilogy(C2[S:X],label = 'Cohen-Addad')
pylab.legend(loc='upper left')
plt.xlabel('Number of updates')



plt.figure(3)
plt.ylabel('Time in seconds (log scale)')
plt.semilogy(A3[S:X],label = 'Our Alg')
plt.semilogy(B3[S:X],label = 'Meyerson')
plt.semilogy(C3[S:X],label = 'Cohen-Addad')
pylab.legend(loc='upper left')
plt.xlabel('Number of updates')