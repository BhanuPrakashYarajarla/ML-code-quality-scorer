import sys
import os

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

from analysis.analyzer import extract_metrics_from_code
from analysis.ml_scoring import maintainability_score, apply_structural_penalties
from analysis.xai import compute_semantic_evidence

def calculate_final_score(code):
    print(f"\n--- Testing Code ---\n{code[:50]}...")
    metrics = extract_metrics_from_code(code)
    print(f"Metrics: {metrics}")
    
    score = maintainability_score(metrics)
    print(f"Initial ML Score: {score}")

    evidence = compute_semantic_evidence(metrics)
    high_severity_count = sum(1 for e in evidence if e["severity"] == "high")
    print(f"High Severity Count: {high_severity_count}")
    
    # Apply Severity Adjustment
    score -= high_severity_count * 10
    score = max(score, 0)
    print(f"Score after Severity Adj: {score}")

    # Apply Structural Penalties
    score = apply_structural_penalties(score, metrics)
    print(f"Final Score in App: {score}")
    return score

# Case 1: Good Code
good_code = """
def hello():
    print("Hello world")
"""
calculate_final_score(good_code)

# Case 2: Bad Code (Deep Nesting, High Complexity)
bad_code = """
def complex_bad():
    x = 0
    if x == 0:
        for i in range(10):
            if i > 5:
                while x < 100:
                    if x % 2 == 0:
                        print(x)
                    x += 1
    if x > 50:
        print("Done")
    if x < 0:
        print("Negative")
    if x == 100:
        print("Hundred")
"""
calculate_final_score(bad_code)
