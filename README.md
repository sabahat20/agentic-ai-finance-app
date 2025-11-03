# Agentic AI Financial Assistant

This is a lightweight FastAPI web app that uses Groq’s Llama 3.1 model via the Phidata framework to answer finance-related queries.

## Features
- FastAPI backend
- DuckDuckGo + YFinance tools
- Interactive HTML chat interface
- Agentic reasoning with Groq model

## Run locally
```bash
pip install -r requirements.txt
uvicorn app_fastapi:app --reload
