import requests
import json

MCP_REPORT_URL = "http://127.0.0.1:8001/tool/generate_market_report"


def report_writer_agent(industry: str, competitors: list, impact_items: list, sources: list):
    print("\n==============================")
    print(" REPORT WRITER AGENT STARTED")
    print("==============================\n")

    print("[Writer] Calling MCP tool: generate_market_report")

    payload = {
        "competitors": competitors,
        "impact_items": impact_items,
        "sources": sources
    }

    try:
        response = requests.post(
            MCP_REPORT_URL,
            json={"args": {"data": payload}},
            timeout=10
        )

        data = response.json()

        if "result" not in data:
            raise ValueError("Invalid MCP response")

        print("\n[Writer] Received report from MCP:")
        print(json.dumps(data["result"], indent=2))

        return data["result"]

    except Exception as e:
        print(f"\n[Writer] MCP failed: {e}")
        print("[Writer] Using deterministic fallback")

        # Fallback (guarantees schema correctness)
        report = {
            "summary": f"The {industry} sector is experiencing notable developments driven by regulatory changes and competitive pressure. Organizations must adapt operations and strategy accordingly.",

            "drivers": [
                "Regulatory tightening by financial authorities",
                "Increased competition from fintech players",
                "Digital adoption across lending workflows",
                "Risk management modernization",
                "Customer demand for faster credit"
            ],

            "competitors": competitors,

            "impact_radar": impact_items,

            "opportunities": [
                "Automation of credit assessment workflows",
                "Partnerships with fintech platforms",
                "Expansion into underserved customer segments",
                "Launch of digital-first loan products",
                "Data-driven personalization of offerings"
            ],

            "risks": [
                "Rising compliance and audit requirements",
                "Margin pressure due to competition",
                "Operational risk from legacy systems",
                "Cybersecurity vulnerabilities",
                "Macroeconomic credit slowdown"
            ],

            "90_day_plan": {
                "0_30": [
                    "Review compliance posture",
                    "Identify high-risk operational gaps"
                ],
                "30_60": [
                    "Define technology modernization roadmap",
                    "Explore fintech partnerships"
                ],
                "60_90": [
                    "Pilot new digital initiatives",
                    "Scale successful process improvements"
                ]
            },

            "sources": sources
        }

        print(json.dumps(report, indent=2))
        return report


# Local test
if __name__ == "__main__":
    sample_competitors = ["Bajaj Finance", "Paytm Payments Bank"]
    sample_sources = ["https://example.com/news1", "https://example.com/news2"]

    sample_impact_items = [
        {
            "event": "RBI introduces stricter compliance guidelines for NBFCs",
            "impact_level": "High",
            "score": 77,
            "why": ["Higher compliance cost", "Process changes required"],
            "actions": ["Audit workflows", "Update policies"],
            "url": "https://example.com/news1"
        }
    ]

    report_writer_agent(
        industry="NBFC",
        competitors=sample_competitors,
        impact_items=sample_impact_items,
        sources=sample_sources
    )
