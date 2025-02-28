import os
import subprocess
from memory_profiler import memory_usage

def run_python_script(filepath):
    command = ["python3", filepath]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def monitor_memory_usage(process, interval=0.1):
    mem_usage = memory_usage(proc=process.pid, interval=interval, timeout=None)
    return max(mem_usage) 

def process_directory(directory):
    max_memory_usages = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            filepath = os.path.join(directory, filename)
            process = run_python_script(filepath)
            max_usage = monitor_memory_usage(process)
            max_memory_usages[filename] = max_usage
            print(f"Processed {filename}: Max memory usage = {max_usage} MB")
    return max_memory_usages

def save_results(results, output_filepath):
    with open(output_filepath, 'w') as file:
        for filename, max_usage in results.items():
            file.write(f"{filename}: {max_usage} MB\n")

directory = './output/Humaneval-prompt/pass/HumanEval-prompt2-30_cprofile' 
results = process_directory(directory)
output_filepath = './result/Memory/memory_prompt2.txt'  
save_results(results, output_filepath)
