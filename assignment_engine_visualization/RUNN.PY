import traceback
import importlib
import main
import gc


class MainRunner:
    def __init__(self):
        self.total_time_des = []
        self.total_velocities_des = []

    def run_main_multiple_times(self, num_runs):
        for _ in range(num_runs):
            try:
                importlib.reload(main)
                result = main.main()
                if isinstance(result,(list,tuple)) and len(result)>=2:
                    self.total_time_des.append(result[0])
                    self.total_velocities_des.append(result[1])
                else:
                    print(f"Unexpected result format or size: {result}")
               
            except Exception as e:
                
                print(f"An error occurred running RUNN Class: {e}")
                traceback.print_exc()
                # Optionally, you can decide to continue or stop on error

            gc.collect()

    def get_results(self):
        return self.total_time_des,self.total_velocities_des

# Example usage
if __name__ == '__main__':
    runner = MainRunner()
    runner.run_main_multiple_times(2)
    results = runner.get_results()
    print(results[0])
    print(results[1])
