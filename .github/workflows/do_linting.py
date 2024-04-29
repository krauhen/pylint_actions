import os
import sys

from pylint import lint
from io import StringIO

BASE_PATH = "./.github/workflows/"
PYLINT_WHITELIST = os.path.join(BASE_PATH, ".pylint_whitelist.txt")
ARGS = []

with open(PYLINT_WHITELIST, "r") as f:
    filenames = f.readlines()

for filename in filenames:

    filename = filename.strip()

    stdout = sys.stdout
    sys.stdout = StringIO()
    r = lint.Run([filename]+ARGS, exit=False)

    test = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = stdout

    lines = test.split('\n')
    print("========================================================================================================================================")
    print(filename)
    for line in lines:
        if (".py:") in line:
            print(line)
    print("========================================================================================================================================")
    print()
