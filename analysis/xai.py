import joblib
import pandas as pd

# Load assets
best_model = joblib.load("models/rf_model.pkl")
FEATURES = joblib.load("models/features.pkl")
X_train_stats = joblib.load("models/x_train_stats.pkl")

# -------------------------
# Global Feature Importance
# -------------------------
importance = pd.Series(
    best_model.feature_importances_,
    index=FEATURES
).sort_values(ascending=False)

# -------------------------
# Human-readable metric info
# -------------------------
METRIC_LABELS = {
    "LOC": "Code Size",
    "MCC": "Decision Complexity",
    "NBD": "Nested Logic Depth",
    "NOM": "Number of Methods",
    "RFC": "Response Complexity",
    "CBO": "External Dependencies",
    "WMC": "Overall Method Complexity",
    "LCOM": "Cohesion Quality",
    "ATFD": "Foreign Data Access"
}

METRIC_HINTS = {
    "LOC": "Larger code is harder to understand and maintain",
    "MCC": "More decision paths increase testing and bug risk",
    "NBD": "Deep nesting makes logic difficult to follow",
    "NOM": "More methods increase maintenance effort",
    "RFC": "Higher response complexity reduces predictability",
    "CBO": "High coupling spreads changes across modules",
    "WMC": "Overall complexity of the code unit",
    "LCOM": "Low cohesion indicates unrelated responsibilities",
    "ATFD": "Accessing foreign data reduces encapsulation"
}

# -------------------------
# Semantic XAI
# -------------------------
METRIC_EXPLANATIONS = {
    "MCC": {
        "name": "Cyclomatic Complexity",
        "meaning": "the number of independent execution paths",
        "impact": "higher values increase cognitive load and testing effort",
        "maintainability_effect": "harder to understand, modify, and debug"
    },
    "CBO": {
        "name": "Coupling Between Objects",
        "meaning": "dependency on external modules",
        "impact": "high coupling propagates changes across the system",
        "maintainability_effect": "changes become risky and error-prone"
    },
    "LOC": {
        "name": "Lines of Code",
        "meaning": "the physical size of the code",
        "impact": "larger code units are harder to read and maintain",
        "maintainability_effect": "increases effort for comprehension and refactoring"
    },
    "NBD": {
        "name": "Nested Block Depth",
        "meaning": "depth of nested control structures",
        "impact": "deep nesting reduces readability",
        "maintainability_effect": "logic becomes difficult to follow"
    },
    "LCOM": {
        "name": "Lack of Cohesion",
        "meaning": "how unrelated components are",
        "impact": "low cohesion indicates scattered responsibilities",
        "maintainability_effect": "harder to evolve and refactor"
    }
}

def compute_semantic_evidence(sample):
    evidence = []

    # Threshold-based checks that always produce meaningful evidence
    # Complexity
    if sample.get("MCC", 1) >= 5:
        evidence.append({"feature": "MCC", "z": 2.0, "severity": "high"})
    elif sample.get("MCC", 1) >= 3:
        evidence.append({"feature": "MCC", "z": 1.0, "severity": "low"})
    else:
        evidence.append({"feature": "MCC", "z": -1.0, "severity": "good"})

    # Nesting depth
    if sample.get("NBD", 0) >= 3:
        evidence.append({"feature": "NBD", "z": 2.0, "severity": "high"})
    elif sample.get("NBD", 0) >= 2:
        evidence.append({"feature": "NBD", "z": 1.0, "severity": "low"})
    else:
        evidence.append({"feature": "NBD", "z": -1.0, "severity": "good"})

    # Code size
    if sample.get("LOC", 0) > 50:
        evidence.append({"feature": "LOC", "z": 2.0, "severity": "high"})
    elif sample.get("LOC", 0) > 25:
        evidence.append({"feature": "LOC", "z": 1.0, "severity": "low"})
    else:
        evidence.append({"feature": "LOC", "z": -1.0, "severity": "good"})

    # Coupling
    if sample.get("CBO", 0) > 3:
        evidence.append({"feature": "CBO", "z": 2.0, "severity": "high"})
    elif sample.get("CBO", 0) > 1:
        evidence.append({"feature": "CBO", "z": 1.0, "severity": "low"})

    # Cohesion (only when modular)
    if sample.get("NOM", 0) > 0:
        if sample.get("LCOM", 0) < 0.3:
            evidence.append({"feature": "LCOM", "z": 2.0, "severity": "high"})
        elif sample.get("LCOM", 0) < 0.5:
            evidence.append({"feature": "LCOM", "z": 1.0, "severity": "low"})

    return evidence

def semantic_xai_explanation(evidence):
    explanations = []

    for e in evidence:
        meta = METRIC_EXPLANATIONS[e["feature"]]
        severity = e["severity"]

        if severity == "good":
            text = (
                f"{meta['name']} is well within acceptable range. "
                f"This positively contributes to maintainability."
            )
        else:
            deviation = (
                "significantly higher than normal"
                if e["z"] > 1.5 else
                "moderately higher than normal"
                if e["z"] > 0 else
                "lower than normal"
            )

            influence = (
                "strongly reduced"
                if e["z"] > 1 else
                "reduced"
                if e["z"] > 0 else
                "improved"
            )

            text = (
                f"{meta['name']} is {deviation}. "
                f"This reflects {meta['meaning']}. "
                f"As a result, {meta['impact']}, making the code "
                f"{meta['maintainability_effect']}. "
                f"Therefore, this factor {influence} the maintainability score."
            )

        explanations.append({
            "text": text,
            "severity": severity
        })

    return explanations

    