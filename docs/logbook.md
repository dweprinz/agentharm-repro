10:00-11:00 Friday 28 march: I started out reading the paper and installing the inspect framework.
Installing the inspect framework is super easy, but permission to llama is still to be granted.  That's why I am now installing llama3.1 through ollama.

Permission was granted within 30 minutes.

Both work now. but I had to force less memory to be used: uv run inspect eval hello.py --model hf/meta-llama/Llama-3.1-8B-Instruct -M torch_dtype=float16 -M max_memory='{"mps": "24GiB"}' 

11:30 - Sunday 30 march: 
I'll be starting off with the tutorial of inspect, in hello.py
I'll be working on making a more complex script than hello.py


12:15 - sunday 30 march. So now I finished the loading of the data, found the prompts and found out how to use it in inspect. Now I'm going to run 
uv run inspect eval src/chat.py --model hf/meta-llama/Llama-3.1-8B-Instruct -M torch_dtype=float16 -M max_memory='{"mps": "24GiB"}'

This will use exact matching and will probably have a very low score.

13:30 had to update the prompt template to use answer instead of generation to use model_qa otherwise i got memory error of running two models.

Now I have a benchmark that runs all chats then the refusal judge decides whether it was refusal or not. 

13:50 I'm thinking whether I should include any tools or grading. The assignment specifically mentions focusing on the refusal judge. This makes sense as it seems like there are a lot of grading functions not detailed in the paper.

This means that for the agentic benchmark I will still just run a prompt, get the output and see what the refusal rate is. Now the question is, what is the difference between our llm chat call and an agentic call.