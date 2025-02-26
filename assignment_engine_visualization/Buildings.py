# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 22:17:21 2023

@author: Bijo Sebastian, Sayooj P
"""
class Parking_lot:
    node = None
    #Default constructor
    def __init__(self, station_id):
        """
        Default constructor to set up the Loading_station
        """
        self.station_id = "Parking_lot_"+str(station_id)
        return

class Shovel:
    station_id = None 
    shovel_rate = None #Rate at which shovelling is being done 
    material_available = None #Material available in tonn
    material_requirement = None #Material requirement in tonn
    material_to_be = None #Material in future in tonn
    service_list = None #Queue of trucks to be serviced
    prev_available_material = None # available material in loading or unloading station before starts shoveling for a truck.

    def __init__(self, shovel_rate, material_available, material_requirement):
        """
        Default constructor to set up the shovel
        """
        self.shovel_rate = shovel_rate
        self.material_available = material_available
        self.material_requirement = material_requirement
        return

class Loading_station(Shovel):
    node = None
    #Default constructor
    def __init__(self, station_id, shovel_rate, material_available):
        """
        Default constructor to set up the Loading_station
        """
        self.station_id = "Loading_station_"+str(station_id)
        self.service_list = []
        self.truck_on_work = None
        self.prev_available_material = material_available
        Shovel.__init__(self, shovel_rate, material_available, None)
        return
    
class Unloading_station(Shovel):
    node = None
    #Default constructor
    def __init__(self, station_id, shovel_rate, material_available, material_requirement):
        """
        Default constructor to set up the Unloading_station
        """
        self.station_id = "Unloading_station_"+str(station_id)
        self.prev_available_material = 0.0
        self.service_list = []
        Shovel.__init__(self, shovel_rate, material_available, material_requirement)
        return

