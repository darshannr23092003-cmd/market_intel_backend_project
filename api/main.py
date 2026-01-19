from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import run_full_pipeline
import uuid


print(">>> MAIN API LOADED <<<")

app = FastAPI(title="Market Intelligence API")

# Simple in-memory store (good enough for assignment)
REPORT_STORE = {}


class AnalyzeRequest(BaseModel):
    industry: str
    from_date: str
    to_date: str
    focus: str | None = None


class ChatRequest(BaseModel):
    report_id: str
    question: str


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    report = run_full_pipeline(
        industry=req.industry,
        start_date=req.from_date,
        end_date=req.to_date,
        focus=req.focus
    )

    report_id = str(uuid.uuid4())
    REPORT_STORE[report_id] = report

    return {
        "report_id": report_id,
        "report": report
    }


@app.post("/chat")
def chat(req: ChatRequest):
    report = REPORT_STORE.get(req.report_id)

    if not report:
        return {"error": "Report not found"}

    # Simple deterministic Q&A over report
    question = req.question.lower()

    if "risk" in question:
        return {
            "answer": ", ".join(report.get("risks", [])),
            "citations": report.get("sources", [])
        }

    if "opportunit" in question:
        return {
            "answer": ", ".join(report.get("opportunities", [])),
            "citations": report.get("sources", [])
        }

    return {
        "answer": report.get("summary", "No answer available."),
        "citations": report.get("sources", [])
    }
