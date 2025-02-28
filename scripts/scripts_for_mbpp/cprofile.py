import cProfile
import pstats
import os

def profile_function(file_path, profile_file):
    with open(file_path, "rb") as file:
        code = compile(file.read(), file_path, 'exec')
        cProfile.run(code, profile_file)

def extract_cumtime(profile_file):
    p = pstats.Stats(profile_file)
    cumtime = p.stats[list(p.stats.keys())[0]][3]
    return cumtime

def save_times_to_file(times, output_file):
    with open(output_file, 'w') as file:
        for time in times:
            file.write(f"{time}\n")

def profile_folder(folder_path, output_file):
    run_times = []
    profile_data = "profile_data"
    file_list = [filename for filename in os.listdir(folder_path) if filename.endswith('.py')]
    
    file_list.sort()
    for filename in file_list:
        if filename.endswith('.py'):
            file_path = os.path.join(folder_path, filename)
            profile_function(file_path, profile_data)
            run_times.append(extract_cumtime(profile_data))
    
    save_times_to_file(run_times, output_file)

    return run_times

def add_line_numbers(txt_file_path, output_file_path, folder_path):
    file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    valid_files = []
    for f in file_names:
        parts = f.split('_') 
        if len(parts) > 1 and parts[1].split('.')[0].isdigit(): 
            valid_files.append(int(parts[1].split('.')[0])) 

    sorted_numbers = sorted(valid_files)
    
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if len(sorted_numbers) != len(lines):
        raise ValueError("The number of files does not match the number of lines")

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for line_number, line in zip(sorted_numbers, lines):
            file.write(f"{line_number}: {line}")

def main():
    folder_path = './output/MBPP-prompt/pass/MBPP-prompt2_30_cprofile'
    temp_output_file = './cprofile_temp.txt'
    final_output_file = './result/Execution-Time/numbered_cprofile_prompt2.txt'
    
    times = profile_folder(folder_path, temp_output_file)
    add_line_numbers(temp_output_file, final_output_file, folder_path)
    print("Run times have been saved to file.")

if __name__ == "__main__":
    main()