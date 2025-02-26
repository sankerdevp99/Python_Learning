# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 20:55:36 2023

@author: Bijo Sebastian, Sayooj P
"""
class Node:
    node_id = None
    location_coordinates = []
    connectivity = []
    
    def __init__(self, node_id, location_coordinates):
        self.node_id = "Node_"+str(node_id)
        self.location_coordinates = location_coordinates
        return
    
#Distance matrix for the Map
distance_matrix = None
#Lists of nodes in the Map 
node_list =[]

def calculate_distance(start_node, goal_node):
        startpoint = start_node.node_id.split("_")[1]
        goalpoint = goal_node.node_id.split("_")[1]
        
        distance = distance_matrix[int(startpoint)][int(goalpoint)]                              
        return distance 


    




