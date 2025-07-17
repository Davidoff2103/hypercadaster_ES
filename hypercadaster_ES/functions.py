import os
import geopandas as gpd
from hypercadaster_ES import mergers
from hypercadaster_ES import utils
from hypercadaster_ES import downloaders
from zipfile import ZipFile, BadZipFile

"""
Download cadaster data for specified geographical areas.

Parameters:
    wd: Working directory path.
    province_codes: List of province codes (optional).
    ine_codes: List of municipality INE codes (optional).
    cadaster_codes: List of cadaster codes (optional).
    neighborhood_layer: Whether to include neighborhood data (default True).
    postal_code_layer: Whether to include postal code data (default True).
    census_layer: Whether to include census data (default True).
    elevation_layer: Whether to include elevation data (default True).
    open_data_layers: Whether to include OpenDataBarcelona layers (default True).
    force: Force re-download (default False).

Returns:
    gdf: GeoDataFrame containing merged cadaster data.
"""

def download(wd, province_codes=None, ine_codes=None, cadaster_codes=None,
             neighborhood_layer=True, postal_code_layer=True, census_layer=True,
             elevation_layer=True, open_data_layers=True, force=False):

    """
    Force re-download of data by removing existing directory.
    """
    if force:
        try:
            os.removedirs(wd)
        except FileNotFoundError:
            pass
    utils.create_dirs(data_dir=wd)
    downloaders.download_file(dir=utils.cadaster_dir_(wd),
                              url="https://www.catastro.minhap.es/regularizacion/Regularizacion_municipios_finalizados.xlsx",
                              file="ine_inspire_codes.xlsx")

    """
    Filter geographical area based on provided codes.
    """
    if ine_codes is not None and cadaster_codes is not None:
        raise ValueError("Municipality INE codes (ine_codes) or cadaster codes (cadaster_codes) should be provided, not both!")
    elif ine_codes is None and cadaster_codes is None:
        if province_codes is None:
            raise ValueError("One of the arguments must be provided: municipality INE codes (ine_codes) or cadaster codes \"\n                             \"(cadaster_codes), or province codes (province_codes)")
        else:
            municipalities = utils.list_municipalities(
                province_codes=province_codes, echo=False
            )
            cadaster_codes = [item['name'].split("-")[0] for item in municipalities]
            ine_codes = utils.cadaster_to_ine_codes(utils.cadaster_dir_(wd), cadaster_codes)
    elif ine_codes is None:
        ine_codes = utils.cadaster_to_ine_codes(utils.cadaster_dir_(wd), cadaster_codes)
        province_codes = list(set([code[:2] for code in ine_codes]))
    elif cadaster_codes is None:
        province_codes = list(set([code[:2] for code in ine_codes]))
        cadaster_codes = utils.ine_to_cadaster_codes(utils.cadaster_dir_(wd), ine_codes)

    """
    Download cadaster datasets for the specified area.
    """
    downloaders.cadaster_downloader(cadaster_dir=utils.cadaster_dir_(wd), cadaster_codes=cadaster_codes)
    """
    Districts and neighborhoods data available only for Barcelona (INE code 08019).
    """
    if '08019' in ine_codes and neighborhood_layer:
        downloaders.download_file(dir=utils.districts_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-\"\n                                      \"925a-fa5afdb1ed41/resource/576bc645-9481-4bc4-b8bf-f5972c20df3f/download",
                                  file="districts.csv")
        downloaders.download_file(dir=utils.neighborhoods_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-\"\n                                      \"925a-fa5afdb1ed41/resource/b21fa550-56ea-4f4c-9adc-b8009381896e/download",
                                  file="neighbourhoods.csv")
    """
    Postal codes layer processing.
    """
    if postal_code_layer or elevation_layer:
        downloaders.download_postal_codes(postal_codes_dir=utils.postal_codes_dir_(wd), province_codes=province_codes)
    """
    Digital Elevation Model (DEM) data processing.
    """
    if elevation_layer:
        postal_codes_gdf = gpd.read_file(f"{utils.postal_codes_dir_(wd)}/postal_codes.geojson")
        postal_codes_gdf = gpd.GeoDataFrame(postal_codes_gdf, geometry='geometry', crs='EPSG:4326')
        bbox_postal_code = utils.get_bbox(gdf = postal_codes_gdf)
        downloaders.download_DEM_raster(raster_dir=utils.DEM_raster_dir_(wd), bbox=bbox_postal_code)
    """
    Census tracts and districts data processing.
    """
    if census_layer:
        downloaders.download_census_tracts(census_tracts_dir=utils.census_tracts_dir_(wd), year=2022)
    """
    OpenDataBarcelona layers processing.
    """
    if '08019' in ine_codes and open_data_layers:
        downloaders.download_file(dir=utils.open_data_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/3dc277bf-ff89-4b49-8f\"\n                                      \"29-48a1122bb813/resource/2e123ea9-1819-46cf-a545-be61151fa97d/download",
                                  file="barcelona_establishments.csv")
        downloaders.download_file(dir=utils.open_data_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/fe177673-0f83-42e7-b3\"\n                                      \"5a-ddea901be8bc/resource/99764d55-b1be-4281-b822-4277442cc721/download/22093\"\n                                      \"0_censcomercialbcn_opendata_2022_v10_mod.csv",
                                  file="barcelona_ground_premises.csv")
        downloaders.download_file(dir=utils.open_data_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/6b5cfa7b-1d8d-45f0-990a-\"\n                                      \"d1844d43ffd1/resource/26c6be33-44f5-4596-8a29-7ac152546ca7/download",
                                  file="barcelona_carrerer.zip")
        try:
            with ZipFile(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip", 'r') as zip:
                zip.extractall(utils.open_data_dir_(wd))
                os.rename(f"{utils.open_data_dir_(wd)}/Adreces_elementals.gpkg",
                          f"{utils.open_data_dir_(wd)}/barcelona_carrerer.gpkg")
                os.remove(f"{utils.open_data_dir_(wd)}/bar_carrerer.zip")
        except BadZipFile:
            os.remove(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip")


def merge(wd, province_codes=None, ine_codes=None, cadaster_codes=None,
          neighborhood_layer=True, postal_code_layer=True, census_layer=True, elevations_layer=True,
          open_data_layers=True, building_parts_inference=False, building_parts_plots=False,
          use_CAT_files=False, CAT_files_rel_dir="CAT_files"):

    """
    Merge cadaster data with additional layers.
    
    Parameters:
        wd: Working directory path.
        province_codes: List of province codes (optional).
        ine_codes: List of municipality INE codes (optional).
        cadaster_codes: List of cadaster codes (optional).
        neighborhood_layer: Whether to include neighborhood data (default True).
        postal_code_layer: Whether to include postal code data (default True).
        census_layer: Whether to include census data (default True).
        elevations_layer: Whether to include elevation data (default True).
        open_data_layers: Whether to include OpenDataBarcelona layers (default True).
        building_parts_inference: Whether to infer building parts (default False).
        building_parts_plots: Whether to generate plots for building parts (default False).
        use_CAT_files: Whether to use CAT files (default False).
        CAT_files_rel_dir: Relative directory path for CAT files (default "CAT_files").
    
    Returns:
        gdf: GeoDataFrame containing merged cadaster data.
    """

    """
    Filter geographical area based on provided codes.
    """
    if ine_codes is not None and cadaster_codes is not  None:
        raise ValueError(\n            \"Municipality INE codes (ine_codes) or cadaster codes (cadaster_codes) should be provided, not both!\")
    elif ine_codes is None and cadaster_codes is None:\n        if province_codes is None:\n            raise ValueError(\n                \"One of the arguments must be provided: municipality INE codes (ine_codes) or cadaster codes \"\n                \"(cadaster_codes), or province codes (province_codes)\")\n        else:\n            municipalities = utils.list_municipalities(\n                province_codes=province_codes, echo=False\n            )\n            cadaster_codes = [item['name'].split(\"-\")[0] for item in municipalities]\n    elif cadaster_codes is None:\n        cadaster_codes = utils.ine_to_cadaster_codes(utils.cadaster_dir_(wd), ine_codes)\n
    """
    Process data merging with additional layers.
    """
    gdf = mergers.join_cadaster_data(\n        cadaster_dir=utils.cadaster_dir_(wd),\n        cadaster_codes=cadaster_codes,\n        results_dir=utils.results_dir_(wd),\n        open_street_dir=utils.open_street_dir_(wd),\n        building_parts_inference=building_parts_inference,\n        use_CAT_files=use_CAT_files,\n        building_parts_plots=building_parts_plots,\n        open_data_layers=open_data_layers,\n        open_data_layers_dir=utils.open_data_dir_(wd),\n        CAT_files_dir=f\"{wd}/{CAT_files_rel_dir}\")\n
    """
    Join with census tract data.
    """
    if census_layer:\n        gdf = mergers.join_by_census_tracts(\n            gdf = gdf,\n            census_tract_dir=utils.census_tracts_dir_(wd))\n    """
    Join with neighborhood data.
    """
    if neighborhood_layer:\n        gdf = mergers.join_by_neighbourhoods(\n            gdf = gdf,\n            neighbourhoods_dir=utils.neighborhoods_dir_(wd))\n    """
    Join with postal code data.
    """
    if postal_code_layer:\n        gdf = mergers.join_by_postal_codes(\n            gdf = gdf,\n            postal_codes_dir=utils.postal_codes_dir_(wd))\n    """
    Join with elevation data.
    """
    if elevations_layer:\n        gdf = mergers.join_DEM_raster(\n            gdf = gdf,\n            raster_dir = utils.DEM_raster_dir_(wd)\n        )\n    """
    Remove index column if present.
    """
    if "index" in gdf.columns:\n        gdf.drop("index", axis=1, inplace=True)\n    """
    Remove duplicate rows.
    """
    gdf = gdf.drop_duplicates()\n
    return gdf
