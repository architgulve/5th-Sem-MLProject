"use client";
import React, { useState } from "react";

const label = "font-semibold text-gray-300 mb-2 block text-sm uppercase tracking-wide";

export default function App() {
  const [student, setStudent] = useState({});
  const [risk, setRisk] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const setField = (field, value) =>
    setStudent((prev) => ({ ...prev, [field]: value }));

  const handlePredict = async () => {
    setError("");
    setRisk(null);
    setLoading(true);

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
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 flex items-center justify-center p-6">
      <div className="w-full max-w-5xl bg-gray-800/50 backdrop-blur-xl rounded-3xl shadow-2xl p-12 space-y-8 border border-purple-500/30">
        <div className="text-center space-y-3">
          <div className="text-7xl mb-3 animate-bounce">🎓</div>
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
            Student Dropout Risk Predictor
          </h1>
          <p className="text-gray-400 text-base">Predict student retention with AI-powered analytics</p>
        </div>

        {/* --- DROPDOWNS --- */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

          <div className="group">
            <label className={label}>Gender</label>
            <select
              className="w-full border-2 border-gray-700 bg-gray-900/80 text-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-500/30 p-3 rounded-xl transition-all duration-200 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20"
              onChange={(e) => setField("gender", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="gender_M">Male</option>
              <option value="gender_F">Female</option>
            </select>
          </div>

          <div className="group">
            <label className={label}>Age Band</label>
            <select
              className="w-full border-2 border-gray-700 bg-gray-900/80 text-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-500/30 p-3 rounded-xl transition-all duration-200 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20"
              onChange={(e) => setField("age_band", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="age_band_0-35">0–35</option>
              <option value="age_band_35-55">35–55</option>
              <option value="age_band_55<=">55+</option>
            </select>
          </div>

          <div className="group">
            <label className={label}>Region</label>
            <select
              className="w-full border-2 border-gray-700 bg-gray-900/80 text-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-500/30 p-3 rounded-xl transition-all duration-200 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20"
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

          <div className="group">
            <label className={label}>Highest Education</label>
            <select
              className="w-full border-2 border-gray-700 bg-gray-900/80 text-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-500/30 p-3 rounded-xl transition-all duration-200 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20"
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

          <div className="group">
            <label className={label}>IMD Band</label>
            <select
              className="w-full border-2 border-gray-700 bg-gray-900/80 text-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-500/30 p-3 rounded-xl transition-all duration-200 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20"
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

          <div className="group">
            <label className={label}>Disability</label>
            <select
              className="w-full border-2 border-gray-700 bg-gray-900/80 text-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-500/30 p-3 rounded-xl transition-all duration-200 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20"
              onChange={(e) => setField("disability", e.target.value || null)}
            >
              <option value="">Select</option>
              <option value="disability_N">No</option>
              <option value="disability_Y">Yes</option>
            </select>
          </div>
        </div>

        {/* --- NUMERIC INPUTS --- */}
        <div className="border-t-2 border-purple-500/30 pt-8 mt-8">
          <h2 className="text-2xl font-bold text-gray-200 mb-6 flex items-center gap-2">
            <span className="text-3xl">📊</span>
            Academic Metrics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

            {[
              { key: "num_of_prev_attempts", label: "Previous Attempts", min: 0, max: 10 },
              { key: "studied_credits", label: "Studied Credits", min: 0, max: 600 },
              { key: "date_registration", label: "Registration Date", min: -365, max: 365 },
              { key: "vle_total_clicks", label: "VLE Total Clicks", min: 0, max: 100000 },
              { key: "vle_days_active", label: "VLE Days Active", min: 0, max: 365 },
              { key: "vle_first14", label: "VLE First 14 Days", min: 0, max: 14 },
              { key: "vle_first28", label: "VLE First 28 Days", min: 0, max: 28 },
              { key: "avg_assessment_score", label: "Avg Assessment Score", min: 0, max: 100 },
              { key: "n_submissions", label: "Number of Submissions", min: 0, max: 50 },
            ].map(({ key, label: fieldLabel, min, max }) => (
              <div key={key} className="group">
                <label className={label}>{fieldLabel}</label>
                <input
                  type="number"
                  placeholder="0"
                  min={min}
                  max={max}
                  className="w-full border-2 border-gray-700 bg-gray-900/80 text-gray-200 placeholder-gray-500 focus:border-purple-500 focus:ring-4 focus:ring-purple-500/30 p-3 rounded-xl transition-all duration-200 hover:border-purple-400 hover:shadow-lg hover:shadow-purple-500/20"
                  onChange={(e) =>
                    setField(key, Number(e.target.value) || 0)
                  }
                />
              </div>
            ))}
          </div>
        </div>

        {/* BUTTON */}
        <button
          onClick={handlePredict}
          disabled={loading}
          className="w-full py-4 bg-gradient-to-r from-cyan-600 via-purple-600 to-pink-600 hover:from-cyan-500 hover:via-purple-500 hover:to-pink-500 text-white font-bold rounded-xl text-lg shadow-2xl shadow-purple-500/50 hover:shadow-purple-400/70 transform hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              Predicting...
            </span>
          ) : (
            "🔮 Predict Dropout Risk"
          )}
        </button>

        {/* RESULT */}
        {risk !== null && (
          <div className="text-center mt-8 p-8 bg-gradient-to-br from-gray-800/80 to-purple-900/50 rounded-2xl border-2 border-purple-500/50 shadow-2xl shadow-purple-500/30">
            <p className="text-xl font-semibold text-gray-300 mb-4">Predicted Risk Score</p>
            <div className="flex flex-col items-center gap-4">
              <span
                className={`inline-block px-10 py-5 text-4xl font-extrabold rounded-2xl shadow-2xl transform transition-all duration-300 hover:scale-110
                  ${risk > 0.7 ? "bg-gradient-to-r from-red-600 to-red-700 text-white shadow-red-500/50" : ""}
                  ${risk > 0.4 && risk <= 0.7 ? "bg-gradient-to-r from-yellow-500 to-orange-500 text-black shadow-orange-500/50" : ""}
                  ${risk <= 0.4 ? "bg-gradient-to-r from-emerald-600 to-green-700 text-white shadow-green-500/50" : ""}`}
              >
                {(risk * 100).toFixed(1)}%
              </span>
              <p className="text-sm text-gray-400">
                {risk > 0.7 && "⚠️ High Risk - Immediate intervention recommended"}
                {risk > 0.4 && risk <= 0.7 && "⚡ Moderate Risk - Monitor and support"}
                {risk <= 0.4 && "✅ Low Risk - Student on track"}
              </p>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 bg-red-900/30 border-2 border-red-500/50 rounded-xl text-center">
            <p className="text-red-400 font-semibold flex items-center justify-center gap-2">
              <span className="text-2xl">⚠️</span>
              {error}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}