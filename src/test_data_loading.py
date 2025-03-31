from inspect_ai import Task, task
from inspect_ai.solver import system_message
from inspect_ai.solver import basic_agent
from inspect_ai.scorer import model_graded_qa

from utils import load_agentharm_inspect, load_prompt

from tools import *
from tools import TOOL_NAMES
from huggingface_hub import login
import os
from dotenv import load_dotenv

load_dotenv()
login(token=os.getenv("HF_LOGIN_TOKEN"))

# tools = [globals()[name] for name in TOOL_NAMES]
tools = None



def harmful_task():
    # Load dataset
    dataset = load_agentharm_inspect(split="test_public", version="harmful", trust=True)

    # # # take first sample only
    dataset = dataset[:10]
    # Tools
    # tools = [post_x_reply, get_public_databases, generate_ai_voice]

    for sample in dataset:
        # Print the tools of the sample
        print(sample.metadata["tools"])

if __name__ == "__main__":
    harmful_task()
    