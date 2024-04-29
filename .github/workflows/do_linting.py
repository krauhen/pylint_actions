import pylint

with open(".pylint_whitelist.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    print(line)
    print()
    (pylint_stdout, pylint_stderr) = lint.py_run(line, return_std=True)
    print("pylint_stdout")
    print(pylint_stdout)
    print()
    print("pylint_stderr")
    print(pylint_stderr)
    print()
