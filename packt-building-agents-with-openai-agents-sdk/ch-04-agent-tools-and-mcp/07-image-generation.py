import os

from dotenv import load_dotenv

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

from agents import Agent, ImageGenerationTool, Runner
from agents.tool import ImageGeneration

tool_config: ImageGeneration = {"type": "image_generation"}

image_tool = ImageGenerationTool(tool_config=tool_config)

agent = Agent(
    name="Image Generator Agent",
    instructions="You are an AI Agent that can generate images.",
    tools=[image_tool],
)

result = Runner.run_sync(agent, "Generate the image of a racing car.")

print(result.final_output)
