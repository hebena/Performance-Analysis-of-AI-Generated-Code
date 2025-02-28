import os

def encapsulate_python_script(source_filepath, target_filepath):
    with open(source_filepath, 'r') as file:
        code = file.read()
        indented_code = '\n    '.join(code.splitlines())
        encapsulated_code = f"def encapsulated_function():\n    {indented_code}\n"
    
    with open(target_filepath, 'w') as file:
        file.write(encapsulated_code)

def process_directory(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory) 

    for filename in os.listdir(source_directory):
        if filename.endswith('.py'):
            source_filepath = os.path.join(source_directory, filename)
            target_filepath = os.path.join(target_directory, 'enc_' + filename)
            try:
                print(f"Processing {filename}...")
                encapsulate_python_script(source_filepath, target_filepath)
                print(f"Saved encapsulated {filename} to {target_filepath}.")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

source_directory = './output/Humaneval-prompt/pass/HumanEval-prompt2-filter-30' 
target_directory = './output/Humaneval-prompt/pass/HumanEval-prompt2-filter-30_cprofile'  
process_directory(source_directory, target_directory)
