import openai
from phi.agent import Agent
import phi.api
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from phi.model.groq import Groq

import os
import phi
from phi.playground import Playground,serve_playground_app

#load_dotenv()
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY missing — add it to your .env file")



phi.api=os.getenv("Phi_API_key")

# Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the model",
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

# Financial Agent
finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_API_KEY),
    tools=[YFinanceTools(
        stock_price=True,
        analyst_recommendations=True,
        stock_fundamentals=True,
        company_news=True
    )],
    instructions=["Use tables to display financial data clearly."],
    show_tool_calls=True,
    markdown=True,
)

app=Playground(agents=[finance_agent,web_search_agent]).get_app()
if __name__=="__main__":
    serve_playground_app("playground:app",reload=True)

