import io
import os
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="AI Data Quality Assistant", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
SAMPLE_DATA_PATH = "sample_data.csv"


def load_dataframe(upload_file: Optional[UploadFile] = None) -> pd.DataFrame:
    if upload_file is not None and getattr(upload_file, "filename", None):
        content = upload_file.file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        try:
            return pd.read_csv(io.BytesIO(content))
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Unable to parse CSV file: {exc}") from exc

    if os.path.exists(SAMPLE_DATA_PATH):
        return pd.read_csv(SAMPLE_DATA_PATH)

    raise HTTPException(status_code=404, detail="No data source available")


def build_issue_details(column: str, issue_type: str, count: int, percent: float, severity: str, description: str, recommendation: str) -> Dict[str, Any]:
    return {
        "column": column,
        "issue_type": issue_type,
        "count": count,
        "percent": round(percent, 2),
        "severity": severity,
        "severity_score": 25 if severity == "high" else 15 if severity == "medium" else 8,
        "description": description,
        "recommendation": recommendation,
    }


def analyze_dataframe(df: pd.DataFrame, source_name: str) -> Dict[str, Any]:
    rows = len(df)
    cols = list(df.columns)
    issues: List[Dict[str, Any]] = []

    for column in cols:
        series = df[column]
        missing_count = int(series.isna().sum())
        if missing_count > 0:
            missing_pct = round((missing_count / rows) * 100, 2) if rows else 0.0
            severity = "high" if missing_pct >= 20 else "medium" if missing_pct >= 5 else "low"
            issues.append(
                build_issue_details(
                    column=column,
                    issue_type="missing_values",
                    count=missing_count,
                    percent=missing_pct,
                    severity=severity,
                    description=f"{missing_count} missing values were found in {column}.",
                    recommendation=f"Standardize the {column} field and backfill or validate records before downstream analysis.",
                )
            )

    duplicate_count = int(df.duplicated().sum())
    if duplicate_count > 0:
        issues.append(
            build_issue_details(
                column="dataset",
                issue_type="duplicates",
                count=duplicate_count,
                percent=round((duplicate_count / rows) * 100, 2) if rows else 0.0,
                severity="high" if duplicate_count >= 2 else "medium",
                description=f"{duplicate_count} duplicate row(s) were detected in the dataset.",
                recommendation="Deduplicate records using a business key, then re-run the pipeline to avoid skewed metrics.",
            )
        )

    for column in cols:
        if pd.api.types.is_object_dtype(df[column]):
            normalized = df[column].fillna("").astype(str).str.strip().str.upper()
            sentinel_values = {"UNKNOWN", "N/A", "NULL", "NONE", "", "TBD"}
            inconsistent_count = int(normalized.isin(sentinel_values).sum())
            if inconsistent_count > 0:
                severity = "high" if inconsistent_count >= 4 else "medium"
                issues.append(
                    build_issue_details(
                        column=column,
                        issue_type="inconsistencies",
                        count=inconsistent_count,
                        percent=round((inconsistent_count / rows) * 100, 2) if rows else 0.0,
                        severity=severity,
                        description=f"The {column} column contains placeholder or low-quality values that may distort reporting.",
                        recommendation=f"Create a controlled vocabulary or validation rule for {column} and quarantine invalid values.",
                    )
                )

    quality_score = max(0, 100 - min(70, sum(issue["severity_score"] for issue in issues)))
    preview_rows = df.head(8).fillna("").to_dict(orient="records")

    report = generate_report(source_name, rows, len(cols), issues, quality_score)

    return {
        "source_name": source_name,
        "rows": rows,
        "columns": cols,
        "quality_score": quality_score,
        "issue_count": len(issues),
        "issues": issues,
        "preview_rows": preview_rows,
        "report": report,
    }


def generate_report(source_name: str, row_count: int, column_count: int, issues: List[Dict[str, Any]], quality_score: int) -> str:
    lines = [
        f"Data quality report for {source_name}",
        f"Rows scanned: {row_count}",
        f"Columns reviewed: {column_count}",
        f"Quality score: {quality_score}/100",
        "",
        "Executive summary:",
    ]

    if not issues:
        lines.append("No material data quality issues were detected. Continue monitoring the pipeline for drift.")
        return "\n".join(lines)

    lines.append(
        f"{len(issues)} issue area(s) were identified. The most urgent items should be remediated before downstream reporting.")
    lines.append("")
    lines.append("Priority findings:")

    for issue in issues[:4]:
        lines.append(
            f"- {issue['issue_type'].replace('_', ' ').title()} in {issue['column']}: {issue['description']}"
        )
        lines.append(f"  Recommended action: {issue['recommendation']}")

    return "\n".join(lines)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/analyze")
async def analyze(
    request: Request,
    file: Optional[UploadFile] = File(default=None),
    source_name: str = Form(default="demo_pipeline"),
) -> JSONResponse:
    try:
        df = load_dataframe(file)
        result = analyze_dataframe(df, source_name or "demo_pipeline")
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc


@app.get("/api/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}
