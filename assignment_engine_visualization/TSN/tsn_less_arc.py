# -*- coding: utf-8 -*-
"""
@author: Sayooj P , Bijo Sebastian
"""
import pandas as pd
from ast import literal_eval
from ortools.linear_solver import pywraplp
solver = pywraplp.Solver.CreateSolver('SCIP')
import datetime
import time
import json
import yaml
import os

# Load the parameter YAML configuration file
properties = yaml.safe_load(open(os.path.join("Common_Files", "CommonProperties.yaml"), "r"))

# Setup logfile
# Get date time string for creating log file name
now = datetime.datetime.now()
date_and_time_string = now.strftime("%Y_%m_%d_%H_%M_%S")
lp_log_file_name = "LP_" + date_and_time_string + ".lp"

lp_log_file_handle = open(os.path.join("Results",lp_log_file_name), "w+")

#Import dataframe contains informations about nodes_and_junctions
all_states = pd.read_excel(os.path.join("Common_Files","all_states.xlsx"))
# changing the datatype of connectivity to list
all_states['connectivity'] = all_states['connectivity'].apply(literal_eval)

#define important parameters
num_time_steps = properties["num_time_steps"]
num_of_loading_stations = properties["num_loading_stations"]
num_of_unloading_stations = properties["num_unloading_stations"]
num_of_junctions = properties["num_junctions"]
num_states = len(all_states)
num_trucks = properties["num_trucks"]
truck_capacity = properties["truck_capacity"]
velocity_unloaded = properties["unloaded_truck_velocity"]
velocity_loaded = properties["loaded_truck_velocity"]
start_parking_stations = properties["trucks_per_station"]
num_start_stations = len(start_parking_stations)
tsn_dt = properties["tsn_dt"]  # 1 time step in tsn equal to  tsn_dt seconds. 


#create node matrix
def create_node_matrix(num_rows,num_columns):
    matrix = []
    counter = 0
    for i in range(num_rows):
      row = []
      for j in range(counter,num_columns+counter):
         row.append(j)
         counter = j+1
      matrix.append(row)       
    return matrix 


node_matrix = create_node_matrix(num_states,num_time_steps)

#define the index minimum and maximum of states based on the excel sheet.
loading_min_index = 0
loading_max_index = num_of_loading_stations - 1 #5
unloading_min_index = loading_max_index +1  #6
unloading_max_index = unloading_min_index + num_of_unloading_stations -1 # 11
min_junction_index = unloading_max_index +1 # 12
max_junction_index = min_junction_index + 2* num_of_junctions -1          #41
min_waiting_index = max_junction_index +1  #42
max_waiting_index = min_waiting_index + num_of_loading_stations + num_of_unloading_stations -1  #53
min_travelling_index = max_waiting_index + 1 #54

max_parking_end_index = num_states -1 #151
min_parking_end_index = max_parking_end_index - num_of_unloading_stations + 1 #146
max_parking_start_index = min_parking_end_index - 1
min_parking_start_index = max_parking_start_index - num_start_stations + 1

max_travelling_index = min_parking_start_index - 1 #144


