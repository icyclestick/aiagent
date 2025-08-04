import os


def get_files_info(working_directory, directory="."):
    joined_directory = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(directory)
    working_abs_path = os.path.abspath(directory)

    if abs_path not in working_directory:
        return f'Error: "{directory}" is not a directory'

    is_dir = os.path.isdir(directory)

    if not is_dir:
        return f'Error: "{directory}" is not a directory'
