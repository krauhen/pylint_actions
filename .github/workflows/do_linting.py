import os
import sys

from pylint import lint
from io import StringIO

from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LLM = os.environ.get("LLM")

def send(msg):

    prompt = ""
    prompt += "You are a pylint code fixer.\n"
    prompt += "Fix code snippets according to the pylint response.\n"
    prompt += "Return only the corrected code in the form: \n\n```python\n CODE_GOES_HERE\n```\n"
    prompt += "\n"
    prompt += msg
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model=LLM,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion, prompt

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

    msg = ""
    for line in lines:
        msg += " ".join(line.split(" ")[1:]) + "\n"
    
    for line in lines:
        if (".py:") in line:
            left_part, right_part = line.split(".py:")
            filename = left_part + ".py"
            break

    text = ""
    text += f"Pylint messages: \n{msg}\n"
    text += f"Filename: {filename}\n"
    text += f"File-content:\n"
    
    with open(filename, "r") as f:
        content = f.readlines()
        content = "".join(content)
        text += "```python\n"
        text += content
        text += "```\n"
    
    answer, prompt = send(text)
    content = answer.choices[0].message.content
    print("============================================================================================")
    print(prompt)
    print()
    print("============================================================================================")
    print(content)
    print()
    print("============================================================================================")
    print()

    content = content.replace("```python", "")
    content = content.replace("```", "")
    
    with open(filename, "w") as f:
        f.write(content)
