import sys
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("api key not found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt}
]

something = False
for i in range(20):
    response = client.chat.completions.create(
        model = "openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    response_text = response.choices[0].message
    messages.append(response_text)
    if not response.usage:
        raise RuntimeError("response usage not found")
    else:
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens

    if not response_text.tool_calls:
        print(response_text.content)
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
            print(f"Response: {response_text}")
        else:
            print(f"Response: {response_text}")
        something = True
        break
    else:
        for tool_call in response_text.tool_calls:
            result_message = call_function(tool_call, args.verbose)

            if not result_message["content"]:
                raise Exception("no content returned")
            dict_to_add = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_message["content"],
            }
            messages.append(dict_to_add)
            if args.verbose is True:
                print(f"-> {result_message['content']}")
if not something:
    print("Max iterations reached. The agent did not produce a final response")
    sys.exit(1)
    

