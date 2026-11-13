
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "Dataset"
CLEAN_DIR = BASE_DIR / "clean_dataset"

# Create output folder
CLEAN_DIR.mkdir(exist_ok=True)

# Dataset files
files = {
    "weather_hourly": "weather_hourly.csv",
    "weather_daily": "weather_daily.csv",
    "soil_data": "soil_data.csv",
    "crop_data": "crop_data.csv"
}

for name, filename in files.items():
    input_file = DATASET_DIR / filename

    try:
        # Read CSV
        df = pd.read_csv(input_file)

        # Clean column names
        df.columns = df.columns.str.strip()

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove unnecessary spaces from text
        for column in df.select_dtypes(include="object").columns:
            df[column] = df[column].str.strip()

        # Save cleaned dataset
        output_file = CLEAN_DIR / filename
        df.to_csv(output_file, index=False)

        # Display summary
        print(f"\n{name} cleaned successfully!")
        print(f"Records: {len(df)}")
        print(f"Missing values:\n{df.isnull().sum()}")

    except FileNotFoundError:
        print(f"\nFile not found: {input_file}")

    except Exception as error:
        print(f"\nError processing {filename}: {error}")

print("\nData cleaning process completed.")
