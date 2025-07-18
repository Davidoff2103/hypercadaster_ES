"""
hypercadaster_ES Module

This module provides functionalities to download and merge geospatial data related to Spanish cadastres,
including municipal boundaries, postal codes, census tracts, elevation data, and OpenDataBarcelona resources.

Functions:
- download: Download geospatial datasets based on specified geographic parameters.
- merge: Merge downloaded datasets into a unified GeoDataFrame for analysis.
"""

import os
import geopandas as gpd
from hypercadaster_ES import mergers
from hypercadaster_ES import utils
from hypercadaster_ES import downloaders
from zipfile import ZipFile, BadZipFile

def download(wd, province_codes=None, ine_codes=None, cadaster_codes=None,
             neighborhood_layer=True, postal_code_layer=True, census_layer=True,
             elevation_layer=True, open_data_layers=True, force=False):
    """
    Download geospatial datasets for specified geographic areas.

    This function downloads municipal boundaries, postal codes, census tracts, elevation data,
    and other relevant layers based on provided parameters. It supports downloading
    data for specific provinces, municipalities (INE codes), or cadaster codes.

    Parameters:
        wd (str): Working directory where downloaded files will be stored.
        province_codes (list of str, optional): Province codes to filter data.
        ine_codes (list of str, optional): INE municipality codes to filter data.
        cadaster_codes (list of str, optional): Cadaster codes to filter data.
        neighborhood_layer (bool, default=True): Whether to download Barcelona neighborhoods.
        postal_code_layer (bool, default=True): Whether to download postal code data.
        census_layer (bool, default=True): Whether to download census tract data.
        elevation_layer (bool, default=True): Whether to download elevation data.
        open_data_layers (bool, default=True): Whether to download OpenDataBarcelona resources.
        force (bool, optional): If True, remove existing directory before downloading.

    Returns:
        None: The function saves downloaded files in the specified working directory.
    """
    
    # Remove existing directory if 'force' is True
    if force:
        try:
            os.removedirs(wd)
        except FileNotFoundError:
            pass
    
    # Create necessary directories for data storage
    utils.create_dirs(data_dir=wd)
    
    # Download INE codes file containing municipality-inspire mapping
    downloaders.download_file(
        dir=utils.cadaster_dir_(wd),
        url="https://www.catastro.minhap.es/regularizacion/Regularizacion_municipios_finalizados.xlsx",
        file="ine_inspire_codes.xlsx"
    )

    # Determine target geographic area based on provided codes
    if ine_codes is not  None and cadaster_codes is not None:
        raise ValueError(
            "Municipality INE codes (ine_codes) or cadaster codes (cadaster_codes) should be provided, not both!"
        )
    elif ine_codes is None and cadaster_codes is None:
        if province_codes is None:
            raise ValueError(
                "One of the arguments must be provided: municipality INE codes (ine_codes) or cadaster codes "
                "(cadaster_codes), or province codes (province_codes)"
            )
        else:
            # List municipalities by province and extract cadaster codes
            municipalities = utils.list_municipalities(
                province_codes=province_codes, echo=False
            )
            cadaster_codes = [item['name'].split("-")[0] for item in municipalities]
            ine_codes = utils.cadaster_to_ine_codes(utils.cadaster_dir_(wd), cadaster_codes)
    elif ine_codes is None:
        # Convert cadaster codes to INE codes
        ine_codes = utils.cadaster_to_ine_codes(utils.cadaster_dir_(wd), cadaster_codes)
        # Extract province codes from INE codes
        province_codes = list(set([code[:2] for code in ine_codes]))
    elif cadaster_codes is None:
        # Convert INE codes to cadaster codes
        province_codes = list(set([code[:2] for code in ine_codes]))
        cadaster_codes = utils.ine_to_cadaster_codes(utils.cadaster_dir_(wd), ine_codes)

    # Download cadaster datasets for the specified area
    downloaders.cadaster_downloader(
        cadaster_dir=utils.cadaster_dir_(wd), 
        cadaster_codes=cadaster_codes
    )

    # Barcelona-specific layers: districts and neighborhoods
    if '08019' in ine_codes and neighborhood_layer:
        downloaders.download_file(
            dir=utils.districts_dir_(wd),
            url="https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-"
                "925a-fa5afdb1ed41/resource/576bc645-9481-4bc4-b8bf-f5972c20df3f/download",
            file="districts.csv"
        )
        downloaders.download_file(
            dir=utils.neighborhoods_dir_(wd),
            url="https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-"
                "925a-fa5afdb1ed41/resource/b21fa550-56ea-4f4c-9adc-b8009381896e/download",
            file="neighbourhoods.csv"
        )

    # Download postal code data if required
    if postal_code_layer or elevation_layer:
        downloaders.download_postal_codes(
            postal_codes_dir=utils.postal_codes_dir_(wd), 
            province_codes=province_codes
        )
    
    # Download Digital Elevation Model (DEM) if required
    if elevation_layer:
        # Read postal code boundaries and extract bounding box
        postal_codes_gdf = gpd.read_file(f"{utils.postal_codes_dir_(wd)}/postal_codes.geojson")
        postal_codes_gdf = gpd.GeoDataFrame(
            postal_codes_gdf, geometry='geometry', crs='EPSG:4326'
        )
        bbox_postal_code = utils.get_bbox(gdf=postal_codes_gdf)
        
        # Download DEM raster for the bounding box
        downloaders.download_DEM_raster(
            raster_dir=utils.DEM_raster_dir_(wd), 
            bbox=bbox_postal_code
        )

    # Download census tract data if required
    if census_layer:
        downloaders.download_census_tracts(
            census_tracts_dir=utils.census_tracts_dir_(wd), 
            year=2022
        )
    
    # Download OpenDataBarcelona resources if requested
    if '08019' in ine_codes and open_data_layers:
        downloaders.download_file(
            dir=utils.open_data_dir_(wd),
            url="https://opendata-ajuntament.barcelona.cat/data/dataset/3dc277bf-ff89-4b49-8f"
                "29-48a1122bb813/resource/2e123ea9-1819-46cf-a545-be61151fa97d/download",
            file="barcelona_establishments.csv"
        )
        
        downloaders.download_file(
            dir=utils.open_data_dir_(wd),
            url="https://opendata-ajuntament.barcelona.cat/data/dataset/fe177673-0f83-42e7-b3"
                "5a-ddea901be8bc/resource/99764d55-b1be-4281-b822-4277442cc721/download/22093"
                "0_censcomercialbcn_opendata_2022_v10_mod.csv",
            file="barcelona_ground_premises.csv"
        )
        
        downloaders.download_file(
            dir=utils.open_data_dir_(wd),
            url="https://opendata-ajuntament.barcelona.cat/data/dataset/6b5cfa7b-1d8d-45f0-990a-"
                "d1844d43ffd1/resource/26c6be33-44f5-4596-8a29-7ac152546ca7/download",
            file="barcelona_carrerer.zip"
        )
        
        # Handle zip extraction for Barcelona road data
        try:
            with ZipFile(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip", 'r') as zip:
                zip.extractall(utils.open_data_dir_(wd))
                os.rename(
                    f"{utils.open_data_dir_(wd)}/Adreces_elementals.gpkg",
                    f"{utils.open_data_dir_(wd)}/barcelona_carrerer.gpkg"
                )
                os.remove(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip")
        except BadZipFile:
            os.remove(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip")

def merge(wd, province_codes=None, ine_codes=None, cadaster_codes=None,
          neighborhood_layer=True, postal_code_layer=True, census_layer=True, elevations_layer=True,
          open_data_layers=True, building_parts_inference=False, building_parts_plots=False,
          use_CAT_files=False, CAT_files_rel_dir="CAT_files"):
    """
    Merge downloaded geospatial datasets into a unified GeoDataFrame.

    This function combines various layers (cadaster data, postal codes, census tracts, elevation data,
    etc.) into a single GeoDataFrame for spatial analysis. It can also process building parts
    using CAT files if specified.

    Parameters:
        wd (str): Working directory containing downloaded datasets.
        province_codes (list of str, optional): Province codes to filter data.
        ine_codes (list of str, optional): INE municipality codes to filter data.
        cadaster_codes (list of str, optional): Cadaster codes to filter data.
        neighborhood_layer (bool, default=True): Whether to include neighborhood data.
        postal_code_layer (bool, default=True): Whether to include postal code data.
        census_layer (bool, default=True): Whether to include census tract data.
        elevations_layer (bool, default=True): Whether to include elevation data.
        open_data_layers (bool, default=True): Whether to include OpenDataBarcelona resources.
        building_parts_inference (bool, default=False): Whether to infer building parts.
        building_parts_plots (bool, default=False): Whether to generate plots for building parts.
        use_CAT_files (bool, default=False): Whether to process CAT files for building details.
        CAT_files_rel_dir (str, default="CAT_files"): Relative path for CAT file directory.

    Returns:
        geopandas.GeoDataFrame: A unified GeoDataFrame containing merged spatial data.
    """
    
    # Determine target geographic area based on provided codes
    if ine_codes is not None and cadaster_codes is not None:
        raise ValueError(
            "Municipality INE codes (ine_codes) or cadaster codes (cadaster_codes) should be provided, not both!"
        )
    elif ine_codes is None and cadaster_codes is None:
        if province_codes is None:
            raise ValueError(
                "One of the arguments must be provided: municipality INE codes (ine_codes) or cadaster codes "
                "(cadaster_codes), or province codes (province_codes)"
            )
        else:
            # List municipalities by province and extract cadaster codes
            municipalities = utils.list_municipalities(
                province_codes=province_codes, echo=False
            )
            cadaster_codes = [item['name'].split("-")[0] for item in municipalities]
    elif cadaster_codes is None:
        # Convert INE codes to cadaster codes
        cadaster_codes = utils.ine_to_cadaster_codes(utils.cadaster_dir_(wd), ine_codes)

    # cadaster_dir = utils.cadaster_dir_(wd)
    # results_dir = utils.results_dir_(wd)
    # open_street_dir = utils.open_street_dir_(wd)
    # open_data_layers_dir = utils.open_data_dir_(wd)
    # CAT_files_dir = f"{wd}/{CAT_files_rel_dir}"

    # Merge datasets into a single GeoDataFrame
    gdf = mergers.join_cadaster_data(
        cadaster_dir=utils.cadaster_dir_(wd),
        cadaster_codes=cadaster_codes,
        results_dir=utils.results_dir_(wd),
        open_street_dir=utils.open_street_dir_(wd),
        building_parts_inference=building_parts_inference,
        use_CAT_files=use_CAT_files,
        building_parts_plots=building_parts_plots,
        open_data_layers=open_data_layers,
        open_data_layers_dir=utils.open_data_dir_(wd),
        CAT_files_dir=f"{wd}/{CAT_files_rel_dir}"
    )

    # Join census tract data if requested
    if census_layer:
        gdf = mergers.join_by_census_tracts(
            gdf=gdf,
            census_tract_dir=utils.census_tracts_dir_(wd)
        )
    
    # Join neighborhood data if requested
    if neighborhood_layer:
        gdf = mergers.join_by_neighbourhoods(
            gdf=gdf,
            neighbourhoods_dir=utils.neighborhoods_dir_(wd)
        )
    
    # Join postal code data if requested
    if postal_code_layer:
        gdf = mergers.join_by_postal_codes(
            gdf=gdf,
            postal_codes_dir=utils.postal_codes_dir_(wd)
        )
    
    # Join elevation data if requested
    if elevations_layer:
        gdf = mergers.join_DEM_raster(
            gdf=gdf,
            raster_dir=utils.DEM_raster_dir_(wd)
        )
    
    # Remove index column if present
    if "index" in gdf.columns:
        gdf.drop("index", axis=1, inplace=True)

    return gdf

