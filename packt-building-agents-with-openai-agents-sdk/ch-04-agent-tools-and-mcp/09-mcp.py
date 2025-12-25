import os

from dotenv import load_dotenv

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

from agents import Agent, HostedMCPTool, Runner
from agents.tool import Mcp

tool_config = Mcp(
    type="mcp",
    server_label="CryptocurrencyPriceFetcher",
    server_url="https://mcp.api.coingecko.com/sse",
    require_approval="never",
)

mcp_tool = HostedMCPTool(tool_config=tool_config)

agent = Agent(
    name="Crypto Price Agent",
    instructions="You are an AI Agent that can fetch crypto prices using the tool.",
    tools=[mcp_tool],
)

result = Runner.run_sync(agent, "What is the price of Bitcoin?")

print(result.final_output)
