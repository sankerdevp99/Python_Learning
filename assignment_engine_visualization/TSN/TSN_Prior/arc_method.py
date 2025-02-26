from ortools.linear_solver import pywraplp
# import viz # for plotly visualization
import visualizations as viz # uncomment for matplotlib visualization
import schedule_generation
# Create a solver instance
solver = pywraplp.Solver.CreateSolver('SCIP')
import time

import datetime
from enum import Enum

# Setup logfile
# Get date time string for creating log file name

now = datetime.datetime.now()
date_and_time_string = now.strftime("%Y_%m_%d_%H_%M_%S")
# date_and_time_string = "date_time"
lp_log_file_name = "LP_" + date_and_time_string + ".lp"
lp_log_file_handle = open(lp_log_file_name, "w+")

#giving name to a variable
class Mine_Process(Enum):
    parking = 0
    waiting_at_LS1 = 1
    waiting_at_LS2 = 2
    loading_at_LS1 = 3
    loading_at_LS2 = 4

    traveling_from_LS1_to_US1 = 5
    traveling_from_LS1_to_US2 = 6
    traveling_from_LS2_to_US1 = 7
    traveling_from_LS2_to_US2 = 8
    waiting_at_US1 = 9
    waiting_at_US2 = 10
    unloading_at_US1 = 11
    unloading_at_US2 = 12

    traveling_from_US1_to_LS_1 = 13
    traveling_from_US1_to_LS_2 = 14
    traveling_from_US2_to_LS_1 = 15
    traveling_from_US2_to_LS_2 = 16
    parked_at_US1 = 17
    parked_at_US2 = 18

viz.row_labels = {member.value: member.name for member in Mine_Process}
#define the rows connected with a vertical/transition arc
row_connectivity = {Mine_Process.parking.value: [Mine_Process.waiting_at_LS1.value,Mine_Process.waiting_at_LS2.value],
                    Mine_Process.waiting_at_LS1.value : [Mine_Process.loading_at_LS1.value],
                    Mine_Process.waiting_at_LS2.value : [Mine_Process.loading_at_LS2.value],
                    Mine_Process.loading_at_LS1.value: [Mine_Process.traveling_from_LS1_to_US1.value,Mine_Process.traveling_from_LS1_to_US2.value],
                    Mine_Process.loading_at_LS2.value: [Mine_Process.traveling_from_LS2_to_US1.value,Mine_Process.traveling_from_LS2_to_US2.value],
                    Mine_Process.traveling_from_LS1_to_US1.value: [Mine_Process.waiting_at_US1.value],
                    Mine_Process.traveling_from_LS1_to_US2.value: [Mine_Process.waiting_at_US2.value],
                    Mine_Process.traveling_from_LS2_to_US1.value: [Mine_Process.waiting_at_US1.value],
                    Mine_Process.traveling_from_LS2_to_US2.value: [Mine_Process.waiting_at_US2.value],
                    Mine_Process.waiting_at_US1.value:[Mine_Process.unloading_at_US1.value],
                    Mine_Process.waiting_at_US2.value: [Mine_Process.unloading_at_US2.value],
                    Mine_Process.unloading_at_US1.value: [Mine_Process.traveling_from_US1_to_LS_1.value,Mine_Process.traveling_from_US1_to_LS_2.value,Mine_Process.parked_at_US1.value],
                    Mine_Process.unloading_at_US2.value: [Mine_Process.traveling_from_US2_to_LS_1.value,Mine_Process.traveling_from_US2_to_LS_2.value,Mine_Process.parked_at_US2.value],
                    Mine_Process.traveling_from_US1_to_LS_1.value: [Mine_Process.waiting_at_LS1.value],
                    Mine_Process.traveling_from_US1_to_LS_2.value: [Mine_Process.waiting_at_LS2.value],
                    Mine_Process.traveling_from_US2_to_LS_1.value: [Mine_Process.waiting_at_LS1.value],
                    Mine_Process.traveling_from_US2_to_LS_2.value: [Mine_Process.waiting_at_LS2.value],
               

}
  
#define the parameters
num_states = 19
num_time_steps = 30
viz.num_nodes_per_row = num_time_steps
num_trucks = 3
truck_capacity = 1

material_avaialble_LS1 = 3
material_avaialble_LS2 = 2
loading_rate_of_LS1 = 0.33
loading_rate_of_LS2 = 0.5
material_requirment_US1 = 2
material_requirment_US2 = 3
unloading_rate_of_US1 = 1.0
unloading_rate_of_US2 = 0.5

travel_time_LS1_to_US1 = 2
travel_time_LS1_to_US2 = 3
travel_time_LS2_to_US1 = 3
travel_time_LS2_to_US2 = 1
travel_time_US1_to_LS1 = 1 
travel_time_US1_to_LS2 = 2
travel_time_US2_to_LS1 = 3
travel_time_US2_to_LS2 = 2

