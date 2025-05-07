import subprocess
import os
import time
import sys
from pathlib import Path

STUDENT_BIN = "./build/app"
REF_BIN = "./build/app"
INPUT_FILE = "data/sort_1_08.in"
# INPUT_FILE = "data/my_sort_01.in"

def run_compile():
    subprocess.run(['mkdir', 'build'])
    subprocess.run(['cmake', '..'], cwd='build')
    process = subprocess.run(['cmake', '--build', '.'], cwd='build')
    if(process.returncode != 0):
        raise RuntimeError("Building error")

def run_program(binary_path, input_file):
    time_output = {}
    with open(input_file, "r") as f:
        start = time.perf_counter()
        proc = subprocess.run([binary_path], stdin=f, capture_output=True)
        end = time.perf_counter()

    time_output["real"] = int((end - start) * 1000)  # ms
    time_output["return"] = proc.returncode
    time_output["stdout"] = proc.stdout.decode()
    time_output["stderr"] = proc.stderr.decode()
    return time_output

def run_valgrind(binary_path, input_file):
    valgrind_log = "valgrind_log.txt"
    with open(input_file, "r") as input_f:
        subprocess.run([
            "valgrind", 
            "--tool=massif",
            "--stacks=yes",
            "--massif-out-file=massif.out",
            # "--leak-check=full",
            # "--show-leak-kinds=all",
            # f"--log-file={valgrind_log}",
            # "-s",
            binary_path
        ], stdin=input_f, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open(valgrind_log) as f:
        valgrind_output = f.read()
    
    return parse_valgrind(valgrind_output)

def parse_valgrind(log_text):
    import re
    heap_usage = re.search(r"total heap usage:\s+(\d+) allocs, (\d+) frees, ([\d,]+) bytes allocated", log_text)
    error_summary = re.search(r"ERROR SUMMARY:\s+(\d+) errors", log_text)

    return {
        "allocs": heap_usage.group(1) if heap_usage else "?",
        "frees": heap_usage.group(2) if heap_usage else "?",
        "heap_bytes": heap_usage.group(3).replace(",", "") if heap_usage else "?",
        "errors": error_summary.group(1) if error_summary else "?",
        "leaks": "No leaks" if "no leaks are possible" in log_text else "Leaks possible"
    }

def parse_massif_output(file_path="massif.out"):
    heap = None
    stack = None

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("mem_heap_B="):
                heap = int(line.strip().split('=')[1])
            elif line.startswith("mem_stacks_B="):
                stack = int(line.strip().split('=')[1])

    if stack is not None:
        print(f"Stack memory usage: {stack} b")
    if heap is not None:
        print(f"Heap memory usage: {heap} b")

def print_report(test_number, student, valgrind):
    print(f"Test {test_number} " + "="*43)
    print(f"{'Student:':<20} {'Student + Valgrind:'}")
    print(f"Return value: {student['return']:<10} Return value: {student['return']}")
    print(f"Real time: {student['real']} ms     Real time: {valgrind.get('real', '?')} ms")
    # print(f"Stdout:       {student['stdout'].strip()}")
    print(f"Stderr:       {student['stderr'].strip()}")
    parse_massif_output()
    print(f"Errors:             {valgrind['errors']}")
    print("="*50)

if __name__ == "__main__":

    run_compile()

    tests = [
        "my_sort_01.in",
        # "my_sort_02.in",
        # "my_sort_03.in",
        # "my_sort_04.in",
        # "my_sort_05.in",
        "my_sort_06.in",
    ]

    for i, file in enumerate(tests):
        try:
            student_result = run_program(STUDENT_BIN, f"data/{file}")
            valgrind_result = run_valgrind(STUDENT_BIN, f"data/{file}")
            print_report(i + 1, student_result, valgrind_result)
        except Exception as e:
            print(e)
