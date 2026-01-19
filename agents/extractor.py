import requests
import json

MCP_EXTRACT_URL = "http://127.0.0.1:8001/tool/extract_entities"


def extractor_agent(text: str):
    print("\n==============================")
    print(" EXTRACTOR AGENT STARTED")
    print("==============================\n")

    print("[Extractor] Calling MCP tool: extract_entities")

    try:
        response = requests.post(
            MCP_EXTRACT_URL,
            json={"args": {"text": text}},
            timeout=10
        )

        data = response.json()

        if "result" not in data:
            raise ValueError("Invalid MCP response")

        print("\n[Extractor] Received structured data from MCP:")
        print(json.dumps(data["result"], indent=2))

        return data["result"]

    except Exception as e:
        print(f"\n[Extractor] MCP failed: {e}")
        print("[Extractor] Using safe fallback")

        # Fallback so pipeline never crashes
        fallback = {
            "competitors": [],
            "themes": [],
            "pricing_models": []
        }

        print(json.dumps(fallback, indent=2))
        return fallback


if __name__ == "__main__":
    sample_text = """
    RBI introduced new compliance guidelines affecting major NBFCs such as Bajaj Finance
    and Paytm Payments Bank. These regulations are expected to increase operational costs.
    """

    extractor_agent(sample_text)
