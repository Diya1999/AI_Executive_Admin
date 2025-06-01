from modules.llm_brain import call_llm_brain
from modules.calendar import handle_calendar
from modules.email import handle_email
from modules.task import handle_tasks

def handle_user_input(user_input):
    llm_result = call_llm_brain(user_input)
    intent = llm_result.get("intent", "unknown")
    sentiment = llm_result.get("sentiment", "neutral")
    tasks = llm_result.get("tasks", [])
    responses = []

    if intent == "calendar":
        responses.append(handle_calendar(user_input))
    elif intent == "email":
        responses.append(handle_email(user_input))
    elif intent == "task":
        responses.append(handle_tasks(user_input))
    else:
        responses.append("[Sorry, I couldn't determine the intent.]")

    formatted = f"**Sentiment:** {sentiment}\n\n**Tasks:** {tasks}\n\n" + "\n".join(responses)
    return formatted 