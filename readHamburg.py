# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 16:54:35 2020

@author: li
"""
import numpy as np
from pandas import read_csv
import matplotlib.pyplot as plt

path = "Federico/dump/"
df = read_csv(path + "Hamburg_dataset.csv")

print(list(df.columns))

dups_user_type = df.pivot_table(index=['user_type'], aggfunc='size')
print(dups_user_type)
