#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run the data loading script
echo "Loading data into database..."
python /app/load_yearly_averages.py

# Start Streamlit
echo "Starting Streamlit application..."
streamlit run dashboard.py