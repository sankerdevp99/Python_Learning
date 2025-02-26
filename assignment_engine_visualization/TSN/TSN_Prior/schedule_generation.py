

num_time_steps = None
end_rows = None

row_results = None

column_results = None

schedules = []

explored = []

search_elements= []

process_times = None
def find_schedule(search_element, schedule, row_search):
    while True:
        row_number = search_element // num_time_steps
        if row_number in end_rows:
            break
        if row_search:
            time = process_times[row_number]
            if time is None:
                trucks_already_waiting = row_results.get((search_element - 1, search_element), 0)
                while True:
                    possible_var_key = next((var_key for var_key, variable in column_results.items() if var_key[0] == search_element and var_key not in explored), None)
                    if possible_var_key:
                        if trucks_already_waiting:
                            schedule.append(row_results[(search_element, search_element + 1)].name()[16:])
                            # schedule.append(row_results[(search_element, search_element + 1)].name())
                            trucks_already_waiting -= 1
                            search_element += 1
                        else:
                            schedule.append(column_results[possible_var_key].name()[16:])
                            # schedule.append(column_results[possible_var_key].name())
                            explored.append(possible_var_key)
                            search_element = possible_var_key[1]
                            break
                    else:
                        schedule.append(row_results[(search_element, search_element + 1)].name()[16:])
                        # schedule.append(row_results[(search_element, search_element + 1)].name())
                        search_element += 1
            else:
                for _ in range(time):
                    schedule.append(row_results[(search_element, search_element + 1)].name()[16:])
                    # schedule.append(row_results[(search_element, search_element + 1)].name())
                    search_element += 1
                row_search = False
        else:
            for var_key, variable in column_results.items():
                if var_key[0] == search_element and var_key not in explored:
                    if variable.solution_value() >= 1:
                        schedule.append(variable.name()[16:])
                        # schedule.append(variable.name())
                        explored.append(var_key)
                        search_element = var_key[1]
                        break
                    elif variable.solution_value() > 1:
                        schedule.append(variable.name()[16:])
                        # schedule.append(variable.name())
                        search_element = var_key[1]
                        column_results[var_key] -= 1
                        break
            row_search = True

def main():
    for var_key, variable in column_results.items():
        if var_key[0] in range(num_time_steps):
            if variable.solution_value() >= 1:
                schedules.extend([[variable.name()[16:]] for _ in range(int(variable.solution_value()))])
                # schedules.extend([[variable.name()] for _ in range(int(variable.solution_value()))])
                search_elements.extend([var_key[1] for _ in range(int(variable.solution_value()))])
                explored.append(var_key)

    count = 1

    with open("output.txt", "w") as file:
        for i, schedule in enumerate(schedules):
            find_schedule(search_elements[i], schedule, row_search=True)
            print("--------------------------------------------------------")
            print(f"schedule_{count}: ", schedule)
            file.write(f"schedule_{count}: {schedule}\n")
            count += 1
