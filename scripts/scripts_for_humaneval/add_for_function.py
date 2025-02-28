import os
import ast

folder_path = "./output/Humaneval-prompt/pass/HumanEval-prompt2-30"

file_list = os.listdir(folder_path)

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "r") as file:
        code = file.read()
    
    parsed_code = ast.parse(code)

    for node in parsed_code.body:
        if isinstance(node, ast.FunctionDef) and node.name == 'check':
            loop = ast.For(
                target=ast.Name(id='item', ctx=ast.Store()),
                iter=ast.Call(
                    func=ast.Name(id='range', ctx=ast.Load()),
                    args=[ast.Constant(n=30)],
                    keywords=[]
                ),
                body=node.body,
                orelse=[]
            )
            node.body = [loop]

        modified_code = ast.fix_missing_locations(parsed_code)

        modified_code_str = ast.unparse(modified_code)

        with open(file_path, 'w') as file:
            file.write(modified_code_str)

        print(f'Processed file: {file_name}')
