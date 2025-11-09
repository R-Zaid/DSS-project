import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

def get_sarimax_forecasts(db_path):
    """
    Retrieve SARIMAX forecasts from the database and prepare them for visualization
    """
    # Create database connection
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Read the forecasts from the database
    query = "SELECT * FROM predicted_values_2025_2030"
    df = pd.read_sql(query, engine)
    
    return df

def create_forecast_plot(df, pollutant_type, region=None):
    """
    Create a line plot for the specified pollutant forecast
    """
    # Map 'Brabant' to 'Noord-Brabant' for region filtering
    if region:
        region_map = {
            'Brabant': 'Noord-Brabant',
            'Noord-Brabant': 'Noord-Brabant'
        }
        region_query = region_map.get(region, region)
        df = df[df['RegioS'] == region_query]
    
    # Map pollutant type to column name
    pollutant_map = {
        'NO2': 'Average NO2 Value',
        'PM2.5': 'Average PM2.5 Value',
        'PM10': 'Average PM10 Value'
    }
    
    column = pollutant_map.get(pollutant_type)
    if not column:
        raise ValueError(f"Invalid pollutant type: {pollutant_type}")
    
    title = f"Predicted {pollutant_type} Values (2025-2030)"

    
    import plotly.graph_objects as go
    import numpy as np

    # Base line chart for actual forecast values
    fig = px.line(df, x='Year', y=column, markers=True, title=title)

    # Example: scale LEZ area and show impact for several factors (demo, not real prediction)
    # You may want to replace this with your actual model prediction logic
    # For demo, we use the last value and year, and scale it for 4 factors
    area = 1000  # Placeholder, replace with real area if available
    lastyear = df['Year'].max()
    lastvalueyear = df[column].iloc[-1]
    factor = [1.5, 2, 2.5, 3]

    for factors in factor:
        areapred = np.linspace(area, area * factors, 7).reshape(-1, 1)
        futurepred = np.arange(lastyear, lastyear + 7).reshape(-1, 1)
        xpred = np.concatenate((areapred, futurepred), axis=1)
        # ypred should be replaced with your model's prediction, here we just scale the last value for demo
        ypred = np.linspace(lastvalueyear, lastvalueyear * factors, 7)
        xyear = np.arange(lastyear, lastyear + 7)
        fig.add_trace(go.Scatter(x=xyear, y=np.insert(ypred, 0, lastvalueyear), mode='lines+markers', name=f'Scaling with factor {factors}'))

    fig.update_layout(legend_title_text="Factor")
    return fig