def create_variables():
    #create variables and store in a dictionary
    variable_dict = {}
    variable_start_dict = {} #a variable starting with node name 
    variable_end_dict = {} # not used
    for row in range(num_states):
      for column in range(num_time_steps):
        #create variables for start parking states and store in different dictionries
        if row >= min_parking_start_index and row <= max_parking_start_index:
            connectivity = all_states["connectivity"][row]
            num_trucks_parked = all_states["num_trucks_parked"][row]
            connection = connectivity[0] # parking row only contain single element. Same junction node
            var_name = f'X_{node_matrix[row][column]}_{node_matrix[connection][column]}'
            variable = solver.IntVar(0,num_trucks_parked,var_name)
            variable_dict[(node_matrix[row][column], node_matrix[connection][column])] = variable

            if node_matrix[row][column] in variable_start_dict:  # if key in dictionary append variable in the list
                variable_start_dict[node_matrix[row][column]].append(variable)
            else:       #else create a list and add the variable
                variable_start_dict[node_matrix[row][column]] = [variable]
            if node_matrix[connection][column] in variable_end_dict:  # not used
                variable_end_dict[node_matrix[connection][column]].append(variable)
            else:
                variable_end_dict[node_matrix[connection][column]] = [variable]

        #create variables for loading and unloading states and store in different dictionries
        elif row >= loading_min_index and row <= unloading_max_index:
            connectivity = all_states["connectivity"][row]
            time = int(all_states["time"][row] / tsn_dt) 
            for connection in connectivity:
                if column < num_time_steps -time:
                    var_name = f'X_{node_matrix[row][column]}_{node_matrix[connection][column+time]}'
                    variable = solver.BoolVar(var_name)
                    variable_dict[(node_matrix[row][column], node_matrix[connection][column+time])] = variable

                    if node_matrix[row][column] in variable_start_dict:  
                        variable_start_dict[node_matrix[row][column]].append(variable)
                    else:       
                        variable_start_dict[node_matrix[row][column]] = [variable]
                    if node_matrix[connection][column+time] in variable_end_dict:
                        variable_end_dict[node_matrix[connection][column+time]].append(variable)
                    else:
                        variable_end_dict[node_matrix[connection][column+time]] = [variable]
        #create variables for waiting states and store in different dictionries
        elif row >= min_waiting_index and row <= max_waiting_index:
            if column < num_time_steps -1:
                var1_name = f'X_{node_matrix[row][column]}_{node_matrix[row][column+1]}'
                variable = solver.BoolVar(var1_name)
                variable_dict[(node_matrix[row][column], node_matrix[row][column+1])] = variable

                if node_matrix[row][column] in variable_start_dict:  
                        variable_start_dict[node_matrix[row][column]].append(variable)
                else:       
                    variable_start_dict[node_matrix[row][column]] = [variable]
                if node_matrix[row][column+1] in variable_end_dict:
                    variable_end_dict[node_matrix[row][column+1]].append(variable)
                else:
                    variable_end_dict[node_matrix[row][column+1]] = [variable]

            connectivity = all_states["connectivity"][row]
            connection = connectivity[0] #single connection for waiting row
            
            var_name = f'X_{node_matrix[row][column]}_{node_matrix[connection][column]}'
            variable = solver.BoolVar(var_name)
            variable_dict[(node_matrix[row][column], node_matrix[connection][column])] = variable

            if node_matrix[row][column] in variable_start_dict:  # if key in dictionary append variable in the list
                variable_start_dict[node_matrix[row][column]].append(variable)
            else:       #else create a list and add the variable
                variable_start_dict[node_matrix[row][column]] = [variable]
            if node_matrix[connection][column] in variable_end_dict:
                variable_end_dict[node_matrix[connection][column]].append(variable)
            else:
                variable_end_dict[node_matrix[connection][column]] = [variable]
        
        #create variables for end parking states and store in different dictionries
        elif row >= min_parking_end_index and row <= max_parking_end_index:
            pass
        #create variables for travelling states and store in different dictionries
        elif row >= min_travelling_index and row <= max_travelling_index:
            connectivity = all_states["connectivity"][row]
            connection = connectivity[0] #single connection in travelling row
            distance = int(all_states["distance"][row])
            # based on which node youre moving find truck is loaded or unloaded
            if connectivity[0] <= loading_max_index or (connectivity[0] >=min_junction_index and connectivity[0] <= min_junction_index+num_of_junctions -1) : # moving to ls or ls junctions => truck is unloaded
                time = int((distance/ velocity_unloaded)/ tsn_dt)  # just integer conversion is okay ?????????????
            else:
                time = int((distance/velocity_loaded)/tsn_dt)

        
            if column < num_time_steps -time:
                var_name = f'X_{node_matrix[row][column]}_{node_matrix[connection][column+time]}'
                variable = solver.IntVar(0,num_trucks,var_name)
                variable_dict[(node_matrix[row][column], node_matrix[connection][column+time])] = variable

                if node_matrix[row][column] in variable_start_dict:  
                    variable_start_dict[node_matrix[row][column]].append(variable)
                else:       
                    variable_start_dict[node_matrix[row][column]] = [variable]
                if node_matrix[connection][column+time] in variable_end_dict:
                    variable_end_dict[node_matrix[connection][column+time]].append(variable)
                else:
                    variable_end_dict[node_matrix[connection][column+time]] = [variable]

        #create variables for junction states and store in different dictionries
        else: #junction 
            connectivity = all_states["connectivity"][row]
            time = 0 
            for connection in connectivity:
                if column < num_time_steps -time:
                    var_name = f'X_{node_matrix[row][column]}_{node_matrix[connection][column+time]}'
                    variable = solver.IntVar(0,num_trucks,var_name)
                    variable_dict[(node_matrix[row][column], node_matrix[connection][column+time])] = variable

                    if node_matrix[row][column] in variable_start_dict:  
                        variable_start_dict[node_matrix[row][column]].append(variable)
                    else:       
                        variable_start_dict[node_matrix[row][column]] = [variable]
                    if node_matrix[connection][column+time] in variable_end_dict:
                        variable_end_dict[node_matrix[connection][column+time]].append(variable)
                    else:
                        variable_end_dict[node_matrix[connection][column+time]] = [variable]


    return variable_dict, variable_start_dict, variable_end_dict
