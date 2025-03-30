10:00-11:00 Friday 28 march: I started out reading the paper and installing the inspect framework.
Installing the inspect framework is super easy, but permission to llama is still to be granted.  That's why I am now installing llama3.1 through ollama.

Permission was granted within 30 minutes.

Both work now. but I had to force less memory to be used: uv run inspect eval hello.py --model hf/meta-llama/Llama-3.1-8B-Instruct -M torch_dtype=float16 -M max_memory='{"mps": "24GiB"}' 

11:30 - Sunday 30 march: 
I'll be starting off with the tutorial of inspect, in hello.py
I'll be working on making a more complex script than hello.py
