# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 21:11:45 2023

@author: Bijo Sebastian, Sayooj P
"""

import random
import Map
import Params
import Data_Logger
import numpy as np

class Truck:
    
    truck_id = None
    
    dt = None #Simulation step time
    
    is_loaded = False #to denote if truck is loaded 
    velocity_loaded = None #m/s
    velocity_unloaded = None #m/s
    
    dist_remaining = None #distance to be travelled
    
    bed_capacity = None #truck bed capcity in Tonne
    
    material = None #Material currently in truck bed
    
    #Flag to detect a change in state
    flag_change = False
    
    #State variable to denote which state we are on
    state = None #Can only be stop, travel, load or unload
    
    location  = None #Current  location of truck
    start_node = None #Start location of truck
    goal_node = None #Goal location of truck
    
    path = [] #Current path travelled by truck expressed as a list of nodes

    loading_velocity_tracking_array = []
    unloading_velocity_tracking_array=[]
    loading_shovelrate_array=[]
    unloading_shovelrate_array = []
    
    #Schedule for the truck
    schedule = None
    
    #Default constructor
    def __init__(self, truck_id, is_loaded, material, location):
        """
        Default constructor to set up the truck
        """
        self.truck_id = "Truck_"+str(truck_id)
        self.is_loaded = is_loaded
        self.material = material
        self.location = location
        self.state = 'Stop' #Idling on creation
        return  
    
    def set_params(self, dt, velocity_loaded, velocity_unloaded, bed_capacity):
        """
        Sets up the parameters for truck cacluations

        """
        self.dt = dt
        self.velocity_loaded = velocity_loaded
        self.velocity_unloaded = velocity_unloaded
        self.bed_capacity = bed_capacity
        
    #Step the truck through one simulation 
    def step_sim(self, truck_list):
    #  for truck in truck_list:
            # truckdetails=open("Searching_Information","w+")
            # truckdetails.write(str(truck.__dict__)+"\n")
        if self.state == 'Stop':
            self.guard()
        elif self.state == 'Travel':
            self.travel(truck_list)
        elif self.state == 'Load':
            self.load()
        elif self.state == 'Unload':
            self.unload()
        else:
            Data_Logger.terminate_on_error(str(self.truck_id) + " is in undefined state :" + str(self.state) + "\n")            
        return
    
    #Guard to ensure we follow the correct step as per schedule
    def guard(self):
        if self.schedule:
            action  = self.schedule.pop(0)
            self.state = action[0]
            if self.state == 'Travel':
                self.start_node = self.location.node 
                self.path = action[3]
                self.goal_node = self.path.pop(0)
                self.dist_remaining = Map.calculate_distance(self.start_node, self.goal_node)
                self.location = None
            elif (self.state == 'Load' or self.state == 'Unload'):
                self.location = action[1]
                self.location.service_list.append(self.truck_id)
                self.start_node = None
                self.goal_node = None
            else:
                Data_Logger.terminate_on_error(str(self.truck_id) + " is in undefined state :" + str(self.state) + "\n")            
        else:
            self.state = 'Stop'
        
        self.flag_change = True    
        return    
            
    def travel(self, truck_list):
        self.velocity_loaded=abs(round(random.gauss(4,2),2))
        Truck.loading_velocity_tracking_array.append(self.velocity_loaded)
        self.velocity_unloaded=abs(round(random.gauss(6,4),2))
        Truck.unloading_velocity_tracking_array.append(self.velocity_unloaded)
        #check if any other truck travelling on same segment
        for truck in truck_list:
            if truck.truck_id != self.truck_id:
                if (truck.goal_node == self.goal_node and truck.start_node == self.start_node):                    
                    #Move only if we keep a minimum distance to the vehicle going front  
                    if (self.dist_remaining - truck.dist_remaining) < Params.truck_gap and (self.dist_remaining - truck.dist_remaining) > 0 :
                        #If so we remain where we are
                        Data_Logger.log_data(str(truck.truck_id) + " is on same lane as " + str(self.truck_id) + " : " + str(self.truck_id) + " will wait \n")
                        return                    
        
        if self.flag_change:
            Data_Logger.log_data(str(self.truck_id) + " has started travelling \n")
            self.flag_change = False
            
        #Progress the state
        if self.dist_remaining == 0:  
            pass
        elif self.is_loaded:
            self.dist_remaining = self.dist_remaining - self.velocity_loaded*self.dt
        else:
            self.dist_remaining = self.dist_remaining - self.velocity_unloaded*self.dt
           
        Data_Logger.log_data(str(self.truck_id) + " has distance remaining " + str(self.dist_remaining) + "\n")   
        
        #Check if waypoint reached
        if self.dist_remaining < (((self.velocity_unloaded*self.dt)) + Params.float_accuracy_fix):

            Data_Logger.log_data(str(self.truck_id) + " has reached waypoint \n")   
            if self.path:
                self.start_node = self.goal_node
                self.goal_node = self.path.pop(0)
                self.dist_remaining = Map.calculate_distance(self.start_node, self.goal_node)
            else:
                Data_Logger.log_data(str(self.truck_id) + " has finished journey \n")   
                self.guard()
            
        #Check if something went wrong
        if self.dist_remaining < -1.0*(((self.velocity_unloaded*self.dt)) + Params.float_accuracy_fix):
            Data_Logger.terminate_on_error(str(self.truck_id) + " distance remaining for travel is negative:" + str(self.dist_remaining) + "\n")                        
            
        return
            
    def load(self):
        #Check if we are good to load
        self.location.shovel_rate = abs(round(random.gauss(0.5,0.1),2))
       
        Truck.loading_shovelrate_array.append(self.location.shovel_rate)
        if self.location.service_list[0] != self.truck_id:
            Data_Logger.log_data(str(self.truck_id) + " is waiting for turn at " + str(self.location.station_id) + " : ")
            Data_Logger.log_data("Currently servicing " + str(self.location.service_list[0][0]) + "\n")
            return
        
        if self.flag_change:
           Data_Logger.log_data(str(self.truck_id) + " has started Loading \n")
           self.flag_change = False
         
        #Progress the state
        self.material = self.material + self.location.shovel_rate*self.dt
        self.location.material_available = self.location.material_available - self.location.shovel_rate*self.dt
        Data_Logger.log_data(str(self.truck_id) + " has current load " + str(self.material) + "\n")
        Data_Logger.log_data("Material available at " + str(self.location.station_id) + " is " + str(self.location.material_available) + "\n")    
            
        #Check if bed full 
        if abs(self.material - self.bed_capacity) < (((self.location.shovel_rate*self.dt)/2.0) + Params.float_accuracy_fix):         
           Data_Logger.log_data(str(self.truck_id) + " has finished loading\n")
           #Remove from truck list at the station
           self.location.service_list.pop(0)
           self.is_loaded = True   
           self.material = self.bed_capacity 
           self.location.material_available = self.location.prev_available_material - self.bed_capacity   
           self.location.prev_available_material = self.location.material_available   
           self.guard()
         
        #Check if something went wrong
        if self.material > (self.bed_capacity + Params.float_accuracy_fix):
           Data_Logger.terminate_on_error(str(self.truck_id) + " is on overload by" + str(self.material - self.bed_capacity) + "\n")                                  
        
        return
         
    def unload(self):
        self.location.shovel_rate = abs(round(random.gauss(0.25,0.1),2))
       
        Truck.unloading_shovelrate_array.append(self.location.shovel_rate)
        #Check if we are good to unload
        if self.location.service_list[0] != self.truck_id:
            Data_Logger.log_data(str(self.truck_id) + " is waiting for turn at " + str(self.location.station_id) + " : ")
            Data_Logger.log_data("Current servicing " + str(self.location.service_list[0][0]) + "\n")            
            return
        
        if self.flag_change:
            Data_Logger.log_data(str(self.truck_id) + " has started unloading \n")            
            self.flag_change = False
         
        #Progress the state
        self.material = self.material - self.location.shovel_rate*self.dt
        self.location.material_available  = self.location.material_available  + self.location.shovel_rate*self.dt
        Data_Logger.log_data(str(self.truck_id) + " has current load" + str(self.material) + "\n")
        Data_Logger.log_data("Material available at" + str(self.location.station_id) + " is " + str(self.location.material_available) + "\n")
                        
        #Check if bed empty 
        if self.material < Params.float_accuracy_fix:
           Data_Logger.log_data(str(self.truck_id) + " has finished unloading\n")
               
           #Remove from truck list at the station
           self.location.service_list.pop(0)
           self.is_loaded = False   
           self.material = 0.0
           self.location.material_available = self.location.prev_available_material + self.bed_capacity      
           self.location.prev_available_material = self.location.material_available  
           self.guard()
                      
        #Check if something went wrong
        if self.material < -1.0*Params.float_accuracy_fix:
           Data_Logger.terminate_on_error(str(self.truck_id) + " is on underload by" + str(self.material) + "\n")                                             
             
        return
         
    