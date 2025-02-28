import matplotlib.pyplot as plt
import re

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

data1 = read_profile_data('./result/Memory/Answers_HumanEval_30_memory.txt')
data2 = read_profile_data('./result/Memory/HumanEval_30_memory.txt')

filenames = sorted(set(data1.keys()) & set(data2.keys()), key=extract_number)
array_memory1 = [data1[name] for name in filenames]
array_memory2 = [data2[name] for name in filenames]


plt.figure(figsize=(10, 6))
# plt.plot(times1, label='Answers')
# plt.plot(times2, label='Copilot')
plt.plot(array_memory1, label='Canonical Code')
plt.plot(array_memory2, label='Genenrated Code by Copilot')
plt.xlabel('File Index', fontsize=15)
plt.ylabel('Memory Usage (MB)', fontsize=15)
# plt.title('Comparison of Memory Usage between Answers and Copilot')
plt.legend(fontsize=15)
plt.savefig('./memory.pdf')
plt.show()