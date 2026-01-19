Market Intelligence Multi-Agent System (MCP Architecture)
A modular multi-agent system that generates structured market intelligence reports using local open-source LLMs (Ollama)[used tinyllama in this project] and MCP Tool Server architecture.
This project implements a full pipeline of autonomous agents — Collector, Extractor, Impact, and Writer — that interact only via MCP tools, following a real agent-tool architecture.


Architecture Overview:

market_intel/
│
├── api/                  # FastAPI application (public interface)
│   └── main.py
│
├── agents/               # Autonomous agents
│   ├── collector.py
│   ├── extractor.py
│   ├── impact.py
│   └── writer.py
│
├── mcp_server/           # MCP Tool Server (tool execution layer)
│   ├── server.py
│   └── tools.py
│
├── pipeline.py           # Orchestrates full agent workflow

Features

Multi-agent pipeline:
Collector → generates search queries
Extractor → extracts competitors & themes
Impact → generates impact scores
Writer → produces final market report
MCP Tool Server abstraction layer
Fully local inference using Ollama (no paid APIs)
Deterministic fallbacks (project never crashes)
JSON-only structured outputs

Requirements

Python 3.10+
Ollama installed locally
👉 https://ollama.com/download

A lightweight model pulled:
ollama pull tinyllama

Installation

git clone https://github.com/your-username/market_intel.git
cd market_intel

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install fastapi uvicorn httpx requests

Running the System
Terminal 1 — Start MCP Tool Server

uvicorn mcp_server.server:app --port 8001 --reload

Verify:
curl http://127.0.0.1:8001/health

Terminal 2 — Start Main API Server
uvicorn api.main:app --port 8000 --reload

Open Swagger UI:
http://127.0.0.1:8000/docs

Models Used

All inference is performed locally using:
tinyllama (Ollama)
No OpenAI, no closed-source APIs.
Fully compliant with open-source requirement.