variable_dict,variable_start_dict, variable_end_dict = create_variables()


def main():
    #call every constraints
    truck_start_constraint(min_parking_start_index, max_parking_start_index)
    for row in range(loading_min_index, unloading_max_index+1):
        capacity_constraint(row,truck_capacity,all_states['material'][row])
    mass_constraint()
    #call the objective function
    objective_function()
    #solve the model and generate schedule
    results = solve_and_print()
    schedule_extraction(results)
    

def truck_start_constraint(parking_row_min, parking_row_max):
    # total sum of values of transition arcs starts from start state should be equal to number of trucks
    for row in range(parking_row_min, parking_row_max+1):
        num_trucks_parked = all_states["num_trucks_parked"][row]
        truck_constraint = solver.Constraint(num_trucks_parked,num_trucks_parked)
        for var_key in node_matrix[row]:
            try:
                variable_list = variable_start_dict[var_key]
                for variable in variable_list:
                    truck_constraint.SetCoefficient(variable,1)
            except KeyError:
                pass

def capacity_constraint(row_num, truck_capaciy,total_material):
    #The values of hybrid arcs starting from the loading or unloading station should equal the number of trips needed to satisfy material availability or requirements
    total_visits = total_material/truck_capaciy
    if row_num <= loading_max_index:
        capacity_constraint = solver.Constraint(-solver.infinity(),total_visits)
    else:
        capacity_constraint = solver.Constraint(total_visits, solver.infinity())
    
    for var_key in node_matrix[row_num]:
        try:
            variable_list = variable_start_dict[var_key]
            for variable in variable_list:
                capacity_constraint.SetCoefficient(variable,1)
        except KeyError:
            pass


def mass_constraint():
    #The sum of values of incoming arc and outgoing arc to a state node should be  the same.
    for row in range(loading_min_index, max_travelling_index+1):
        for column in range(num_time_steps):
            key = node_matrix[row][column]
            mass_constraint_value = solver.Constraint(0,0)

            if key in variable_start_dict:
                for variable in variable_start_dict[key]:
                    mass_constraint_value.SetCoefficient(variable,-1)
            if key in variable_end_dict:
                for variable in variable_end_dict[key]:
                    mass_constraint_value.SetCoefficient(variable,1)


def objective_function():
    # Set the objective function: minimize the sum of values of hybrid acrc starts from unloading states and travelling states multiplied by a coefficient, where coefficient is column number plus one
    objective = solver.Objective()
    # to minimize unloading time
    for unloading_row in range(unloading_min_index,unloading_max_index+1):
        for var_start in node_matrix[unloading_row]:
            value = value = var_start - node_matrix[unloading_row][0] +1
            try:
                variables_list = variable_start_dict[var_start]
                for variable in variables_list:
                    objective.SetCoefficient(variable,value)
            except KeyError:
                pass
    # to minimize travelling time
    for travelling_row in range(min_travelling_index,max_travelling_index+1):
        for var_start in node_matrix[travelling_row]:
            value = value = var_start - node_matrix[travelling_row][0] +1
            try:
                variables_list = variable_start_dict[var_start]
                for variable in variables_list:
                    objective.SetCoefficient(variable,value)
            except KeyError:
                pass
        
    objective.SetMinimization()

def solve_and_print():
    #solve the mathematical model created
    solver_time = time.time()
    status = solver.Solve()
    print("Time taken by the solver alone to find the solution ", time.time()- solver_time, "seconds")
    #save the objective function and constraints in an .lp file
    model_as_string = solver.ExportModelAsLpFormat(False)
    lp_log_file_handle.write( model_as_string )
    lp_log_file_handle.close()

    #returns a dictionary of variable name and values which represent a truck movement to generate schedules 
    results = {}
    if status == pywraplp.Solver.OPTIMAL:
        for var_key, variable in variable_dict.items():
            ## store the variable values
            if variable.solution_value() >= 1:
                results[var_key] = int(variable.solution_value())
    else:
        print("no solution")

    return results

def find_state_name(var_key):
    #find the state name from excel sheet
    row = var_key // num_time_steps
    column =  var_key % num_time_steps
    row_name = all_states["node_name"][row]
    state_name_and_time = f"{row_name}_at_timestep_{column}"
    return state_name_and_time



