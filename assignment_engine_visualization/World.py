# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 14:28:01 2023

@author: Bijo Sebastian, Sayooj P
"""
import Map_Search_Setup
import TaskMaster
import Data_Logger
import Params

class World:
    world_id = None
    
    #Lists of items in the world
   
    #Current simulation time in the world 
    current_time = None
    
    #Process parameters
    dt = None #simulation time step in seconds
    
    #truck parameters
    truck_velocity_loaded = None #velocity of loaded truck in meter per seconds
    truck_velocity_unloaded = None #velocity of unloaded truck in meter per seconds
    truck_capacity = None #in tonn
    
    #sbovel parameters
    loading_rate = None #tonn per second
    unloading_rate = None #tonn per second    

    #Setup the search base
    map_search_setup = Map_Search_Setup.Map_search_setup()
    map_search_setup.map_node_list = None
    
    #Flag denoting if loading station requirments have been met 
    flag_unloading_station_requirment_met = False

    

    total_testing_loadedvelocities = []
    total_testing_unloadedvelocities = []
    total_testing_unloadedvelocities = []
    total_testing_loaded_shovelrate=[]

    
    #Default constructor
    def __init__(self, world_id):

        """
        Default constructor to set up the world
        """
        
        self.world_id = "World_"+str(world_id)
       
    
        
        #Initiate time 
        self.current_time = 0.0

        self.loading_station_list = []
        self.unloading_station_list = []
        self.parking_lot_list = []
        self.truck_list = []
            
        return  
                            
    #Steps all the trucks in the world through one simulation time step
    def step_sim(self):        
        self.current_time = self.current_time + self.dt 
          
        
        if (self.current_time % Params.data_log_interval) < 0.1:            
            Data_Logger.data_logger_flag  = True
            Data_Logger.log_data("\n\nForward simulating the world to sim_time :" + str(self.current_time) + "\n")            
        else:
            Data_Logger.data_logger_flag  = False
        
        TaskMaster.task_master(self)
        # print(TaskMaster.schedules,"World Class Schedules")


        
        for truck in self.truck_list:
            # print(f'Truck is {truck} from Truck List {self.truck_list}')
            # print(f'Truck_ID data type is {truck.truck_id} and Truck State data type is {truck.state}')
            # print(f'Truck_ID is {str(truck.truck_id)} and Truck State is {str(truck.state)}')
            # Data_Logger.log_data(str(truck.truck_id) + " is currently in state " + str(truck.state) + "\n")
            truck.step_sim(self.truck_list)
        World.total_testing_loadedvelocities=truck.loading_velocity_tracking_array
        World.total_testing_unloadedvelocities=truck.unloading_velocity_tracking_array
        World.total_testing_loaded_shovelrate=truck.loading_shovelrate_array
        World.total_testing_unloaded_shovelrate=truck.unloading_shovelrate_array
        

        

        
            
                
            
        
    