import re

def read_file(filepath):
    memory_usages = {}
    with open(filepath, 'r') as file:
        for line in file:
            mem_match = re.search(r': (\d+\.\d+) MB', line)
            index_match = re.search(r'(\d+).py', line)
            if mem_match and index_match:
                index = int(index_match.group(1))
                memory_usage = float(mem_match.group(1))
                memory_usages[index] = memory_usage
    return memory_usages

def extract_common_entries(data1, data2):
    common_keys = set(data1.keys()) & set(data2.keys())
    if not common_keys:
        print("No common entries found.")
    extracted_data1 = {k: data1[k] for k in common_keys}
    extracted_data2 = {k: data2[k] for k in common_keys}
    return extracted_data1, extracted_data2

def save_common_data_to_file(common_data, filename):
    if common_data:
        with open(filename, 'w') as file:
            for index, memory_usage in common_data.items():
                file.write(f"enc_{index}.py: {memory_usage} MB\n")
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

data1_path = './result/Memory/answers_mbpp_30_memory_all.txt'
data2_path = './result/Memory/memory_prompt2.txt'

data1 = read_file(data1_path)
data2 = read_file(data2_path)

common_data1, common_data2 = extract_common_entries(data1, data2)

save_common_data_to_file(common_data1, './answers_memory_prompt2.txt')

