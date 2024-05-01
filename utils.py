# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:43:37 2024

@author: Dr. M
"""

## imports 
import os
import geopandas as gpd
import matplotlib.pyplot as plt

#### Set Up AWS Credentials

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import s3fs
import xarray as xr
import h5netcdf
from shapely.geometry import box
import rioxarray
from shapely.geometry import mapping
import rioxarray
import netCDF4

from concurrent.futures import ThreadPoolExecutor, as_completed


#####
#####

def extract_bounds(Country = "India"):  
    
    # Relative path to the shapefile
    shapefile_path = 'Data\\Shapefile\\World_Countries_Generalized.shp'

    # Read the shapefile
    gdf = gpd.read_file(shapefile_path) 
    
    ## only select COUNTRY and geometry ##

    gdf = gdf[["COUNTRY","geometry"]]

    ## removing Antarctica 

    gdf = gdf[gdf["COUNTRY"] != "Antarctica"] 


    ##### Now extracting a the roi of a specific area 
    ### isolating a continent and setting the crs

    gdf = gdf[gdf["COUNTRY"] == Country].to_crs("EPSG: 4326")  
    
    ### extracting the bounds
    bounds = gdf.total_bounds 
    
    # Define the expansion delta (in degrees)
    delta = 3.0

    # Expand the bounds
    expanded_bounds = [bounds[0] - delta, bounds[1] - delta, bounds[2] + delta, bounds[3] + delta]
    
    ## converting to tuple
    bounds = tuple(expanded_bounds)
    
    return bounds 

### process one file ### 

# Previously remembered model names


def prepare_cmip6_netcdf(start_year, end_year, model, scenario, variable, bounds=None, num_workers=None):
    
    # Convert input parameters to correct types
    start_year = int(start_year)
    end_year = int(end_year)
    num_workers = int(num_workers) if num_workers is not None else 1  # default to 1 if None
    
    valid_models = ["ACCESS-CM2","ACCESS-ESM1-5","BCC-CSM2-MR","CanESM5","CESM2-WACCM",
                    "CESM2","CMCC-CM2-SR5","CMCC-ESM2","CNRM-CM6-1",
                    "CNRM-ESM2-1","EC-Earth3-Veg-LR","EC-Earth3","FGOALS-g3",
                    "GFDL-CM4","GFDL-CM4_gr1","GFDL-ESM4","GISS-E2-1-G",
                    "HadGEM3-GC31-LL","HadGEM3-GC31-MM","IITM-ESM","INM-CM4-8",
                    "INM-CM5-0","IPSL-CM6A-LR","KACE-1-0-G","KIOST-ESM",
                    "MIROC-ES2L","MIROC6","MPI-ESM1-2-HR","MPI-ESM1-2-LR",
                    "MRI-ESM2-0","NESM3","NorESM2-LM","NorESM2-MM","TaiESM1",
                    "UKESM1-0-LL"]

    
    if model not in valid_models:
        raise ValueError(f"Invalid model '{model}'. Choose from {valid_models}.")

    # Validate scenarios
    valid_scenarios = ['ssp126', 'ssp245', 'ssp370', 'ssp585']
    if scenario not in valid_scenarios:
        raise ValueError(f"Invalid scenario '{scenario}'. Choose from {valid_scenarios}.")

    fs = s3fs.S3FileSystem(anon=True)

    # Model-specific ensemble mapping
    ensemble_mapping = {
        "CESM2": "r4i1p1f1",
        "CNRM-CM6-1": "r1i1p1f2",
        "GISS-E2-1-G": "r1i1p1f2",
        "MIROC-ES2L": "r1i1p1f2",
        "UKESM1-0-LL": "r1i1p1f2",
        "FGOALS-g3": "r3i1p1f1",
        "HadGEM3-GC31-LL": "r1i1p1f3",
        "HadGEM3-GC31-MM": "r1i1p1f3"
    }
    ensemble = ensemble_mapping.get(model, "r1i1p1f1")

    # Base path
    base_path = f's3://nex-gddp-cmip6/NEX-GDDP-CMIP6/{model}/{scenario}/{ensemble}/{variable}/'

    # Process file function defined once
    def process_file(file_path, bounds, variable, fs):
        try:
            with fs.open(file_path, mode='rb') as f:
                ds = xr.open_dataset(f, engine='h5netcdf')
                ds.load()  # Make sure data is loaded into memory
                
            # Resample and compute the mean, ensure the right method syntax
            monthly_nc = ds[variable].resample(time='1ME').mean().astype('float32')
            
            # Convert DataArray to Dataset
            monthly_nc_ds = monthly_nc.to_dataset()
                
            # Preserve attributes and set CRS
            monthly_nc_ds.attrs = ds.attrs
            monthly_nc_ds[variable].attrs = ds[variable].attrs  # Preserve variable-specific attributes
            monthly_nc_ds.rio.write_crs("epsg:4326", inplace=True)
            
                
            # Apply geographical bounds if provided
            if bounds:
                monthly_nc_ds = monthly_nc_ds.rio.clip_box(*bounds)
                
            return monthly_nc_ds

    
        except Exception as e:
            print(f"Failed to process file {file_path}: {e}")
            return None


    datasets = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for year in range(start_year, end_year + 1):
            file_path = f"{base_path}{variable}_day_{model}_{scenario}_{ensemble}_gn_{year}.nc"
            if "_v1.1" not in file_path:
                future = executor.submit(process_file, file_path, bounds, variable, fs)
                datasets.append(future)
        datasets = [future.result() for future in as_completed(datasets) if future.result() is not None]

    if datasets:
        combined_nc = xr.concat(datasets, dim="time")
        # Sort the concatenated dataset by the time dimension
        combined_nc = combined_nc.sortby('time')
        print(f"All datasets for variable {variable} processed successfully.")
    else:
        combined_nc = None
        print(f"No datasets were processed for variable {variable}.")
    return combined_nc

def process_multiple_scenarios(start_year, end_year, model,variable, scenarios, bounds=None, num_workers=4):
    results = {}
    for scenario in scenarios:
        key = f"{model}_{variable}_{scenario}"
        print(f"Starting processing for: {key}")
        try:
            dataset = prepare_cmip6_netcdf(start_year, end_year, model, scenario, variable, bounds, num_workers)
            results[key] = dataset
            if dataset is not None:
                print(f"Data processed for: {key}")
            else:
                print(f"No data returned for: {key}")
        except Exception as e:
            print(f"Exception while processing {key}: {str(e)}")
            results[key] = None
    return results



def export_datasets_to_netcdf(dataset_dict, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    for dataset_name, dataset in dataset_dict.items():
        output_path = os.path.join(output_folder, f"{dataset_name}.nc")
        dataset.to_netcdf(output_path)
        print(f"Saved dataset '{dataset_name}' to '{output_path}'")


