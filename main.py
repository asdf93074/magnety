import os
import argparse

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

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
messages.append(build_msg("assistant", "You are a coding agent. Give short, to the point answers in minimal number of lines."))
messages.append(build_msg("user", usr_msg))

try:
    while not stop_program:
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )

        response = completion.choices[0].message.content 
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

