import os
import pandas as pd
import numpy as np

# Auto-detect project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "data", "raw")
PROC_DIR = os.path.join(ROOT, "data", "processed")
os.makedirs(PROC_DIR, exist_ok=True)

def load_oulad():
    files = [
        "studentInfo.csv",
        "studentVle.csv",
        "vle.csv",
        "assessments.csv",
        "studentAssessment.csv",
        "studentRegistration.csv",
        "courses.csv"
    ]
    dfs = {}
    for f in files:
        path = os.path.join(RAW_DIR, f)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing: {path}")
        dfs[f[:-4]] = pd.read_csv(path)
    return dfs


def make_features(dfs):
    si = dfs["studentInfo"]
    sv = dfs["studentVle"]
    sa = dfs["studentAssessment"]
    sr = dfs["studentRegistration"]

    si["dropout"] = (si["final_result"] == "Withdrawn").astype(int)

    base = si[[
        "code_module", "code_presentation", "id_student",
        "gender", "region", "highest_education", "imd_band",
        "age_band", "num_of_prev_attempts", "studied_credits",
        "disability", "dropout"
    ]].copy()

    sr_min = sr.groupby(["code_module","code_presentation","id_student"])["date_registration"].min().reset_index()
    base = base.merge(sr_min, on=["code_module","code_presentation","id_student"], how="left")
    base["date_registration"] = base["date_registration"].fillna(-1)

    # VLE aggregates
    sv["within14"] = sv["date"] <= 14
    sv["within28"] = sv["date"] <= 28

    vle_agg = sv.groupby(["code_module","code_presentation","id_student"]).agg(
        vle_total_clicks=("sum_click","sum"),
        vle_days_active=("date", lambda s: s.nunique()),
        vle_first14=("sum_click", lambda x: x[sv.loc[x.index,"within14"]].sum()),
        vle_first28=("sum_click", lambda x: x[sv.loc[x.index,"within28"]].sum())
    ).reset_index()

    base = base.merge(vle_agg, on=["code_module","code_presentation","id_student"], how="left")

    # assessment features
    sa_agg = sa.groupby("id_student").agg(
        avg_assessment_score=("score","mean"),
        n_submissions=("score","count")
    ).reset_index()

    base = base.merge(sa_agg, on="id_student", how="left")

    # numeric fill
    num_cols = ["vle_total_clicks","vle_days_active","vle_first14","vle_first28",
                "avg_assessment_score","n_submissions"]
    base[num_cols] = base[num_cols].fillna(0)

    # ---- KEY FIX ----
    # Convert ALL remaining object columns (including region, gender, disability, imd_band)
    obj_cols = base.select_dtypes(include=["object"]).columns.tolist()

    # Exclude ID + module identifiers
    exclude = ["code_module", "code_presentation", "id_student"]
    obj_cols = [c for c in obj_cols if c not in exclude]

    # One-hot encode them
    base = pd.get_dummies(base, columns=obj_cols, dummy_na=True)

    # Save
    out_path = os.path.join(PROC_DIR, "oulad_per_student.parquet")
    base.to_parquet(out_path, index=False)
    print("Saved:", out_path)

    # DEBUG CHECK
    print("Remaining object columns after encoding:",
          base.select_dtypes(include=["object"]).columns.tolist())

    return base


if __name__ == "__main__":
    dfs = load_oulad()
    make_features(dfs)
