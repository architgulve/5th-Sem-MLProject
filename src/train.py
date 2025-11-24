import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report, roc_auc_score, recall_score
)

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from imblearn.over_sampling import SMOTE

# Detect project paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(ROOT, "data", "processed")
MODEL_DIR = os.path.join(ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)


# -------------------------------------------------------------
# UTILS
# -------------------------------------------------------------

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names so XGBoost accepts them."""
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


def load_data():
    path = os.path.join(PROC_DIR, "oulad_per_student.parquet")
    if not os.path.exists(path):
        raise FileNotFoundError("Processed dataset not found: " + path)
    df = pd.read_parquet(path)
    return df


# -------------------------------------------------------------
# TRAINING PIPELINE
# -------------------------------------------------------------

def train():

    print("\nLoading data...")
    df = load_data()

    # Drop identifiers from X
    drop_cols = ["dropout", "id_student", "code_module", "code_presentation"]
    X = df.drop(columns=drop_cols, errors="ignore")
    y = df["dropout"].astype(int)

    # Clean feature names
    X = clean_columns(X)

    print("\nTrain/Val Split...")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Check for remaining non-numeric columns
    non_numeric = X_train.select_dtypes(include=["object"]).columns.tolist()
    if len(non_numeric) > 0:
        print("\nERROR: Non-numeric columns still present:", non_numeric)
        raise ValueError("Fix preprocessing; SMOTE/XGBoost require numeric.")

    # ---------------------------------------------------------
    # SMOTE Oversampling
    # ---------------------------------------------------------
    print("\nBefore SMOTE:", np.bincount(y_train))

    sm = SMOTE(random_state=42)
    X_sm, y_sm = sm.fit_resample(X_train, y_train)

    print("After SMOTE:", np.bincount(y_sm))

    # Clean columns after SMOTE (just to be safe)
    X_sm = clean_columns(X_sm)

    # ---------------------------------------------------------
    # MODEL 1 — RANDOM FOREST
    # ---------------------------------------------------------
    print("\nTraining RandomForest...")
    rf = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        class_weight="balanced",
        n_jobs=-1,
        random_state=42
    )
    rf.fit(X_sm, y_sm)

    rf_preds = rf.predict(X_val)
    rf_proba = rf.predict_proba(X_val)[:, 1]

    print("\nRandomForest Results:")
    print(classification_report(y_val, rf_preds, digits=4))
    print("RF ROC AUC:", roc_auc_score(y_val, rf_proba))
    rf_recall = recall_score(y_val, rf_preds)

    # ---------------------------------------------------------
    # MODEL 2 — XGBOOST
    # ---------------------------------------------------------
    print("\nTraining XGBoost...")

    # imbalance ratio for XGBoost
    neg, pos = np.bincount(y_train)
    scale_pos_weight = neg / pos

    xgb = XGBClassifier(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        tree_method="hist"  # best for large tabular data
    )

    xgb.fit(X_sm, y_sm)

    xgb_preds = xgb.predict(X_val)
    xgb_proba = xgb.predict_proba(X_val)[:, 1]

    print("\nXGBoost Results:")
    print(classification_report(y_val, xgb_preds, digits=4))
    print("XGB ROC AUC:", roc_auc_score(y_val, xgb_proba))
    xgb_recall = recall_score(y_val, xgb_preds)

    # ---------------------------------------------------------
    # PICK BEST MODEL BY RECALL
    # ---------------------------------------------------------
    print("\nSelecting best model...")

    if xgb_recall >= rf_recall:
        best = xgb
        best_name = "xgboost"
    else:
        best = rf
        best_name = "random_forest"

    out_path = os.path.join(MODEL_DIR, "best_model.joblib")
    joblib.dump(best, out_path)

    print(f"\nSaved BEST model ({best_name}) → {out_path}")


if __name__ == "__main__":
    train()
