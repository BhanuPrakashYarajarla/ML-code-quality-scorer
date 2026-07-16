# ML-Based Code Quality & Maintainability Scoring System

> A machine learning–powered web application that statically analyzes Python code and produces an interpretable maintainability score, complete with actionable refactoring suggestions.

---


## Overview

This project addresses a core problem in software engineering: **quantifying code quality objectively**. Rather than relying on manual code reviews alone, this system uses a trained **Random Forest classifier** to predict the maintainability of Python code snippets based on static analysis metrics.

The result is a 0–100 score labeled as **High**, **Moderate**, or **Low** quality, accompanied by:
- An **XAI (Explainable AI)** breakdown of which metrics influenced the score
- Concrete **refactoring suggestions** to improve the code

---

## Features

- **Static Code Analysis** — Parses Python source using the `ast` module to extract structural and complexity metrics
- **ML-Based Scoring** — Random Forest model trained on real-world open-source project data predicts maintainability probability
- **Structural Penalty System** — Rule-based post-processing penalizes deep nesting, poor cohesion, and high cyclomatic complexity
- **Explainable AI (XAI)** — Semantic evidence engine highlights which metrics are problematic and why
- **Refactoring Suggestions** — Threshold-based rule engine generates human-readable improvement hints
- **Web Interface** — Clean Flask UI for submitting code and viewing results
- **Code Comparison** — Side-by-side comparison view for evaluating two code snippets

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask |
| ML Model | Scikit-learn (Random Forest) |
| Static Analysis | Python `ast` module |
| Data Processing | Pandas, Joblib |
| Frontend | HTML, CSS (Jinja2 templates) |
| Dataset | Open-source Java project code smell & quality attributes |

---

## Project Structure

```
CD_Project/
│
├── app.py                  # Flask application entry point
├── verify_scoring.py       # Standalone scoring verification script
│
├── analysis/
│   ├── analyzer.py         # AST-based static metric extractor
│   ├── ml_scoring.py       # ML model inference + structural penalties
│   ├── rules.py            # Threshold-based suggestion generator
│   └── xai.py              # Semantic XAI evidence & explanation engine
│
├── models/
│   ├── rf_model.pkl        # Trained Random Forest classifier
│   ├── scaler.pkl          # Feature scaler (StandardScaler)
│   ├── features.pkl        # Ordered feature list used during training
│   ├── thresholds.pkl      # Per-metric thresholds for rule suggestions
│   └── x_train_stats.pkl   # Training set statistics
│
├── dataset/
│   ├── repositories.csv        # Source repository metadata
│   ├── versions.csv            # Version history
│   ├── attribute-details.csv   # Quality attribute definitions
│   ├── quality_attributes/     # Per-project quality metric CSVs
│   └── codesmells/             # Code smell reports (CSV + HTML)
│
├── templates/
│   ├── index.html          # Code input page
│   ├── result.html         # Score & explanation page
│   └── compare.html        # Side-by-side comparison page
│
├── static/
│   └── style.css           # Application stylesheet
│
└── .gitignore
```

---

## Metrics Explained

The system extracts the following metrics via static AST analysis:

| Metric | Name | Description |
|--------|------|-------------|
| `LOC` | Lines of Code | Total lines in the snippet |
| `MCC` | McCabe Cyclomatic Complexity | Number of independent execution paths |
| `NBD` | Nested Block Depth | Maximum nesting level of control structures |
| `NOM` | Number of Methods | Count of function definitions |
| `RFC` | Response for a Class | Number of method/function calls made |
| `CBO` | Coupling Between Objects | Number of external module imports |
| `WMC` | Weighted Methods per Class | Sum of complexity across all methods |
| `LCOM` | Lack of Cohesion in Methods | Measures how unrelated methods are within a unit |
| `ATFD` | Access to Foreign Data | Number of external attribute accesses |

---

## Scoring Pipeline

The final score is computed in three stages:

```
Raw Code
   │
   ▼
[1] Static Analysis (ast)
    → Extract 9 metrics (LOC, MCC, NBD, NOM, RFC, CBO, WMC, LCOM, ATFD)
   │
   ▼
[2] ML Inference (Random Forest)
    → predict_proba × 100 → Base Score (0–100)
   │
   ▼
[3] Post-Processing Adjustments
    ├── XAI Severity Penalty  : −10 pts per high-severity metric flag
    └── Structural Penalties  :
            NBD ≥ 3           → −20 pts
            LCOM < 0.3        → −20 pts  (only if NOM > 0)
            MCC ≥ 5           → −10 pts
            Trivial scripts   → no penalty
   │
   ▼
Final Score (clamped to 0–100)
    ≥ 70  →  High      (clean, well-structured)
    ≥ 35  →  Moderate  (some issues, partially maintainable)
    < 35  →  Low       (major structural/complexity problems)
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/BhanuPrakashYarajarla/ML-code-quality-scorer.git
cd ML-code-quality-scorer

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install flask scikit-learn pandas joblib
```

### Run the Application

```bash
python app.py
```

Open your browser and navigate to: **http://127.0.0.1:5000**

### Verify Scoring Logic

To test the scoring pipeline on sample code snippets without the web UI:

```bash
python verify_scoring.py
```
