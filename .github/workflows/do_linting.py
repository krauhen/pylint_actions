import os
import sys

from pylint import lint
from io import StringIO

from openai import OpenAI

def send(msg):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a pydantic code fixer. Fix code snippets according to the pylint response. Return only the corrected code in the form: ```python\n CODE_GOES_HERE\n```"},
            {"role": "user", "content": msg}
        ]
    )
    return completion

BASE_PATH = "./.github/workflows/"
PYLINT_WHITELIST = os.path.join(BASE_PATH, ".pylint_whitelist.txt")
ARGS = []

with open(PYLINT_WHITELIST, "r") as f:
    filenames = f.readlines()

for filename in filenames:

    filename = filename.strip()

    stdout = sys.stdout
    sys.stdout = StringIO()
    r = lint.Run([filename] + ARGS, exit=False)

    test = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = stdout

    lines = test.split('\n')
    for line in lines:
        if (".py:") in line:
            print("============================================================================================")
            left_part, right_part = line.split(".py:")

            msg = " ".join(line.split(" ")[1:])
            filename = left_part + ".py"
            line_nr = right_part.split(":")[0]

            with open(filename, "r") as f:
                text = ""
                text += f"Pylint message: {msg}\n"
                text += f"Filename: {filename}\n"
                text += f"Line Number: {line_nr}\n"
                text += f"File-content:\n"
                content = f.readlines()
                content = "".join(content)
                text += "\n"
                text += content
            print(text)
            print()
            answer = send(msg)
            print(answer.choices[0].message.content)
            print()
            print("============================================================================================")
    print()
