from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from dotenv import load_dotenv
from Jarvis_google_search import google_search, get_current_datetime
from jarvis_get_whether import get_weather
from Jarvis_window_CTRL import open_app, close_app, folder_file
from Jarvis_file_opner import Play_file
from langchain import hub
import os
import asyncio
from livekit.agents import function_tool

load_dotenv()

# Verify Google API key is present
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

@function_tool(
    name="thinking_capability",
    description=(
        "Uses LangChain with Google's Gemini model for reasoning and task execution. "
        "Handles tasks like searches, weather checks, app control, and file operations."
    )
)
async def thinking_capability(query: str) -> dict:
    """
    LangChain-powered reasoning and action tool.
    Takes a natural language query and executes the appropriate workflow.
    """
    
    model = ChatGoogleGenerativeAI(
        model="gemini-pro",  # Using gemini-pro instead of gemini-1.5-flash
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        convert_system_message_to_human=True
    )
    
    prompt = hub.pull("hwchase17/react")
    
    tools = [
        google_search,
        get_current_datetime,
        get_weather,
        open_app,
        close_app,
        folder_file,
        Play_file
    ]

    agent = create_react_agent(
        llm=model,
        tools=tools,
        prompt=prompt
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True  # Added to handle parsing errors gracefully
    )

    try:
        result = await executor.ainvoke({"input": query})
        return result
    except Exception as e:
        return {"error": f"Agent execution failed: {str(e)}"}