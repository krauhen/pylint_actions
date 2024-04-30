# Experiment to automate static code analysis with github actions and LLMs
1. For every .py file in repo execute pylint
2. Pipe pylint warning/errors to a LLM with the matching source code and a prompt
3. Push the newly generated code into a new branch
4. Automatillcy create a Pull Request to appy changes

- As a github secret you need to set the secret OPENAI_API_KEY to a valid Openai API-Key.
- As a github variable you need to set the variable LLM to e.g. gpt-3.5-turbo

- See ![pylint.yml](https://github.com/krauhen/pylint_actions/blob/main/.github/workflows/pylint.yml) for the github action definition.
- See ![do_linting.py](https://github.com/krauhen/pylint_actions/blob/main/.github/workflows/do_linting.py) for the python script that does the work.
- See ![.pylint_whitelist.txt](https://github.com/krauhen/pylint_actions/blob/main/.github/workflows/.pylint_whitelist.txt) for the processed files.
