import folium
import pandas as pd
import geopandas as gpd
import ast

center_lat = 52.2
center_lon = 5.3


m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles='CartoDB Positron'
    )


LEZ_location = pd.read_csv(r"..\..\data\ProcessedData\NDW_locations.csv")
LEZ_location.head()

for idx, row in LEZ_location.iterrows():
    LEZ_location['coordinate_sets_list'] = LEZ_location['coordinate_sets'].apply(ast.literal_eval)
    LEZ_location['coordinate_sets_list'].iloc[idx][0] = LEZ_location['coordinate_sets_list'].iloc[idx][0].split()

    Lez_lat = LEZ_location['coordinate_sets_list'].iloc[idx][0][0]
    Lez_long = LEZ_location['coordinate_sets_list'].iloc[idx][0][1]

    folium.Marker(
    location=[Lez_lat, Lez_long],
    popup= LEZ_location['zone_name'].iloc[idx], # pop-up label for the marker
    icon=folium.Icon(color='red', icon='glyphicon-screenshot', icon_color='white')
    ).add_to(m)


gdf = gpd.read_file(r"..\..\data\ProcessedData\georef-netherlands-provincie.geojson")
df = pd.read_json(r"..\..\data\ProcessedData\georef-netherlands-provincie.json")
# Extract unique province names
gdf['prov_name'] = df['prov_name']


folium.GeoJson(gdf).add_to(m)

m