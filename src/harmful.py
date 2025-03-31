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

from inspect_ai.tool import python as python_tool  # or your custom Tool wrapper



load_dotenv()
login(token=os.getenv("HF_LOGIN_TOKEN"))

    
# @solver
# def provide_sample_tools() -> Solver:
#     def solve(state: TaskState, generate: Generate) -> TaskState:
#         functions = state.metadata.get("target_functions", [])
#         tools = [python_tool(f) for f in functions]  # or build Tool from dict
#         return use_tools(*tools)(state, generate)
#     return solve

@solver
def dynamic_tools_solver(**params) -> Solver:
    """
    This solver dynamically loads tools based on the metadata of the task.
    It retrieves the function names from the metadata and creates tools for them.
    
    Returns:
    A solver that inserts the tools into the task state.
    """
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        """

        Args:
            state (TaskState): 
            generate (Generate): 

        Returns:
            TaskState: 
        """
        kwargs = state.metadata
        function_names = kwargs.get("target_functions", [])

        tools_objs = [globals()[name] for name in function_names]
        state = use_tools(*tools_objs)(state, generate)
        
        return state
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
        instructions=None
    )

    
    # Load dataset
    dataset = load_agentharm_inspect(split="test_public", version="harmful", trust=True)

    # # # take first sample only
    dataset = dataset[:10]

    return Task(
        dataset=dataset,
        solver=basic_agent(
            init=system_message(full_prompt),
            tools=dynamic_tools_solver(),
            max_attempts=1
        ),
        scorer=refusal_judge
    )
