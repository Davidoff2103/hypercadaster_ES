from hypercadaster_ES import utils
from hypercadaster_ES import building_inference
from hypercadaster_ES import downloaders
import geopandas as gpd
import pandas as pd
import polars as pl
import rasterio
from shapely import wkt
from shapely.geometry import Point
import sys
import numpy as np
import regex as re

""
Module containing functions to merge various geospatial datasets related to cadaster data.
"" 

def make_valid(gdf):
    """
    Make the geometry of a GeoDataFrame valid.

    Parameters:
    gdf (GeoDataFrame): Input GeoDataFrame with geometry column.

    Returns:
    GeoDataFrame: GeoDataFrame with valid geometry.
    """
    gdf.geometry = gdf.geometry.make_valid()
    return gdf

... (rest of the code with existing docstrings and comments) ...
