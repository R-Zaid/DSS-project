import pandas as pd
import plotly.express as px
from flask import Flask, render_template_string, render_template, send_from_directory
from sqlalchemy import create_engine, text, inspect, Table
import os
from src.scripts.NO2_API import draw_NO2_chart, draw_NO2_province_chart

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student:infomdss@db_dashboard:5432/dashboard')

# Initialize the Flask application, change the normal format of flask to normal express format
app = Flask(__name__, template_folder='src/html', static_folder='src/style' )
def start_app():
    # preprocess everything

    # load everything

    print("Starting app...")
    # return web page
    return render_template('index.html', bar_NO2_clean=draw_NO2_chart(), bar_NO2_province=draw_NO2_province_chart()) 

@app.route('/')
def index():
    # As soon as the page is loaded, the data is retrieved from the db and the graph is created
    # And is put in the HTML div
    
    return start_app() #render_template('index.html', plot_html=generate_population_graph())

@app.route('/test-db')
def test_db():
    """Test database connection"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return "Database connectios successful!" + str(result.fetchone()[0])
    except Exception as e:
        return f"Database connection failed: {e}"
    
@app.route('/map')
def map_view():
    # render the dashboard.tsx file (serve it as a static file for development)

    return render_template('dashboard.html') 



if __name__ == '__main__':
    # Test database connection on startup but don't fail if it doesn't work
    # Run in debug mode to reload on code changes
    print("Testing database connection...")
    app.run(debug=True, host='0.0.0.0')