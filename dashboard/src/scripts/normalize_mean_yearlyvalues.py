"""
Small utility to normalize the mean_yearlyvalues.csv file:
- Replace 'Noord-Brabant' -> 'Brabant'
- Add a new column 'NO2' copied from 'Average NO2 Value' for compatibility
- Save file back using UTF-8

Run from repository root (PowerShell):
python .\dashboard\src\scripts\normalize_mean_yearlyvalues.py
"""
import os
import pandas as pd

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CSV_PATH = os.path.join(ROOT, "data", "ProcessedData", "mean_yearlyvalues.csv")

if not os.path.exists(CSV_PATH):
    print("CSV not found at", CSV_PATH)
    raise SystemExit(1)

print("Reading:", CSV_PATH)
df = pd.read_csv(CSV_PATH, dtype=str)

# Normalize RegioS values
if 'RegioS' in df.columns:
    df['RegioS'] = df['RegioS'].str.replace('Noord-Brabant', 'Brabant', regex=False)
    df['RegioS'] = df['RegioS'].str.strip()
else:
    print("Warning: 'RegioS' column not found in CSV. Columns:", df.columns.tolist())

# Add NO2 column copied from Average NO2 Value (if exists)
src_col = None
for candidate in ['Average NO2 Value', 'Average NO2 Value', 'NO2', 'NO2']:
    if candidate in df.columns:
        src_col = candidate
        break

if src_col:
    # coerce to numeric when possible
    df['NO2'] = pd.to_numeric(df[src_col], errors='coerce')
    print(f"Created 'NO2' column from '{src_col}'")
else:
    print("No NO2-like source column found; adding empty 'NO2' column")
    df['NO2'] = pd.NA

# Write back with utf-8 encoding
backup = CSV_PATH + '.bak'
if not os.path.exists(backup):
    os.rename(CSV_PATH, backup)
    print('Backup written to', backup)

df.to_csv(CSV_PATH, index=False, encoding='utf-8')
print('Updated CSV written to', CSV_PATH)
print(df.head(10).to_string())
