from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    raise RuntimeError("GROQ_API_KEY missing from .env file")

# Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the model",
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_KEY),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

# Financial Agent
finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_KEY),
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

# Multi-Agent Team - FIXED: Added model
multi_ai_agents = Agent(
    team=[web_search_agent, finance_agent],
    model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_KEY),  # ✅ ADDED THIS
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)


# if __name__ == "__main__":
#     multi_ai_agents.print_response("Summarise analyst recommendation and share the latest news for NVDA",stream=True)

if __name__ == "__main__":
    resp = multi_ai_agents.run(
        "Summarise analyst recommendation and share the latest news for NVDA"
    )
    print(resp)

# ✅ ADD THE QUery Section
# if __name__ == "__main__":
#     print("Starting Financial Research Agent...")
    
#     # Test query
#     query = "Give me Apple's latest stock price and 3 recent news headlines with sources."
    
#     print(f"Query: {query}")
#     print("⏳ Processing...\n")
    
#     try:
#         # Use the multi-agent team
#         multi_ai_agents.print_response(query, stream=True)
#     except Exception as e:
#         print(f" Error with multi-agent: {e}")
#         print("Trying single agent approach...")
        
#         # Fallback to single agent
#         single_agent = Agent(
#             model=Groq(id="llama-3.1-8b-instant", api_key=GROQ_KEY),
#             tools=[YFinanceTools(stock_price=True, company_news=True)],
#             markdown=True,
#         )
#         single_agent.print_response(query, stream=True)



















# from phi.agent import Agent
# from phi.model.groq import Groq
# from phi.tools.yfinance import YFinanceTools
# from phi.tools.duckduckgo import DuckDuckGo
# from dotenv import load_dotenv
# import openai
# import os

# # Load environment variables
# load_dotenv()
# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# # Web Search Agent
# web_search_agent = Agent(
#     name="Web Search Agent",
#     role="Search the web for the model",
#     model=Groq(id="llama-3.1-8b-instant"),
#     tools=[DuckDuckGo()],
#     instructions=["Always include sources"],
#     show_tool_calls=True,
#     markdown=True,
# )

# # Financial Agent
# finance_agent = Agent(
#     name="Finance AI Agent",
#     model=Groq(id="llama-3.1-8b-instant"),
#     tools=[YFinanceTools(
#         stock_price=True,
#         analyst_recommendations=True,
#         stock_fundamentals=True,
#         company_news=True
#     )],
#     instructions=["Use tables to display financial data clearly."],
#     show_tool_calls=True,
#     markdown=True,
# )

# # Multi-Agent Team
# multi_ai_agents = Agent(
#     team=[web_search_agent, finance_agent],
#     instructions=["Always include sources", "Use tables to display data"],
#     show_tool_calls=True,
#     markdown=True,
# )
