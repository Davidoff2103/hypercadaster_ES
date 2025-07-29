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
Module containing functions to merge geospatial data from various sources

This module provides utilities to combine address, building, and zoning data
from cadaster records with additional spatial and administrative layers.
"""


def make_valid(gdf):
    """
    Validate and clean geometry data

    Parameters:
    gdf (GeoDataFrame): Input geospatial data

    Returns:
    GeoDataFrame: Cleaned geospatial data with valid geometries
    """
    gdf.geometry = gdf.geometry.make_valid()
    return gdf


def get_cadaster_address(cadaster_dir, cadaster_codes, directions_from_CAT_files=True, CAT_files_dir="CAT_files",
                         directions_from_open_data=True, open_data_layers_dir="open_data"):
    """
    Extract cadaster address data

    Parameters:
    cadaster_dir (str): Directory containing cadaster data
    cadaster_codes (list): List of cadaster codes
    directions_from_CAT_files (bool): Whether to include CAT files data
    CAT_files_dir (str): Directory containing CAT files
    directions_from_open_data (bool): Whether to include open data
    open_data_layers_dir (str): Directory containing open data layers

    Returns:
    DataFrame: Combined address data
    """
    # ... [rest of the code with added comments] ...

    return gdf


def join_cadaster_building(gdf, cadaster_dir, cadaster_codes, results_dir, open_street_dir, building_parts_plots=False,
                           building_parts_inference=False, building_parts_inference_using_CAT_files=False,
                           open_data_layers=False, open_data_layers_dir=None, CAT_files_dir = None):
    """
    Join building data with cadaster records

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    cadaster_dir (str): Directory containing cadaster data
    cadaster_codes (list): List of cadaster codes
    results_dir (str): Directory for results
    open_street_dir (str): Directory for open street data
    building_parts_plots (bool): Whether to generate plots
    building_parts_inference (bool): Whether to perform inference
    building_parts_inference_using_CAT_files (bool): Whether to use CAT files for inference
    open_data_layers (bool): Whether to use open data layers
    open_data_layers_dir (str): Directory containing open data layers
    CAT_files_dir (str): Directory containing CAT files

    Returns:
    DataFrame: Combined building data
    """
    # ... [rest of the code with added comments] ...

    return pd.merge(gdf, building_gdf, left_on="building_reference", right_on="building_reference", how="left")


def join_cadaster_zone(gdf, cadaster_dir, cadaster_codes):
    """
    Join cadaster zoning data

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    cadaster_dir (str): Directory containing cadaster data
    cadaster_codes (list): List of cadaster codes

    Returns:
    DataFrame: Combined zoning data
    """
    # ... [rest of the code with added comments] ...

    return joined


def join_cadaster_parcel(gdf, cadaster_dir, cadaster_codes, how="left"):
    """
    Join cadastral parcel data

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    cadaster_dir (str): Directory containing cadaster data
    cadaster_codes (list): List of cadaster codes
    how (str): Type of join operation

    Returns:
    tuple: Combined data and parcel geometry
    """
    # ... [rest of the code with added comments] ...

    return (gdf_joined,parcel_gdf)


def join_adm_div_naming(gdf, cadaster_dir, cadaster_codes):
    """
    Join administrative division naming

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    cadaster_dir (str): Directory containing cadaster data
    cadaster_codes (list): List of cadaster codes

    Returns:
    DataFrame: Combined administrative data
    """
    # ... [rest of the code with added comments] ...

    return pd.merge(gdf, utils.get_administrative_divisions_naming(cadaster_dir, cadaster_codes=cadaster_codes),
                    left_on="cadaster_code", right_on="cadaster_code", how="left")


def join_cadaster_data(cadaster_dir, cadaster_codes, results_dir, open_street_dir, building_parts_plots=False,
                       building_parts_inference=False, use_CAT_files=False,
                       open_data_layers=False, open_data_layers_dir=None, CAT_files_dir = None):
    """
    Main function to join all cadaster data

    Parameters:
    cadaster_dir (str): Directory containing cadaster data
    cadaster_codes (list): List of cadaster codes
    results_dir (str): Directory for results
    open_street_dir (str): Directory for open street data
    building_parts_plots (bool): Whether to generate plots
    building_parts_inference (bool): Whether to perform inference
    use_CAT_files (bool): Whether to use CAT files
    open_data_layers (bool): Whether to use open data layers
    open_data_layers_dir (str): Directory containing open data layers
    CAT_files_dir (str): Directory containing CAT files

    Returns:
    DataFrame: Combined cadaster data
    """
    # ... [rest of the code with added comments] ...

    return gdf


def join_DEM_raster(gdf, raster_dir):
    """
    Join Digital Elevation Model (DEM) data

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    raster_dir (str): Directory containing DEM files

    Returns:
    GeoDataFrame: Data with elevation information
    """
    # ... [rest of the code with added comments] ...

    return gdf


def join_by_census_tracts(gdf, census_tract_dir, columns=None, geometry_column = "census_geometry", year = 2022):
    """
    Join census tract data

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    census_tract_dir (str): Directory containing census data
    columns (dict): Column mapping
    geometry_column (str): Geometry column name
    year (int): Census year

    Returns:
    GeoDataFrame: Data with census tract information
    """
    # ... [rest of the code with added comments] ...

    return census_gdf


def join_by_neighbourhoods(gdf, neighbourhoods_dir, columns=None, geometry_column="neighborhood_geometry"):
    """
    Join neighborhood data

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    neighbourhoods_dir (str): Directory containing neighborhood data
    columns (dict): Column mapping
    geometry_column (str): Geometry column name

    Returns:
    GeoDataFrame: Data with neighborhood information
    """
    # ... [rest of the code with added comments] ...

    return neighbourhoods_gdf


def join_by_postal_codes(gdf, postal_codes_dir, columns=None, geometry_column="postal_code_geometry"):
    """
    Join postal code data

    Parameters:
    gdf (GeoDataFrame): Base geospatial data
    postal_codes_dir (str): Directory containing postal code data
    columns (dict): Column mapping
    geometry_column (str): Geometry column name

    Returns:
    GeoDataFrame: Data with postal code information
    """
    # ... [rest of the code with added comments] ...

    return postal_codes_gdf
