import openai
import os
from dotenv import load_dotenv
import re

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
    - intent: one of [\"calendar\", \"email\", \"task\"]
    - sentiment: one of [\"positive\", \"neutral\", \"negative\"]
    - tasks: a list of actionable tasks

    Return ONLY a valid JSON object with keys: intent, sentiment, tasks. Do not include any explanation or extra text. Example:
    {{"intent": "calendar", "sentiment": "positive", "tasks": ["Schedule a meeting with Ravi"]}}

    User request: {user_input}
    """
    if deepseek_client:
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
        print("LLM raw output:", content)  # Debug print
        # Extract the first JSON object from the output
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            return data
        else:
            return {"intent": "unknown", "sentiment": "neutral", "tasks": [], "error": "No JSON found in LLM output"}
    except Exception as e:
        return {"intent": "unknown", "sentiment": "neutral", "tasks": [], "error": str(e)} 