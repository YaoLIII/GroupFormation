# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 17:14:41 2020

@author: li
"""

import ndjson

with open('../data/traj++/SamplePrediction/Predictions.ndjson') as f:
    data = ndjson.load(f)
    
text = ndjson.dumps(data)
data = ndjson.loads(text)