def schedule_extraction(results):
    #extracting the schedule generated by TSN
    schedules = [] #state name as in excel sheet. format: list of strings
    schedules_in_digits= [] # node value.format: list of integers. reference to find next state name of schedule

    #calculatiing the sum of all values of all variables in the results
    total_arcs = 0
    for key,var in results.items():
        total_arcs += var

    if len(results) <1:
        return
    else:
        #creating n number of lists which have first process state name. n means number of trucks
        for var_key,variable in results.items(): 
            if var_key[0] >= node_matrix[min_parking_start_index][0] and var_key[0] <= node_matrix[max_parking_start_index][num_time_steps-1]:
                #first process state name as per the excel sheet
                schedules.extend([[find_state_name(var_key[0])] for _ in range(variable)])
                #firs process state node number for reference inorder to find next state 
                schedules_in_digits.extend([[var_key[0],var_key[1]] for _ in range(variable)])

    
    #find the total schedules
    
    for i in range(len(schedules)):

        while schedules_in_digits[i][-1] <= node_matrix[min_parking_end_index][0]:
            search_element = schedules_in_digits[i][-1]

            #for the waiting states, there might be a chance of more than one truck waiting already at that state or no trucks waiting      
            if search_element >= node_matrix[min_waiting_index][0] and search_element <=node_matrix[max_waiting_index][num_time_steps-1]:
                #find the number of trucks already waiting when we reach a waiting node
                trucks_already_waiting = results.get((search_element - 1, search_element), 0) # find the value of the activity arc comes to the current node
                column_variable_count = 0
                #find the number of hybrid arcs leaving from the current waiting node
                column_variable_count += sum(variable for var_key, variable in results.items() if var_key[0] == search_element and var_key[1] != search_element+1) # find the variable key if there a column variable start from search element. else None
                #if 3 trucks where already waiting when we reach there, wait until 3 hybrid arcs leaves, next one will be ours
                while column_variable_count <= trucks_already_waiting: # while all trucks which are waiting are left 
                    if results[(search_element,search_element+1)] >= 1:
                        schedules[i].append(find_state_name(search_element + 1))
                        results[(search_element,search_element+1)] -= 1
                        schedules_in_digits[i].append(search_element + 1)
                        search_element = schedules_in_digits[i][-1]
                        column_variable_count += sum(variable for var_key, variable in results.items() if var_key[0] == search_element and var_key[1] != search_element+1)
                #the next one
                else:   
                    for var_key,variable in results.items():
                        if var_key[0] == search_element and var_key[1] != search_element+1:
                            if variable >= 1:
                                schedules[i].append(find_state_name(var_key[1]))
                                results[var_key] -=1
                                schedules_in_digits[i].append(var_key[1])
                                break
            else:
                for var_key,variable in results.items():
                    if var_key[0] == search_element:
                        if variable >= 1:
                            schedules[i].append(find_state_name(var_key[1]))
                            results[var_key] -=1
                            schedules_in_digits[i].append(var_key[1])
                            break

        # print("---------------------")
        # print(f"truck_{i+1}_schedule= {schedules[i]}")
    

    total_schedule_arcs = 0
    schedules_path = os.path.join("Results", "schedules_unformated.txt")
    with open(schedules_path, "w") as file:
        for i,schedule in enumerate(schedules):
            file.write(f"schedule_{i+1}: {schedule}\n")
            #calculating total arcs in schedules
            total_schedule_arcs += len(schedule) 

    # For testing the schedule extraction part uncomment print below: if total arcs and total schedule arcs are same, every schedule from results are added to schedule
    # print("sum of results from TSN=",total_arcs, "total number of schedules after schedule genaration =", total_schedule_arcs, "should be equal")

    convert_schedules_to_nodes(schedules_in_digits)
   
def convert_schedules_to_nodes(schedules_in_digits):
    """
    This function generates schedules considering loading station, unloading station and junctions. 
    Others like waiting, travelling etc are avoided 
    """
    node_schedule = []
    for schedule in schedules_in_digits:
        temp_schedule = []
        for digit in schedule:
            row = digit // num_time_steps
            if row <= max_junction_index:
                if row >= min_junction_index + num_of_junctions: # convert back the additional duplicate junctions
                    row -= num_of_junctions
                row_name = all_states["node_name"][row]
                temp_schedule.append(row)
        node_schedule.append(temp_schedule)
    print(node_schedule)
    #save the node shedule into a json file
    path_to_save = os.path.join('Results', "output.json")
    with open(path_to_save, "w") as file:
        json.dump(node_schedule, file)


if __name__ == "__main__":
    time_main = time.time()
    main()
    print("total time taken", time.time()- time_main, "seconds")

