import subprocess
import numpy as np
# import matplotlib
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

from scipy.stats import norm
import statistics
from sklearn.linear_model import LinearRegression


number_of_times = 500
results = []
total_simulation_time = []
total_velocities_time = []

for _ in range(number_of_times):
    # Run the script using subprocess
    result = subprocess.run(
        ['python', 'main.py'],  # Command to run the script
        capture_output=True,      # Capture stdout and stderr
        text=True                 # Return output as string
    )

    # Check if the subprocess was successful
    if result.returncode == 0:
        # Append the output to the results list
        results.append(result.stdout.strip())  # Strip to remove extra newlines

    else:
        print(f"Error running script: {result.stderr}")

# print("Collected results:", results)

Total_Simulation_Time = []
Total_Simulation_Loaded_Velocities = []
Total_Simulation_Unloaded_Velocities = []
Total_Simulation_Loaded_ShovelRate = []
Total_Simulation_Unloaded_ShovelRate=[]
Total_Simulation_Loaded_Velocities_Variance=[]
Total_Simulation_Unloaded_Velocities_Variance=[]
Total_Simulation_Loaded_ShovelRate_Variance=[]
Total_Simulation_Unloaded_ShovelRate_Variance=[]



for item in results:
    # print(item)
    
    lines = item.split('\n')
    for line in lines:
        if "Simulation_Time" in line:
            time_value = float(line.split()[1])
            # print(time_value)
            Total_Simulation_Time.append(time_value)
            # print(Total_Simulation_Time)
        elif "Simulation_Loaded_Velocities" in line and "Variance" not in line:
            loaded_velocity_value = float(line.split()[1])
            # print(loaded_velocity_value)
            Total_Simulation_Loaded_Velocities.append(loaded_velocity_value)
        elif "Simulation_Unloaded_Velocities" in line and "Variance" not in line:
            unloaded_velocity_value = float(line.split()[1])
            Total_Simulation_Unloaded_Velocities.append(unloaded_velocity_value)
        elif "Simulation_Loaded_ShovelRate" in line and "Variance" not in line:
            loaded_shovel_rate = float(line.split()[1])
            Total_Simulation_Loaded_ShovelRate.append(loaded_shovel_rate)
        elif "Simulation_UnLoaded_ShovelRate" in line and "Variance" not in line:
            unloaded_shovel_rate = float(line.split()[1])
            Total_Simulation_Unloaded_ShovelRate.append(unloaded_shovel_rate)
        elif "Simulation_Loaded_Velocities" in line:
            loaded_velocity_variance = float(line.split()[1])
            
            Total_Simulation_Loaded_Velocities_Variance.append(loaded_velocity_variance)
        elif "Simulation_Unloaded_Velocities" in line:
            unloaded_velocity_variance = float(line.split()[1])
            Total_Simulation_Unloaded_Velocities_Variance.append(unloaded_velocity_variance)
        elif "Simulation_Loaded_ShovelRate" in line:
            loaded_shovel_rate_variance = float(line.split()[1])
            Total_Simulation_Loaded_ShovelRate_Variance.append(loaded_shovel_rate_variance)
        elif "Simulation_UnLoaded_ShovelRate" in line:
            unloaded_shovel_rate_variance = float(line.split()[1])
            Total_Simulation_Unloaded_ShovelRate_Variance.append(unloaded_shovel_rate_variance)
        
print(f'Total_Simulation_Time = {Total_Simulation_Time}')
print(f'Total_Simulation_Loaded_Velocities={Total_Simulation_Loaded_Velocities}')
print(f'Total_Simulation_Unloaded_Velocities={Total_Simulation_Unloaded_Velocities}')
print(f'Total_Simulation_Loaded_ShovelRate={Total_Simulation_Loaded_ShovelRate}')
print(f'Total_Simulation_UnLoaded_ShovelRate={Total_Simulation_Unloaded_ShovelRate}')
print(f'Total_Simulation_Loaded_Velocities_Variance={Total_Simulation_Loaded_Velocities_Variance}')
print(f'Total_Simulation_Unloaded_Velocities_Variance={Total_Simulation_Unloaded_Velocities_Variance}')
print(f'Total_Simulation_Loaded_ShovelRate_Variance={Total_Simulation_Loaded_ShovelRate_Variance}')
print(f'Total_Simulation_UnLoaded_ShovelRate_Variance={Total_Simulation_Unloaded_ShovelRate_Variance}')
print(len(Total_Simulation_Time))
data_sets = [Total_Simulation_Time,
Total_Simulation_Loaded_Velocities,
Total_Simulation_Unloaded_Velocities,
Total_Simulation_Loaded_ShovelRate,
Total_Simulation_Unloaded_ShovelRate]

