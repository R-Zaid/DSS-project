# Import necessary packages
import os
import math
import folium
from folium import plugins
import pandas as pd
import geopandas as gpd
import numpy as np
import requests
from branca.element import Template, MacroElement
import requests

AQI_NO2 = {
    (0, 10):           ("Good",           "green"),
    (10, 25):          ("Fair",           "yellow"),
    (25, 60):          ("Moderate",       "orange"),
    (60, 100):         ("Poor",           "red"),
    (100, 150):        ("Very Poor",      "darkred"),
    (150, math.inf):   ("Extremely Poor", "purple"),
}

def no2_colour_pollution(val): # colour based on no2 value range 
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return "gray"
    try:
        x = float(val)
    except (TypeError, ValueError):
        return "gray"
    for (lo, hi), (_label, color) in AQI_NO2.items():
        if lo <= x < hi:
            return color
    return "gray"


def norm_prov(p):                           # to allign province naam (Fryslân -> Friesland)
    if isinstance(p, list) and len(p) > 0:
        p = p[0]
    if isinstance(p, str):
        p = p.strip()
    return {"Fryslân": "Friesland"}.get(p, p)

# so no overlap in province name 
def load_geodata(geojson_path: str, json_path: str) -> gpd.GeoDataFrame: 
    gdf = gpd.read_file(geojson_path)
    df  = pd.read_json(json_path) 
   
    gdf['prov_name'] = df['prov_name']     
    gdf['province']  = gdf['prov_name'].apply(norm_prov)
    return gdf


def get_no2_mean(year: int = 2025, measurement: str = "NO2") -> pd.DataFrame:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.normpath(os.path.join(script_dir, "..", "..", "..", "data", "ProcessedData", "mean_yearlyvalues.csv"))
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.columns = [c.strip() for c in df.columns]
        
        # Map the column names
        column_mapping = {
            'Average NO2 Value': 'value',
            'RegioS': 'RegioS'
        }
        df = df.rename(columns=column_mapping)
        
        # Filter for the selected year
        df = df[df["Year"] == year]
        
        if 'value' not in df.columns:
            # Try to find the right column
            for col in df.columns:
                if 'NO2' in col or 'NO2' in col:
                    df['value'] = df[col]
                    break
        
        return df[['RegioS', 'value']]
        
    print("failed to find mean_yearlyvalues.csv")
    return pd.DataFrame(columns=["RegioS", "value"])

   

def attach_no2_mean(gdf: pd.DataFrame, meanprovince: pd.DataFrame) -> pd.DataFrame: 
    # Defensive: accept many possible column names for the region and value.
    mp = meanprovince.copy() if isinstance(meanprovince, pd.DataFrame) else pd.DataFrame()

    # Identify region column -> normalize to 'RegioS'
    if 'RegioS' not in mp.columns:
        regio_col = None
        for c in mp.columns:
            lc = c.lower()
            if 'regio' in lc or 'region' in lc or 'prov' in lc or 'province' in lc or 'name' in lc:
                regio_col = c
                break
        if regio_col:
            mp['RegioS'] = mp[regio_col]
        else:
            # No region column found: try index if it looks like names
            if mp.index.nlevels == 1 and mp.index.dtype == object:
                try:
                    mp = mp.reset_index()
                    mp.rename(columns={mp.columns[0]: 'RegioS'}, inplace=True)
                except Exception:
                    mp['RegioS'] = None
            else:
                mp['RegioS'] = None

    # Create normalized province names used for mapping
    mp['province'] = mp['RegioS'].apply(lambda x: norm_prov(x) if pd.notna(x) else x)

    # Identify value column -> normalize to 'value'
    if 'value' not in mp.columns:
        val_col = None
        for c in mp.columns:
            lc = c.lower()
            if lc in ('value', 'avg', 'average') or ('average' in lc) or ('mean' in lc) or (measure_in := False):
                # pick obvious candidates
                if pd.api.types.is_numeric_dtype(mp[c]) or mp[c].dtype == object:
                    val_col = c
                    break
        # fallback: any numeric column that's not year
        if val_col is None:
            for c in mp.columns:
                if c.lower() != 'year' and pd.api.types.is_numeric_dtype(mp[c]):
                    val_col = c
                    break
        if val_col:
            mp['value'] = pd.to_numeric(mp[val_col], errors='coerce')
        else:
            mp['value'] = np.nan

    # Build mapping province -> mean value
    try:
        mean_map = dict(zip(mp['province'].astype(str).str.strip(), mp['value']))
    except Exception:
        mean_map = {}

    # Add NO2_mean to gdf via matching province name
    # normalize gdf province column if present
    if 'province' in gdf.columns:
        gdf['province'] = gdf['province'].apply(lambda x: norm_prov(x) if pd.notna(x) else x)
    else:
        # if no province column, try prov_name
        if 'prov_name' in gdf.columns:
            gdf['province'] = gdf['prov_name'].apply(norm_prov)

    gdf['NO2_mean'] = gdf['province'].map(lambda p: mean_map.get(str(p).strip(), np.nan))
    return gdf



