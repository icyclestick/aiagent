from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file

print("Run:")
print(run_python_file("calculator", "main.py"))
print("File info:")
print(get_files_info(".", "calculator"))
print("File content:")
print(get_file_content("calculator", "main.py"))
print("Write file:")
print(write_file("calculator", "lorem.txt", "Hello"))
