import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_recall_curve,
    roc_curve,
    auc
)

# Paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(ROOT, "data", "processed")
MODEL_DIR = os.path.join(ROOT, "models")

# ---------------------------------------------------------
# CLEAN COLUMN NAMES (same as train.py)
# ---------------------------------------------------------
def clean_columns(df):
    df = df.copy()
    df.columns = (
        df.columns
        .str.replace("<", "lt", regex=False)
        .str.replace(">", "gt", regex=False)
        .str.replace("[", "(", regex=False)
        .str.replace("]", ")", regex=False)
        .str.replace("%", "pct", regex=False)
        .str.replace(" ", "_", regex=False)
    )
    return df

# ---------------------------------------------------------
# LOAD MODEL + DATA
# ---------------------------------------------------------
def load():
    print("Loading model...")
    model_path = os.path.join(MODEL_DIR, "best_model.joblib")
    model = joblib.load(model_path)

    print("Loading dataset...")
    df = pd.read_parquet(os.path.join(PROC_DIR, "oulad_per_student.parquet"))

    # Prepare X, y
    X = df.drop(columns=["dropout", "id_student", "code_module", "code_presentation"], errors="ignore")
    y = df["dropout"].astype(int)

    X = clean_columns(X)
    return model, X, y


# ---------------------------------------------------------
# EVALUATION PIPELINE
# ---------------------------------------------------------
def evaluate_model():
    model, X, y = load()

    # Train-test split (20% hold-out test set)
    print("\nCreating test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("\nEvaluating model...")
    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    # -----------------------------------------------------
    # BASIC METRICS
    # -----------------------------------------------------
    print("\n=== CLASSIFICATION REPORT (threshold = 0.5) ===")
    print(classification_report(y_test, y_pred, digits=4))

    print("\n=== CONFUSION MATRIX ===")
    print(confusion_matrix(y_test, y_pred))

    roc_auc = roc_auc_score(y_test, y_proba)
    print("\nROC AUC:", roc_auc)

    # -----------------------------------------------------
    # PRECISION-RECALL ANALYSIS
    # -----------------------------------------------------
    prec, rec, th = precision_recall_curve(y_test, y_proba)
    pr_auc = auc(rec, prec)
    print("PR AUC:", pr_auc)

    # -----------------------------------------------------
    # OPTIMAL THRESHOLD FOR MAX RECALL / F1 / F2
    # -----------------------------------------------------
    f1_scores = 2 * (prec * rec) / (prec + rec + 1e-9)
    best_idx = np.argmax(f1_scores)
    best_threshold = th[best_idx]

    print(f"\n=== BEST THRESHOLD (F1 optimized) ===")
    print("Threshold:", float(best_threshold))
    print("Precision:", float(prec[best_idx]))
    print("Recall:", float(rec[best_idx]))
    print("F1:", float(f1_scores[best_idx]))

    # -----------------------------------------------------
    # SAVE PLOTS
    # -----------------------------------------------------
    print("\nSaving plots...")

    # PR Curve
    plt.figure(figsize=(7, 6))
    plt.plot(rec, prec)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"Precision-Recall Curve (AUC = {pr_auc:.4f})")
    plt.grid(True)
    plt.savefig("pr_curve_test.png")

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curve (AUC = {roc_auc:.4f})")
    plt.grid(True)
    plt.savefig("roc_curve_test.png")

    print("Saved: pr_curve_test.png, roc_curve_test.png")

    # -----------------------------------------------------
    # FEATURE IMPORTANCE (if XGBoost)
    # -----------------------------------------------------
    if hasattr(model, "get_booster"):
        booster = model.get_booster()
        importance_gain = booster.get_score(importance_type='gain')

        imp_df = pd.DataFrame([
            (feat, importance_gain.get(feat, 0.0))
            for feat in X.columns
        ], columns=["feature", "gain"])

        imp_df = imp_df.sort_values("gain", ascending=False)
        imp_df.to_csv("feature_importance_test.csv", index=False)

        print("Saved: feature_importance_test.csv")

    print("\n=== Evaluation Complete ===")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    evaluate_model()
