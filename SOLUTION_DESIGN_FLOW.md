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

## 3. End-to-End Solution Flow
```text
User -> Web UI -> Backend API -> Data Profiling Engine -> Issue Detection -> Report Generation -> UI Display
```

## 4. Functional Design Flow
- Input: CSV file or sample dataset
- Processing: reading, cleaning, validation, profiling
- Detection: missing values, duplicates, inconsistent values
- Output: summary metrics, issue cards, remediation report, data preview

## 5. Technical Design Flow
- The frontend sends the CSV to the backend through a form submission.
- The backend reads the file into a Pandas DataFrame.
- Pandas performs rule-based profiling across each column.
- Findings are converted into structured issue objects.
- The backend returns the report to the UI for display.

## 6. Architecture Summary
- Simple three-layer architecture
- lightweight and demo-friendly
- easy to extend to database sources later
- ready for Docker packaging and GitHub sharing

## 7. Design Considerations
- prioritize clear issue explanations
- keep the prototype lightweight
- ensure a smooth user experience for non-technical users
- allow later expansion to richer AI-driven reasoning

## 8. Future Design Expansion
- add database connectors
- add pipeline monitoring and scheduling
- add AI-generated root cause analysis
- add alerts and notifications
