import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    args = sys.argv[1:]

    if not args:
        print("Enter you prompt")
        sys.exit(1)

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, user_prompt)


def generate_content(client, messages, prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )
    if "--verbose" in sys.argv:
        print("User prompt:", prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    print(response.text)


if __name__ == "__main__":
    main()
