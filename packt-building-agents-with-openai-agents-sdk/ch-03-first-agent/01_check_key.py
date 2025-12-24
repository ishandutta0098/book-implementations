import os

from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

agent = Agent(
    name="Echo Agent",
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    model="openai/gpt-4o",
)

result = Runner.run_sync(agent, "What is the capital of France?")
print("\n=== Agent Response ===")
print(result.final_output)
