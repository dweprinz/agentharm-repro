https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct

# Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="meta-llama/Llama-3.1-8B-Instruct")
pipe(messages)

inspect eval hello.py --model hf/meta-llama/Llama-3.1-8B-Instruct
inspect eval theory.py --model openai/gpt-4

inspect eval hello.py --model ollama/llama3.1

memory tries to get 29 GB but that is not needed so i use
uv run inspect chat.py --model hf/meta-llama/Llama-3.1-8B-Instruct -M torch_dtype=float16 -M max_memory='{"mps": "24GiB"}' 


to try it out with deepinfra I would use 
uv run inspect eval src/chat.py --model openai/meta-llama/Meta-Llama-3-8B-Instruct


for the agent we run
uv run inspect eval src/harmful.py --model openai/meta-llama/Meta-Llama-3-8B-Instruct
costs: 15 cent
uv run inspect eval src/harmless_benign.py --model openai/meta-llama/Meta-Llama-3-8B-Instruct
costs: 
