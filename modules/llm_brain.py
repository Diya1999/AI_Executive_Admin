import openai
import os

def call_llm_brain(user_input):
    """
    Calls OpenAI GPT-4 to extract structured info from user input.
    Returns a dict: {"intent": ..., "sentiment": ..., "tasks": [...]}
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"""
    Analyze the following user request and extract:
    - intent: calendar/email/task
    - sentiment: positive/neutral/negative
    - tasks: a list of actionable tasks
    Return as JSON.
    User request: {user_input}
    """
    response = openai.chat.completions.create(
        model="gpt-4",
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