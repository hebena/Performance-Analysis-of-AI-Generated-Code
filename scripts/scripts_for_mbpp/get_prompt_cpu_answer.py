import re

def read_file(filepath):
    data_usages = {}
    with open(filepath, 'r') as file:
        for line in file:
            mem_match = re.search(r'Max Memory = (\d+\.\d+) MB', line)
            cpu_match = re.search(r'CPU Usages = \[(\d+\.\d+)\]', line)
            index_match = re.search(r'enc_(\d+)', line)
            if mem_match and cpu_match and index_match:
                index = int(index_match.group(1))
                memory_usage = float(mem_match.group(1))
                cpu_usage = float(cpu_match.group(1))
                data_usages[index] = {'memory': memory_usage, 'cpu': cpu_usage}
    return data_usages

def extract_common_entries(data1, data2):
    common_keys = set(data1.keys()) & set(data2.keys())
    print(f"Common keys: {common_keys}")  
    extracted_data1 = {k: data1[k] for k in common_keys}
    extracted_data2 = {k: data2[k] for k in common_keys}
    return extracted_data1, extracted_data2

def save_common_data_to_file(common_data1, common_data2, filename):
    with open(filename, 'w') as file:
        for index in common_data1:
            memory_usage = common_data1[index]['memory']
            cpu_usage = common_data1[index]['cpu']
            file.write(f"enc_{index}.py: Max Memory = {memory_usage} MB, CPU Usages = [{cpu_usage}]\n")
    print(f"Data saved to {filename}")

data1_path = './result/copilot/results_for_humaneval/CPU/Answers_Humaneval_30_cpu_usages_all.txt'
data2_path = './result/deepseek-coder/results_for_humaneval/CPU/humaneval_cpu_before_fewshot_prompt.txt'

data1 = read_file(data1_path)
data2 = read_file(data2_path)

common_data1, common_data2 = extract_common_entries(data1, data2)

save_common_data_to_file(common_data1, common_data2, './result/deepseek-coder/results_for_humaneval/CPU/after.txt')