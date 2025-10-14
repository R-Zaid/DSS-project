import folium
import pandas as pd
import geopandas as gpd
import ast
import os

def draw_LEZ_map():
    
    center_lat = 52.2
    center_lon = 5.3

    m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=7,
            tiles='CartoDB Positron'
        )

    # In Docker, data is mounted at /data, otherwise use relative path
    if os.path.exists("/data"):
        data_dir = "/data/processedData"
    else:
        # Fallback for local development
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "..",  "..", "data", "processedData")
        data_dir = os.path.normpath(data_dir)

    print(data_dir)
    
    # Load NDW locations
    ndw_path = os.path.join(data_dir, "NDW_locations.csv")
    LEZ_location = pd.read_csv(ndw_path)
    LEZ_location.head()

    print(LEZ_location)

    LEZ_location['coordinate_sets_list'] = LEZ_location['coordinate_sets'].apply(ast.literal_eval)
    
    for idx, row in LEZ_location.iterrows():
        LEZ_location['coordinate_sets_list'].iloc[idx][0] = LEZ_location['coordinate_sets_list'].iloc[idx][0].split()

        Lez_lat = LEZ_location['coordinate_sets_list'].iloc[idx][0][0]
        Lez_long = LEZ_location['coordinate_sets_list'].iloc[idx][0][1]

        folium.Marker(
        location=[Lez_lat, Lez_long],
        popup= LEZ_location['zone_name'].iloc[idx], # pop-up label for the marker
        icon=folium.Icon(color='red', icon='glyphicon-screenshot', icon_color='white')
        ).add_to(m)

    # Load province data
    geojson_path = os.path.join(data_dir, "georef-netherlands-provincie.geojson")
    json_path = os.path.join(data_dir, "georef-netherlands-provincie.json")
    
    gdf = gpd.read_file(geojson_path)
    df = pd.read_json(json_path)
    # Extract unique province names
    gdf['prov_name'] = df['prov_name']

    folium.GeoJson(gdf).add_to(m)
    m.add_child(folium.LayerControl())
    

    return m._repr_html_()


if __name__ == "__main__":
    draw_LEZ_map()