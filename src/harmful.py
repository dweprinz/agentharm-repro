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



@task
def harmful_task():
    # Load prompts
    base_prompt = load_prompt("../prompts/default_prompt.txt")
    llama_suffix = load_prompt("../prompts/llama_suffix.txt")
    full_prompt = f"{base_prompt}\n\n{llama_suffix}"
    judge_prompt = load_prompt("../prompts/refusal_judge.txt")

    # Refusal judge
    refusal_judge = model_graded_qa(
        template=judge_prompt,
        grade_pattern=r"Answer:\s+(Yes|No)",
        instructions=None
    )

    
    # Load dataset
    dataset = load_agentharm_inspect(split="test_public", version="harmful", trust=True)

    # Tools
    # tools = [post_x_reply, get_public_databases, generate_ai_voice]

    return Task(
        dataset=dataset,
        solver=basic_agent(
            init=system_message(full_prompt),
            tools=tools,
            max_attempts=1
        ),
        scorer=refusal_judge
    )
