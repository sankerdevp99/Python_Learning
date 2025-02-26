#!/usr/env/bin python3
from ortools.linear_solver import pywraplp
import numpy as np

# Create a solver instance
solver = pywraplp.Solver.CreateSolver('SCIP')

num_states = 8 #Last two being the transfer rows
num_transfer_rows = 2
num_time_steps = 14
num_trucks = 3

material_avaialble_LS1 = 3
loading_rate = 1
material_requirment_US1 = 3
unloading_rate = 0.33
loading_time = int(material_avaialble_LS1/loading_rate)
unloading_time = int(material_requirment_US1/unloading_rate)
travel_time = 2

def create_variables(num_rows,num_columns):
    variables = {}
    for i in range(num_rows):
        for j in range(num_columns):
            var_name = f'X_{i}_{j}'
            if i == 1 or i == 4: # load or unload row
                variables[(i,j)] = solver.BoolVar(var_name)
            else: #All other rowas max is the number of trucks
                variables[(i,j)] = solver.IntVar(0,num_trucks,var_name)        
    return variables

        
def main():
    print ('Starting assigmment')    
    #Create variables
    variables_list = create_variables(num_states,num_time_steps)
    
    #Create constraints
    loading_capacity_constraint = solver.Constraint(loading_time, loading_time) #time steps at LS_1  
    unloading_capacity_constraint = solver.Constraint(unloading_time, unloading_time) #tiem steps at US_1 
    truck_constraint_start = solver.Constraint(num_trucks, num_trucks) # Number of trucks at start state
    
    for var_key, variable in variables_list.items():     
        if var_key[0] == 0 and var_key[1] == 0:
            ##  Truck constraint at start:  Number of trucks starts to travel == num of trucks  
            truck_constraint_start.SetCoefficient(variable,1)
        
        if var_key[0] == 1:
            #Total loading capcity 
            loading_capacity_constraint.SetCoefficient(variable,1)

        if var_key[0] == 4:
            #Total unloading capacity
            unloading_capacity_constraint.SetCoefficient(variable,1)
                
    for column in range(num_time_steps):
        #total number of truck at a given time step
        trucks_at_a_time = solver.Constraint(3,3)
        for row in range(num_states-num_transfer_rows):
            variable = variables_list[row,column]
            trucks_at_a_time.SetCoefficient(variable,1)
       
    #Process constraint for row 0 to row 1: wait to load
    for column in range(num_time_steps-1):
        solver.Add(variables_list[(0,column+1)] + variables_list[(1,column+1)] == variables_list[(0,column)])
    
    #Process constraint for row 1 to row 2: load to travel
    for column in range(num_time_steps-2):
        solver.Add(variables_list[(1,column)] + variables_list[(1,column+1)] == variables_list[(2,column+2)])
    
    #Process constraint from row 2 to row 6: travel to transfer 
    for column in range(num_time_steps-2):
        solver.Add(variables_list[(2,column)] == variables_list[(6,column+1)] + variables_list[(6,column+2)])
    
    #Process constraint for row 3 to row 7 using row 6: wait to transfer using transfer
    for column in range(num_time_steps-1):
        solver.Add(variables_list[(3,column)] + variables_list[(6,column+1)] - variables_list[(7,column+1)] == variables_list[(3,column+1)])
         
    #Process constraint for row 7 to row 4: transfer to unload
    for column in range(num_time_steps-2):
        solver.Add(variables_list[(7,column)] + variables_list[(7,column+1)]  + variables_list[(7, column+2)] == variables_list[(4, column+2)])
                   
    #Process constraint for row 4 to row 5: unload to parking
    for column in range(num_time_steps-3):
        solver.Add(variables_list[(5,column+3)] - variables_list[(5,column)] == variables_list[(4,column)])
    
    # Set the objective function: minimize the sum of all unloading steps multiplied by a coefficient where coefficient is column number plus one
    objective = solver.Objective()
    for var_key, variable in variables_list.items():  
        if var_key[0] == 4:
            value = 1 + var_key[1]    
            objective.SetCoefficient(variable,value)
    objective.SetMinimization()
    solver.Solve()
    
    sol_matrix = np.zeros((num_states- num_transfer_rows,  num_time_steps))
    #sol_matrix = np.zeros((num_states ,  num_time_steps))
    for var_key, variable in variables_list.items():
        if variable.solution_value() >= 1 and var_key[0] < num_states - num_transfer_rows:
            sol_matrix[var_key[0]][var_key[1]] = variable.solution_value()
    
    print(sol_matrix)
    
if __name__ == '__main__':
    main()                    
    print ('Assignment completed')    
