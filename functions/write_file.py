from pathlib import Path
from google.genai import types


def write_file(working_directory: str, file_path: str, content: str):

    abs_working_dir = Path(working_directory).resolve()
    abs_file_path = (Path(working_directory) / file_path).resolve()

    if not abs_file_path.is_relative_to(abs_working_dir):
        return f"Error: {file_path} is not in working directory"

    if not abs_file_path.is_file():
        parent_dir = abs_file_path.parent
        try:
            if not parent_dir.is_dir():
                parent_dir.mkdir(parents=True)
        except:
            return f"Error: Unable to make parent directory of {file_path}"

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f"Successfully written to file {file_path}, {len(content)} characters written"
    except:
        return f"Error: Failed to write to the file"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)


if __name__ == "__main__":
    print(write_file(".", "./games", "hi this is a game"))
