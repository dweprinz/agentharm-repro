from dotenv import load_dotenv

load_dotenv()
import os
print("Using key:", os.getenv("OPENAI_API_KEY"))
print("Base URL:", os.getenv("OPENAI_API_BASE"))

