# -*- coding: utf-8 -*-
"""
@author: Sayooj P , Bijo Sebastian
"""

import pandas as pd
from ast import literal_eval
import yaml
import os


# Load the parameter YAML configuration file
properties = yaml.safe_load(open(os.path.join("Common_Files", "CommonProperties.yaml"), "r"))
#Import dataframe contains informations about nodes_and_junctions
nodes_junctions = pd.read_excel(os.path.join("Common_Files","nodes_junctions_xy.xlsx"))
nodes_junctions['map_connection'] = nodes_junctions['map_connection'].apply(literal_eval) #converted into list
#import file containing distance information
distance_matrix = pd.read_excel(os.path.join("Common_Files",'distance_matrix.xlsx'))

current_total_node_junctions = len(nodes_junctions)
num_of_loading_stations = properties["num_loading_stations"]
num_of_unloading_stations = properties["num_unloading_stations"]
num_of_junctions = properties["num_junctions"]
trucks_per_station = properties["trucks_per_station"]

#add duplicate junctions for unloading and update connectivities of junctions(split)
for row in range(num_of_junctions):
    name = f"junction_u_{row}"
    node_id = len(nodes_junctions)
    #for junctions(unloading). connect only with loading stations and junctions(unloading)
    connectivity = [x for x in nodes_junctions['map_connection'][row+num_of_loading_stations+num_of_unloading_stations] if x >= num_of_loading_stations and x < num_of_loading_stations+num_of_loading_stations]
    connectivity = connectivity + [x+num_of_junctions for x in nodes_junctions['map_connection'][row+num_of_loading_stations+num_of_unloading_stations] if x >= num_of_loading_stations+num_of_unloading_stations]
    new_row = {
        'node':node_id,
        'node_name': name,
        'map_connection': connectivity
        }
    #add junctions(unloading junctions)
    nodes_junctions = pd.concat([nodes_junctions, pd.DataFrame([new_row])], ignore_index=True)
    #edit connectivity of junctions(loading junctions)
    nodes_junctions.at[row + num_of_loading_stations+num_of_unloading_stations,'map_connection'] =list(set(nodes_junctions['map_connection'][row + num_of_loading_stations+num_of_unloading_stations]) - set(connectivity))

#need to change the connections of loading and unloading stations to juncttions based on they are loading or unloading in state
for row in range(num_of_loading_stations):
    #from loading station connect to junction(unloading)
    value =  nodes_junctions['map_connection'][row]
    connectivity = value[0] + num_of_junctions
    nodes_junctions.at[row,'map_connection'] = [connectivity]


#addd waiting rows
for row in range(num_of_loading_stations):
    name = f"waiting_at_LS_{row}"
    node_id = len(nodes_junctions) 
    new_row = {
        'node' : node_id,
        "node_name": name,
        'connectivity': [row]
    }
    nodes_junctions = pd.concat([nodes_junctions, pd.DataFrame([new_row])], ignore_index=True)
    
    

for row in range(num_of_unloading_stations):
    name = f"waiting_at_US_{row}"
    node_id = len(nodes_junctions) 
    new_row = {
        'node' : node_id,
        "node_name": name,
        "connectivity":[row +num_of_loading_stations]
    }
    nodes_junctions = pd.concat([nodes_junctions, pd.DataFrame([new_row])], ignore_index=True)

#add travelling rows
for row in range(current_total_node_junctions+num_of_junctions):
    connection_list = nodes_junctions['map_connection'][row]
    connectivity_of_station = []
    for connection in connection_list:
        actual_row = row
        actual_column = connection
        if row >= num_of_loading_stations + num_of_unloading_stations + num_of_junctions : # duplicate junction
            actual_row = row - num_of_junctions
        if connection >= num_of_loading_stations + num_of_unloading_stations + num_of_junctions : # duplicate junction
            actual_column = connection - num_of_junctions
        distance = distance_matrix[actual_row][actual_column]

        if connection < num_of_loading_stations: # need to connect to waiting at loading station instead of direct loading station
            connection = connection + num_of_loading_stations + num_of_unloading_stations + 2*num_of_junctions

        name = f"travelling_from_{row}_to_{connection}"
        node_id = len(nodes_junctions)
        new_row = {
        'node' : node_id,
        "node_name": name,
        "connectivity": [connection],  
        "distance": distance
        }
        nodes_junctions = pd.concat([nodes_junctions, pd.DataFrame([new_row])], ignore_index=True)
        connectivity_of_station.append(node_id)
    nodes_junctions.at[row, 'connectivity'] = connectivity_of_station
    

#create start location and end location

    # create start location
for node_name in trucks_per_station:
    name = "truck_start_location_at_"+node_name
    node = int(node_name)
    node_id = len(nodes_junctions)
    start_row = {
            'node' : node_id,
            "node_name": name,
            "connectivity": [node],
            "num_trucks_parked":trucks_per_station[node_name]  
            }
    nodes_junctions = pd.concat([nodes_junctions, pd.DataFrame([start_row])], ignore_index=True)

# end location at each unloading station
for row in range(num_of_loading_stations, num_of_loading_stations + num_of_unloading_stations):
    name = f"truck_end_at_us_{row}"
    node_id = len(nodes_junctions)
    new_row = {
    'node' : node_id,
    "node_name": name,
    "connectivity": []   
    }
    

    connection_list = nodes_junctions['connectivity'][row]
    connection_list.append(node_id)
    nodes_junctions.at[row, 'connectivity'] = connection_list

    nodes_junctions = pd.concat([nodes_junctions, pd.DataFrame([new_row])], ignore_index=True)

#with all above changes create new excel sheet
path_to_save = os.path.join("Common_Files", "all_states.xlsx")
nodes_junctions.to_excel(path_to_save, index=False)
