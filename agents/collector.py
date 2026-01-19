import httpx
import json
import re
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "tinyllama"

MCP_URL = "http://127.0.0.1:8001/tool/search_web"


def call_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            },
            timeout=60
        )
        return response.json().get("response", "")
    except Exception as e:
        print(f"[Collector] Ollama error: {e}")
        return ""


def call_mcp_search(query: str):
    print(f"[Collector] calling tool: search_web('{query}')")

    response = httpx.post(
        MCP_URL,
        json={"args": {"query": query}},
        timeout=10
    )

    return response.json().get("result", [])


def collector_agent(industry: str, start_date: str, end_date: str, focus: str | None = None):
    print("\n==============================")
    print(" COLLECTOR AGENT STARTED")
    print("==============================\n")

    system_prompt = f"""
You are a market research assistant.

Your task:
Generate exactly 3 high-quality web search queries.

Context:
Industry: {industry}
Date range: {start_date} to {end_date}
Focus: {focus or "general"}

Requirements:
- Return ONLY a JSON array
- No explanation
- No markdown
- No extra text
- Each query must be realistic and specific

Example format:
[
  "NBFC regulatory updates India January 2026",
  "RBI circular NBFC compliance changes",
  "NBFC fintech competition trends 2026"
]

Now generate the JSON array.
"""

    print("[Collector] Sending prompt to LLM...\n")
    raw_output = call_ollama(system_prompt)

    print("[Collector] Raw LLM output:")
    print(raw_output)
    print()

    # Try to extract JSON safely
    queries = []
    try:
        match = re.search(r"\[[\s\S]*?\]", raw_output)
        if match:
            queries = json.loads(match.group())
            if not isinstance(queries, list):
                raise ValueError("Not a list")
    except Exception:
        print("[Collector] Failed to parse LLM output, using fallback queries.")
        queries = [
            f"{industry} regulatory updates India",
            f"{industry} RBI circular compliance changes",
            f"{industry} market trends fintech competition"
        ]

    print("[Collector] Final queries:", queries)

    print("\n[Collector] Calling MCP tools...\n")

    all_results = []

    for q in queries:
        print(f"> Searching for: {q}")
        results = call_mcp_search(q)
        all_results.extend(results)

    print("\n[Collector] Final collected sources:")
    print(json.dumps(all_results, indent=2))

    return all_results
