import ast
import cProfile
import importlib.util
import json
import os
import re
import time
from typing import Dict, Any

import psutil


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


def test_task_cpu_usage(file_path: str, file_name: str, tag_name='', runs=1) -> Dict[str, Any]:
    print(f'  Testing {file_name} cpu usage...')

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

        if func_candidate is None:
            # 先运行一次，预热
            func_check()

            profiler = cProfile.Profile()
            profiler.enable()

            start_time = time.time()
            for _ in range(runs):
                func_check()
            end_time = time.time()

            profiler.disable()

            cpu_runtime = sum(stat.totaltime for stat in profiler.getstats()) / runs
            total_runtime = (end_time - start_time) / runs

            cpu_usage = (cpu_runtime / total_runtime) * 100
            kernel_usage = cpu_usage / len(psutil.Process().cpu_affinity())
        else:
            # 先运行一次，预热
            func_check(func_candidate)

            profiler = cProfile.Profile()
            profiler.enable()

            start_time = time.time()
            for _ in range(runs):
                func_check(func_candidate)
            end_time = time.time()

            profiler.disable()

            cpu_runtime = sum(stat.totaltime for stat in profiler.getstats()) / runs
            total_runtime = (end_time - start_time) / runs

            cpu_usage = (cpu_runtime / total_runtime) * 100
            kernel_usage = cpu_usage / len(psutil.Process().cpu_affinity())

        return {
            'task_id': file_name,
            'status': 'success',
            'cpu_usage': cpu_usage,
            'kernel_usage': kernel_usage,
            'cpu_runtime': cpu_runtime,
            'total_runtime': total_runtime,
        }
    except Exception as e:
        return {
            'task_id': file_name,
            'status': 'error',
            'error': str(e)
        }


def run(run_round):
    runs_config = {
        # 'HumanEval_0.py': 10,
        # 'example.py': 10,
    }


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
    print(f'Testing all {len(test_tasks)} tasks...')

    results = []
    good_tasks = 0
    total_tasks = len(test_tasks)

    for i, file_name in enumerate(test_tasks):
        runs = runs_config.get(file_name, 1)
        print(f'\nTesting task {i + 1}/{total_tasks}: {file_name}, run times: {runs}')

        result = test_task_cpu_usage(file_path, file_name, tag_name='check', runs=runs)
        results.append(result)

        if result['status'] == 'success':
            good_tasks += 1
            print(f'  ✓ Success:')
            print(f"    Kernel usage: {result['kernel_usage']:.2f}%")
            print(f"    CPU usage: {result['cpu_usage']:.2f}%")
            print(f"    CPU Runtime: {result['cpu_runtime']:.2f}s")
            print(f"    Total Runtime: {result['total_runtime']:.2f}s")
        else:
            print(f"  ✗ {result['status']}: {result.get('error', 'Unknown error')}")

    output_file = os.path.join(output_path, f'cpu_profile_results_{run_round}.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    cpu_file = os.path.join(output_path, f'cpu_profile_usage_{run_round}.txt')
    with open(cpu_file, 'w', encoding='utf-8') as f:
        for result in results:
            if result['status'] == 'success':
                f.write(f"{result['task_id']}: CPU Usage = {result['cpu_usage']}, Kernel Usage = {result['kernel_usage']}\n")
            else:
                f.write(f"{result['task_id']}: ERROR - {result.get('error', 'Unknown')}\n")

    cpu_summary_file = os.path.join(output_path, f'cpu_profile_summary_{run_round}.txt')
    with open(cpu_summary_file, 'w') as f:
        for result in results:
            if result['status'] == 'success':
                f.write(f"{result['task_id']}: Kernel usage: {result['kernel_usage']:.2f}%, CPU usage: {result['cpu_usage']:.2f}%, CPU Runtime: {result['cpu_runtime']:.2f}s, Total Runtime: {result['total_runtime']:.2f}s\n")
            else:
                f.write(f"{result['task_id']}: ERROR\n")

    print(f'\nResults saved to:')
    print(f'  Detailed: {output_file}')
    print(f'  CPU usage: {cpu_file}')
    print(f'  CPU summary: {cpu_summary_file}')

    print(f'\nFinal Summary:')
    print(f'  Total tasks: {len(results)}')
    print(f'  Successful: {good_tasks}')
    print(f'  Failed: {len(results) - good_tasks}')

    if good_tasks > 0:
        all_cpu_usage = list()
        all_kernel_usage = list()
        all_cpu_runtime = list()
        all_total_runtime = list()
        for r in results:
            if r['status'] == 'success':
                all_kernel_usage.append(r['kernel_usage'])
                all_cpu_usage.append(r['cpu_usage'])
                all_cpu_runtime.append(r['cpu_runtime'])
                all_total_runtime.append(r['total_runtime'])

        if all_cpu_usage:
            print(f'  Avg Kernel usage: {sum(all_kernel_usage) / len(all_kernel_usage):.2f}%,  Overall Kernel usage: {sum(all_kernel_usage):.2f}%')
            print(f'  Avg CPU usage: {sum(all_cpu_usage) / len(all_cpu_usage):.2f}%, Overall CPU usage: {sum(all_cpu_usage):.2f}%')
            print(f'  Avg CPU Runtime: {sum(all_cpu_runtime) / len(all_cpu_runtime):.2f}s, Overall CPU Runtime: {sum(all_cpu_runtime):.2f}s')
            print(f'  Avg Total Runtime: {sum(all_total_runtime) / len(all_total_runtime):.2f}s, Overall Total Runtime: {sum(all_total_runtime):.2f}s')


def main():
    for mt in range(11):
        run(mt)


if __name__ == '__main__':
    main()