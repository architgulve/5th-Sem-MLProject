import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(ROOT, "data", "processed")
MODEL_DIR = os.path.join(ROOT, "models")

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


def explain_model():

    print("Loading model...")
    model = joblib.load(os.path.join(MODEL_DIR, "best_model.joblib"))
    print("Model type:", type(model))

    print("Loading dataset...")
    df = pd.read_parquet(os.path.join(PROC_DIR, "oulad_per_student.parquet"))
    X = df.drop(columns=["dropout", "id_student", "code_module", "code_presentation"], errors="ignore")
    X = clean_columns(X)

    # Get feature importance
    print("Extracting feature importance...")

    # XGBoost classifier has get_booster()
    booster = model.get_booster()
    importance_gain = booster.get_score(importance_type='gain')

    # Convert to dataframe
    imp_df = pd.DataFrame([
        (feat, importance_gain.get(feat, 0.0))
        for feat in X.columns
    ], columns=["feature", "gain"])

    imp_df = imp_df.sort_values("gain", ascending=False)

    # Save CSV
    out_csv = "feature_importance_gain.csv"
    imp_df.to_csv(out_csv, index=False)
    print("Saved:", out_csv)

    # Plot top 20 features
    top = imp_df.head(20)
    plt.figure(figsize=(10, 8))
    plt.barh(top["feature"], top["gain"])
    plt.gca().invert_yaxis()
    plt.xlabel("Gain")
    plt.ylabel("Feature")
    plt.title("Top 20 Most Important Features (XGBoost Gain)")
    plt.tight_layout()
    plt.savefig("feature_importance_plot.png")
    print("Saved plot: feature_importance_plot.png")

    print("\nExplanation complete.")


if __name__ == "__main__":
    explain_model()
