import numpy as np

# Given data
T = np.array([24.1, 23.9, 25.2, 24.3])
Loaded_Velocity = np.array([4.13, 4.04, 3.92, 4.01])
Unloaded_Velocity = np.array([6.2, 6.68, 5.99, 6.67])
Loaded_ShovelRate = np.array([0.5028, 0.5046, 0.4901, 0.5076])
UnLoaded_ShovelRate = np.array([0.2508, 0.2566, 0.2348, 0.2457])

# Compute the local gradients (partial derivatives) using the given formula
dT_dLV = -28.28 / (Loaded_Velocity ** 2)
dT_dUV = -24.15 / (Unloaded_Velocity ** 2)
dT_dLS = -1.68 / (Loaded_ShovelRate ** 2)
dT_dUS = -2.28 / (UnLoaded_ShovelRate ** 2)

# Compute sensitivity indices S_X = (dT/dX) * (X/T) and convert to percentage
S_LV = (dT_dLV * Loaded_Velocity) / T * 100
S_UV = (dT_dUV * Unloaded_Velocity) / T * 100
S_LS = (dT_dLS * Loaded_ShovelRate) / T * 100
S_US = (dT_dUS * UnLoaded_ShovelRate) / T * 100

# Display results in gradient-wise structure
print("===================================")
print(" Local Sensitivity Analysis ")
print("===================================\n")

print("Inputs:")
# print(f"T: {T}")
print(f"Loaded Velocity: {Loaded_Velocity}")
print(f"Unloaded Velocity: {Unloaded_Velocity}")
print(f"Loaded Shovel Rate: {Loaded_ShovelRate}")
print(f"Unloaded Shovel Rate: {UnLoaded_ShovelRate}\n")

print("Gradients:")
print(f"∂T/∂(Loaded Velocity): {dT_dLV}")
print(f"∂T/∂(Unloaded Velocity): {dT_dUV}")
print(f"∂T/∂(Loaded Shovel Rate): {dT_dLS}")
print(f"∂T/∂(Unloaded Shovel Rate): {dT_dUS}\n")

print("Sensitivity Indices (in Percentage):")
print(f"Loaded Velocity: {S_LV}")
print(f"Unloaded Velocity: {S_UV}")
print(f"Loaded Shovel Rate: {S_LS}")
print(f"Unloaded Shovel Rate: {S_US}")
print("===================================")
