import os

from dotenv import load_dotenv

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

from agents import Agent, Runner, WebSearchTool

web_search_tool = WebSearchTool(
    user_location={
        "type": "approximate",
        "country": "CA",
        "city": "Toronto",
        "region": "Ontario",
    }
)

agent = Agent(
    name="Web Search Agent",
    instructions="You are an AI Agent which can access the web to answer queries in one sentence.",
    tools=[web_search_tool],
)

result = Runner.run_sync(agent, "What are top 3 italian restaurants?")

print(result.final_output)
