import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    file_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_dir):
        return f'Error: File "{file_path}" not found.'

    if not file_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python", file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            timeout=30,
            text=True,
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output is produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"
