import os
import geopandas as gpd
from hypercadaster_ES import mergers
from hypercadaster_ES import utils
from hypercadaster_ES import downloaders
from zipfile import ZipFile, BadZipFile

"""
Download cadaster data for specified geographical areas.

Parameters:
----------
wd : str
    Working directory path.
province_codes : list of str, optional
    Province codes to filter data (default: None).
ine_codes : list of str, optional
    INE municipality codes to filter data (default: None).
cadaster_codes : list of str, optional
    Cadaster codes to filter data (default: None).
neighborhood_layer : bool, optional
    Whether to include neighborhood data (default: True).
postal_code_layer : bool, optional
    Whether to include postal code data (default: True).
census_layer : bool, optional
    Whether to include census tract data (default: True).
elevation_layer : bool, optional
    Whether to include elevation data (default: True).
open_data_layers : bool, optional
    Whether to include OpenDataBarcelona layers (default: True).
force : bool, optional
    If True, delete existing working directory (default: False).

Returns:
-------
None
"""

def download(wd, province_codes=None, ine_codes=None, cadaster_codes=None,
             neighborhood_layer=True, postal_code_layer=True, census_layer=True,
             elevation_layer=True, open_data_layers=True, force=False):
    """
    Main function to download and process cadaster data.

    Parameters:
    ----------
    wd : str
        Working directory path.
    province_codes : list of str, optional
        Province codes to filter data (default: None).
    ine_codes : list of str, optional
        IN   ... (rest of the content is the same as before)
