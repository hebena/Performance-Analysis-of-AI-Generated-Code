import cProfile
import json
import os
import pstats
import re
from typing import Dict, Any
import builtins



def sort_key(s):
    return int(re.search(r'\d+', s).group())


def profile_function_with_cprofile(file_path: str, file_name: str, tag_name: str) -> float:
    cumtime = 0.0
    temp_file = file_path + 'temp.txt'

    try:
        task_file = file_path + file_name
        with open(task_file, 'rb') as fr:
            code = compile(fr.read(), task_file, 'exec')
            prof = cProfile.Profile()
            g = {'__builtins__': builtins, '__name__': '__main__'}
            prof.enable()
            exec(code, g, g)
            prof.disable()
            prof.dump_stats(temp_file)

        p = pstats.Stats(temp_file)
        if p.stats:
            for func_key, stats in p.stats.items():
                if isinstance(func_key, tuple) and len(func_key) >= 3:
                    _, _, func_name = func_key
                    if func_name == tag_name:
                        cumtime = stats[3]
        else:
            raise Exception('Error Stats')
    except Exception as e:
        raise Exception(str(e))
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return cumtime


def test_task_execution_time(file_path: str, file_name: str) -> Dict[str, Any]:
    task_file = file_path + file_name
    if not os.path.exists(task_file):
        return {
            'task_id': file_name,
            'status': 'error',
            'error': f'Task file not found: {task_file}'
        }

    print(f'  Testing {task_file} with cProfile...')

    try:
        cumtime = profile_function_with_cprofile(file_path, file_name, tag_name='check')
        return {
            'task_id': file_name,
            'status': 'success',
            'cumtime_seconds': cumtime,
            'test_cases_used': 30,  # check function loops 30 times internally
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
    print(f'Testing all {len(test_tasks)} tasks with cProfile...')

    results = list()
    good_tasks = 0
    total_tasks = len(test_tasks)

    for i, file_name in enumerate(test_tasks):
        print(f'\nTesting task {i + 1}/{total_tasks}: {file_name}')

        result = test_task_execution_time(file_path, file_name)
        results.append(result)

        if result['status'] == 'success':
            good_tasks += 1
            print(f"  ✓ Success: cumtime = {result['cumtime_seconds']:.6f}s")
            print(f"    Test cases used: {result['test_cases_used']}/{result['total_test_cases']}")
        else:
            print(f"  ✗ {result['status']}: {result.get('error', 'Unknown error')}")

    output_file = os.path.join(output_path, f'execution_times_results_cprofile_{run_round}.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    times_file = os.path.join(output_path, f'execution_times_cprofile_{run_round}.txt')
    with open(times_file, 'w') as f:
        for result in results:
            if result['status'] == 'success':
                f.write(f"{result['cumtime_seconds']:.6f}\n")
            else:
                f.write('ERROR\n')

    numbered_file = os.path.join(output_path, f'numbered_execution_times_cprofile_{run_round}.txt')
    with open(numbered_file, 'w') as f:
        for result in results:
            if result['status'] == 'success':
                f.write(f"{result['task_id']}: {result['cumtime_seconds']:.6f}s\n")
            else:
                f.write(f"{result['task_id']}: ERROR - {result.get('error', 'Unknown')}\n")

    print('\nResults saved to:')
    print(f'  Detailed: {output_file}')
    print(f'  Times only: {times_file}')
    print(f'  Numbered: {numbered_file}')

    print('\nFinal Summary:')
    print(f'  Total tasks: {len(results)}')
    print(f'  Successful: {good_tasks}')
    print(f'  Failed: {len(results) - good_tasks}')

    if good_tasks > 0:
        all_times = [r['cumtime_seconds'] for r in results if r['status'] == 'success']
        if all_times:
            print(f'  Overall avg execution time: {builtins.sum(all_times) / len(all_times):.6f}s')
            print(f'  Overall max execution time: {builtins.max(all_times):.6f}s')
            print(f'  Overall min execution time: {builtins.min(all_times):.6f}s')


def main():
    for mt in range(11):
        run(mt)


if __name__ == '__main__':
    main()
