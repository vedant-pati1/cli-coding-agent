


from typing import List
import sys

def parse_args(argument: List[str]):
    verbose = False
    working_directory = None
    prompt = None
    try:
        for arg in range(len(argument)):
            if argument[arg] == "--verbose":
                verbose = True
            if argument[arg] == "--wd":
                working_directory = argument[arg + 1]
            if argument[arg] == "--p":
                prompt = argument[arg + 1]
    except IndexError:
        print("Argument value missing for ", argument[arg])
        sys.exit()

    if prompt is None or working_directory is None:
        print("arguments missing")
        sys.exit()
    return {
        "verbose": verbose,
        "working_directory": working_directory,
        "prompt": prompt,
    }
