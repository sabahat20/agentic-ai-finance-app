# app.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

model = Groq(id="llama-3.1-8b-instant", api_key=GROQ_KEY)

agent = Agent(
    name="Finance+Search Agent",
    model=model,
    tools=[DuckDuckGo(), YFinanceTools(stock_price=True, company_news=True)],
    instructions=["Always include sources"],
    markdown=True,
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def read_root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Financial AI Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
            .input { display: flex; }
            input { flex: 1; padding: 10px; }
            button { padding: 10px 20px; }
            .user { text-align: right; margin: 10px 0; }
            .bot { text-align: left; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>Financial AI Assistant</h1>
        <div id="chat" class="chat"></div>
        <div class="input">
            <input type="text" id="message" placeholder="Ask about stocks or news...">
            <button onclick="sendMessage()">Send</button>
        </div>
        <script>
            async function sendMessage() {
                const message = document.getElementById('message').value;
                if (!message) return;
                
                const chat = document.getElementById('chat');
                chat.innerHTML += `<div class="user"><strong>You:</strong> ${message}</div>`;
                document.getElementById('message').value = '';
                
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                
                const data = await response.json();
                chat.innerHTML += `<div class="bot"><strong>AI:</strong> ${data.reply}</div>`;
                chat.scrollTop = chat.scrollHeight;
            }
            
            document.getElementById('message').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """)

@app.post("/chat")
async def chat(req: ChatRequest):
    resp = agent.run(req.message)
    return {"reply": str(resp.content)}
