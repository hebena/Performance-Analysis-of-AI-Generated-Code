import os
import subprocess
import psutil
from memory_profiler import memory_usage

def run_python_script(filepath):
    command = ["python3", filepath]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def monitor_memory_usage(process, interval=0.01):
    mem_usage = memory_usage(proc=process.pid, interval=interval, timeout=None)
    max_mem = max(mem_usage)
    return max_mem


def monitor_cpu_usage(process, interval=0.1):
    ps_process = psutil.Process(process.pid)
    cpu_usages = []
    try:
        while True:
            cpu_usage = ps_process.cpu_percent(interval=interval)
            if cpu_usage == 0: 
                break
            cpu_usages.append(cpu_usage)
    except psutil.NoSuchProcess:
        pass
    return cpu_usages

def process_directory(directory):
    results = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            filepath = os.path.join(directory, filename)
            print(f"Processing file: {filename}")
            process = run_python_script(filepath)
            max_memory_usage = monitor_memory_usage(process)
            cpu_usages = monitor_cpu_usage(process)
            results[filename] = (max_memory_usage, cpu_usages)
            print(f"Processed {filename}: Max memory usage = {max_memory_usage} MB, CPU Usages = {cpu_usages}")
    return results

def save_results(results, output_filepath):
    with open(output_filepath, 'w',encoding='utf-8') as file:
        for filename, (max_memory, cpu_usages) in results.items():
            cpu_usage_str = ", ".join(map(str, cpu_usages))
            file.write(f"{filename}: Max Memory = {max_memory} MB, CPU Usages = [{cpu_usage_str}]\n")



directory = './output/Humaneval-prompt/pass/HumanEval-prompt2-30_cprofile' 
output_filepath = './result/CPU/cpu_prompt2.txt'  
cpu_usages_results = process_directory(directory)
save_results(cpu_usages_results, output_filepath)