# for data in data_sets:
    # print(f'Length of the data: {len(data)}')



plt.figure(figsize=(12,8))

# Subplot 1: Sensitivity to x
plt.subplot(2,2,1)
plt.scatter(Total_Simulation_Loaded_Velocities,Total_Simulation_Time)
plt.xlabel('Loaded Velocities m/s')
plt.ylabel('T in s')
# plt.title('Sensitivity to Loading Velocities')
plt.grid(True)

# plt.xlim(0, 50)  # Set x-axis limits
# plt.ylim(0, 250)  # Set y-axis limits

# Subplot 2: Sensitivity to y
plt.subplot(2,2,2)
plt.scatter(Total_Simulation_Unloaded_Velocities,Total_Simulation_Time , color='orange')
plt.xlabel('Unloaded Velocities m/s')
plt.ylabel('T in s')
# plt.title('Sensitivity to Unloading Velocities')
plt.grid(True)

# plt.xlim(0, 50)  # Set x-axis limits
# plt.ylim(0, 250)  # Set y-axis limits

# Subplot 3: Sensitivity to z
plt.subplot(2,2,3)
plt.scatter(Total_Simulation_Loaded_ShovelRate, Total_Simulation_Time, color='green')
plt.xlabel('Loaded_Shovel_Rate ton/s')
plt.ylabel('T in s')
# plt.title('Sensitivity to Loaded_ShovelRate')
plt.grid(True)
# plt.legend()
# plt.xlim(0, 50)  # Set x-axis limits
# plt.ylim(0, 250)  # Set y-axis limits

plt.subplot(2,2,4)
plt.scatter(Total_Simulation_Unloaded_ShovelRate, Total_Simulation_Time, color='red')
plt.xlabel('Unloaded_Shovel_Rate ton/s')
plt.ylabel('T in s')
# plt.title('Sensitivity to UnLoaded_ShovelRate')
plt.grid(True)
# plt.legend()

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show() 
plt.close() 

# Display the plots


# fig,axs = plt.subplots()
# colors = ['red','green','blue','purple','orange']
# plot_1 = ['Time','Loaded_Velocities','Unloaded_Velocities','Loaded_ShovelRate','Unloaded_ShovelRate']

# for i , data in enumerate(data_sets):
#     mu,std = statistics.mean(data),statistics.stdev(data)
#     axs.plot(data,norm.pdf(data,mu,std),color =colors[i],label=plot_1[i])
# plt.tight_layout()  # Adjust layout to prevent overlap
# plt.show()  # Display the plots

# fig, axs = plt.subplots()

# colors = ['red', 'green', 'blue', 'purple', 'orange']
# plot_labels = ['Time', 'Loaded Velocities', 'Unloaded Velocities', 'Loaded Shovel Rate', 'Unloaded Shovel Rate']

# for i, data in enumerate(data_sets):
#     mu, std = statistics.mean(data), statistics.stdev(data)
    
#     # Plot using your preferred syntax
#     axs.plot(data, norm.pdf(data, mu, std), color=colors[i], label=plot_labels[i])

# Add labels and legend
# axs.set_xlabel('Value')
# axs.set_ylabel('Probability Density')
# axs.legend()
# plt.tight_layout()  # Adjust layout to prevent overlap
# plt.title('Gaussian Probability Density Functions')
# plt.show()  # Display the plots

# X = np.array([[x1,x2,x3,x4] for x1,x2,x3,x4 in zip(Total_Simulation_Loaded_Velocities,
# Total_Simulation_Unloaded_Velocities,
# Total_Simulation_Loaded_ShovelRate,
# Total_Simulation_Unloaded_ShovelRate)])
# Y = np.array(Total_Simulation_Time)

# reg_model = LinearRegression().fit(X,Y)
# print(f'The Score value is {reg_model.score}')

# coefficients= reg_model.coef_
# intercept = reg_model.intercept_

# print(f'Time = {intercept} + {coefficients[0]} * Loaded_Velocities + {coefficients[1]} * Unloaded_Velocities + {coefficients[2]} * Loaded_ShovelRate + {coefficients[3]}  *Unloaded_ShovelRate')














 

