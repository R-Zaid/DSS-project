import pandas as pd
from sqlalchemy import create_engine
import os

# Read the CSV file
csv_path = '/data/PredictedData/combined_historical_and_future_yearly_averages.csv'
df = pd.read_csv(csv_path)

# Create database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student:infomdss@db_dashboard:5432/dashboard')
engine = create_engine(DATABASE_URL)

# Load data into database
# If table exists, replace it
df.to_sql('yearly_averages', engine, if_exists='replace', index=False)

print("Data loaded successfully into the yearly_averages table!")