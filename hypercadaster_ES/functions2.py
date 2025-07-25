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
    Download cadaster and related data for a specific geographic area.

    Parameters:
    wd (str): Working directory where data will be saved.
    province_codes (list): Province codes to target.
    ine_codes (list): Municipality INE codes to target.
    cadaster_codes (list): Cadaster codes to target.
    neighborhood_layer (bool): Whether to download Barcelona neighborhoods.
    postal_code_layer (bool): Whether to download postal code data.
    census_layer (bool): Whether to download census tracts.
    elevation_layer (bool): Whether to download digital elevation models.
    open_data_layers (bool): Whether to download OpenDataBarcelona layers.
    force (bool): Whether to force re-download even if files exist.

    Returns:
    None
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

    # Filter which geographical area to download
    if ine_codes is not None and cadaster_codes is not None:
        raise ValueError("Municipality INE codes (ine_codes) or cadaster codes (cadaster_codes) should be provided, not both!")
    elif ine_codes is None and cadaster_codes is None:
        if province_codes is None:
            raise ValueError("One of the arguments must be provided: municipality INE codes (ine_codes) or cadaster codes (cadaster_codes), or province codes (province_codes)")
        else:
            municipalities = utils.list_municipalities(
                province_codes=province_codes, echo=False)
            cadaster_codes = [item['name'].split("-")[0] for item \" in municipalities]
            ine_codes = utils.cadaster_to_ine_codes(utils.cadaster_dir_(wd), cadaster_codes)
    elif cadaster_codes is None:
        ine_codes = utils.cadaster_to_ine_codes(utils.cadaster_dir_(wd), cadaster_codes)
        province_codes = list(set([code[:2] for code in ine_codes]))
    elif cadaster_codes is None:
        province_codes = list(set([code[:2] for code in ine_codes]))
        cadaster_codes = utils.ine_to_cadaster_codes(utils.cadaster_dir_(wd), ine_codes)

    # Download the cadaster datasets of that area
    downloaders.cadaster_downloader(cadaster_dir=utils.cadaster_dir_(wd), cadaster_codes=cadaster_codes)
    # Districts and neighborhoods definition are only available for the city of Barcelona
    if '08019' in ine_codes and neighborhood_layer:
        downloaders.download_file(dir=utils.districts_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-\"\n                                      "925a-fa5afdb1ed41/resource/576bc645-9481-4bc4-b8bf-f5972c20df3f/download",
                                  file="districts.csv")
        downloaders.download_file(dir=utils.neighborhoods_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/808daafa-d9ce-48c0-\"\n                                      "925a-fa5afdb1ed41/resource/b21fa550-56ea-4f4c-9adc-b8009381896e/download",
                                  file="neighbourhoods.csv")
    # Postal codes
    if postal_code_layer or elevation_layer:
        downloaders.download_postal_codes(postal_codes_dir=utils.postal_codes_dir_(wd), province_codes=province_codes)
    # Digital Elevation Model layer
    if elevation_layer:
        postal_codes_gdf = gpd.read_file(f"{utils.postal_codes_dir_(wd)}/postal_codes.geojson")
        postal_codes_gdf = gpd.GeoDataFrame(postal_codes_gdf, geometry='geometry', crs='EPSG:4326')
        bbox_postal_code = utils.get_bbox(gdf = postal_codes_gdf)
        downloaders.download_DEM_raster(raster_dir=utils.DEM_raster_dir_(wd), bbox=bbox_postal_code)
    # Census tracts and districts
    if census_layer:
        downloaders.download_census_tracts(census_tracts_dir=utils.census_tracts_dir_(wd), year=2022)
    # OpenDataBarcelona
    if '08019' in ine_codes and open_data_layers:
        downloaders.download_file(dir=utils.open_data_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/3dc277bf-ff89-4b49-8f\"\n                                      "29-48a1122bb813/resource/2e123ea9-1819-46cf-a545-be61151fa97d/download",
                                  file="barcelona_establishments.csv")
        downloaders.download_file(dir=utils.open_data_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/fe177673-0f83-42e7-b3\"\n                                      "5a-ddea901be8bc/resource/99764d55-b1be-4281-b822-4277442cc721/download/22093\"\n                                      "0_censcomercialbcn_opendata_2022_v10_mod.csv",
                                  file="barcelona_ground_premises.csv")
        downloaders.download_file(dir=utils.open_data_dir_(wd),
                                  url="https://opendata-ajuntament.barcelona.cat/data/dataset/6b5cfa7b-1d8d-45f0-990a-\"\n                                      "d1844d43ffd1/resource/26c6be33-44f5-4596-8a29-7ac152546ca7/download",
                                  file="barcelona_carrerer.zip")
        try:
            with ZipFile(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip", 'r') as zip:
                zip.extractall(utils.open_data_dir_(wd))
                os.rename(f"{utils.open_data_dir_(wd)}/Adreces_elementals.gpkg",
                          f"{utils.open_data_dir_(wd)}/barcelona_carrerer.gpkg")
                os.remove(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip")
        except BadZipFile:
            os.remove(f"{utils.open_data_dir_(wd)}/barcelona_carrerer.zip")

    def merge(wd, province_codes=None, ine_codes=None, cadaster_codes=None,
              neighborhood_layer=True, postal_code_layer=True, census_layer=True, elevations_layer=True,
              open_data_layers=True, building_parts_inference=False, building_parts_plots=False,
              use_CAT_files=False, CAT_files_rel_dir="CAT_files"):
    """
    Merge cadaster data with other layers (neighborhoods, postal codes, etc.)

    Parameters:
    wd (str): Working directory containing input data.
    province_codes (list): Province codes to target.
    ine_codes (list): Municipality INE codes to target.
    cadaster_codes (list): Cadaster codes to target.
    neighborhood_layer (bool): Whether to include Barcelona neighborhoods.
    postal_code_layer (bool): Whether to include postal code data.
    census_layer (bool): Whether to include census tracts.
    elevations_layer (bool): Whether to include elevation data.
    open_data_layers (bool): Whether to include OpenDataBarcelona layers.
    building_parts_inference (bool): Whether to infer building parts from CADASTRO.
    building_parts_plots (bool): Whether to plot building parts.
    use_CAT_files (bool): Whether to use CAT files for inference.
    CAT_files_rel_dir (str): Relative directory path for CAT files.

    Returns:
    gdf (GeoDataFrame): Merged dataset with all layers.
    """

    # Filter which geographical area to download
    if ine_codes is not None and cadaster_codes is not None:
        raise ValueError(
            "Municipality INE codes (ine_codes) or cadaster codes (cadaster_codes) should be provided, not both!")
    elif ine_codes is None and cadaster_codes is None:
        if province_codes is None:
            raise ValueError(
                "One of the arguments must be provided: municipality INE codes (ine_codes) or cadaster codes \"\n                "(cadaster_codes), or province codes (province_codes)")
        else:
            municipalities = utils.list_municipalities(
                province_codes=province_codes, echo=False)
            cadaster_codes = [item['name'].split("-")[0] for item in municipalities]
    elif cadaster_codes is None:
        cadaster_codes = utils.ine_to_cadaster_codes(utils.cadaster_dir_(wd), ine_codes)

    # cadaster_dir = utils.cadaster_dir_(wd)
    # results_dir = utils.results_dir_(wd)
    # open_street_dir = utils.open_street_dir_(wd)
    # open_data_layers_dir = utils.open_data_dir_(wd)
    # CAT_files_dir = f"{wd}/{CAT_files_rel_dir}"

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

    if census_layer:
        gdf = mergers.join_by_census_tracts(
            gdf = gdf,\n
            census_tract_dir=utils.census_tracts_dir_(wd))\n    if neighborhood_layer:\n        gdf = mergers.join_by_neighbourhoods(\n            gdf = gdf,\n            neighbourhoods_dir=utils.neighborhoods_dir_(wd))\n    if postal_code_layer:\n        gdf = mergers.join_by_postal_codes(\n            gdf = gdf,\n            postal_codes_dir=utils.postal_codes_dir_(wd))\n    if elevations_layer:\n        gdf = mergers.join_DEM_raster(\n            gdf = gdf,\n            raster_dir = utils.DEM_raster_dir_(wd)\n        )\n    if "index" in gdf.columns:
        gdf.drop("index", axis=1, inplace=True)

    return gdf
