#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 10:43:38 2021

@author: yaoli
"""

import numpy as np
import matplotlib.pyplot as plt
import statistics 
import pylab

X = 0
with open('result_sdd_ownMethod_1.txt') as f:
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
        
with open('result_sdd_simpleMeyerson_1.txt') as f:
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
        
with open('result_sdd_cohen_added_1.txt') as f:
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

smother=100
print(statistics.mean(A1[S:X]),statistics.mean(B1[S:X]))
D1 = [float(a) / float(b) for a,b in zip(A1[S:X], B1[S:X])]
D1smooth = [0] * X
#print(len(D1))
for i in range(0,X):
    sumS=0.0
    antal=0
    
    for j in range(max(0,i-smother),min(i+smother,X-1)):
        #sumS+=D1[j]
        antal+=1
    D1smooth[i]=sumS/antal
         

plt.figure(0)
plt.title('Smoothed rcatio (our algorithm)/(always recomputing)')
plt.plot(D1smooth)
plt.show()

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


# estimate waiting_time
# f = 200
# h = 15
X = 0
S = 0
with open('result_sdd_ownMethod_f100.txt') as f:
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
        
with open('result_sdd_ownMethod_f500.txt') as f:
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
        
with open('result_sdd_ownMethod_f1000.txt') as f:
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
        
plt.figure(1)
plt.ylabel('Cost')
plt.plot(A1[S:X],label = 'f100')
plt.plot(B1[S:X],label = 'f500')
plt.plot(C1[S:X],label = 'f1000')
pylab.legend(loc='upper left')
plt.xlabel('Number of updates')
plt.show()

plt.figure(2)
plt.ylabel('Clusters opened (log scale)')
plt.semilogy(A2[S:X],label = 'f100')
plt.semilogy(B2[S:X],label = 'f500')
plt.semilogy(C2[S:X],label = 'f1000')
pylab.legend(loc='upper left')
plt.xlabel('Number of updates')

plt.figure(3)
plt.ylabel('Time in seconds (log scale)')
plt.semilogy(A3[S:X],label = 'f100')
plt.semilogy(B3[S:X],label = 'f500')
plt.semilogy(C3[S:X],label = 'f1000')
pylab.legend(loc='upper left')
plt.xlabel('Number of updates')