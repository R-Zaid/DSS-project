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


def get_no2_mean():
    # simulate data
    return pd.DataFrame({
        "RegioS": ["Groningen", "Friesland", "Drenthe", "Overijssel", "Flevoland", "Gelderland", "Utrecht", "Noord-Holland", "Zuid-Holland", "Zeeland", "Noord-Brabant", "Limburg"],
        "value": [15, 20, 18, 30, 25, 35, 40, 50, 55, 22, 45, 60]
    })
   

def attach_no2_mean(gdf: pd.DataFrame, meanprovince: pd.DataFrame) -> pd.DataFrame: 
    mp = meanprovince.copy() # so province matches  meanprovince -
    mp["province"] = mp["RegioS"].apply(norm_prov)
    mean_map = dict(zip(mp["province"], mp["value"]))   # province -> NO2_mean 
    # add NO2_mean to gdf via with matching province name 
    gdf["NO2_mean"] = gdf["province"].map(mean_map)
    return gdf



def legenda(m, bins=AQI_NO2, title="Air Quality (NO₂)", unit="µg/m³"):
    items = sorted(((lo, hi, lbl, col) for (lo, hi), (lbl, col) in bins.items()), key=lambda t: t[0])
    rows = "".join(
        f'<div style="display:flex;align-items:center;margin:4px 0">'
        f'<span style="background:{col};width:12px;height:12px;border:1px solid #555;margin-right:8px"></span>'
        f'<span style="font-size:12px">{lbl} '
        f'<span style="color:#777">({int(lo)}–{("∞" if not math.isfinite(hi) else int(hi))} {unit})</span></span>'
        f'</div>' for lo, hi, lbl, col in items
    )
    html = ('<div style="position:fixed;bottom:20px;left:20px;z-index:9999;background:#fff;'
            'padding:8px 10px;border:1px solid #bbb;border-radius:4px;box-shadow:0 1px 4px rgba(0,0,0,.2)">'
            f'<div style="font-weight:600;margin-bottom:6px">{title}</div>{rows}</div>')
    macro = MacroElement(); macro._template = Template("{% macro html(this, kwargs) %}"+html+"{% endmacro %}")
    m.get_root().add_child(macro)

def build_map(gdf: pd.DataFrame, center_lat: float = 52.2, center_lon: float = 5.3) -> folium.Map:
    #map
    # Get NO2 data and attach it to the GeoDataFrame before creating the map
    meanprovince = get_no2_mean()  # Fetch mean NO2 values
    gdf = attach_no2_mean(gdf, meanprovince)  # Attach mean NO2 values to the GeoDataFrame
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles="CartoDB Positron")
    for _, row in gdf.iterrows():
        prov = row["province"]
        geometry = row["geometry"]  # Use 'geometry' directly from GeoDataFrame
        mean_no2 = row.get("NO2_mean")
        color = no2_colour_pollution(mean_no2)
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
                f"{prov}<br>NO₂ (mean): {mean_no2:.2f} µg/m³" if pd.notna(mean_no2) else f"{prov}<br>NO₂: n.v.t."
            ),
        ).add_to(m)
    folium.LayerControl().add_to(m)

    return m

def draw_no2_map():
    # In Docker, data is mounted at /data, otherwise use relative path
    if os.path.exists("/data"):
        data_dir = "/data/processedData"
    else:
        # Fallback for local development
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "..", "..", "..", "data", "processedData")
        data_dir = os.path.normpath(data_dir)
    
    geojson_path = os.path.join(data_dir, "georef-netherlands-provincie.geojson")
    json_path = os.path.join(data_dir, "georef-netherlands-provincie.json")
    
    gdf = load_geodata(geojson_path, json_path)
    
    province_data = gdf[['prov_name', 'geometry']].copy() # provinces and geometry
    print(province_data)

    m = build_map(gdf, center_lat=52.2, center_lon=5.3)  #folium map nl 
    legenda(m)
    
    return m._repr_html_()