time_to_load_a_truck_at_LS1 =int(truck_capacity/loading_rate_of_LS1)
time_to_load_a_truck_at_LS2 = int(truck_capacity/loading_rate_of_LS2)
time_to_unload_a_truck_at_US1 = int(truck_capacity/unloading_rate_of_US1)
time_to_unload_a_truck_at_US2 = int(truck_capacity/unloading_rate_of_US2)

num_of_unloading_stations = 2
num_of_loading_stations = 2


boolian_rows = [3,4,11,12]
process_times = {0:0, 1:None, 2:None, 3:time_to_load_a_truck_at_LS1, 4:time_to_load_a_truck_at_LS2,
                 5:travel_time_LS1_to_US1, 6:travel_time_LS1_to_US2, 7:travel_time_LS2_to_US1, 8:travel_time_LS2_to_US2, 9:None, 10:None,
                 11:time_to_unload_a_truck_at_US1, 12:time_to_unload_a_truck_at_US2, 13:travel_time_US1_to_LS1, 14:travel_time_US1_to_LS2, 15:travel_time_US2_to_LS1, 16:travel_time_US2_to_LS2,
                 17:0, 18:0}
schedule_generation.num_time_steps = num_time_steps
schedule_generation.end_rows = [17,18]

schedule_generation.process_times = process_times


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


def create_variables(num_rows,num_columns):
    # Create a dictionary to store the decision variables in a row sequentially
    variables_in_row = {} # 0-->0-->
    #create a dictionary to store the decision variables in a column sequentially
    variables_in_column = {}
    # Create binary decision variables. integers and booleans
    for i in range(num_rows):
        for j in range(num_columns - 1):
            #var_name = f'X_{node_matrix[i][j]}_{node_matrix[i][j+1]}'
            # var_name = f'Num_trucks_{Mine_Process(i).name}_from_timestep_{j}_to_{j+1}'  #for number of trucks at time
            var_name = f'Num_trucks_from_{Mine_Process(i).name}(ts:{j}) to {Mine_Process(i).name}(ts:{j+1})'  #for schedule generation
            if i in boolian_rows:
                variables_in_row[(node_matrix[i][j], node_matrix[i][j+1])] = solver.BoolVar(var_name)
            else:
                variables_in_row[(node_matrix[i][j], node_matrix[i][j+1])] = solver.IntVar(0,num_trucks,var_name)

    for i, connected_rows in row_connectivity.items():
        for j in range(num_columns):
            for connected_row in connected_rows:
                # var_name = f'X_{node_matrix[i][j]}_{node_matrix[connected_row][j]}'
                # var_name = f'Num_trucks_transfer_from_{Mine_Process(i).name}_to_{Mine_Process(connected_row).name}_at_timestep_{j}'
                var_name = f'Num_trucks_from_{Mine_Process(i).name}(ts:{j}) to {Mine_Process(connected_row).name}(ts:{j})'
                if i in boolian_rows or connected_row in boolian_rows:
                   
                    variables_in_column[(node_matrix[i][j],node_matrix[connected_row][j])] = solver.BoolVar(var_name)  
                else:
                    variables_in_column[(node_matrix[i][j],node_matrix[connected_row][j])] = solver.IntVar(0,num_trucks,var_name)  
    return variables_in_row,variables_in_column

variables_in_row,variables_in_column = create_variables(num_states,num_time_steps)


def main():
    print('assignment started')
    #create the constraints
    truck_start_constraint(Mine_Process.parking.value) 
    mass_constraint()
    capacity_constraint(Mine_Process.loading_at_LS1.value,time_to_load_a_truck_at_LS1,material_avaialble_LS1)
    capacity_constraint(Mine_Process.loading_at_LS2.value,time_to_load_a_truck_at_LS2,material_avaialble_LS2)
    capacity_constraint(Mine_Process.unloading_at_US1.value,time_to_unload_a_truck_at_US1,material_requirment_US1)
    capacity_constraint(Mine_Process.unloading_at_US2.value,time_to_unload_a_truck_at_US2,material_requirment_US2)
    process_time_constraint(Mine_Process.loading_at_LS1.value,time_to_load_a_truck_at_LS1)
    process_time_constraint(Mine_Process.loading_at_LS2.value,time_to_load_a_truck_at_LS2)
    process_time_constraint(Mine_Process.unloading_at_US1.value,time_to_unload_a_truck_at_US1)
    process_time_constraint(Mine_Process.unloading_at_US2.value,time_to_unload_a_truck_at_US2)
    process_time_constraint(Mine_Process.traveling_from_LS1_to_US1.value,travel_time_LS1_to_US1)
    process_time_constraint(Mine_Process.traveling_from_LS1_to_US2.value,travel_time_LS1_to_US2)
    process_time_constraint(Mine_Process.traveling_from_LS2_to_US1.value,travel_time_LS2_to_US1)
    process_time_constraint(Mine_Process.traveling_from_LS2_to_US2.value,travel_time_LS2_to_US2)
    process_time_constraint(Mine_Process.traveling_from_US1_to_LS_1.value,travel_time_US1_to_LS1)
    process_time_constraint(Mine_Process.traveling_from_US1_to_LS_2.value,travel_time_US1_to_LS2)
    process_time_constraint(Mine_Process.traveling_from_US2_to_LS_1.value,travel_time_US2_to_LS1)
    process_time_constraint(Mine_Process.traveling_from_US2_to_LS_2.value,travel_time_US2_to_LS2)
 


    #create objective function
    objective_function([Mine_Process.unloading_at_US1.value,Mine_Process.unloading_at_US2.value])
    #solve, print schedule, visualize
    solve_and_print()



