import matplotlib.pyplot as plt

def read_data(file_path):
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            index, value = line.strip().split(':')
            data[int(index)] = float(value)
    return data

time_data1 = read_data('./result/Execution-Time/numbered_answers_humaneval_30_cprofile-no1.txt')
time_data2 = read_data('./result/Execution-Time/numbered_humaneval_30_cprofile-no1.txt')

common_indices = set(time_data1.keys()) & set(time_data2.keys())
array_time1 = [time_data1[i] for i in sorted(common_indices)]
array_time2 = [time_data2[i] for i in sorted(common_indices)]

def plot_and_save_times(times1, times2,output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(times1, label='Canonical Code')
    plt.plot(times2, label='Generated Code by Copilot')
    plt.legend(fontsize=15)
    # plt.plot(times1, label='Answers')
    # plt.plot(times2, label='Copilot')
    plt.xlabel('File Index', fontsize=15)
    plt.ylabel('Cumulative Time (Seconds)', fontsize=15)
    # plt.title('Comparison of runtime performance between Answers and Copilot')
    plt.savefig(output_file)
    plt.show()
 
output_file = './cprofile.pdf'

plot_and_save_times(array_time1, array_time2, output_file)
print(f"Graph saved as {output_file}")