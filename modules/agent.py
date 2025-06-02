from modules.calendar import handle_calendar
from modules.email import handle_email
from modules.task import handle_tasks
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables

# Define tools for each agent
calendar_tool = Tool(
    name="Calendar",
    func=handle_calendar,
    description="Handles calendar requests"
)
email_tool = Tool(
    name="Email",
    func=handle_email,
    description="Handles email requests"
)
task_tool = Tool(
    name="Task",
    func=handle_tasks,
    description="Handles task requests"
)

tools = [calendar_tool, email_tool, task_tool]

# Initialize the LLM based on available API keys
nvidia_api_key = os.getenv("NVIDIA_API_KEY")

if nvidia_api_key:
    # Use DeepSeek via NVIDIA endpoint
    llm = ChatOpenAI(
        openai_api_key=nvidia_api_key,
        base_url="https://integrate.api.nvidia.com/v1",
        model="deepseek-ai/deepseek-r1", # Specify the model name for this endpoint
        temperature=0
    )
else:
    # Fallback to OpenAI
    llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo", temperature=0)

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True,
)

def handle_user_input(user_input):
    response = agent.run(user_input)
    return response 