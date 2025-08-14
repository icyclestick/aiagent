import os
from google import genai

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="Content to write to the file"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    file_dir = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_dir.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.exists(file_dir) == False:
        os.makedirs(os.path.dirname(file_dir), exist_ok=True)

    try:
        with open(file_dir, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error writing file: {e}"
