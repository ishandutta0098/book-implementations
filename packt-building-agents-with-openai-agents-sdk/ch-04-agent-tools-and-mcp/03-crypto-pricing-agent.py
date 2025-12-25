import os
from typing import List

import requests
from agents import Agent, ModelSettings, Runner, StopAtTools, function_tool
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


class Crypto(BaseModel):
    coin_ids: List[str]


@function_tool
def get_crypto_prices(crypto: Crypto) -> str:
    """
    Get the price of bitcoin
    """
    # The following line takes the list of cryptocurrency IDs from the Crypto object
    # and combines them into a single comma-separated string, as expected by the CoinGecko API.
    ids = ",".join(crypto.coin_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data


crypto_agent = Agent(
    name="Crypto Agent",
    instructions="You are a crypto assistant. Use tools to get real-time data. \
        When getting crypto prices call the tool only once to fetch all the prices",
    tools=[get_crypto_prices],
    model_settings=ModelSettings(tool_choice="required"),
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_crypto_prices"]),
)

result = Runner.run_sync(
    crypto_agent, "What is the current price of Bitcoin and Ethereum?"
)

print(result.final_output)
