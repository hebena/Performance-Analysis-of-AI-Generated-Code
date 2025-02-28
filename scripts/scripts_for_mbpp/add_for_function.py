import os
import re

def add_loop_to_first_assert(script_path):
    with open(script_path, 'r') as file:
        script_content = file.read()

    assert_regex = re.compile(r'assert\s.*', re.MULTILINE)
    match = assert_regex.search(script_content)

    if match:
        first_assert_pos = match.start()
        first_assert = match.group()

        modified_content = script_content[:first_assert_pos] + f'for _ in range(30):\n' + script_content[first_assert_pos:]

        assert_statements = assert_regex.findall(modified_content)
        for assert_statement in assert_statements:
            modified_content = modified_content.replace(assert_statement, f'    {assert_statement}', 1)

        with open(script_path, 'w') as file:
            file.write(modified_content)

def main():
    folder_path = './output/MBPP-prompt/pass/MBPP-prompt2_30'

    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            script_path = os.path.join(folder_path, filename)
            print(f"Processing script: {script_path}")

            add_loop_to_first_assert(script_path)

if __name__ == "__main__":
    main()
