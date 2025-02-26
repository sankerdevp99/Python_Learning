import subprocess

def process_output(output):
    total_simulation_time = []
    total_velocities_time = []

    for line in output.splitlines():
        if line.startswith("Simulation_Time"):
            total_simulation_time.append(line)
        elif line.startswith("Simulation_Velocities"):
            total_velocities_time.append(line)
    return total_simulation_time,total_velocities_time

def main():
    result = subprocess.run(['python','main.py'],capture_output=True,text=True)
    if result.returncode == 0:
        output = result.stdout.strip()
        print(output)
        total_simulation_time,total_velocities_time=process_output(output)
        print("Simulation Time",total_simulation_time)
        print("Simulation Velocities",total_velocities_time)
    else:
        print(f'Error running sript:{result.stderr}')
if __name__ == "__main___":
    main()


