import os
import subprocess
import difflib
import sys

TESTS_DIR = 'tests'

class TestResult:
    Ok = 'OK'
    OutputMismatch = 'output mismatch'
    ExitStatusMismatch = 'exit status mismatch'
    NotFound = 'not found'

def run_test(program, test_name):
    input_file = os.path.join(TESTS_DIR, f'{program}.{test_name}.in')
    output_file = os.path.join(TESTS_DIR, f'{program}.{test_name}.out')

    # Run the program with input from file
    process = subprocess.Popen(['python', f'{program}.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with open(input_file, 'r') as file:
        input_data = file.read()

    try:
        output_data, _ = process.communicate(input=input_data, timeout=5)
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        return TestResult.NotFound

    # Check if the expected output file exists
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            expected_output = file.read()

        # Compare the output with expected output
        if output_data == expected_output:
            return TestResult.Ok
        else:
            print(f'FAIL: {program} {test_name} failed ({TestResult.OutputMismatch})')
            print(f'      expected:\n{expected_output}\n\n           got:\n{output_data}\n')
            return TestResult.OutputMismatch
    else:
        # Check exit status
        if process.returncode == 0:
            return TestResult.Ok
        else:
            print(f'FAIL: {program} {test_name} failed ({TestResult.ExitStatusMismatch})')
            return TestResult.ExitStatusMismatch

def run_tests(program):
    print(f'Testing {program}...')
    test_results = {'Ok': 0, 'OutputMismatch': 0, 'ExitStatusMismatch': 0, 'NotFound': 0}

    for test_name in os.listdir(TESTS_DIR):
        if test_name.startswith(f'{program}.') and test_name.endswith('.in'):
            result = run_test(program, test_name[len(program)+1:-3])
            test_results[result] += 1

    print(f'OK: {test_results["Ok"]}')
    print(f'output mismatch: {test_results["OutputMismatch"]}')
    print(f'exit status mismatch: {test_results["ExitStatusMismatch"]}')
    print(f'not found: {test_results["NotFound"]}')
    print(f'total: {sum(test_results.values())}')

    if test_results['OutputMismatch'] > 0 or test_results['ExitStatusMismatch'] > 0 or test_results['NotFound'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test.py <program>")
        sys.exit(1)

    program = sys.argv[1]
    run_tests(program)
