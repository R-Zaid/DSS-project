import pandas as pd
from sqlalchemy import create_engine
import os
import sys
from sqlalchemy.exc import SQLAlchemyError

try:
    # Read the CSV file
    csv_path = '/app/data/PredictedData/combined_historical_and_future_yearly_averages.csv'
    print(f"Attempting to read CSV from: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        print("Current directory contents:")
        os.system("ls -R /app")
        sys.exit(1)
        
    df = pd.read_csv(csv_path)
    print(f"Successfully read CSV file with {len(df)} rows")

    # Create database connection
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student:infomdss@db_dashboard:5432/dashboard')
    print(f"Connecting to database: {DATABASE_URL}")
    
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as conn:
        print("Successfully connected to database")
        
    # Load data into database
    print("Starting data upload to database...")
    df.to_sql('yearly_averages', engine, if_exists='replace', index=False)
    print("Data loaded successfully into the yearly_averages table!")
    
except FileNotFoundError as e:
    print(f"Error: Could not find the CSV file: {e}")
    sys.exit(1)
except SQLAlchemyError as e:
    print(f"Database error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)