"use client";
import React, { useState } from "react";

const label = "font-semibold text-gray-700 mb-1 block";

export default function App() {
  const [student, setStudent] = useState({});
  const [risk, setRisk] = useState(null);
  const [error, setError] = useState("");

  const setField = (field, value) =>
    setStudent((prev) => ({ ...prev, [field]: value }));

  const handlePredict = async () => {
    setError("");
    setRisk(null);

    try {
      const resp = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(student),
      });

      const data = await resp.json();

      if (data.error) {
        setError(data.error);
        return;
      }

      setRisk(Number(data.risk_score));
    } catch (err) {
      setError("Network error — backend not running?");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-white rounded-xl shadow-lg p-8 space-y-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4 text-center">
          🎓 Student Dropout Risk Predictor
        </h1>

        {/* --- DROPDOWNS --- */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          <div>
            <label className={label}>Gender</label>
            <select
              className="w-full border p-2 rounded"
              onChange={(e) => setField("gender", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="gender_M">Male</option>
              <option value="gender_F">Female</option>
            </select>
          </div>

          <div>
            <label className={label}>Age Band</label>
            <select
              className="w-full border p-2 rounded"
              onChange={(e) => setField("age_band", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="age_band_0-35">0–35</option>
              <option value="age_band_35-55">35–55</option>
              <option value="age_band_55<=">55+</option>
            </select>
          </div>

          <div>
            <label className={label}>Region</label>
            <select
              className="w-full border p-2 rounded"
              onChange={(e) => setField("region", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="region_East Anglian Region">East Anglian Region</option>
              <option value="region_East Midlands Region">East Midlands Region</option>
              <option value="region_Ireland">Ireland</option>
              <option value="region_London Region">London Region</option>
              <option value="region_North Region">North Region</option>
              <option value="region_North Western Region">North Western Region</option>
              <option value="region_Scotland">Scotland</option>
              <option value="region_South East Region">South East Region</option>
              <option value="region_South Region">South Region</option>
              <option value="region_South West Region">South West Region</option>
              <option value="region_Wales">Wales</option>
              <option value="region_West Midlands Region">West Midlands Region</option>
              <option value="region_Yorkshire Region">Yorkshire Region</option>
            </select>
          </div>

          <div>
            <label className={label}>Highest Education</label>
            <select
              className="w-full border p-2 rounded"
              onChange={(e) =>
                setField("highest_education", e.target.value || null)
              }
            >
              <option value="">Select</option>
              <option value="highest_education_A Level or Equivalent">
                A Level or Equivalent
              </option>
              <option value="highest_education_HE Qualification">HE Qualification</option>
              <option value="highest_education_Lower Than A Level">Lower Than A Level</option>
              <option value="highest_education_No Formal quals">No Formal quals</option>
              <option value="highest_education_Post Graduate Qualification">
                Post Graduate Qualification
              </option>
            </select>
          </div>

          <div>
            <label className={label}>IMD Band</label>
            <select
              className="w-full border p-2 rounded"
              onChange={(e) => setField("imd_band", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="imd_band_0-10%">0–10%</option>
              <option value="imd_band_10-20">10–20%</option>
              <option value="imd_band_20-30%">20–30%</option>
              <option value="imd_band_30-40%">30–40%</option>
              <option value="imd_band_40-50%">40–50%</option>
              <option value="imd_band_50-60%">50–60%</option>
              <option value="imd_band_60-70%">60–70%</option>
              <option value="imd_band_70-80%">70–80%</option>
              <option value="imd_band_80-90%">80–90%</option>
              <option value="imd_band_90-100%">90–100%</option>
            </select>
          </div>

          <div>
            <label className={label}>Disability</label>
            <select
              className="w-full border p-2 rounded"
              onChange={(e) => setField("disability", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="disability_N">No</option>
              <option value="disability_Y">Yes</option>
            </select>
          </div>
        </div>

        {/* --- NUMERIC INPUTS --- */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">

          {[
            "num_of_prev_attempts",
            "studied_credits",
            "date_registration",
            "vle_total_clicks",
            "vle_days_active",
            "vle_first14",
            "vle_first28",
            "avg_assessment_score",
            "n_submissions",
          ].map((field) => (
            <div key={field}>
              <label className={label}>{field.replace(/_/g, " ")}</label>
              <input
                type="number"
                className="w-full border p-2 rounded"
                onChange={(e) =>
                  setField(field, Number(e.target.value) || 0)
                }
              />
            </div>
          ))}
        </div>

        {/* BUTTON */}
        <button
          onClick={handlePredict}
          className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg mt-4 shadow"
        >
          Predict Dropout Risk
        </button>

        {/* RESULT */}
        {risk !== null && (
          <div className="text-center mt-6">
            <p className="text-lg font-semibold">Predicted Risk:</p>
            <span
              className={`inline-block mt-2 px-6 py-2 text-lg font-bold rounded-lg shadow
                ${risk > 0.7 ? "bg-red-500 text-white" : ""}
                ${risk > 0.4 && risk <= 0.7 ? "bg-yellow-400 text-black" : ""}
                ${risk <= 0.4 ? "bg-green-500 text-white" : ""}`}
            >
              {risk.toFixed(3)}
            </span>
          </div>
        )}

        {error && (
          <div className="mt-4 text-center text-red-600 font-semibold">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
