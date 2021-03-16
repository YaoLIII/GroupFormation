#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:11:57 2021

@author: yaoli
"""
import pandas as pd
import numpy as np
import os
import time
import random

# Course solution: Meyerson algorithm
def distance(p1, p2):
    d = np.einsum('',p1,p2)
    return d

def Meyerson(point, centers):
    distList = [distance(point,i) for i in centers]
    for idx,center in enumerate(centers):
        if random.rand(0,1)*f < distList[idx]:
            centers.append(point)
        else:
            #send this point to the nearest center point
            centers = centers
    return centers