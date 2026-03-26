from pathlib import Path
from google.genai import types


def get_files_info(working_directory: str, directory: str = "."):
    abs_working_path = Path(working_directory).resolve()
    abs_directory = (Path(working_directory) / directory).resolve()

    if not abs_directory.is_relative_to(abs_working_path):
        return f"Error: {directory} is not in working directory"
    if not abs_directory.exists():
        return f"Error: {directory} does not exist"

    contents = abs_directory.iterdir()
    result = ""
    for c in contents:
        result += f"{c}: is_dir= {c.is_dir()}, size= {c.stat().st_size}\n"
    return result


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Get information about files in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files in, relative to the working directory.",
            ),
        },
    ),
)


