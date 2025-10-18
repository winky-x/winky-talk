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
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
async def thinking_capability(query: str) -> str:
    """
    LangChain-powered reasoning and action tool.
    Takes a natural language query and executes the appropriate workflow.
    """
    
    try:
        # Use gemini-1.5-flash-latest for better compatibility
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0",  # Updated model name
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            max_tokens=500,  # Limit response length
            timeout=30  # Add timeout
        )
        
        prompt = hub.pull("hwchase17/react")
        
        tools = [
            Tool(
                name="google_search",
                func=google_search,
                description="Search the web for current information"
            ),
            Tool(
                name="get_current_datetime", 
                func=get_current_datetime,
                description="Get current date and time"
            ),
            Tool(
                name="get_weather",
                func=get_weather,
                description="Get weather information for a location"
            ),
            Tool(
                name="open_app",
                func=open_app,
                description="Open applications on the computer"
            ),
            Tool(
                name="close_app",
                func=close_app, 
                description="Close applications on the computer"
            ),
            Tool(
                name="folder_file",
                func=folder_file,
                description="Manage files and folders"
            ),
            Tool(
                name="Play_file",
                func=Play_file,
                description="Play media files"
            )
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
            handle_parsing_errors=True,
            max_iterations=3,  # Limit iterations to prevent long runs
            early_stopping_method="generate"
        )

        # Run with timeout
        result = await asyncio.wait_for(
            executor.ainvoke({"input": query}),
            timeout=25.0  # 25 second timeout
        )
        
        return str(result.get("output", "Task completed"))
        
    except asyncio.TimeoutError:
        logger.warning("Thinking capability timed out")
        return "I need more time to process that request. Please try again with a simpler query."
        
    except Exception as e:
        logger.error(f"Thinking capability error: {e}")
        return f"I encountered an error while processing your request: {str(e)}"