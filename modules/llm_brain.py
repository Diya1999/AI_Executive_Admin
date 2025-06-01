import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Support for NVIDIA/DeepSeek endpoint
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
if nvidia_api_key:
    from openai import OpenAI
    deepseek_client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=nvidia_api_key
    )
else:
    deepseek_client = None

def call_llm_brain(user_input):
    """
    Calls OpenAI GPT-4 (or NVIDIA/DeepSeek if configured) to extract structured info from user input.
    Returns a dict: {"intent": ..., "sentiment": ..., "tasks": [...]}
    """
    prompt = f"""
    Analyze the following user request and extract:
    - intent: calendar/email/task
    - sentiment: positive/neutral/negative
    - tasks: a list of actionable tasks
    Return as JSON.
    User request: {user_input}
    """
    if deepseek_client:
        # Use the DeepSeek model name for NVIDIA endpoint
        response = deepseek_client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[
                {"role": "system", "content": "You are an expert executive assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2
        )
    else:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert executive assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.2
        )
    import json
    try:
        content = response.choices[0].message.content
        data = json.loads(content)
        return data
    except Exception as e:
        return {"intent": "unknown", "sentiment": "neutral", "tasks": [], "error": str(e)} 