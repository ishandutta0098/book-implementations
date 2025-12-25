import os

from dotenv import load_dotenv

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

from agents import Agent, CodeInterpreterTool, Runner
from agents.tool import CodeInterpreter

tool_config = CodeInterpreter(type="code_interpreter", container={"type": "auto"})

code_tool = CodeInterpreterTool(tool_config=tool_config)

agent = Agent(
    name="Code Interpreter Agent",
    instructions="You are an AI Agent which can write and execute python code to answer questions.",
    tools=[code_tool],
)

result = Runner.run_sync(
    agent,
    "What is the simple interest if principle=100000, rate=10% p.a. and time=2 years ?",
)

print(result.final_output)
