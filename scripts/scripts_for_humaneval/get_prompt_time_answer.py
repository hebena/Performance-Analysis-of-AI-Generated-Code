import os

folder_path = './output/Humaneval-prompt/pass/HumanEval-prompt1'

txt_file_path = './result/Execution-Time/numbered_answers_humaneval_30_cprofile_all.txt'

output_file_path = './result/Execution-Time/numbered_answers_cprofile_prompt1.txt'

file_names = set(f.split('.')[0] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))

with open(txt_file_path, 'r', encoding='utf-8') as file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in file:
        index, other_column = line.strip().split(':')  
        if index in file_names:
            output_file.write(line)
