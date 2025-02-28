import matplotlib.pyplot as plt
import re

def count_differences(array1, array2):
    indices = []
    for i, (x, y) in enumerate(zip(array1, array2)):
        if (y - x) / x > 0.2:
        # if abs(x - y) / max(x, y) > 0.2:
            indices.append(i)
    return indices, len(indices)

def read_data(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            index, value = line.strip().split(':')
            data[int(index)] = float(value)
    return data

time_data1 = read_data('./result/copilot/results_for_humaneval/Execution-Time/numbered_answers_humaneval_30_cprofile_all.txt')
time_data2 = read_data('./result/deepseek-coder/results_for_humaneval/Execution-Time/numbered_humaneval_cprofile_before_fewshot_prompt.txt')

common_indices = set(time_data1.keys()) & set(time_data2.keys())
array_time1 = [time_data1[i] for i in sorted(common_indices)]
array_time2 = [time_data2[i] for i in sorted(common_indices)]

def read_profile_data(filepath):
    data = {}
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.split(':')
            if len(parts) == 2:
                filename = parts[0].strip()
                time = float(parts[1].replace('MB', '').strip())
                data[filename] = time
    return data

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

data1 = read_profile_data('./result/copilot/results_for_humaneval/Memory/Answers_HumanEval_30_memory_all.txt')
data2 = read_profile_data('./result/deepseek-coder/results_for_humaneval/Memory/humaneval_memory_before_fewshot_prompt.txt')

filenames = sorted(set(data1.keys()) & set(data2.keys()), key=extract_number)
array_memory1 = [data1[name] for name in filenames]
array_memory2 = [data2[name] for name in filenames]

def parse_data(filename):
    cpu_usages = {}
    with open(filename, 'r') as file:
        for line in file:
            cpu_match = re.search(r'CPU Usages = \[(\d+\.\d+)\]', line)
            index_match = re.search(r'enc_(\d+)', line)
            if cpu_match and index_match:
                index = int(index_match.group(1))
                cpu_usage = float(cpu_match.group(1))
                cpu_usages[index] = cpu_usage
    sorted_cpu_usages = [cpu_usages[i] for i in sorted(cpu_usages.keys())]
    return sorted_cpu_usages

array_cpu1 = parse_data('./result/copilot/results_for_humaneval/CPU/Answers_Humaneval_30_cpu_usages_all.txt')
array_cpu2 = parse_data('./result/deepseek-coder/results_for_humaneval/CPU/humaneval_cpu_before_fewshot_prompt.txt')

result1 = count_differences(array_time1, array_time2)
print("Number of scripts with more than 20% difference in runtime:", result1)
result2 = count_differences(array_memory1, array_memory2)
print("Number of scripts with more than 20% difference in Memory Usage:", result2)
result3 = count_differences(array_cpu1, array_cpu2)
print("Number of scripts with more than 20% difference in CPU Utilization:", result3)

union = set(result1[0]) | set(result2[0]) | set(result3[0])
print("the union of three sets:", union, len(union))