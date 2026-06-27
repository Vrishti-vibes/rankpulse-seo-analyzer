# RankPulse SEO Analyzer

RankPulse SEO Analyzer is a lightweight Woorank-like SEO audit tool built using Python FastAPI and HTML/CSS/JavaScript. It analyzes a website URL and generates an SEO report covering on-page SEO, technical SEO, metadata, content quality, accessibility signals, and improvement suggestions.

## Features

- Website URL analysis
- SEO score out of 100
- On-page SEO checks
- Technical SEO checks
- Metadata analysis
- Content quality analysis
- Image alt text checking
- Internal and external link analysis
- Smart fix suggestions
- Responsive frontend dashboard

## Tech Stack

### Backend
- Python
- FastAPI
- BeautifulSoup
- Requests

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

## API Endpoints

### POST /api/analyze

Accepts a website URL and starts analysis.

### GET /api/results/{job_id}

Returns the SEO report for the analyzed website.

## How to Run Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload