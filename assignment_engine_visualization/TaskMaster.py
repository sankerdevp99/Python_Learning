# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:08:49 2023

@author: Bijo Sebastian, Sayooj P
"""
import Data_Logger
import Params
import operator
import json
import yaml
import os

#Use the common parameters specified in the yaml file
base_dir = os.path.dirname(os.path.abspath(__file__))
properties = yaml.safe_load(open(os.path.join(base_dir,"Common_Files", "CommonProperties.yaml"), "r"))


# Load the JSON file containing schedules
schedules = json.load(open(os.path.join(base_dir,"Results","output.json"),"r"))
count = 0

#Task master
def task_master(world):
    
    for i,truck in enumerate(world.truck_list):
        # global count
        # count.append(i)
        # print("The truck list",world.truck_list)
        # print("The i th function",i,"The Truck",truck,"The truck list",world.truck_list)
       
        if i >= len(schedules):
            # print(f"Index {i} is out of range for the list 'schedules'") 
            global count
            count+=1
            # print("I THE COUNTER VALUE IS ",count)
                      
       
          
        if len(schedules[i])==1:
            # print("The length of Schedules",len(schedules[i]))
            # print("Class Variable",TaskMaster.schedules)
            # print("This is the Schedules FROM Task Master",schedules)
            continue
        if truck.state == 'Stop':        
            #If not loaded go to closest empty loading station
            if not truck.is_loaded:

                #take the schedule corresponding to the truck and find next loading station and the path to loading station
                path_indexes = []
                # print("path_indexes in taskmaster class if truck state is stop",path_indexes)
                while schedules[i]:
                    # print("i th value is",i,"Schedules",schedules[i])
                    x = schedules[i][0]
                    # print("X variable  in taskmaster class if truck state is stop",x)
                    if x < properties["num_loading_stations"]:                                             # loading station
                        path_indexes.append(x)
                        # print("path_indexes in taskmaster class if truck state is stop and x < properties[num_loading_stations] ",path_indexes)
                        break
                    else:
                        x = schedules[i].pop(0)
                        # print("schedules popping out in else statement",x)
                        

                        path_indexes.append(x)
                        # print("path_index appending with X  ELSE",x)
                       

                goal_node = path_indexes[-1]
                # print("The Goal Node is ", goal_node)
                path, distance_to_travel = world.map_search_setup.node_to_path(path_indexes)
                # print("Path and distance_to_travel",path,"and ", distance_to_travel)
        
                assigned_loading_station = world.loading_station_list[goal_node] 
                # print("Assigned_loading_station is ",world.loading_station_list[goal_node] )                

                
                temp_schedule = [['Travel', assigned_loading_station, distance_to_travel, path], ['Load', assigned_loading_station]]
                # print("The temp_schedule is ",temp_schedule)
                Data_Logger.log_data(str(truck.truck_id) + " is scheduled to travel to " + str(assigned_loading_station.station_id) + "\n")
    
                truck.schedule = temp_schedule
                break
            
            #If loaded go to closest empty unloading station
            else:

                #take the schedule corresponding to the truck and find next unloading station and the path to unloading station
                path_indexes = []
                # print("The path index the schedule corresponding to the truck and find next unloading station and the path to unloading station ",path_indexes)
                while schedules[i]:
                    # print("The schedules for find next unloading station ",schedules[i],"schedules",schedules)
                    x = schedules[i][0]
                    # print("X variable  in taskmaster class for next unloading station ",x)
                    if x >= properties["num_loading_stations"] and x < properties["num_loading_stations"]+properties["num_unloading_stations"]:  
                        # print("path_indexes in taskmaster class if truck state unloading x >= properties[num_loading_stations] and x < properties[num_loading_stations]+properties[num_unloading_stations] ",path_indexes)        # unloading station
                        path_indexes.append(x)
                        # print("X appended variable  in taskmaster class for next unloading station ",x)
                        # print("X appended path index  in taskmaster class for next unloading station ",path_indexes)

                        break
                    else:
                        x = schedules[i].pop(0)
                        # print("X variable  in taskmaster class for next unloading station Else part ",x)
                        path_indexes.append(x)
                        # print(path_indexes,"path_index in else part of unloading station")
                goal_node = path_indexes[-1]
                # print("Goal Node in goal_node  class for next unloading station in else part ",goal_node)
                path, distance_to_travel = world.map_search_setup.node_to_path(path_indexes)
                # print("Path and Distance to travel ",path, " and", distance_to_travel)
                assigned_unloading_station = world.unloading_station_list[goal_node-properties["num_loading_stations"]]      
                # print("Assigned Unloading Station", assigned_unloading_station)
    
                temp_schedule = [['Travel', assigned_unloading_station.node.node_id, distance_to_travel, path], ['Unload', assigned_unloading_station]]
                Data_Logger.log_data(str(truck.truck_id) + " is scheduled to travel to " + str(assigned_unloading_station.station_id) + "\n")
                        
                truck.schedule = temp_schedule
                # print("Temp_SChedule",temp_schedule)
                break

       

    
    #Sort service list at all loading stations
    for loading_station in world.loading_station_list:
        # print("The loading_staions",world.loading_station_list)       
        Data_Logger.log_data("Service list and distance to be travelled by trucks for " + str(loading_station.station_id) + " is: " + str(loading_station.service_list) + "\n")
        
    #Sort service list at all unloading stations
    for unloading_station in world.unloading_station_list:
        
       
        # print("The loading_staions",world.unloading_station_list)
        Data_Logger.log_data("Service list and distance to be tarvelled by trucks for " + str(unloading_station.station_id) + " is: " + str(unloading_station.service_list) + "\n")
        
    #Check if all material requirements are met 
    world.flag_unloading_station_requirment_met = True
    for unloading_station in world.unloading_station_list:
        # print("The Unloading_staions",world.unloading_station_list,"Station",unloading_station)
        # print("Unloading_station material requirement",unloading_station.material_requirement,"Unloading_station material requirement",unloading_station.material_available)

        if (unloading_station.material_requirement - unloading_station.material_available) > Params.float_accuracy_fix:
            world.flag_unloading_station_requirment_met = False
            break
    # print("The total function called task master",count)
            
    return