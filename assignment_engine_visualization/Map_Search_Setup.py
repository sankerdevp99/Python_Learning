# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 11:10:26 2023

@author: Bijo Sebastian, Sayooj P
"""

import Map
import pandas as pd
import os

class Map_search_setup:
    
    #For the shortest path cacluation
    start_node = None
    goal_node = None
    map_node_list = None
    base_dir = os.path.dirname(os.path.abspath(__file__))
    distance_matrix = pd.read_excel(os.path.join(base_dir,"Common_Files",'distance_matrix.xlsx'))       

    def node_to_path(self, path_nodes):
        #expectting path like [26, 25, 21, 19, 20], goal_node = 2
     
        #convert nodes into map node locations
        path = [self.map_node_list[x] for x in path_nodes]  
        path_length = 0
        for i,x in enumerate(path_nodes):
            if i < len(path) -1:
                path_length += self.distance_matrix[int(x)][int(path_nodes[i+1])]
                 
        return path, path_length
        
