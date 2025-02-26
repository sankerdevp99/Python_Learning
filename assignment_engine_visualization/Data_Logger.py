# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 14:39:48 2023

@author: Bijo Sebastian
"""

import datetime
import io

#Setup logfile
#Get date time string for creating log file name
now = datetime.datetime.now()
date_and_time_string = now.strftime("%Y_%m_%d_%H_%M_%S")
log_file_name = "Log_" + date_and_time_string + ".txt"
# log_file_handle = open(log_file_name, "w+")
log_file_handle = io.StringIO()

log_file_handle.write("Time stamp for simulation run :" + date_and_time_string + "\n")
data_logger_flag = True

def log_data(info_string):
#Function to log data contained in info_string
    if data_logger_flag:
        log_file_handle.write(info_string)
    return

def stop_recording():
#Function to stop data logging and close file
    log_file_handle.write("\n\nDiscrete Event Simulation completed \n")  
    log_file_handle.close()
    return

def terminate_on_error(error_msg):
#Function to stop data logging and close file, as well as stop program due to error
    print("Encountered error")
    print(error_msg)
    print("Stopping Discrete Event Simulation")
    log_file_handle.write(error_msg)
    log_file_handle.write("\n\nEncountered error, stopping Discrete Event Simulation \n")  
    log_file_handle.close()
    exit()
    return
