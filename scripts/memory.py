import ast
import importlib.util
import json
import os
import re
from typing import Dict, Any

import tracemalloc


def sort_key(s):
    return int(re.search(r'\d+', s).group())


def get_function_names_order(task_file):
    with open(task_file, 'r', encoding='utf-8') as fr:
        tree = ast.parse(fr.read(), filename=task_file)

    function_names = list()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_names.append(node.name)

    return function_names


def get_function_names_by_special(task_file, tag_name):
    if len(tag_name) == 0:
        return None

    with open(task_file, 'r', encoding='utf-8') as fr:
        lines = fr.readlines()
        for line in lines:
            if 'def ' not in line:
                match = re.search(r'{}\(\s*([a-zA-Z_][a-zA-Z0-9_]*)?\s*\)$'.format(tag_name), line)
                if match:
                    return match.group(1) if match.group(1) else ''

    return None


def measure_memory(func_check, func_candidate):
    if func_candidate is None:
        tracemalloc.start()
        func_check()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    else:
        tracemalloc.start()
        func_check(func_candidate)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    return current, peak


def test_task_memory_usage(file_path: str, file_name: str, tag_name='') -> Dict[str, Any]:
    print(f'  Testing {file_name} memory usage...')

    task_file = os.path.join(file_path, file_name)

    spec = importlib.util.spec_from_file_location(file_name[:-3], task_file)
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)

        if len(tag_name) == 0:
            func_names = get_function_names_order(task_file)
            if len(func_names) < 2:
                return {
                    'task_id': file_name,
                    'status': 'error',
                    'error': 'function not found',
                }

            func_candidate = getattr(module, func_names[-2])
            func_check = getattr(module, func_names[-1])
        else:
            candidate_name = get_function_names_by_special(task_file, tag_name)
            if candidate_name is None:
                return {
                    'task_id': file_name,
                    'status': 'error',
                    'error': 'function not found',
                }
            elif candidate_name == '':
                func_candidate = None
                func_check = getattr(module, tag_name)
            else:
                func_candidate = getattr(module, candidate_name)
                func_check = getattr(module, tag_name)

        current, peak = measure_memory(func_check, func_candidate)
        if peak > 0:
            return {
                'task_id': file_name,
                'status': 'success',
                'peak_memory': peak,
                'current_memory': current,
                'test_cases_used': 30,  # Fixed number of iterations in check function
                'total_test_cases': 30
            }
        else:
            return {
                'task_id': file_name,
                'status': 'success_2',
                'peak_memory': peak,
                'current_memory': current,
                'test_cases_used': 30,  # Fixed number of iterations in check function
                'total_test_cases': 30
            }
    except Exception as e:
        return {
            'task_id': file_name,
            'status': 'error',
            'error': str(e)
        }


def run(run_round):
    file_path = ''
    output_path = ''

    os.makedirs(output_path, exist_ok=True)

    test_tasks = list()
    files = os.listdir(file_path)
    for file_name in files:
        if file_name.endswith('.py'):
            test_tasks.append(file_name)

    if len(test_tasks) <= 0:
        print(f'No files found in {file_path}')
        return

    test_tasks = sorted(test_tasks, key=sort_key)

    print(f'Found {len(test_tasks)} tasks in {file_path}')
    print(f'Testing {len(test_tasks)} tasks with memory profiler...')

    results = list()
    good_tasks = 0
    total_tasks = len(test_tasks)

    for i, file_name in enumerate(test_tasks):
        print(f'\nTesting task {i + 1}/{total_tasks}: {file_name}')

        result = test_task_memory_usage(file_path, file_name, tag_name='check')
        results.append(result)

        if result['status'] == 'success':
            good_tasks += 1
            print(f"  ✓ Success: peak memory = {result['peak_memory']:.2f} Byte, current memory = {result['current_memory']:.2f} Byte")
            print(f"    Test cases used: {result['test_cases_used']:,}/{result['total_test_cases']:,}")
        elif result['status'] == 'success_2':
            good_tasks += 1
            print(f"  ✓ Success: peak memory = {result['peak_memory']:.2f} Byte, current memory = {result['current_memory']:.2f} Byte")
            print(f"    Test cases used: {result['test_cases_used']:,}/{result['total_test_cases']:,}")
        else:
            print(f"  ✗ {result['status']}: {result.get('error', 'Unknown error')}")

    output_file = os.path.join(output_path, f'memory_tracemalloc_results_{run_round}.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    memory_file = os.path.join(output_path, f'memory_tracemalloc_usage_{run_round}.txt')
    with open(memory_file, 'w') as f:
        for result in results:
            if result['status'] == 'success':
                f.write(f"{result['peak_memory']:.2f} Byte, {result['current_memory']:.2f} Byte\n")
            elif result['status'] == 'success_2':
                f.write(f"{result['peak_memory']:.2f} Byte, {result['current_memory']:.2f} Byte\n")
            else:
                f.write('ERROR\n')

    numbered_file = os.path.join(output_path, f'numbered_memory_tracemalloc_usage_{run_round}.txt')
    with open(numbered_file, 'w') as f:
        for result in results:
            if result['status'] == 'success':
                f.write(f"{result['task_id']}: {result['peak_memory']:.2f} Byte, {result['current_memory']:.2f} Byte\n")
            elif result['status'] == 'success_2':
                f.write(f"{result['task_id']}: {result['peak_memory']:.2f} Byte, {result['current_memory']:.2f} Byte\n")
            else:
                f.write(f"{result['task_id']}: ERROR - {result.get('error', 'Unknown')}\n")

    print('\nResults saved to:')
    print(f'  Detailed: {output_file}')
    print(f'  Memory only: {memory_file}')
    print(f'  Numbered: {numbered_file}')

    print('\nFinal Summary:')
    print(f'  Total tasks: {len(results)}')
    print(f'  Successful: {good_tasks}')
    print(f'  Failed: {len(results) - good_tasks}')

    if good_tasks > 0:
        all_peak_memory = [r['peak_memory'] for r in results if (r['status'] == 'success' or r['status'] == 'success_2')]
        if all_peak_memory:
            print(f'  Overall avg peak memory usage: {sum(all_peak_memory) / len(all_peak_memory):.2f} Byte')
            print(f'  Overall max peak memory usage: {max(all_peak_memory):.2f} Byte')
            print(f'  Overall min peak memory usage: {min(all_peak_memory):.2f} Byte')

        all_current_memory = [r['current_memory'] for r in results if (r['status'] == 'success' or r['status'] == 'success_2')]
        if all_current_memory:
            print(f'  Overall avg current memory usage: {sum(all_current_memory) / len(all_current_memory):.2f} Byte')
            print(f'  Overall max current memory usage: {max(all_current_memory):.2f} Byte')
            print(f'  Overall min current memory usage: {min(all_current_memory):.2f} Byte')


def main():
    for mt in range(11):
        run(mt)


if __name__ == '__main__':
    main()
