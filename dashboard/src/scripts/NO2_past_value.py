import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def draw_monthly_no2_average():
     # In Docker, data is mounted at /data, otherwise use relative path
    if os.path.exists("/data"):
        csv_path = "/data/processedData/mean_no2_monthlyvalues.csv"
    else:
        # Fallback for local development
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "..", "..", "..", "data", "processedData", "mean_no2_monthlyvalues.csv")
        csv_path = os.path.normpath(csv_path)
    
    df_NO2 = pd.read_csv(csv_path)
    df_NO2 = df_NO2.iloc[12:]

    # Create the line plot
    fig = px.line(df_NO2, x='Year_Month', y='Average NO2 Value', 
                    title='Monthly National Average NO2 Levels')
    
    # Update layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Average NO2 Value (µg/m³)",
        height=400,
        showlegend=True
    )
    
    # Add horizontal line for max security value
    fig.add_hline(y=40, line_dash="dot", line_color="red", line_width=3,
                    annotation_text="Max security value 40 µg/m³")

    return fig.to_html(include_plotlyjs='cdn', div_id='monthly_NO2_average').replace('<html>', '').replace('</html>', '').replace('<head><meta charset="utf-8" /></head>', '')

