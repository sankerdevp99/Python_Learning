# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:27:36 2023

@author: Bijo Sebastian, Sayooj P
"""

import Map
import World
import Vehicles
import Buildings
import Visualizations
import Data_Logger
import pandas as pd
from ast import literal_eval
import yaml
import numpy as np
import os

# Load the parameter YAML configuration file
properties = yaml.safe_load(open(os.path.join("Common_Files", "CommonProperties.yaml"), "r"))


def main():
    
    print ('Setting up Discrete Event Simualtion')
    Data_Logger.log_data("\n\nSetting up Discrete Event Simualtion \n")  
    
    #Import dataframe contains location coordinates of load zones, dump zones and intersections
    nodes_junctions = pd.read_excel(os.path.join("Common_Files","nodes_junctions_xy.xlsx"))
    nodes_junctions['map_connection'] = nodes_junctions['map_connection'].apply(literal_eval)
    #Giving the distance matrix as a shared dataframe for all trucks
    distance_matrix = pd.read_excel(os.path.join("Common_Files",'distance_matrix.xlsx')) 
    Map.distance_matrix =   distance_matrix
  
    #Create and add the nodes
    for node in range(len(nodes_junctions)):
        Map.node_list.append(Map.Node(node, [nodes_junctions["x"][node], nodes_junctions["y"][node]]))
    
    

    #Setting up the node connectivity   
    for index in range(len(nodes_junctions)):
        Map.node_list[index].connectivity = nodes_junctions["map_connection"][index]
    
        
    #Create World
    current_world = World.World(1)

    #Set parameters
    current_world.map_search_setup.map_node_list = Map.node_list
    current_world.map_search_setup.distance_matrix  = distance_matrix
    #Process parameters
    current_world.dt = 0.1 #simulation time step in seconds
    trucks_per_station = properties["trucks_per_station"]
    
    #truck parameters
    current_world.truck_velocity_loaded = properties["loaded_truck_velocity"] #velocity of loaded truck in meter per seconds
    # print(f'The Loaded Velocity used for this run is {current_world.truck_velocity_loaded}')
    current_world.truck_velocity_unloaded = properties["unloaded_truck_velocity"] #velocity of unloaded truck in meter per seconds
    # print(f'The Loaded UnVelocity used for this run is {current_world.truck_velocity_unloaded}')
    current_world.truck_capacity = properties["truck_capacity"] #in tonn
    
    #shovel parameters
    current_world.loading_rate = properties["loading_rate"] #tonn per second
    current_world.unloading_rate = properties["unloading_rate"] #tonn per second 
    
    #Add elements to world 
    temp_material_in_truck = 0.0 #in tonn 
    temp_material_in_unloading_stations = 0.0 #in tonn
    
    
    # Create parking lots
    num_parking_station = len(properties["trucks_per_station"]) # start location
    for i in range(num_parking_station):
        temp_building = Buildings.Parking_lot(i)
        current_world.parking_lot_list.append(temp_building)
    
    #Create loading stations 
    for i in range(properties["num_loading_stations"]):
        temp_material_in_loading_stations = nodes_junctions["material"][i]
        temp_building = Buildings.Loading_station(i, current_world.loading_rate, temp_material_in_loading_stations)
        current_world.loading_station_list.append(temp_building)
        
    #Create unloading stations 
    for i in range(properties["num_unloading_stations"]):
        index = i + properties["num_loading_stations"]
        temp_material_requirement = nodes_junctions["material"][index]
        temp_building = Buildings.Unloading_station(i, current_world.unloading_rate, temp_material_in_unloading_stations, temp_material_requirement)
        current_world.unloading_station_list.append(temp_building)

    #Create Trucks fully empty at first parking lot
    truck_number = 0 
    for i,node in enumerate(trucks_per_station):
        num_trucks_parked = trucks_per_station[node]
        for x in range(num_trucks_parked):
            temp_truck = Vehicles.Truck(truck_number, False, temp_material_in_truck, current_world.parking_lot_list[i])
            temp_truck.set_params(current_world.dt, current_world.truck_velocity_loaded, current_world.truck_velocity_unloaded, current_world.truck_capacity)
            current_world.truck_list.append(temp_truck)   
            truck_number += 1 
            Data_Logger.log_data(str(temp_truck.truck_id) + " at " + str(temp_truck.location.station_id) + "\n")
        
     
    # Give Map locations for the items in the world
    # Map location to parking lots
    for i,node in enumerate(trucks_per_station):
        current_world.parking_lot_list[i].node = Map.node_list[int(node)]   
    # Map location to loading stations    
    for i in range(properties["num_loading_stations"]):
        current_world.loading_station_list[i].node = Map.node_list[i]
    # Map locations to unloading stations
    for i in range(properties["num_unloading_stations"]):   
        current_world.unloading_station_list[i].node = Map.node_list[i+properties["num_loading_stations"]]
    
    # Setup plots
    Visualizations.visualize_map()
    Visualizations.visualize_world_first_time(current_world)
    Visualizations.visualize_trucks_first_time(current_world)

    #Run the discrete event simulation
    while not current_world.flag_unloading_station_requirment_met:
         current_world.step_sim()
         Visualizations.visualize_world_update(current_world)
         Visualizations.visualize_trucks_update(current_world)

    
    total_loaded_velocities = np.mean(current_world.total_testing_loadedvelocities)
    total_unloaded_velocities=np.mean(current_world.total_testing_unloadedvelocities)
    total_loaded_shovel_rate = np.mean(current_world.total_testing_loaded_shovelrate)
    total_unloaded_shovel_rate = np.mean(current_world.total_testing_unloaded_shovelrate)
    total_loaded_velocities_variance = np.var(current_world.total_testing_loadedvelocities)
    total_unloaded_velocities_variance=np.var(current_world.total_testing_unloadedvelocities)
    total_loaded_shovel_rate_variance = np.var(current_world.total_testing_loaded_shovelrate)
    total_unloaded_shovel_rate_variance = np.var(current_world.total_testing_unloaded_shovelrate)
                                    # Center.simulation_velocities.append(total_velocities)
                                    
    print("Simulation_Time",round(current_world.current_time,2))
    print("Simulation_Loaded_Velocities",round(total_loaded_velocities,2))
    print("Simulation_Unloaded_Velocities",round(total_unloaded_velocities,2))
    print("Simulation_Loaded_ShovelRate",round(total_loaded_shovel_rate,4))
    print("Simulation_UnLoaded_ShovelRate",round(total_unloaded_shovel_rate,4))
    print("Simulation_Loaded_Velocities_Variance",round(total_loaded_velocities_variance,4))
    print("Simulation_Unloaded_Velocities_Variance",round(total_unloaded_velocities_variance,4))
    print("Simulation_Loaded_ShovelRate_Variance",round(total_loaded_shovel_rate_variance,4))
    print("Simulation_UnLoaded_ShovelRate_Variance",round(total_unloaded_shovel_rate_variance,4))
    
if __name__ == '__main__':
    main()                    
    print ('Discrete Event Simualtion completed')    
    Data_Logger.stop_recording()

    # print(temp_truck.__dict__)