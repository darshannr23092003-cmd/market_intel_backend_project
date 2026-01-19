import requests
import json

MCP_IMPACT_URL = "http://127.0.0.1:8001/tool/impact_score"


def impact_agent(event: str, context: dict, url: str):
    print("\n==============================")
    print(" IMPACT AGENT STARTED")
    print("==============================\n")

    print("[Impact] Calling MCP tool: impact_score")

    try:
        payload = {
            "item": {
                "title": event,
                "url": url
            },
            "context": context
        }

        response = requests.post(
            MCP_IMPACT_URL,
            json={"args": payload},
            timeout=10
        )

        data = response.json()

        if "result" not in data:
            raise ValueError("Invalid MCP response")

        print("\n[Impact] Received impact from MCP:")
        print(json.dumps(data["result"], indent=2))

        return data["result"]

    except Exception as e:
        print(f"\n[Impact] MCP failed: {e}")
        print("[Impact] Using safe fallback")

        # Safe fallback so pipeline never crashes
        fallback = {
            "event": event,
            "impact_level": "Low",
            "score": 40,
            "why": ["Unable to compute impact"],
            "actions": ["Monitor situation"],
            "url": url
        }

        print(json.dumps(fallback, indent=2))
        return fallback


# Local test
if __name__ == "__main__":
    sample_event = "RBI introduces stricter compliance guidelines for NBFCs"
    sample_context = {
        "competitors": ["Bajaj Finance", "Paytm Payments Bank"],
        "themes": ["regulation", "compliance"],
        "pricing_models": []
    }
    sample_url = "https://example.com/news1"

    impact_agent(sample_event, sample_context, sample_url)
