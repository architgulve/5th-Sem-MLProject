from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Load model
model = joblib.load("../models/best_model.joblib")

# --- ADD THIS FUNCTION TO app.py ---
def clean_columns(df):
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
# ------------------------------------
# app.py (Original)
# ...
# EXACT training features
FEATURE_COLUMNS = [
    'num_of_prev_attempts', 'studied_credits', 'date_registration',
    # ... (long list of original, uncleaned feature names)
# ...
]

# app.py (Modified)
# ...
# EXACT training features
_RAW_FEATURE_COLUMNS = [
    'num_of_prev_attempts', 'studied_credits', 'date_registration',
    'vle_total_clicks', 'vle_days_active', 'vle_first14', 'vle_first28',
    'avg_assessment_score', 'n_submissions',

    'gender_F', 'gender_M', 'gender_nan',

    'region_East Anglian Region', 'region_East Midlands Region',
    'region_Ireland', 'region_London Region', 'region_North Region',
    'region_North Western Region', 'region_Scotland',
    'region_South East Region', 'region_South Region',
    'region_South West Region', 'region_Wales',
    'region_West Midlands Region', 'region_Yorkshire Region',
    'region_nan',

    'highest_education_A Level or Equivalent',
    'highest_education_HE Qualification',
    'highest_education_Lower Than A Level',
    'highest_education_No Formal quals',
    'highest_education_Post Graduate Qualification',
    'highest_education_nan',

    'imd_band_0-10%', 'imd_band_10-20', 'imd_band_20-30%',
    'imd_band_30-40%', 'imd_band_40-50%', 'imd_band_50-60%',
    'imd_band_60-70%', 'imd_band_70-80%', 'imd_band_80-90%',
    'imd_band_90-100%', 'imd_band_nan',

    'age_band_0-35', 'age_band_35-55', 'age_band_55<=', 'age_band_nan',

    'disability_N', 'disability_Y', 'disability_nan'
]

# Clean the feature names to match the model's expected names
FEATURE_COLUMNS = clean_columns(pd.DataFrame(columns=_RAW_FEATURE_COLUMNS)).columns.tolist()
# ------------------------------------

def preprocess_input(raw):
    """
    Build a COMPLETE feature row for the model:
    - numeric fields copied directly
    - one-hot categorical fields produced manually
    - everything else = 0
    """
    row = {col: 0 for col in FEATURE_COLUMNS}

    # numeric fields
    for f in ["num_of_prev_attempts", "studied_credits",
              "date_registration", "vle_total_clicks",
              "vle_days_active", "vle_first14", "vle_first28",
              "avg_assessment_score", "n_submissions"]:
        if f in raw:
            row[f] = raw[f]

    # ----- one-hot encoding manually -----

    # gender
    g = raw.get("gender")
    if g is None:
        row["gender_nan"] = 1
    else:
        col = f"{g}"
        if col in row:
            row[col] = 1
        else:
            row["gender_nan"] = 1

    # region
    r = raw.get("region")
    if r is None:
        row["region_nan"] = 1
    else:
        col = clean_columns(pd.DataFrame(columns=[f"{r}"])).columns.tolist()[0]
        if col in row:
            row[col] = 1
        else:
            row["region_nan"] = 1

    # highest_education
    h = raw.get("highest_education")
    if h is None:
        row["highest_education_nan"] = 1
    else:
        col = clean_columns(pd.DataFrame(columns=[f"{h}"])).columns.tolist()[0]
        if col in row:
            row[col] = 1
        else:
            row["highest_education_nan"] = 1

    # imd_band
    imd = raw.get("imd_band")
    if imd is None:
        row["imd_band_nan"] = 1
    else:
        col = clean_columns(pd.DataFrame(columns=[f"{imd}"])).columns.tolist()[0]
        if col in row:
            row[col] = 1
        else:
            row["imd_band_nan"] = 1

    # age
    age = raw.get("age_band")
    if age is None:
        row["age_band_nan"] = 1
    else:
        col = clean_columns(pd.DataFrame(columns=[f"{age}"])).columns.tolist()[0]
        if col in row:
            row[col] = 1
        else:
            row["age_band_nan"] = 1

    # disability
    d = raw.get("disability")
    if d is None:
        row["disability_nan"] = 1
    else:
        col = f"{d}"
        if col in row:
            row[col] = 1
        else:
            row["disability_nan"] = 1

    return pd.DataFrame([row])


@app.post("/predict")
def predict():
    try:
        raw = request.get_json()
        X = preprocess_input(raw)
        proba = float(model.predict_proba(X)[0, 1])
        return jsonify({"risk_score": proba})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
