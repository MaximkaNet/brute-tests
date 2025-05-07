import subprocess
import os
import time
from itertools import zip_longest

CPP_EXECUTABLE = ['python3', 'hash.py']
# CPP_EXECUTABLE = ['./build/app']

def run_test_cpp(input_data: bytes):
  start_time = time.perf_counter()
  process = subprocess.run(
    CPP_EXECUTABLE,
    input=input_data.decode(),
    capture_output=True,
    text=True
  )

  end_time = time.perf_counter()
  excecution_time_ms = (end_time - start_time) * 1000

  return {
    "stdout": process.stdout,
    "stderr": process.stderr,
    "code": process.returncode,
    "time_ms": excecution_time_ms
  }

def get_file_data(file, data_folder = "data/") -> bytes:
  path = os.path.join(data_folder, file)
  with open(file=path, mode='rb') as f:
    return f.read()

def format_test_out(text: str, placeholder: str = '[Nothing]') -> str:
  return text if text else placeholder

def print_comparison(expected_blocks, actual_blocks):
    for i, (exp_block, act_block) in enumerate(zip_longest(expected_blocks, actual_blocks, fillvalue=[])):
        max_len = max(len(exp_block), len(act_block))
        for exp_line, act_line in zip_longest(exp_block, act_block, fillvalue=""):
            print(f"{exp_line:<50} | {act_line}")
        print()

class Condition:
  passed: bool
  expected: bytes
  actual: bytes
  name: str

  def __init__(self, name: str, expected: bytes, actual: bytes):
    self.expected = expected
    self.actual = actual
    self.name = name

  def test(self):
    self.passed = self.expected == self.actual

  def print(self, nothing: str = "[NONE]\n"):
    expected_str = f"Expected {self.name}:\n"
    expected_str += self.expected.decode("utf-8") if self.expected else nothing
    actual_str = f"Actual {self.name}:\n"
    actual_str += self.actual.decode("utf-8") if self.actual else nothing

    print_comparison(expected_blocks=[expected_str.split('\n')], actual_blocks=[actual_str.split('\n')])

  def is_passed(self):
    return self.passed

def run_test(test_name, input, expected, error: bytes = bytes()) -> bool:
  res = run_test_cpp(input_data=input)
  
  stderr: bytes = bytes(res["stderr"], encoding="utf-8")
  stdout: bytes = bytes(res["stdout"], encoding="utf-8")
  return_code: int = res["code"]
  exec_time = res["time_ms"]

  conditions = [
    Condition(expected=expected, actual=stdout, name="STDOUT"),
    Condition(expected=error, actual=stderr, name="STDERR")
  ]

  for cond in conditions:
    cond.test()

  failed = filter(lambda x: not x.is_passed(), conditions)
  failed = list(failed)

  # passed = True
  passed = len(failed) == 0

  TEST_STATUS = "PASSED" if passed else "FAILED"
  print(f"[{TEST_STATUS}] {test_name} (Execution time: {exec_time:.2f} ms)")

  if not passed:
    print("Return code:", return_code)
    for cond in failed:
      cond.print()

  print('')

  return passed

def main():
  test_case = [
    'prelude_01',
    'prelude_02',
    'prelude_03',
    'prelude_04',
    'prelude_05',
    'prelude_06',
    'prelude_07',
    'prelude_08',
    'append_01',
    'append_02',
    'append_03',
    'append_04',
    'append_05',
    'delete_01',
    'delete_02',
    'delete_07',
    'delete_08',
    'delete_09',
    'delete_10',
  ]

  result = []

  for case in test_case:
    r = run_test(
      test_name=f"{case}", 
      input=get_file_data(f"{case}.in"), 
      expected=get_file_data(f"STDOUT/{case}.out"),
      error=get_file_data(f"STDERR/{case}.err")
    )

    result.append(r)

  passed = result.count(True)
  failed = result.count(False)

  print("=" * 50)
  print(f"PASSED: {passed}", f"FAILED: {failed}")
  print('')


if __name__ == "__main__":
  main()
  # input = bytes(generate_test(1000, 10_000), encoding='utf-8')
  # print("data generated")
  # run_test(
  #   'big_test',
  #   input=input,
  #   expected=bytes("", encoding='utf-8')
  # )
  