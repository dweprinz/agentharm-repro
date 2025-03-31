# Llama 3.1 Refusal Benchmarking

This project evaluates **refusal behavior** of LLMs using [Meta-Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) across three experimental setups: `chat`, `harmful`, and `harmless_benign`. All evaluations are conducted using the [Inspect](https://inspect.aisi.org.uk/) framework.

---
## Installation
When cloning the github, you'll be ready to use uv immediately if you have this installed.

1. Sync your uv
```bash
uv sync
```

2. Now you should have all the packages ready. Now use the uv run commands to run the code.

## Configuration
1. To configure your deepinfra, you need a .env file containing
```
OPENAI_API_KEY=<your_deepinfra_key>
OPENAI_BASE_URL=https://api.deepinfra.com/v1/openai
```

2. To access your huggingface account (for the data but more so for the model), you'll need to add an access token from your huggingface account to the .env file.

```
HF_LOGIN_TOKEN=<your huggingface_key>
OPENAI_API_KEY=<your_deepinfra_key>
OPENAI_BASE_URL=https://api.deepinfra.com/v1/openai
```

## 🧪 Experiments
You can run the benchmark with the deepinfra or locally on your device.

### Deepinfra
Run the benchmarks with the following commands:
```bash
uv run inspect eval src/chat.py --model openai/meta-llama/Meta-Llama-3.1-8B-Instruct
uv run inspect eval src/harmful.py --model openai/meta-llama/Meta-Llama-3.1-8B-Instruct
uv run inspect eval src/harmless_benign.py --model openai/meta-llama/Meta-Llama-3.1-8B-Instruct
```

### Locally
Run the benchmarks with the following commands:
```bash
uv run inspect eval src/chat.py --model hf/meta-llama/Llama-3.1-8B-Instruct 
uv run inspect eval src/harmful.py --model hf/meta-llama/Llama-3.1-8B-Instruct 
uv run inspect eval src/harmless_benign.py --model hf/meta-llama/Llama-3.1-8B-Instruct
```


### Extra notes
On my macbook I got errors about memory allocation. This was easy to fix using 
```bash
uv run inspect eval src/chat.py \
  --model hf/meta-llama/Llama-3.1-8B-Instruct \
  -M torch_dtype=float16 \
  -M max_memory='{"mps": "24GiB"}'
```

This forced less memory allocation, as it was redundant memory.

## File Overview
Main experiment files
- src/hello.py: A minimal script using the Inspect pipeline.
- src/chat.py: Evaluates refusal behavior on chat prompts.
- src/harmful.py: Evaluates refusal behavior on harmful prompts.
- src/harmless_benign.py: Evaluates over-refusals on benign prompts.

Modules
- src/judge.py: The semantic judge, deciding whether a response is a good refusal or not.
- src/tools.py: Implementation of synthetic tools
- src/utils.py: Utils used during the project.

## Notes
- Inspect was straightforward to set up.
- 
