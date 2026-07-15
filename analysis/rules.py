import joblib

THRESHOLDS = joblib.load("models/thresholds.pkl")

def generate_suggestions(sample):
    suggestions = []

    if sample["LOC"] > THRESHOLDS["LOC"]:
        suggestions.append(
            "Code size is high. Split large methods into smaller functions."
        )

    if sample["MCC"] > THRESHOLDS["MCC"]:
        suggestions.append(
            "High decision complexity detected. Reduce conditional logic to simplify control flow."
        )

    if sample["NBD"] > THRESHOLDS["NBD"]:
        suggestions.append(
            "Deep nesting detected. Flatten nested structures to improve readability."
        )

    if sample["CBO"] > THRESHOLDS["CBO"]:
        suggestions.append(
            "High external dependencies detected. Reduce coupling to make changes safer."
        )

    if sample["LCOM"] > THRESHOLDS["LCOM"]:
        suggestions.append(
            "Low cohesion detected. Group related responsibilities into focused functions or classes."
        )

    return suggestions