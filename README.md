
# CLI Coding Agent

A CLI-based coding agent that operates on a given project directory. It uses an LLM-driven feedback loop to perform automated coding tasks such as reading, modifying, and executing code.

##  Features

*  Read files from the project directory
*  Write or modify files
*  Search for files within the directory
*  Execute programs (currently supports Python only)
* Iterative feedback loop with an LLM for task completion


## How to use
```bash
uv sync
uv run main.py --p "<your prompt>" --wd "<working-directory>"
```

### Arguments

* `--p` : Task prompt for the agent
* `--wd` : Target working directory

##  Example

```bash
uv run main.py --p "Fix the issue in main.py" --wd ./demo-project
```

##  Limitations

* Currently supports execution of Python programs only
* Requires a properly structured project directory
* Can only be used with Google Gemini's API and SDK
* Prompts within the code can be improved.

## TODO
 * make agent model provider agnostic
 * Create workflow to automatically include all the functions from functions folder without manually editing the rest of the project

