# AI Data Quality Assistant

A lightweight prototype that helps data engineers detect, explain, and report data quality issues from CSV samples.

## What it does
- Uploads a CSV file or uses built-in synthetic data
- Detects missing values, duplicate rows, and inconsistent placeholder values
- Produces a contextual remediation report and a compact issue list
- Runs as a local web app or Docker container

## Tech stack
- Python + FastAPI
- Pandas for profiling
- Jinja2 + vanilla JavaScript for the UI

## Run locally
```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Then open http://127.0.0.1:8000/.

## Run with Docker
```bash
docker build -t ai-data-quality-assistant .
docker run -p 8000:8000 ai-data-quality-assistant
```