def legenda(m, bins=AQI_NO2, title="Air Quality (NO2)", unit="µg/m³"):
    """Add a legend to the map."""
    legend_html = '''
        {% macro html(this, kwargs) %}
        <div id="maplegend" style="position: absolute; z-index:9999; background-color:white; color: black;
             border-radius:6px; padding: 10px; font-size:12px; right: 10px; bottom: 20px;">
        <div style="font-weight:600;margin-bottom:6px; color: black;">''' + title + '''</div>
        '''
        
    items = sorted(((lo, hi, lbl, col) for (lo, hi), (lbl, col) in bins.items()), key=lambda t: t[0])
    
    for lo, hi, lbl, col in items:
        legend_html += f'''
            <div style="display:flex;align-items:center;margin:3px 0">
                <div style="background:{col};width:12px;height:12px;margin-right:8px;border:1px solid #555"></div>
                <span style="color: black;">{lbl} ({int(lo)}–{("∞" if not math.isfinite(hi) else int(hi))} {unit})</span>
            </div>
        '''
    
    legend_html += '''
        </div>
        <style>
        #maplegend {
            opacity: 0.9;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            transition: opacity 0.3s;
        }
        #maplegend:hover {
            opacity: 1;
        }
        </style>
        {% endmacro %}
    '''
    
    macro = MacroElement()
    macro._name = 'maplegend'
    macro._template = Template(legend_html)
    m.get_root().add_child(macro)

def build_map(year, measure, data, gdf: pd.DataFrame, center_lat: float = 52.2, center_lon: float = 5.3) -> folium.Map:
    print("DEBUG: Starting build_map")
    print("Input data:")
    print(data)
    
    # Create the base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles="CartoDB Positron"
    )

    # If no data provided, try to get it
    if data is None:
        print("DEBUG: No data provided, getting from get_no2_mean")
        data = get_no2_mean(year, measure)

    print("DEBUG: Data columns available:", data.columns.tolist() if isinstance(data, pd.DataFrame) else "No data")

    # Normalize the input data
    value_dict = {}
    if isinstance(data, pd.DataFrame):
        # First ensure we have a value column
        if 'value' not in data.columns:
            if measure in data.columns:
                data['value'] = data[measure]
            elif 'NO2' in data.columns:
                data['value'] = data['NO2']
                
        # Create value dictionary
        for idx, row in data.iterrows():
            region = None
            # Try different column names for region
            for col in ['province', 'Province', 'RegioS', 'prov_name']:
                if col in row.index:
                    region = row[col]
                    if isinstance(region, str):
                        region = norm_prov(region)
                        try:
                            value = row['value'] if 'value' in row else None
                            if pd.notnull(value):
                                value_dict[region] = float(value)
                                print(f"DEBUG: Added value {value} for region {region}")
                        except (ValueError, TypeError) as e:
                            print(f"DEBUG: Error converting value for {region}: {e}")
                        break

    print("DEBUG: Value dictionary:", value_dict)

    # Add GeoJson for each province
    for _, row in gdf.iterrows():
        prov = row['province']  # Normalized province name
        geometry = row['geometry']
        
        # Get the value for this province
        mean_no2 = value_dict.get(prov, None)
        print(f"DEBUG: Province {prov} has value {mean_no2}")
        
        # Get color based on value
        color = no2_colour_pollution(mean_no2)
        
        # Create the GeoJson layer
        folium.GeoJson(
            geometry,
            style_function=lambda _x, c=color: {
                "fillColor": c,
                "color": "black",
                "weight": 2,
                "fillOpacity": 0.55,
            },
            name=prov,
            tooltip=folium.Tooltip(
                f"{prov}<br>NO2 (mean): {mean_no2:.2f} µg/m³" if mean_no2 is not None else f"{prov}<br>NO2: n.v.t."
            ),
        ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)
    return m

def draw_no2_map(year: int = 2025, measure: str = "NO2", data: pd.DataFrame = None) -> folium.Map:
    print("DEBUG: Starting draw_no2_map with data:")
    if data is not None:
        print("Received data:")
        print(data)
    
    # In Docker, data is mounted at /data, otherwise use relative path
    if os.path.exists("/data"):
        data_dir = "/data/ProcessedData"  # Fixed capitalization
    else:
        # Fallback for local development
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "..", "..", "..", "data", "ProcessedData")
        data_dir = os.path.normpath(data_dir)
    
    print(f"DEBUG: Looking for geo files in {data_dir}")
    geojson_path = os.path.join(data_dir, "georef-netherlands-provincie.geojson")
    json_path = os.path.join(data_dir, "georef-netherlands-provincie.json")
    
    if not os.path.exists(geojson_path):
        print(f"WARNING: geojson file not found at {geojson_path}")
    if not os.path.exists(json_path):
        print(f"WARNING: json file not found at {json_path}")
    
    gdf = load_geodata(geojson_path, json_path)
    print("DEBUG: Loaded geodata:")
    print(gdf.columns.tolist())
    
    m = build_map(year, measure, data, gdf, center_lat=52.2, center_lon=5.3)
    legenda(m)
    return m


def draw_no2_map_html():  
    m = draw_no2_map()
    return m._repr_html_()  # return html representation for flask


