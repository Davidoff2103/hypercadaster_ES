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

"""
Module containing functions to merge cadaster data with administrative, geographic, and other spatial layers.
"""


def make_valid(gdf):
    """
    Ensure GeoDataFrame geometries are valid.

    Parameters:
    gdf (GeoDataFrame): Input GeoDataFrame with geometries to validate.

    Returns:
    GeoDataFrame: GeoDataFrame with validated geometries.
    """
    gdf.geometry = gdf.geometry.make_valid()
    return gdf


def get_cadaster_address(cadaster_dir, cadaster_codes, directions_from_CAT_files=True, CAT_files_dir="CAT_files",
                         directions_from_open_data=True, open_data_layers_dir="open_data"):
    """
    Extract and merge address information from cadaster data.

    Parameters:
    cadaster_dir (str): Directory containing cadaster data files.
    cadaster_codes (list): List of cadaster codes to process.
    directions_from_CAT_files (bool): Whether to include addresses from CAT files.
    CAT_files_dir (str): Directory containing CAT files.
    directions_from_open_data (bool): Whether to include addresses from open data.
    open_data_layers_dir (str): Directory containing open data layers.

    Returns:
    GeoDataFrame: Merged address data with spatial information.
    """
    # ... [rest of the function remains unchanged] ...


def join_cadaster_building(gdf, cadaster_dir, cadaster_codes, results_dir, open_street_dir, building_parts_plots=False,
                           building_parts_inference=False, building_parts_inference_using_CAT_files=False,
                           open_data_layers=False, open_data_layers_dir=None, CAT_files_dir=None):
    """
    Merge building data with cadaster information.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    cadaster_dir (str): Directory containing cadaster data files.
    cadaster_codes (list): List of cadaster codes to process.
    results_dir (str): Directory for storing results.
    open_street_dir (str): Directory containing open street data.
    building_parts_plots (bool): Whether to generate plots for building parts.
    building_parts_inference (bool): Whether to perform building part inference.
    building_parts_inference_using_CAT_files (bool): Whether to use CAT files for inference.
    open_data_layers (bool): Whether to use open data layers.
    open_data_layers_dir (str): Directory containing open data layers.
    CAT_files_dir (str): Directory containing CAT files.

    Returns:
    GeoDataFrame: Merged building data.
    """
    # ... [rest of the function remains unchanged] ...


def join_cadaster_zone(gdf, cadaster_dir, cadaster_codes):
    """
    Merge cadaster zones (urban/rural) with building data.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    cadaster_dir (str): Directory containing cadaster data files.
    cadaster_codes (list): List of cadaster codes to process.

    Returns:
    GeoDataFrame: Merged zone data.
    """
    # ... [rest of the function remains unchanged] ...


def join_cadaster_parcel(gdf, cadaster_dir, cadaster_codes, how="left"):
    """
    Join cadastral parcels with building data.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    cadaster_dir (str): Directory containing cadaster data files.
    cadaster_codes (list): List of cadaster codes to process.
    how (str): Type of join operation (default: "left").

    Returns:
    tuple: (GeoDataFrame with parcel information, GeoDataFrame of parcels).
    """
    # ... [rest of the function remains unchanged] ...


def join_adm_div_naming(gdf, cadaster_dir, cadaster_codes):
    """
    Merge administrative division naming data with cadaster data.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    cadaster_dir (str): Directory containing cadaster data files.
    cadaster_codes (list): List of cadaster codes to process.

    Returns:
    GeoDataFrame: Merged administrative data.
    """
    # ... [rest of the function remains unchanged] ...


def join_cadaster_data(cadaster_dir, cadaster_codes, results_dir, open_street_dir, building_parts_plots=False,
                       building_parts_inference=False, use_CAT_files=False,
                       open_data_layers=False, open_data_layers_dir=None, CAT_files_dir = None):
    """
    Main function to merge all cadaster data layers.

    Parameters:
    cadaster_dir (str): Directory containing cadaster data files.
    cadaster_codes (list): List of cadaster codes to process.
    results_dir (str): Directory for storing results.
    open_street_dir (str): Directory containing open street data.
    building_parts_plots (bool): Whether to generate plots for building parts.
    building_parts_inference (bool): Whether to perform building part inference.
    use_CAT_files (bool): Whether to use CAT files for inference.
    open_data_layers (bool): Whether to use open data layers.
    open_data_layers_dir (str): Directory containing open data layers.
    CAT_files_dir (str): Directory containing CAT files.

    Returns:
    GeoDataFrame: Fully merged cadaster data.
    """
    # ... [rest of the function remains unchanged] ...


def join_DEM_raster(gdf, raster_dir):
    """
    Merge Digital Elevation Model (DEM) data with geographic data.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    raster_dir (str): Directory containing DEM files.

    Returns:
    GeoDataFrame: GeoDataFrame with elevation data.
    """
    # ... [rest of the function remains unchanged] ...


def join_by_census_tracts(gdf, census_tract_dir, columns=None, geometry_column = "census_geometry", year = 2022):
    """
    Join census tract data with geographic data.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    census_tract_dir (str): Directory containing census tract data.
    columns (dict): Column mapping for census data.
    geometry_column (str): Name of the geometry column in census data.
    year (int): Census year.

    Returns:
    GeoDataFrame: GeoDataFrame with census tract information.
    """
    # ... [rest of the function remains unchanged] ...


def join_by_neighbourhoods(gdf, neighbourhoods_dir, columns=None, geometry_column="neighborhood_geometry"):
    """
    Join neighborhood data with geographic data.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    neighbourhoods_dir (str): Directory containing neighborhood data.
    columns (dict): Column mapping for neighborhood data.
    geometry_column (str): Name of the geometry column in neighborhood data.

    Returns:
    GeoDataFrame: GeoDataFrame with neighborhood information.
    """
    # ... [rest of the function remains unchanged] ...


def join_by_postal_codes(gdf, postal_codes_dir, columns=None, geometry_column="postal_code_geometry"):
    """
    Join postal code data with geographic data.

    Parameters:
    gdf (GeoDataFrame): Base GeoDataFrame.
    postal_codes_dir (str): Directory containing postal code data.
    columns (dict): Column mapping for postal code data.
    geometry_column (str): Name of the geometry column in postal code data.

    Returns:
    GeoDataFrame: GeoDataFrame with postal code information.
    """
    # ... [rest of the function remains unchanged] ...
