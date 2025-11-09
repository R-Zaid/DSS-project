import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# Your data as a string
data_str = """Year,PM10,PM25,NO2,Scaling
2024,15.10135196,8.19545943,11.48389581,1.0
2025,14.69828583,7.88148613,10.55002896,1.0
2026,14.29521969,7.56751282,9.6161621,1.0
2027,13.89215355,7.25353952,8.68229525,1.0
2028,13.48908741,6.93956622,7.74842839,1.0
2029,13.08602128,6.62559292,6.81456153,1.0
2030,12.68295514,6.31161961,5.88069468,1.0
2024,15.10135196,8.19545943,11.48389581,1.25
2025,14.55836254,7.78047164,10.41627015,1.25
2026,14.01537313,7.36548385,9.34864449,1.25
2027,13.47238371,6.95049606,8.28101883,1.25
2028,12.92939429,6.53550827,7.21339317,1.25
2029,12.38640487,6.12052048,6.14576751,1.25
2030,11.84341546,5.70553269,5.07814185,1.25
2024,15.10135196,8.19545943,11.48389581,1.5
2025,14.41843926,7.67945715,10.28251135,1.5
2026,13.73552657,7.16345488,9.08112688,1.5
2027,13.05261387,6.6474526,7.87974241,1.5
2028,12.36970117,6.13145032,6.67835795,1.5
2029,11.68678847,5.61544804,5.47697348,1.5
2030,11.00387577,5.09944577,4.27558901,1.5
2024,15.10135196,8.19545943,11.48389581,1.75
2025,14.27851598,7.57844267,10.14875254,1.75
2026,13.45568001,6.9614259,8.81360927,1.75
2027,12.63284403,6.34440914,7.478466,1.75
2028,11.81000805,5.72739237,6.14332273,1.75
2029,10.98717207,5.11037561,4.80817946,1.75
2030,10.16433609,4.49335884,3.47303618,1.75"""

def create_forecast_plot(measurement='ALL'):
    """
    Create a line plot showing pollutants with different scaling factors
    Args:
        measurement (str): 'NO2', 'PM2.5', 'PM10', or 'ALL' to show all pollutants
    """
    # Convert string data to DataFrame
    df = pd.read_csv(StringIO(data_str))

    # Create the figure
    fig = go.Figure()

    # Color schemes for different scaling factors
    colors = {
        1.0: '#1f77b4',    # blue
        1.25: '#ff7f0e',   # orange
        1.5: '#2ca02c',    # green
        1.75: '#d62728'    # red
    }

    # Map measurement names to DataFrame columns
    measure_map = {
        'NO2': 'NO2',
        'PM2.5': 'PM25',
        'PM10': 'PM10'
    }

    # Determine which measurements to plot
    if measurement == 'ALL':
        measurements_to_plot = list(measure_map.keys())
    else:
        measurements_to_plot = [measurement]

    # Add traces for each scaling factor
    for scaling in df['Scaling'].unique():
        df_scale = df[df['Scaling'] == scaling]
        
        for measure in measurements_to_plot:
            column = measure_map[measure]
            fig.add_trace(go.Scatter(
                x=df_scale['Year'],
                y=df_scale[column],
                mode='lines',
                name=f'{measure} (Scaling {scaling})',
                line=dict(color=colors[scaling])
            ))

    # Update layout
    title = 'Air Quality Predictions with Different Scaling Factors (2024-2030)' if measurement == 'ALL' else f'{measurement} Predictions with Different Scaling Factors (2024-2030)'
    
    fig.update_layout(
        title=title,
        xaxis_title='Year',
        yaxis_title=f'Concentration (µg/m³)',
        legend_title='Pollutant (Scaling Factor)',
        template='plotly_white',
        hovermode='x unified',
        width=1200,
        height=800
    )

    # Update x-axis to show all years
    fig.update_xaxes(dtick=1)

    return fig