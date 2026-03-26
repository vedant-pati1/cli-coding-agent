from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info 
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file


registry = {
    "get_file_content": {
        "function": get_file_content,
        "schema": schema_get_file_content,
    },
    "get_files_info": {
        "function": get_files_info,
        "schema": schema_get_files_info,
    },
    "write_file": {
        "function": write_file,
        "schema": schema_write_file,
    },
    "run_python_file": {
        "function": run_python_file,
        "schema": schema_run_python_file,
    },
}