#!/bin/bash

# Wait for the database to be ready
sleep 10  # Give more time for the database to be ready

# Run the Python script
python3 << 'EOF'
import pandas as pd
import os
from sqlalchemy import create_engine

print("Reading CSV file...")
df = pd.read_csv('/data/PredictedData/df_values.csv')

print("Processing data...")
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

print("\nSample of processed data:")
print(yearly_averages.head())

# Create database connection
print("\nConnecting to database...")
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student:infomdss@db_dashboard:5432/dashboard')
engine = create_engine(DATABASE_URL)

# Create table and insert data
print("\nCreating table in database...")
table_name = 'yearly_averages'
yearly_averages.to_sql(table_name, engine, if_exists='replace', index=True)

print(f"\nCreated table {table_name} with shape: {yearly_averages.shape}")
EOF