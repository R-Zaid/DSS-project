#!/bin/bash

# Function to test database connection
wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."
    while ! pg_isready -h db_dashboard -U student -d dashboard; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 2
    done
    echo "PostgreSQL is up and ready!"
}

# Wait for database to be ready
wait_for_postgres

# Run the data loading script
echo "Loading data into database..."
python /app/load_yearly_averages.py || { echo "Failed to load data"; exit 1; }

# Start Streamlit
echo "Starting Streamlit application..."
streamlit run /app/dashboard.py