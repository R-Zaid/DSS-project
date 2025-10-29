import folium
import pandas as pd
import re
from shapely.geometry import Polygon
import geopandas as gpd

def draw_LEZ_map_new():
    LEZ_location = pd.read_csv(r"..\..\data\ProcessedData\NDW_locations.csv")
    LEZ_location = LEZ_location[LEZ_location['zone_name'].str.startswith('ZE') == False].reset_index(drop=True)
    LEZ_location = LEZ_location[LEZ_location['zone_name'] != "Milieuzone Amsterdam"].reset_index(drop=True)
    LEZ_location.loc[3, 'zone_name'] = 'LEZ Apeldoorn'
    LEZ_location.loc[10, 'end_date'] = '2999-01-01T00:00:00Z'

    def parse_coords(coord_str):
        # Clean and parse string into (lat, lon) pairs list
        coord_str = coord_str.strip("[]'\" ")
        coords_split = coord_str.split()
        coords_clean = [re.sub(r"[,'\"]", "", c) for c in coords_split]
        latlons = [(float(coords_clean[i]), float(coords_clean[i + 1])) for i in range(0, len(coords_clean), 2)]
        return latlons

    # Apply function to the column 'coordinate_sets', storing results in a new column 'latlon_pairs'
    LEZ_location['latlon_pairs'] = LEZ_location['coordinate_sets'].apply(parse_coords)

    df = LEZ_location

    df['LAT'] = df['latlon_pairs'].apply(lambda x: [lat for lon, lat in x])
    df['LON'] = df['latlon_pairs'].apply(lambda x: [lon for lon, lat in x])

    geom_list = [(x, y) for x, y in zip(df['LON'], df['LAT'])]

    geom_list_2 = [Polygon(tuple(zip(x, y))) for x, y in geom_list]

    polygon_gdf = gpd.GeoDataFrame(geometry=geom_list_2)

    LEZ_location = pd.merge(LEZ_location, polygon_gdf, left_index=True, right_index=True)
    polygon_gdf = polygon_gdf.set_crs(epsg=4326)
    gdf = polygon_gdf.to_crs(epsg=3857)

    LEZ_location['area_m2'] = gdf.area
    LEZ_location['area_km2'] = LEZ_location['area_m2'] / 1000000

    selected_columns = ['zone_name', 'start_date', 'end_date', 'area_km2']
    LEZ_area = LEZ_location[selected_columns].copy()

    province_map = {"LEZ 's-Hertogenbosch": 'North-Brabant',
                    'LEZ Delft': 'Zuid-Holland',
                    'LEZ Haarlem': 'Noord-Holland',
                    'LEZ Apeldoorn': 'Gelderland',
                    'LEZ Den Haag': 'Zuid-Holland',
                    'LEZ Breda': 'North-Brabant',
                    'LEZ Tilburg': 'North-Brabant',
                    'LEZ Utrecht': 'Utrecht',
                    'LEZ Leiden': 'Zuid-Holland',
                    'LEZ Rijswijk': 'Zuid-Holland',
                    'Milieuzone Arnhem': 'Gelderland',
                    'LEZ Amsterdam': 'Noord-Holland',
                    'Milieuzone Maastricht': 'Limburg',
                    'LEZ Rotterdam Maasvlakte': 'Zuid-Holland'
                    }
    LEZ_area['province'] = LEZ_area['zone_name'].map(province_map)

    center_lat = 52.2
    center_lon = 5.3

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles='CartoDB Positron'
    )

    for idx, row in LEZ_location.iterrows():
        folium.Polygon(
            locations=LEZ_location.latlon_pairs.iloc[idx],
            color="blue",
            weight=3,
            fill_color="red",
            fill_opacity=0.2,
            fill=True,
            popup=LEZ_location['zone_name'].iloc[idx],
        ).add_to(m)

    return m