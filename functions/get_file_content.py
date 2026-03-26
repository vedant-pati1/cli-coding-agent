from pathlib import Path
from google.genai import types


def get_file_content(working_directory: str, file_path: str):

    abs_working_dir = Path(working_directory).resolve()
    abs_file_path = (Path(working_directory) / file_path).resolve()
    # print(f"working directory: {abs_working_dir}, requested file: {abs_file_path}")
    if not abs_file_path.is_relative_to(abs_working_dir):
        return f"Error: {file_path} is not in working directory"

    if not abs_file_path.is_file():
        return f"Error: {file_path} is not a file"

    file_content = ""
    MAX_CHAR_LIMIT = 1000
    try:
        with open(abs_file_path, "r") as f:
            file_content = f.read(MAX_CHAR_LIMIT + 1)
            if len(file_content) > MAX_CHAR_LIMIT:
                file_content = file_content[:MAX_CHAR_LIMIT]
                file_content += (
                    f"File: {file_path} is truncated at {MAX_CHAR_LIMIT} characters"
                )
    except:
        return f"Error: issue in reading the file"
    return file_content


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file in the working directory. The content is limited to 1000 characters. If the file is larger than 1000 characters, only the first 1000 characters will be returned with a message indicating that the content is truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file relative to the working directory.",
            ),
        },
    ),
)