import os
import json
import argparse

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import config
from rich.console import Console
from rich.markdown import Markdown

from agent_tools import tool_defs, tool_funcs

load_dotenv()

base_url = "https://api.cerebras.ai/v1"
api_key = os.getenv("CEREB_API_KEY", None) 
model_name = os.getenv("CEREB_MODEL_NAME", "qwen-3-32b")

stop_program = False

console = Console()
parser = argparse.ArgumentParser()
client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        )

parser.add_argument("message", type=str, default=None)
args = parser.parse_args()

def build_msg(role, msg):
    if role == None:
        raise ValueError("Empty role passed...")

    return {
        "role": role,
        "content": msg
    }

usr_msg = args.message
messages = []
messages.append(build_msg("assistant", "You are a coding agent. Give short, to the point answers in minimal number of lines. Your memory is always stored in memory.txt. After the user's first message read memory.txt to understand the situtation and remember to write back to it every important operation or tidbit or piece of understanding or anything that you think will be relevant in the future. Make sure you summarize it into the best possible version for yourself to understand."))
messages.append(build_msg("user", usr_msg))

try:
    while not stop_program:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tool_defs,
            temperature=0.6,
        )

        message = response.choices[0].message
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result = tool_funcs[tool_call.function.name](**json.loads(tool_call.function.arguments))

                messages.append({
                    "role": "assistant",
                    "tool_calls": [tool_call]
                }) 
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
        else:
            response = message.content 
            # add retry or somethign to handle no response
            messages.append(build_msg("assistant", response))
            markdown = Markdown(response)

            console.print(markdown)

            console.print("\n[bold green]ME: [/bold green]", end="", soft_wrap=True)
            usr_msg = None
            while usr_msg is None:
                usr_msg = input()
            messages.append(build_msg("user", usr_msg))

except KeyboardInterrupt:
    console.print("\n[red]CTRL+C pressed. Exiting...[/red]\n")

