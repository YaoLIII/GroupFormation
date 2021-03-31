#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 11:22:23 2021

@author: yaoli
"""
import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt
from scipy.spatial.distance import directed_hausdorff

a = np.asarray([[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[6,1],[6,2],[6,3],[6,4]])
b = np.asarray([[1,1],[2,1],[3,1],[4,1],[5,1],[5,2],[5,3]])

plt.plot(a[:,0],a[:,1],'x-')
plt.plot(b[:,0],b[:,1],'o-')

max(directed_hausdorff(a,b)[0], directed_hausdorff(b,a)[0])
