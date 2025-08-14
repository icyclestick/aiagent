import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def main():
    args = sys.argv[1:]

    if not args:
        print("Enter you prompt")
        sys.exit(1)

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for i in range(20):
        try:
            response = generate_content(client, messages, user_prompt)
            if response:
                print("Final response:")
                print(response.text)
                return 0
        except Exception as e:
            print(f"Error encountered: {e}")


def generate_content(client, messages, prompt):
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if not response.function_calls:
        print("Didnt call func")
        return (response)
        raise Exception("LLM didn't call a function")
    elif response.function_calls:
        for candidate in response.candidates:
            messages.append(candidate.content)
        if "--verbose" in sys.argv:
            print("User prompt:", prompt)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print(
            f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args}")
        result = call_function(response.function_calls[0])
        messages.append(types.Content(role="user", parts=result.parts))
        if not result.parts[0].function_response.response:
            raise Exception("No response in the result")
        elif result.parts[0].function_response.response and "--verbose" in sys.argv:
            print(f"-> {result.parts[0].function_response.response}")

if __name__ == "__main__":
    main()
