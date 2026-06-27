# AI Data Quality Assistant

## 1. Project Overview
The AI Data Quality Assistant is a web-based prototype that helps data engineers detect and report common data quality issues in datasets. It uses a simple rules-based analysis approach to identify:

- Missing values
- Duplicate rows
- Inconsistent placeholder values such as Unknown, N/A, NULL, and TBD

The application provides an interactive interface where users can upload a CSV file or use built-in synthetic sample data to generate a quality report and remediation suggestions.

---

## 2. Problem Statement
Data pipelines often contain quality issues that are hard to spot manually. These issues can impact analytics, reporting, and business decisions. This application addresses the problem by giving users a fast way to:

- Profile incoming data
- Detect quality problems automatically
- Generate clear reports
- Understand what action to take next

---

## 3. Solution Summary
The solution is built as a lightweight web application with:

- A Python backend using FastAPI
- A simple frontend using HTML, CSS, and JavaScript
- Pandas for data analysis
- A sample CSV dataset for demonstration
- Docker support for containerized deployment

---

## 4. Technology Stack

### Backend
- Python 3.13
- FastAPI
- Pandas
- Uvicorn
- Python multipart

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Docker
- Git/GitHub

---

## 5. Application Architecture
The application is organized into three main parts:

1. Frontend UI
   - Users enter a dataset name and upload a CSV file.
   - The UI displays detected issues, a report, and a preview of the data.

2. Backend API
   - The server receives uploaded data.
   - It analyzes the dataset and generates results.
   - It returns structured results to the frontend.

3. Data Analysis Engine
   - Pandas checks for missing values, duplicate rows, and inconsistent values.
   - Results are converted into a human-readable report.

---

## 6. File Structure

- app.py: Main FastAPI application and analysis logic
- templates/index.html: Web page structure
- static/style.css: UI styling
- static/app.js: Frontend behavior and API calls
- sample_data.csv: Built-in synthetic dataset
- requirements.txt: Python dependencies
- Dockerfile: Container configuration
- README.md: Quick start guide

---

## 7. How the Application Works

### Step 1: User opens the web app
The user visits the local URL in a browser.

### Step 2: User uploads a CSV file or uses sample data
The app accepts a CSV file. If no file is uploaded, it uses the built-in sample dataset.

### Step 3: Backend processes the data
The backend reads the CSV file into a Pandas DataFrame.

### Step 4: Analysis is performed
The system checks for:

- Missing values in each column
- Duplicate rows
- Placeholder or inconsistent values like Unknown or N/A

### Step 5: Results are shown in the UI
The UI displays:

- Summary counts
- Issue cards
- A generated report
- A sample preview table

---

## 8. Example of Detected Issues
Example issues the app can identify:

- Missing email values in a customer dataset
- Duplicate customer rows
- Region values stored as Unknown or N/A

These issues are shown with severity levels and recommendations.

---

## 9. Setup Instructions

### Prerequisites
Make sure Python is installed on the machine.

### Install dependencies
Run the following command:

```bash
pip install -r requirements.txt
```

### Start the application
Run:

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

### Open the app
Open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

## 10. Docker Instructions
To run the application in a container:

### Build the Docker image

```bash
docker build -t ai-data-quality-assistant .
```

### Run the container

```bash
docker run -p 8000:8000 ai-data-quality-assistant
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 11. GitHub and Project Sharing
The project has been initialized as a Git repository and can be pushed to GitHub for sharing.

Example commands:

```bash
git init
git add .
git commit -m "Initial prototype"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```

---

## 12. Future Enhancements
Possible next improvements include:

- Integration with real databases
- Connection to cloud storage or data warehouses
- AI-based root cause analysis using LLMs
- Integration with pipeline orchestration tools
- Dashboard-style reporting
- Email or Slack alerts for recurring issues

---

## 13. Conclusion
This application demonstrates how AI-assisted data quality monitoring can help teams quickly identify and understand data issues. It is a practical prototype for improving trust in data and accelerating remediation workflows.