def process_time_constraint(row_num,time_to_complete_process):
    #eg: if 2 time step required for loading, if there is a transition arc comes to loading state, a transition arc will leave from loading state after 2 time step
    for var_key, variable in variables_in_column.items():
        if var_key[1] in node_matrix[row_num]:
            if not var_key[1] == node_matrix[row_num][num_time_steps-1]: # except last node in the row
             
                process_time_constraint = solver.Constraint(0,0)
                process_time_constraint.SetCoefficient(variable,1)
                for var_key2, variable2 in variables_in_column.items():
                    if var_key2[0] == var_key[1] + time_to_complete_process:
                        process_time_constraint.SetCoefficient(variable2, -1) 
        
def capacity_constraint(row_num, one_truck_time,material_amount):
    # eg:if total amount available at loading station is 3 Tonne and time required to load a truck(1 tonne capacity) is 2 time step. total 3*2 = 6 activity arcs should be there in that row.
    total_time = material_amount*one_truck_time
    capacity_constraint = solver.Constraint(total_time,total_time)
    for var_key, variable in variables_in_row.items():
        # for Ls1 total material available
        if var_key[0] in node_matrix[row_num]:
            capacity_constraint.SetCoefficient(variable,1) 

def truck_start_constraint(parking_row):
    # total sum of values of transition arcs starts from start state should be equal to number of trucks
    truck_constraint = solver.Constraint(num_trucks,num_trucks)
    for var_key, variable in variables_in_column.items():
        #number of truck starting == 3
        if var_key[0] in node_matrix[parking_row]: 
            truck_constraint.SetCoefficient(variable,1)

def mass_constraint():
    #for every elements in our node matrix write a mass constraint. exception start and end states. 
    #total sum of values of incoming arcs and outgoing arcs should be equal 
    for row in range(1,num_states-num_of_unloading_stations): #last elements in parking (can't) satisfy. so avoided those rows compleatly
        for column in range(num_time_steps):
           
            mass_constraint_value = solver.Constraint(0,0)
            
            for var_key, variable in variables_in_column.items():
                
                if var_key[0] == node_matrix[row][column]:
                    mass_constraint_value.SetCoefficient(variable,-1)
                if var_key[1] == node_matrix[row][column]:
                    mass_constraint_value.SetCoefficient(variable,1)    
            for var_key, variable in variables_in_row.items():
                if var_key[0] == node_matrix[row][column]:
                    mass_constraint_value.SetCoefficient(variable,-1)
                if var_key[1] == node_matrix[row][column]:
                    mass_constraint_value.SetCoefficient(variable,1)

def objective_function(unloading_station_list):
    # Set the objective function: minimize the sum of all unloading steps multiplied by a coefficient where coefficient is column number plus one
    objective = solver.Objective()
 
    for unloading_row in unloading_station_list:
        for var_key, variable in variables_in_row.items():
            if var_key[0] in node_matrix[unloading_row]:
                value = var_key[1] - node_matrix[unloading_row][0] 
                objective.SetCoefficient(variable,value)

    objective.SetMinimization()

def solve_and_print():
    status = solver.Solve()
    model_as_string = solver.ExportModelAsLpFormat(False)

    lp_log_file_handle.write( model_as_string )
    lp_log_file_handle.close()
    # print( model_as_string )
    if status == pywraplp.Solver.OPTIMAL:
        #for schedule generation
        row_results = {}
        column_results = {}
        for var_key, variable in variables_in_row.items():
            ##for visualization
            viz.connections[var_key] = int(variable.solution_value())
            ## for printing solution
            if variable.solution_value() >= 1:
                # print("In the row",var_key,"=",variable.solution_value())
                row_results[var_key] = variable
                


        for var_key, variable in variables_in_column.items():
            viz.connections[var_key] = int(variable.solution_value())
            if variable.solution_value() >= 1: 
                # print("In the column",var_key,"=",variable.solution_value())
                column_results[var_key] = variable
                
                
    else:
        print("No solution")

    # for schedule generation
    schedule_generation.row_results = row_results
    schedule_generation.column_results = column_results
    schedule_generation.main()

    #for visualization turn on this
    viz.main() 

    # print("row_res: ", row_results)
    # print("col_res: ", column_results)


if __name__ == "__main__":
    # t = time.time()
    main()
    print("assignment compleated")