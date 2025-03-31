from inspect_ai import Task, task
from inspect_ai.solver import system_message, generate
from inspect_ai.scorer import model_graded_qa

from utils import load_agentharm_inspect, load_prompt

from huggingface_hub import login
import os
from dotenv import load_dotenv

load_dotenv()
login(token=os.getenv("HF_LOGIN_TOKEN"))


@task
def chat_task():
    # Working directory is src

    # Load prompts from files
    base_prompt = load_prompt("../prompts/default_prompt.txt")
    llama_suffix = load_prompt("../prompts/llama_suffix.txt")
    full_prompt = f"{base_prompt}\n\n{llama_suffix}"
    judge_prompt = load_prompt("../prompts/refusal_judge.txt")
    REFUSAL_PATTERN = r"Answer:\s+(Yes|No)"

    refusal_judge = model_graded_qa(
        template=judge_prompt, grade_pattern=REFUSAL_PATTERN, instructions=None
    )

    # Load dataset
    dataset = load_agentharm_inspect(split="test_public", version="chat", trust=True)

    # # # take first sample only
    # dataset = dataset[:2]

    return Task(
        dataset=dataset,
        solver=[system_message(full_prompt), generate()],
        scorer=refusal_judge,
    )
