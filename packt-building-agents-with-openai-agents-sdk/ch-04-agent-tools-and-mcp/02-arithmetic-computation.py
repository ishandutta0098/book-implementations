import os

from agents import Agent, ModelSettings, Runner, StopAtTools, function_tool
from dotenv import load_dotenv

load_dotenv()

# Disable tracing BEFORE importing agents
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


@function_tool
def calculate_mortgage(
    principal_amount: float, annualized_rate: float, number_of_years: int
) -> float:
    monthly_rate = (annualized_rate / 100) / 12
    months = number_of_years * 12
    payment = principal_amount * (monthly_rate) / (1 - (1 + monthly_rate) ** -months)
    print(payment)
    return f"Rs. {payment:, .2f}"


mortgage_agent = Agent(
    name="Mortgage Agent",
    instructions="You are an AI Agent which calculates the mortgage",
    tools=[calculate_mortgage],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["calculate_mortgage"]),
    model_settings=ModelSettings(tool_choice="required"),
)

result = Runner.run_sync(
    mortgage_agent,
    "Calculate my monthly payments if I borrow Rs 10000 at 6% interest rate for 1 year",
)

print(result.final_output)
