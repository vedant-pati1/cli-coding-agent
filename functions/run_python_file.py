import subprocess
from pathlib import Path
from google.genai import types


def run_python_file(working_directory: str, file_path: str, args: list[str] = []):
    abs_working_path = Path(working_directory).resolve()
    abs_file_path = (Path(working_directory) / file_path).resolve()

    if not abs_file_path.is_relative_to(abs_working_path):
        return f"Error: {file_path} is not in working directory"
    if not abs_file_path.exists():
        return f"Error: {file_path} does not exist"
    if not abs_file_path.is_file():
        return f"Error: {file_path} is not a file"

    if not (abs_file_path.suffix == ".py"):
        return f"Error: {file_path} is not a Python file"
    try:
        result = subprocess.run(
            ["python", str(abs_file_path)] + args,
            capture_output=True,
            text=True,
            timeout=20,
            cwd=abs_working_path,
        )
        output_str = f"""
        STDOUUT:
        {result.stdout}

        STDERR:
        {result.stderr}
        """

        if result.stdout.strip() == "" and result.stderr == "":
            output_str = "File ran successfully with no output"

        if result.returncode != 0:
            output_str += (
                f"\nProcess exited with non-zero exit code: {result.returncode}"
            )

    except Exception as e:
        return f"Error: Failed to run the file, {str(e)}"
    return output_str


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file in the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The arguments to pass to the Python file.",
            ),
        },
    ),
)