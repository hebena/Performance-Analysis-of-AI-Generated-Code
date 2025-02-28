import os

folder_path = "./output/Humaneval-prompt/pass/HumanEval-prompt2-30_cprofile"

file_list = os.listdir(folder_path)

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)


    with open(file_path, 'r') as file:
        code = file.read()

    modified_code = "from memory_profiler import profile\n@profile\n" + code

    with open(file_path, 'w') as file:
        file.write(modified_code)

    print(f'Processed file: {file_name}')
