# Autonomous Deal Assessment Framework (M&A Deal Review Bot)

This project automates the assessment of company financials for acquisition decisions using a **CrewAI-driven multi-agent system**.

---

## Overview

The system uses structured SEBI and company PDFs to **extract, analyze, and generate insights** relevant for M&A readiness analysis.

---

## Core Agents

- **PDF Extraction Agent**: Uses PyMuPDF and CrewAI to ingest and structure financial data from PDFs.
- **Red Flag Detection Agent**: Evaluates extracted financial chunks for issues that could impact acquisition decisions.
- **Report Generation Agent**: Summarizes findings into structured reports to support go/no-go M&A calls.

---

## Project Structure

```
ma-deal-review-bot/
│
├── 1.README.md
├── pdf-extract-agent/
│   └── extract.py
│
├── RedFlag_Detection/
│   └── flag_check.py
│
├── Report_Generation/
│   └── report_gen.py
│
└── docs/
    └── project_notes.md
```

---

## Status

✅ PDF extraction workflow stable using CrewAI\
✅ Red flag detection operational\
⏳ Report generation refinement ongoing\
📄 Documentation in progress

---

## How to Use

1. **Place your SEBI/company PDFs** in your local working directory.
2. Run:
   - `extract.py` to extract and structure the data.
   - `flag_check.py` to detect financial red flags.
   - `report_gen.py` to generate your M&A readiness report.

---

## Notes

- Ensure your OpenAI and CrewAI environment is configured before running the agents.
- Intended for early-stage M&A financial screening, not for regulatory filings.

