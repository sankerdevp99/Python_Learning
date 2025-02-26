import os
import subprocess
import ast

class MainRunner:
    def __init__(self):
        self.total_time_des = []
        self.total_velocities_des = []

    def run_main_multiple_times(self, num_runs):
        for _ in range(num_runs):
            if not os.path.isfile('result.txt'):
                    raise FileNotFoundError("result.txt not found")
            try:
                # Run the main.py script
                subprocess.run(['python', 'main.py'], check=True)
                from main import main
                
               
                time_des, velocities_des = main() 
                
                
                self.total_time_des.extend(time_des)
                self.total_velocities_des.extend(velocities_des)

            except Exception as e:
                print(f"An error occurred: {e}")

    def get_results(self):
        return self.total_time_des, self.total_velocities_des

# Example usage
if __name__ == '__main__':
    runner = MainRunner()
    runner.run_main_multiple_times(5)
    results = runner.get_results()
    print("Total Times Desired:", results[0])
    print("Total Velocities Desired:", results[1])
