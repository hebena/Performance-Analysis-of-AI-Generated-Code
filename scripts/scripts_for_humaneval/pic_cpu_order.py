import re
import matplotlib.pyplot as plt

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

array_cpu1 = parse_data('./result/CPU/Answers_Humaneval_30_cpu_usages.txt')
array_cpu2 = parse_data('./result/CPU/Humaneval_30_cpu_usages.txt')


plt.figure(figsize=(10, 6))
# plt.plot(file1_cpu_usages, label='Answers')
# plt.plot(file2_cpu_usages, label='Copilot')
plt.plot(array_cpu1, label='Canonical Code')
plt.plot(array_cpu2, label='Generated Code by Copilot')
plt.xlabel('File Index', fontsize=15)
plt.ylabel('CPU Usage(%)', fontsize=15)
# plt.title('Comparison of CPU Usage between Answers and Copilot')
plt.legend(fontsize=15)
plt.savefig('./cpu_usages.pdf')
plt.show()
