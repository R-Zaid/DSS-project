import pandas as pd
import os
from sqlalchemy import create_engine

# Read the CSV file
df = pd.read_csv('../../data/PredictedData/df_values.csv')

# Extract year from Year_Month column
df['Year'] = pd.to_datetime(df['Year_Month']).dt.year

# Calculate yearly averages for each province
yearly_averages = df.groupby(['Year', 'Province']).agg({
    'Average NO2 Value': 'mean',
    'Average PM2.5 Value': 'mean',
    'Average PM10 Value': 'mean'
}).reset_index()

# Rename columns to match mean_yearlyvalues format
yearly_averages = yearly_averages.rename(columns={
    'Province': 'RegioS',
})

# Create database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student:infomdss@db_dashboard:5432/dashboard')
engine = create_engine(DATABASE_URL)

# Create table and insert data
table_name = 'yearly_averages'
yearly_averages.to_sql(table_name, engine, if_exists='replace', index=True)

print(f"Created table {table_name} with shape: {yearly_averages.shape}")
print("\nSample of the data:")
print(yearly_averages.head())