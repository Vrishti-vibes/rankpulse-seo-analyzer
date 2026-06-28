from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from analyzer import analyze_website

app = FastAPI(title="RankPulse SEO Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

results_store = {}


class AnalyzeRequest(BaseModel):
    url: str


@app.get("/")
def home():
    return {
        "project": "RankPulse SEO Analyzer",
        "status": "running",
        "developer": "Kumari Vrishti"
    }


def run_analysis(job_id: str, url: str):
    results_store[job_id] = {
        "status": "processing",
        "message": "SEO analysis is in progress"
    }

    result = analyze_website(url)
    results_store[job_id] = result


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())

    results_store[job_id] = {
        "status": "queued",
        "message": "Analysis request received"
    }

    background_tasks.add_task(run_analysis, job_id, request.url)

    return {
        "job_id": job_id,
        "status": "queued",
        "message": "Analysis started. Use GET /api/results/{job_id} to fetch results."
    }


@app.get("/api/results/{job_id}")
def get_results(job_id: str):
    if job_id not in results_store:
        return {
            "status": "not_found",
            "message": "Invalid job ID"
        }

    return results_store[job_id]