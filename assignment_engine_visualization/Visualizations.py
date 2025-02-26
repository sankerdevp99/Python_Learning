# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 20:55:36 2023

@author: Bijo Sebastian, Sayooj P
"""
import matplotlib.pyplot as plt
import Map
import Map_Search_Setup

#Setup plot
plt.close('all') 
fig,ax = plt.subplots(1)
plt.ion()
plt.xlim(7900, 10600)
plt.ylim(8500, 13000)
truck_plot_object_list = []
building_plot_object_list = []
material_text_object_list = []

def visualize_map():
    for node in Map.node_list:
        plt.plot(node.location_coordinates[0], node.location_coordinates[1], 'ko', ms = 10.0)
        #Plot path to connections
        for neighbor_id in node.connectivity:
            plt.plot([node.location_coordinates[0], Map.node_list[neighbor_id].location_coordinates[0]], [node.location_coordinates[1], Map.node_list[neighbor_id].location_coordinates[1]], '--k', alpha = 0.5)
    
    return

def visualize_world_first_time(world):
    #plot time
    temp = plt.text(10200, 12700, "Time :" + str(round(world.current_time,1)), fontsize = 7, bbox=dict(facecolor='white', alpha=0.5))    
    material_text_object_list.append(temp)
    
    #Plot parking lot
    for parking_lot in world.parking_lot_list:
        plt.plot(parking_lot.node.location_coordinates[0], parking_lot.node.location_coordinates[1], 'go', ms = 10.0)
        plt.text(parking_lot.node.location_coordinates[0], parking_lot.node.location_coordinates[1], parking_lot.station_id, fontsize = 7, bbox=dict(facecolor='white', alpha=0.5))
    
    #Plot the Loading stations
    for loading_station in world.loading_station_list:
        temp = plt.plot(loading_station.node.location_coordinates[0], loading_station.node.location_coordinates[1], 'ro', ms = 10.0)
        building_plot_object_list.append(temp[0])
        temp = plt.text(loading_station.node.location_coordinates[0], loading_station.node.location_coordinates[1], loading_station.station_id + "\nMaterial:" + str(round(loading_station.material_available,1)), fontsize = 7, bbox=dict(facecolor='white', alpha=0.5))        
        material_text_object_list.append(temp)
        
    #Plot the Unloading stations
    for unloading_station in world.unloading_station_list:
        temp = plt.plot(unloading_station.node.location_coordinates[0], unloading_station.node.location_coordinates[1], 'bo', ms = 10.0)
        building_plot_object_list.append(temp[0])
        temp = plt.text(unloading_station.node.location_coordinates[0], unloading_station.node.location_coordinates[1], unloading_station.station_id + "\nMaterial: " + str(round(unloading_station.material_available,1)), fontsize = 7,  bbox=dict(facecolor='white', alpha=0.5))        
        material_text_object_list.append(temp)
        
    return

def visualize_world_update(world):
    text_object_id = 0
    plot_object_id = 0
    
    #Update time
    # print(f'The text_object_id{text_object_id}')
    # a=len(material_text_object_list[text_object_id])
    # print("The material text object ",a)
    material_text_object_list[text_object_id].set_text("Time :" + str(round(world.current_time,1)))
    text_object_id = text_object_id + 1
    
    #Update the Loading stations
    for loading_station in world.loading_station_list:
        material_text_object_list[text_object_id].set_text(loading_station.station_id + "\nMaterial:" + str(round(loading_station.material_available,1)))
        text_object_id = text_object_id + 1
        
        if loading_station.material_available >= 0.01:
            building_plot_object_list[plot_object_id].set_markerfacecolor('red')
        else:
            building_plot_object_list[plot_object_id].set_markerfacecolor('none')
        plot_object_id = plot_object_id + 1
        
        
    #Update the Unloading stations
    for unloading_station in world.unloading_station_list:
        material_text_object_list[text_object_id].set_text(unloading_station.station_id + "\nMaterial: " + str(round(unloading_station.material_available,1)))
        text_object_id = text_object_id + 1
        
        if (unloading_station.material_available - unloading_station.material_requirement) >= -0.01:
            building_plot_object_list[plot_object_id].set_markerfacecolor('blue')
        else:
            building_plot_object_list[plot_object_id].set_markerfacecolor('none')
        plot_object_id = plot_object_id + 1
        
    return

def visualize_trucks_first_time(world):
    
    #Plot each truck
    for truck in world.truck_list:
        temp = plt.plot(truck.location.node.location_coordinates[0], truck.location.node.location_coordinates[1], 'yo', ms = 5.0)
        truck_plot_object_list.append(temp[0])
        temp = plt.text(truck.location.node.location_coordinates[0], truck.location.node.location_coordinates[1], truck.truck_id, fontsize = 7)
        truck_plot_object_list.append(temp)
            
    return
    
def visualize_trucks_update(world):
    
    #Update each truck
    plot_object_id = 0
    for truck in world.truck_list:
        if truck.state == 'Travel':
            
            #compute new position
            total_distance = Map.calculate_distance(truck.start_node, truck.goal_node)
            start_point = truck.start_node.location_coordinates
            goal_point = truck.goal_node.location_coordinates
            dist_fraction = truck.dist_remaining/total_distance
            current_location_x = goal_point[0] + dist_fraction*(start_point[0] - goal_point[0]) 
            current_location_y = goal_point[1] + dist_fraction*(start_point[1] - goal_point[1]) 
            
            #update position of plot
            truck_plot_object_list[plot_object_id].set_xdata(current_location_x)
            truck_plot_object_list[plot_object_id].set_ydata(current_location_y)
            
            #Update load status
            if truck.is_loaded:
                truck_plot_object_list[plot_object_id].set_markerfacecolor('yellow')
            else:
                truck_plot_object_list[plot_object_id].set_markerfacecolor('none')
                
            plot_object_id = plot_object_id + 1
            
            #update position of text
            truck_plot_object_list[plot_object_id].set_position((current_location_x, current_location_y))
            plot_object_id = plot_object_id + 1
            
        else:
            
            #update position of plot
            truck_plot_object_list[plot_object_id].set_xdata(truck.location.node.location_coordinates[0])
            truck_plot_object_list[plot_object_id].set_ydata(truck.location.node.location_coordinates[1])            
                        
            #Update load status
            if truck.is_loaded:
                truck_plot_object_list[plot_object_id].set_markerfacecolor('yellow')
            else:
                truck_plot_object_list[plot_object_id].set_markerfacecolor('none')
            plot_object_id = plot_object_id + 1
                
            #update position of text
            truck_plot_object_list[plot_object_id].set_position((truck.location.node.location_coordinates[0], truck.location.node.location_coordinates[1]))
            plot_object_id = plot_object_id + 1
            
    plt.show()
    plt.pause(0.001)
    return