from inspect_ai import Task, task
from inspect_ai.solver import system_message, generate
from inspect_ai.scorer import exact

from utils import load_agentharm_inspect, load_prompt
from judge import refusal_judge_scorer

from huggingface_hub import login
import os
from dotenv import load_dotenv

load_dotenv()
login(token=os.getenv("HF_LOGIN_TOKEN"))

@task
def agentharm_chat_task():
    # Working directory is src
    
    # Load prompts from files
    base_prompt = load_prompt("../prompts/default_prompt.txt")
    llama_suffix = load_prompt("../prompts/llama_suffix.txt")
    full_prompt = f"{base_prompt}\n\n{llama_suffix}"
    judge_prompt = load_prompt("../prompts/refusal_judge.txt")

    # Load dataset
    dataset = load_agentharm_inspect(split="test_public", version="chat", trust=True)
    
    # take first sample only
    dataset = dataset[:1]

    return Task(
        dataset=dataset,
        solver=[
            system_message(full_prompt),
            generate()
        ],
        scorer=refusal_judge_scorer(judge_prompt, model_name="meta-llama/Meta-Llama-3.1-8B-Instruct"
    )
        )
