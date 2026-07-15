import joblib
import pandas as pd

# Load trained assets
best_model = joblib.load("models/rf_model.pkl")
scaler = joblib.load("models/scaler.pkl")
FEATURES = joblib.load("models/features.pkl")

def maintainability_score(sample_row):
    """
    sample_row: dictionary of metrics (before scaling)
    """
    sample_df = pd.DataFrame([sample_row], columns=FEATURES)
    sample_scaled = scaler.transform(sample_df)
    prob = best_model.predict_proba(sample_scaled)[0][1]
    return round(prob * 100, 2)

def apply_structural_penalties(score, metrics):
    penalty = 0

    # Deep nesting penalty
    if metrics["NBD"] >= 3:
        penalty += 20

    # Apply cohesion penalty only when modular structure exists
    if metrics["NOM"] > 0:
        if metrics["LCOM"] < 0.3:
            penalty += 20

    # High complexity penalty
    if metrics["MCC"] >= 5:
        penalty += 10

    # Do not penalize trivial scripts
    if metrics["MCC"] <= 1 and metrics["NBD"] == 0 and metrics["LOC"] < 25:
        penalty = 0

    return max(score - penalty, 0)