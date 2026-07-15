from flask import Flask, render_template, request
from analysis.analyzer import extract_metrics_from_code
from analysis.ml_scoring import maintainability_score, apply_structural_penalties
from analysis.xai import (
    compute_semantic_evidence,
    semantic_xai_explanation,
    METRIC_LABELS,
    METRIC_HINTS
)
from analysis.rules import generate_suggestions

app = Flask(__name__)

def score_label(score):
    """
    Classify the maintainability score into a severity level.

    Thresholds:
      0-35  → Low   (code has major structural/complexity issues)
      35-70 → Moderate (some problems but partially maintainable)
      70-100→ High  (clean, well-structured code)

    Rationale:
      - The ML model outputs predict_proba * 100, so 50 is the raw decision boundary.
      - Structural penalties can subtract up to 50 pts (NBD≥3: -20, LCOM<0.3: -20, MCC≥5: -10).
      - XAI high-severity hits subtract 10 pts each (up to ~50).
      - Clean code typically scores 80-100 before penalties.
      - Code with 1-2 moderate issues lands in 40-70 range.
      - Code with deep nesting + high complexity + poor cohesion drops below 35.
      - 35 as the lower bound captures truly problematic code (needs 65+ pts of penalties).
      - 70 as the upper bound ensures only genuinely clean code earns "High" quality.
    """
    if score >= 70:
        return "High", "label-high"
    elif score >= 35:
        return "Moderate", "label-moderate"
    else:
        return "Low", "label-low"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form["code"]

        metrics = extract_metrics_from_code(code)
        score = maintainability_score(metrics)

        evidence = compute_semantic_evidence(metrics)
        why = semantic_xai_explanation(evidence)
        
        # FIX 2: Severity-aware adjustment
        high_severity = sum(1 for e in evidence if e["severity"] == "high")
        score -= high_severity * 10
        score = max(score, 0)

        # FIX 1: Structural Severity Penalty
        score = apply_structural_penalties(score, metrics)

        # Classify score into quality level
        quality_label, quality_class = score_label(score)

        fixes = generate_suggestions(metrics)

        return render_template(
            "result.html",
            score=score,
            quality_label=quality_label,
            quality_class=quality_class,
            why=why,
            fixes=fixes,
            metrics=metrics,
            labels=METRIC_LABELS,
            hints=METRIC_HINTS
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
