import random

STDERR_FOLDER='STDERR'
STDOUT_FOLDER='STDOUT'
STDIN_FOLDER=''

DATA_PATH = 'data'

def head(
    maximum: int,
    type: int,
    virus: int
):
  return f"{maximum} {type} {virus}\n"

def generate(
    name: str,
    in_data: list,
    out_data: list,
    sort_type: int,
    virus: bool,
    max_val: int = 10
):
  with open(f"{DATA_PATH}/{STDERR_FOLDER}/{name}.err", 'w') as f:
    pass

  with open(f"{DATA_PATH}/{STDOUT_FOLDER}/{name}.out", 'w') as f:
    for item in out_data:
      f.write(str(item) + '\n')

  with open(f"{DATA_PATH}/{STDIN_FOLDER}/{name}.in", 'w+') as f:
    f.write(head(maximum=max_val, type=sort_type, virus=int(virus)))
    for item in in_data:
      f.write(str(item) + '\n')

def main():

  MAX_VAL = 2000
  LENGTH = 2_000_000

  data = [random.randint(1, MAX_VAL) for _ in range(LENGTH)]

  generate(
    name="my_sort_06",
    sort_type=0,
    virus=True,
    max_val=MAX_VAL,
    in_data=data,
    out_data=sorted(data)
  )

if __name__ == "__main__":
  main()