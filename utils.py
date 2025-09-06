import os
from openai import OpenAI

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

# Initialize client
client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

def generate_chat_response(prompt: str) -> str:
    """
    Send prompt to vLLM (Mistral / GPT-OSS) and return the response text
    """
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
