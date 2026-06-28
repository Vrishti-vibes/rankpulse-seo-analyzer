# RankPulse SEO Analyzer

RankPulse SEO Analyzer is a Woorank-like SEO analysis project built using Python FastAPI and a custom frontend dashboard. It analyzes a website URL and generates a structured SEO report covering on-page SEO, technical SEO, metadata, content quality, indexability, performance basics, accessibility signals, and improvement suggestions.

The project uses custom-built logic, manual crawling, and open-source Python libraries. It does not use Woorank APIs, paid SEO APIs, or direct SEO scoring services.

## Live Links

- Live Frontend URL: Add your Vercel URL here
- Backend API URL: https://rankpulse-seo-backend.onrender.com
- GitHub Repository: https://github.com/Vrishti-vibes/rankpulse-seo-analyzer

## Features

### Website Analysis Engine

- Website URL crawling
- SEO score out of 100
- Technical SEO score
- On-page SEO score
- Performance score
- Content quality score
- Metadata score
- Smart fix suggestions
- Downloadable JSON report

### SEO Audit Checks

- Meta title analysis
- Meta description analysis
- H1-H6 heading analysis
- Heading hierarchy validation
- Image alt tag analysis
- URL structure checks
- Internal links analysis
- External links analysis
- Broken internal link sampling

### Technical SEO Checks

- HTTPS / SSL check
- robots.txt detection
- sitemap.xml detection
- Mobile viewport detection
- Canonical tag detection
- Redirect count detection
- Indexability checks
- Meta robots noindex/nofollow detection
- Structured data detection
- Charset detection
- HTML language attribute detection
- Favicon detection

### Performance Analysis

- HTTP status code check
- Response time measurement
- Page size calculation
- Compression header detection
- Cache header detection
- Redirect count analysis

### Content Analysis

- Word count
- Keyword presence analysis
- Keyword density calculation
- Readability estimate
- Heading structure validation
- Internal linking check

### Trust and Metadata Checks

- Open Graph metadata
- Twitter metadata
- Social profile link detection
- Email presence detection
- Phone presence detection
- JSON-LD / Schema.org detection

## Tech Stack

### Backend

- Python
- FastAPI
- Requests
- BeautifulSoup
- Regular Expressions
- Uvicorn

### Frontend

- HTML5
- CSS3
- JavaScript

### Deployment

- Render for backend
- Vercel for frontend
- GitHub for version control

## API Endpoints

### POST /api/analyze

Accepts a website URL and starts SEO analysis.

### GET /api/results/{job_id}

Returns the SEO report for the analyzed website.

## How to Run Locally

### Backend

```bash
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload