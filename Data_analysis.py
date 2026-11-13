
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent
CLEAN_DIR = BASE_DIR / "clean_dataset"
RESULT_DIR = BASE_DIR / "analysis_results"

RESULT_DIR.mkdir(exist_ok=True)

# Load cleaned datasets
weather = pd.read_csv(CLEAN_DIR / "weather_daily.csv")
soil = pd.read_csv(CLEAN_DIR / "soil_data.csv")
crops = pd.read_csv(CLEAN_DIR / "crop_data.csv")

# --------------------------------
# 1. WEATHER ANALYSIS
# --------------------------------

weather_summary = pd.DataFrame({
    "Parameter": ["Maximum Temperature", "Minimum Temperature",
                  "Rainfall", "Rain Probability"],
    "Average": [
        weather["Temperature_Max"].mean(),
        weather["Temperature_Min"].mean(),
        weather["Rainfall_mm"].mean(),
        weather["Rain_Probability_Percent"].mean()
    ],
    "Minimum": [
        weather["Temperature_Max"].min(),
        weather["Temperature_Min"].min(),
        weather["Rainfall_mm"].min(),
        weather["Rain_Probability_Percent"].min()
    ],
    "Maximum": [
        weather["Temperature_Max"].max(),
        weather["Temperature_Min"].max(),
        weather["Rainfall_mm"].max(),
        weather["Rain_Probability_Percent"].max()
    ]
})

weather_summary.to_csv(
    RESULT_DIR / "weather_summary.csv", index=False
)

# Average forecast temperature
average_temperature = (
    weather["Temperature_Max"].mean()
    + weather["Temperature_Min"].mean()
) / 2

# --------------------------------
# 2. SOIL ANALYSIS
# --------------------------------

average_soil_ph = soil["pH"].mean()

# --------------------------------
# 3. CROP SUITABILITY ANALYSIS
# --------------------------------

results = []

for _, crop in crops.iterrows():

    # Check temperature compatibility
    temp_ok = (
        crop["Temperature_Tolerance_Min_C"]
        <= average_temperature
        <= crop["Temperature_Tolerance_Max_C"]
    )

    # Check soil pH compatibility
    ph_ok = (
        crop["Preferred_Soil_pH_Min"]
        <= average_soil_ph
        <= crop["Preferred_Soil_pH_Max"]
    )

    score = int(temp_ok) + int(ph_ok)

    if score == 2:
        status = "Suitable based on available checks"
    elif score == 1:
        status = "Partially suitable"
    else:
        status = "Not suitable based on available checks"

    results.append({
        "Crop_Name": crop["Crop_Name"],
        "Average_Forecast_Temperature_C": round(
            average_temperature, 2
        ),
        "Average_Soil_pH": round(average_soil_ph, 2),
        "Temperature_Match": temp_ok,
        "Soil_pH_Match": ph_ok,
        "Match_Score": f"{score}/2",
        "Suitability_Status": status
    })

crop_analysis = pd.DataFrame(results)

crop_analysis.to_csv(
    RESULT_DIR / "crop_suitability_analysis.csv",
    index=False
)

# --------------------------------
# 4. DISPLAY RESULTS
# --------------------------------

print("\n===== WEATHER ANALYSIS =====")
print(weather_summary)

print("\nAverage forecast temperature:",
      round(average_temperature, 2), "°C")

print("\nAverage soil pH:",
      round(average_soil_ph, 2))

print("\n===== CROP SUITABILITY ANALYSIS =====")
print(crop_analysis.to_string(index=False))

print("\nAnalysis completed successfully!")
print("Results saved in the analysis_results folder.")
