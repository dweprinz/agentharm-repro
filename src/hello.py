from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import exact
from inspect_ai.solver import generate      

from huggingface_hub import login
import os

from dotenv import load_dotenv
load_dotenv()

# load token from environment variable
login(token = os.getenv("HF_LOGIN_TOKEN"))

@task
def hello_world():
    return Task(
        dataset=[
            Sample(
                input="Just reply with Hello World",
                target="Hello World",
            )
        ],
        solver=[generate()],
        scorer=exact(),
    )