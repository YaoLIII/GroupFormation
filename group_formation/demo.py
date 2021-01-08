# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 13:28:31 2021

@author: li
"""
from typing import TypeVar, Dict, List, Iterator, Tuple, Optional
Location = TypeVar('Location')

'''class'''
class SimpleGraph:
    def __init__(self):
        self.edges: Dict[Location, List[Location]] = {}
        self.weights: Dict[Location, float] = {}
    def neighbors(self, id: Location) -> List[Location]:
        return self.edges[id]
    def cost(self, from_node: Location, to_node: Location) -> float:
        return self.weights.get(to_node, 1)
    
'''function'''
# init group
def initGroup():
    graph = SimpleGraph()
    graph.edges = {'A':['B','D']}
    return None

# init graph
def initGraph():
    return None

# assign inital path
def initPath():
    return None

# column generation
def columnGeneration():
    return None