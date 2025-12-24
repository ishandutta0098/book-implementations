import os

from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


# Define the Tool
@function_tool
def get_order_status(order_number: int) -> str:
    if order_number in (100, 101):
        return "Delivered"
    elif order_number in (200, 201):
        return "Delayed"
    elif order_number in (300, 301):
        return "Cancelled"
    else:
        return "Invalid order_number"


# Define the Agents
customer_retention_agent = Agent(
    name="Customer Retention Agent",
    instructions="You are an AI Agent that responds to customers that want to close their account and retain their business. \
        You are allowed to provide upto 10% discounts if it helps. Additionally be curteous, \
        respectful and sincere in your conversation.",
    model="openai/gpt-4.1",
)

customer_service_agent = Agent(
    name="Customer Service Agent",
    instructions="You are an AI Agent that responds to customer queries for a local paper company.",
    model="openai/gpt-4o",
    tools=[get_order_status],
    handoffs=[customer_retention_agent],
)


result = Runner.run_sync(customer_service_agent, "I want to close my account.")

print(result.final_output)
