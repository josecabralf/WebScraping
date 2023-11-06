import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from config import path_map_barrios


class GeoCorrector:
  _map_file = path_map_barrios
  def execute(self, df: pd.DataFrame) -> pd.DataFrame:
    gdf = gpd.read_file(self._map_file)
    filt = df['coordX'].notna()
    for index, row in df[filt].iterrows():
        house_coords = Point(row['coordY'], row['coordX'])
        matching_rows = gdf[gdf.geometry.contains(house_coords)]
        if not matching_rows.empty and (matching_rows.iloc[0]['Nombre'] != 'SD'):
            correct_barrio = matching_rows.iloc[0]['Nombre']
            df.at[index, 'barrio'] = correct_barrio
    return df