# Solution Design Flow

## 1. Business Goal
The application helps data engineers detect data quality issues quickly and generate understandable remediation reports for downstream analytics.

## 2. User Journey
1. A user opens the web app.
2. The user uploads a CSV file or uses the built-in synthetic dataset.
3. The system profiles the data.
4. The system detects issues such as missing values, duplicates, and inconsistent values.
5. The system displays a summary, issue list, and report.
6. The user uses the report to fix the data pipeline.

## 3. Solution Flow
```text
User -> Web UI -> Backend API -> Data Profiling Engine -> Issue Detection -> Report Generation -> UI Display
```

## 4. Functional Flow
- Input: CSV file or sample dataset
- Processing: Data cleaning, validation, profiling
- Detection: Missing values, duplicates, inconsistent values
- Output: Summary metrics, issue cards, remediation report

## 5. Technical Flow
- Frontend sends data to the backend API.
- Backend reads CSV into a Pandas DataFrame.
- Pandas performs rule-based profiling.
- Findings are converted into structured issue objects.
- The report is returned to the UI for display.

## 6. System Design Highlights
- Simple, lightweight, and easy to run locally
- Suitable for demo and prototype use
- Modular enough to extend to database sources later
- Can be containerized using Docker

## 7. Future Design Expansion
- Add database connectors
- Add scheduling and pipeline monitoring
- Add AI-generated root cause explanations
- Add alerting and notification features
