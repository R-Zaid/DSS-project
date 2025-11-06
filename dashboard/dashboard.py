import streamlit as st
import geopandas as gpd
import plotly.express as px
import os
import pandas as pd
from streamlit_folium import st_folium
import folium
from src.scripts.NO2_map import draw_no2_map, load_geodata, build_map
from src.scripts.LEZ_map_new import draw_LEZ_map_new
from src.scripts.NO2_API import draw_measures_chart
import streamlit.components.v1 as components
from sqlalchemy import create_engine
import os

# Create database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student:infomdss@db_dashboard:5432/dashboard')
engine = create_engine(DATABASE_URL)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_map_data(year, measurement, data_year):
    """Cache the map data preparation to prevent unnecessary recomputation"""
    map_data = pd.DataFrame()
    map_data['RegioS'] = data_year['Province']
    
    
    map_data['value'] = values
    return map_data

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")


def load_series_data(measurement: str, province: str = None) -> pd.DataFrame:
    """Return the full yearly-series DataFrame from the database."""
    try:
        # Query data from the database
        query = """
        SELECT 
            "Year",
            "RegioS" as "Province",
            "Average NO2 Value" as "NO2",
            "Average PM2.5 Value" as "PM2.5",
            "Average PM10 Value" as "PM10"
        FROM mean_yearlyvalues
        WHERE "Average NO2 Value" IS NOT NULL 
        OR "Average PM2.5 Value" IS NOT NULL 
        OR "Average PM10 Value" IS NOT NULL
        """
        
        if province:
            query += f" AND \"RegioS\" = '{province}'"
            
        df = pd.read_sql_query(query, engine)
        print("DEBUG: Loading series data for measurement:", measurement)
        print("DEBUG: Original columns:", df.columns.tolist())
        
        # Convert values to numeric
        for col in ['NO2', 'PM2.5', 'PM10']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Normalize province names
        province_mapping = {
            'Noord-Brabant': 'Brabant',
        }
        df['Province'] = df['Province'].replace(province_mapping)
        
        print("DEBUG: Final data shape:", df.shape)
        print("DEBUG: Sample of values for", measurement, ":", df[measurement].head())
        
        return df
        
    except Exception as e:
        print(f"Error loading data from database: {e}")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['Year', 'Province', 'NO2', 'PM2.5', 'PM10'])


def load_processed_data(year: int, measurement: str, province: str = None) -> pd.DataFrame:
    df = load_series_data(measurement, province)
    if df is not None and 'Year' in df.columns:
        return df[df["Year"] == year]
    return pd.DataFrame()

