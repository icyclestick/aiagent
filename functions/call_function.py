from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google import genai

def call_function(function_call_part, verbose=False):
    print("Function call part:", function_call_part)
    functions_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    elif function_call_part.name not in functions_dict:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    if function_call_part:
        print(f" - Calling function: {function_call_part.name}")
        if function_call_part.name in functions_dict:
            result = functions_dict[function_call_part.name]("./calculator", **function_call_part.args)
            return genai.types.Content(
                role="tool",
                parts=[
                    genai.types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"result": result},
                    )
                ],
            )
