from google.genai import types
from google.genai.types import FunctionCall

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

working_directory = "demo-project"


def call_function(function_call: FunctionCall, thought_signature: bytes) -> types.Content:

    result = ""
    if function_call.name == "get_files_info":
        result = get_files_info(working_directory, **function_call.args)
    elif function_call.name == "get_file_content":
        result = get_file_content(working_directory, **function_call.args)
    elif function_call.name == "write_file":
        result = write_file(working_directory, **function_call.args)
    elif function_call.name == "run_python_file":
        result = run_python_file(working_directory, **function_call.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Function {function_call.name} not found"},
                    # thought_signature=thought_signature,
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": result},
                # thought_signature=thought_signature,
            )
        ],
    )
