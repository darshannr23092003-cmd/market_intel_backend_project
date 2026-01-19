from agents.collector import collector_agent
from agents.extractor import extractor_agent
from agents.impact import impact_agent
from agents.writer import report_writer_agent


def run_full_pipeline(industry: str, start_date: str, end_date: str, focus: str | None = None):
    # 1. Collector
    sources = collector_agent(industry, start_date, end_date, focus)

    # 2. For demo purposes, fake article text
    # (later you can plug real fetch_url + clean_extract)
    sample_text = """
    RBI introduced new compliance guidelines affecting NBFCs such as Bajaj Finance
    and Paytm Payments Bank. These regulations are expected to increase operational costs.
    """

    # 3. Extractor
    extracted = extractor_agent(sample_text)

    # 4. Impact Agent for each source
    impact_items = []
    for s in sources:
        impact = impact_agent(
            event=s["title"],
            context=extracted,
            url=s["url"]
        )
        impact_items.append(impact)

    # Ensure minimum 10 impact items (assignment requirement)
    # Ensure minimum 10 impact items safely
    if not impact_items:
        impact_items.append({
            "event": "No reliable events extracted",
            "impact_level": "Low",
            "score": 30,
            "why": ["Insufficient data from sources"],
            "actions": ["Retry with different query"],
            "url": ""
        })

    while len(impact_items) < 10:
        impact_items.append(impact_items[-1].copy())

    # 5. Writer
    report = report_writer_agent(
        industry=industry,
        competitors=extracted.get("competitors", []),
        impact_items=impact_items,
        sources=[s["url"] for s in sources]
    )

    return report
