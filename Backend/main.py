from fastapi import FastAPI
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

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    job_id = str(uuid.uuid4())
    result = analyze_website(request.url)
    results_store[job_id] = result

    return {
        "job_id": job_id,
        "status": "completed"
    }

@app.get("/api/results/{job_id}")
def get_results(job_id: str):
    if job_id not in results_store:
        return {
            "status": "not_found",
            "message": "Invalid job ID"
        }

    return results_store[job_id]