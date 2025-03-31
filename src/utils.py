from datasets import load_dataset
from inspect_ai.dataset import FieldSpec, hf_dataset
from inspect_ai import solver

def load_agentharm_hf(version="chat"):
    """
    Load the AgentHarm dataset from the Hugging Face Hub.
    
    We have two versions of the dataset:
    - `chat`: This version contains the chat data.
    - `harmful`: This version contains the harmful data.
    - `harmless-benign`: This version contains the harmless data.
    
    Args:
        version (str): The version of the dataset to load. Defaults to "chat".
    Returns:
        datasets.DatasetDict: The loaded dataset.
    Raises:
        AssertionError: If the version is not one of the expected values.
        Exception: If there is an error loading the dataset.
    """
    try:
        assert version in ["chat", "harmful", "harmless_benign"], "Invalid version picked. Choose from 'chat', 'harmful', or 'harmless_benign'."
        ds = load_dataset("ai-safety-institute/AgentHarm", version)
    except AssertionError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None
    return ds


def load_agentharm_chat(split="test_public", trust=True):
    """
    Load the 'chat' subset of AgentHarm using hf_dataset + FieldSpec.
    """
    return hf_dataset(
        path="ai-safety-institute/AgentHarm",
        name="chat",
        split=split,
        trust=trust,
        sample_fields=FieldSpec(
            id="id",                     # We'll just use 'id'
            input="prompt",              # Single string prompt
            target=None,                 # No final 'output' column
            metadata=["id_original", "name", "category"]
        )
    )



def load_agentharm_agent(split="test_public", version="harmful", trust=True):
    """
    Load the 'harmful' or 'harmless_benign' agent subsets of AgentHarm using hf_dataset + FieldSpec.
    """
    # version must be either 'harmful' or 'harmless_benign'
    return hf_dataset(
        path="ai-safety-institute/AgentHarm",
        name=version,
        split=split,
        trust=trust,
        sample_fields=FieldSpec(
            id="id",              # We'll just use 'id' again
            input="prompt",       # Single string prompt
            target=None,          # No final 'output' column in the snippet
            metadata=[
                "id_original", "name", "category",
                "detailed_prompt", "hint_included",
                "target_functions", "grading_function"
            ]
        )
    )

def load_agentharm_inspect(split="test_public", version="chat", trust=True):
    """
    Unified loader for any version of the AgentHarm dataset.
    """
    if version == "chat":
        return load_agentharm_chat(split=split, trust=trust)
    elif version in ["harmful", "harmless_benign"]:
        return load_agentharm_agent(split=split, version=version, trust=trust)
    else:
        raise ValueError(f"Unknown version: {version}")



def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
if __name__ == "__main__":
    # Test prompt loading 
    
    prompt = load_prompt("prompts/default_prompt.txt")
    print(prompt)
    
    prompt = load_prompt("prompts/llama_suffix.txt")
    print(prompt)