from inspect_ai import Task, task
from inspect_ai.solver import system_message
from inspect_ai.solver import basic_agent
from inspect_ai.scorer import model_graded_qa

from utils import load_agentharm_inspect, load_prompt


from tools import *
from huggingface_hub import login
import os
from dotenv import load_dotenv
from inspect_ai.solver import TaskState, Generate, solver, Solver
from inspect_ai.solver import use_tools


load_dotenv()
login(token=os.getenv("HF_LOGIN_TOKEN"))


@solver
def dynamic_tools_solver() -> Solver:
    """A solver *factory* that returns an async solve() function for dynamic tools."""

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        # Grab the list of tool names from metadata
        function_names = state.metadata.get("target_functions", [])

        print(f"Function names: {function_names}")

        if not function_names:
            return state

        # Convert each function name into an actual python_tool
        tools = []
        for fn in function_names:
            if fn in globals():
                tool_obj = globals()[fn]()
                tools.append(tool_obj)

        # Print the picked tools
        print(f"Tools picked: {[name for name in function_names if name in globals()]}")

        # Now use the built-in use_tools solver (it’s also async)
        solver_for_tools = use_tools(*tools, tool_choice=True)

        # Must await the returned solver call
        return await solver_for_tools(state, generate)

    return solve


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
        instructions=None,
        # model="openai/meta-llama/Meta-Llama-3.1-70B-Instruct",
    )

    # Load dataset
    dataset = load_agentharm_inspect(split="test_public", version="harmful", trust=True)

    # # # take first sample only
    # dataset = dataset

    return Task(
        dataset=dataset,
        solver=basic_agent(
            init=system_message(full_prompt),
            tools=dynamic_tools_solver(),
            max_attempts=1,
            max_messages=20,
        ),
        scorer=refusal_judge,
    )
