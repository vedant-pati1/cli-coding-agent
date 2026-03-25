import os
import sys
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

verbose = True

def main():
    input_tokens: List[int] = []
    output_tokens: List[int] = []
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if len(sys.argv) < 2:
        print("Prompt is missing")
        sys.exit()

    prompt = sys.argv[1]
    system_prompt = """
You're a helpful AI coding agent. When a user asks a question or makes a request, make a function call plan. You can perform the following operations: list files and directories, read the content of a file, write to a file (create or update), and run a Python file with optional arguments.All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. When the user asks about the code project, they are referring to the working directory, so you should typically start by looking at the project's files and figuring out how to run the project and how to run its tests. You'll always want to test the tests and the actual project to verify that behavior is working.
"""

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    client = genai.Client(api_key=api_key)

    avaiable_functions = types.Tool(
        function_declarations=[
            schema_get_file_content,
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[avaiable_functions],
        thinking_config=types.ThinkingConfig(include_thoughts=False),
    )

    MAX_ITERATIONS = 20

    while len(messages) < MAX_ITERATIONS:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", contents=messages, config=config
        )
        if response is None:
            print("No response from the model.")
            return
        # things that model want to do like "call function get_file_content with these arguments"
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
                if candidate.content.parts is None:
                    continue
                for part in candidate.content.parts:
                    if part is None or part.function_call is None:
                        continue
                    result = call_function(part.function_call, part.thought_signature)
                    if verbose:
                        print("----------------------------------")
                        print(f"executed function: {part.function_call.name}({part.function_call.args}), got result: {result.parts[0].function_response.response.get('result')}")
                        print("----------------------------------")
                    else:
                        print(f"executed function: {part.function_call.name}({part.function_call.args})")
                    messages.append(result)

        # this actually calls the above mentioned functions and adds the result to the messages so that model can learn from it
        # if response.function_calls:
        #     for function_call in response.function_calls:
        #         result = call_function(
        #             function_call,
        #         )
        #         messages.append(result)
        else:
            # last response from model where there is no function call and model has done its work
            print(response.text)
            return
        if verbose:
            print(f"Input tokens: {response.usage_metadata.prompt_token_count}, Output tokens: {response.usage_metadata.candidates_token_count}")
        input_tokens.append(response.usage_metadata.prompt_token_count)
        output_tokens.append(response.usage_metadata.candidates_token_count)
    print(f"input token count: {sum([i for i in input_tokens if i is not None])}")
    print(f"Output token count: {sum([i for i in output_tokens if i is not None])}")


main()

