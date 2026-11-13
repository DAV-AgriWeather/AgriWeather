
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR / "analysis_results"
CHART_DIR = BASE_DIR / "visualisations"

CHART_DIR.mkdir(exist_ok=True)

# Load analysis results
weather = pd.read_csv(RESULT_DIR / "weather_summary.csv")
crops = pd.read_csv(RESULT_DIR / "crop_suitability_analysis.csv")

# --------------------------------
# 1. WEATHER STATISTICS CHART
# --------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    weather["Parameter"],
    weather["Average"]
)

plt.title("AgriWeather - Average Weather Conditions")
plt.xlabel("Weather Parameters")
plt.ylabel("Average Value")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(CHART_DIR / "weather_analysis.png")
plt.show()

# --------------------------------
# 2. CROP SUITABILITY CHART
# --------------------------------

plt.figure(figsize=(12, 6))

plt.bar(
    crops["Crop_Name"],
    crops["Match_Score"].str.replace("/2", "").astype(int)
)

plt.title("AgriWeather - Crop Suitability Analysis")
plt.xlabel("Crop Name")
plt.ylabel("Matching Criteria (Out of 2)")
plt.ylim(0, 2)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(CHART_DIR / "crop_suitability.png")
plt.show()

print("\nVisualisation completed successfully!")
print("Charts saved in the visualisations folder.")
