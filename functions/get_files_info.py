import os

from genai import types


def get_files_info(working_directory, directory="."):
    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declerations=[
            schema_get_files_info,
        ]
    )

    joined_directory = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(joined_directory)
    working_abs_path = os.path.abspath(working_directory)

    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    # print("JOINED", joined_directory)
    # print("abs:", abs_path, "\n", "working:", working_abs_path)

    if working_abs_path not in abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    is_dir = os.path.isdir(joined_directory)

    if not is_dir:
        return f'Error: "{directory}" is not a directory'

    files = os.listdir(joined_directory)
    # print("files", files)

    file_info = []

    for file in files:
        item_path = os.path.join(joined_directory, file)
        file_size = os.path.getsize(item_path)
        is_file_dir = os.path.isdir(item_path)
        file_info.append(f"{file} file_size={file_size} is_dir={is_file_dir}")
    return "\n".join(file_info) + "\n"