# ---------- STYLES ----------
st.markdown("""
    <style>
    .main {
        background-color: #0b132b;
        color: #ffffff;
    }
    .stSlider label, .stSelectbox label {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# (old global updater removed) - we now use cached loaders below

# ---------- SIDEBAR ----------
st.sidebar.header("Controls")
start_year = 1990
end_year = 2030
year = st.sidebar.slider("Select Year", start_year, end_year, 2024)
measurement = st.sidebar.selectbox("Select Measurement", ["NO2", "PM2.5", "PM10", "LEZ"])
province = st.sidebar.selectbox("Select Province", [
                                                    "Brabant",
                                                    "Drenthe", 
                                                    "Flevoland", 
                                                    "Friesland", 
                                                    "Groningen", 
                                                    "Gelderland",
                                                    "Limburg",
                                                    "Noord-Holland",
                                                    "Overijssel", 
                                                    "Utrecht",
                                                    "Zeeland",
                                                    "Zuid-Holland",
                                                    ])
# Toggle for LEZ overlay when showing NO2 base map

# Load per-year slice and the full series (small, compact loaders)
data_year = load_processed_data(year, measurement, province)



# Data has already been loaded above

series = load_series_data(measurement, province)

# ---------- MAP ----------
# Prepare data for the map
st.subheader("Air Quality Map")

if measurement == "LEZ":
    # Handle LEZ map
    folium_map = draw_LEZ_map_new()
    if isinstance(folium_map, str):
        components.html(folium_map, width=700, height=500, key="lez_map_html")
    else:
        st_folium(folium_map, width=700, height=500, key="lez_map_folium")
else:
    try:
        print("\nDEBUG: Preparing map data")
        print("Available columns:", data_year.columns.tolist())
        
        # Scale the values to make them more visible on the map
        map_data = pd.DataFrame()
        map_data['province'] = data_year['Province']  # Changed from RegioS to province to match the map expectations
        
        if measurement in data_year.columns:
            values = data_year[measurement]
            map_data['value'] = values  # Use original values without scaling
            print("DEBUG: Original values:", values)
            
            # Only scale for visualization if needed
            if values.min() < 0 or values.max() > 150:  # NO2 scale typically goes up to 150
                min_val = values.min()
                max_val = values.max()
                if not pd.isna(min_val) and not pd.isna(max_val) and max_val > min_val:
                    map_data['value'] = ((values - min_val) / (max_val - min_val)) * 150  # Scale to AQI range
                else:
                    map_data['value'] = values
            
            print("DEBUG: Value range:", map_data['value'].min(), "-", map_data['value'].max())
            print("DEBUG: Final map_data:")
            print(map_data)
            
            # Create map with the prepared data using a unique key based on year and measurement
            map_key = f"{year}_{measurement}"
            folium_map = draw_no2_map(year, measurement, map_data)
            
            if isinstance(folium_map, str):
                components.html(folium_map, width=700, height=500, key=f"map_html_{map_key}")
            else:
                st_folium(folium_map, width=700, height=500, key=f"map_folium_{map_key}")
        else:
            print(f"DEBUG: Measurement {measurement} not found in columns")
            st.warning(f"No data available for {measurement}")
            
    except Exception as e:
        st.error(f"Error loading map: {str(e)}")
        st.write("Data available:", data_year.columns.tolist())


# ---------- METRICS ----------
col1, col2 = st.columns(2)
with col1:
    # Determine column name used in data_year / series
    measurement_map = {"NO2": "NO2", "PM2.5": "PM2.5", "PM10": "PM10", "LEZ": "LEZ"}
    mapped_measure = measurement_map.get(measurement, measurement)

    print(f"DEBUG: Looking for measurement '{mapped_measure}' in columns: {data_year.columns.tolist()}")
    
    avg_value = None
    try:
        if mapped_measure in data_year.columns:
            avg_value = data_year[mapped_measure].iloc[0]
        elif 'value' in data_year.columns:
            avg_value = data_year['value'].mean()
    except Exception:
        avg_value = None

    if avg_value is not None:
        st.metric(f"Average {measurement} Value", f"{avg_value:.1f}")
    else:
        print("WARNING: No valid average value found")
        st.metric(f"Average {measurement} Value", "n.v.t.")

with col2:
    st.metric("Prediction Index", "4.93%", delta="-0.12%")



#---------------- API CALLS ----------------
# Cache the API calls with a 1-hour refresh interval
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_measures_chart(measurement: str) -> str:
    """Cache the measures chart to prevent unnecessary API calls"""
    return draw_measures_chart(measurement=measurement)

# Preload data for all measurement types in the background
@st.cache_data(ttl=3600)
def preload_all_measurements():
    """Preload data for all measurement types"""
    return {
        m: get_cached_measures_chart(m)
        for m in ["NO2", "PM2.5", "PM10"]
    }

# Initialize the preloaded data in the background
if 'preloaded_data' not in st.session_state:
    st.session_state['preloaded_data'] = preload_all_measurements()

# Display API data
if not (measurement == "LEZ"):
    try:
        # Use preloaded data if available, otherwise fetch it
        if measurement in st.session_state['preloaded_data']:
            bar_NO2_clean_html = st.session_state['preloaded_data'][measurement]
        else:
            with st.spinner("Loading measures chart..."):
                bar_NO2_clean_html = get_cached_measures_chart(measurement)
        st.components.v1.html(bar_NO2_clean_html, height=500)
    except Exception as e:
        st.error(f"Error loading measures chart: {str(e)}")


# ---------- LINE CHART ----------
st.subheader(f"Average Yearly {measurement} Value for {province}")

# Prepare series for the chosen measurement for the line chart
year_col = next((c for c in series.columns if c.lower() == 'year'), 'Year')
plot_y = mapped_measure if mapped_measure in series.columns else next((c for c in series.columns if measurement.lower().replace('₂','2') in c.lower().replace('₂','2')), None)
if plot_y is None:
    # fallback: try 'value' column
    plot_y = 'value' if 'value' in series.columns else None

# Create the line chart with the data for the selected province
fig = None
if plot_y is not None:
    # Filter data for the selected province and years >= 2019
    province_data = series[
        (series['Province'] == province) & 
        (series[year_col] >= 2016)
    ].copy()  # Create a copy to avoid SettingWithCopyWarning
    
    if not province_data.empty:
        # Scale the values if they're outside a reasonable range
        if plot_y in province_data.columns:
            values = province_data[plot_y]
            
            # Define reasonable ranges for each measurement type
            ranges = {
                "NO2": (0, 70),    # Typical NO2 range in µg/m³
                "PM2.5": (0, 70),   # Typical PM2.5 range in µg/m³
                "PM10": (0, 70),   # Typical PM10 range in µg/m³
            }

            fig = px.line(
                province_data,
                x=year_col,
                y=plot_y,
                title=f"Average Yearly {measurement} Value for {province}",
                markers=True,
                template="plotly_dark",
            )
            
            # Customize the layout
            fig.update_layout(
                yaxis_title=f"{measurement} Concentration (µg/m³)",
                xaxis_title="Year",
                yaxis=dict(
                    gridcolor="#1a1a1a",
                    range=[0, ranges.get(measurement, (0, 100))[1]]  # Set y-axis range
                ),
                xaxis=dict(
                    gridcolor="#1a1a1a",
                    dtick=1  # Show all years
                )
            )
            
            # Add hover data to show exact values
            fig.update_traces(
                hovertemplate=f"Year: %{{x}}<br>{measurement}: %{{y:.1f}} µg/m³<extra></extra>",
                line=dict(width=3),  # Make the line thicker
                marker=dict(size=8)  # Make the markers larger
            )
fig.update_layout(
    title_x=0.5,
    margin=dict(l=20, r=20, t=40, b=20),
    plot_bgcolor="#0b132b",
    paper_bgcolor="#0b132b",
)
if fig is not None:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No time-series data available for the selected measurement.")
