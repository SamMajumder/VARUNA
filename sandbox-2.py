# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 18:07:01 2024

@author: Dr. M
"""


## imports 
import os
import geopandas as gpd

#### Set Up AWS Credentials

import boto3
from botocore import UNSIGNED
from botocore.client import Config
import s3fs
import xarray as xr
import h5netcdf
from shapely.geometry import box
import folium
import rioxarray
from shapely.geometry import mapping

from concurrent.futures import ThreadPoolExecutor, as_completed


#####

def extract_bounds(Continent = "Asia"):  
    
    # Relative path to the shapefile
    shapefile_path = 'Data\\Shapefile\\World_Continents.shp'

    # Read the shapefile
    gdf = gpd.read_file(shapefile_path) 
    
    ## only select CONTINENT and geometry ##

    gdf = gdf[["CONTINENT","geometry"]]

    ## removing Antarctica 

    gdf = gdf[gdf["CONTINENT"] != "Antarctica"] 


    ##### Now extracting a the roi of a specific area 
    ### isolating a continent and setting the crs

    gdf = gdf[gdf["CONTINENT"] == Continent].to_crs("EPSG: 4326")  
    
    ### extracting the bounds
    bounds = gdf.total_bounds 
    
    ## converting to tuple
    bounds = tuple(bounds)
    
    return bounds 

### process one file ### 

def prepare_cmip6_netcdf(start_year, end_year, variable='pr', bounds=None, num_workers=None):
    """
    Prepares and processes CMIP6 NetCDF files for a specified variable from a given year range.

    Parameters:
    - start_year: int, the start year of the files to process.
    - end_year: int, the end year of the files to process.
    - variable: str, the CMIP6 variable to process (e.g., 'pr' for precipitation).
    - bounds: tuple, optional bounding box for clipping the data.
    - num_workers: int, number of worker threads in the thread pool.
    """
    # Establishing connection to the S3 bucket
    fs = s3fs.S3FileSystem(anon=True)
    base_path = f's3://nex-gddp-cmip6/NEX-GDDP-CMIP6/ACCESS-CM2/ssp126/r1i1p1f1/{variable}/'

    def process_file(file_path, bounds, variable, fs):
        """Process an individual NetCDF file."""
        try:
            with fs.open(file_path, mode='rb') as f:
                ds = xr.open_dataset(f, engine='h5netcdf')
                ds.load()  # Ensure data is loaded into memory

            # Compute the monthly mean
            monthly_nc = ds[variable].groupby('time.month').mean('time').astype('float32')

            # Set the CRS
            monthly_nc.rio.write_crs("epsg:4326", inplace=True)

            # Clip the dataset if bounds are provided
            if bounds:
                monthly_nc = monthly_nc.rio.clip_box(*bounds)
            
            return monthly_nc
        except Exception as e:
            print(f"Failed to process file {file_path}: {e}")
            return None

    # List to store datasets from each file
    datasets = []
    futures = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for year in range(start_year, end_year + 1):
            file_path = f"{base_path}{variable}_day_ACCESS-CM2_ssp126_r1i1p1f1_gn_{year}.nc"
            if "_v1.1" not in file_path:
                future = executor.submit(process_file, file_path, bounds, variable, fs)
                futures.append(future)
            else:
                print(f"Skipping file: {file_path} due to version exclusion.")

        # Gather results from the futures
        datasets = [future.result() for future in as_completed(futures) if future.result() is not None]

    # Concatenate datasets across time
    if datasets:
        combined_nc = xr.concat(datasets, dim="time")
        print("Congratulations! All datasets processed successfully.")
    else:
        combined_nc = None
        print("No datasets were processed.")

    return combined_nc


### process multiple variables 

def process_multiple_variables(start_year, end_year, variables, bounds=None, num_workers=4):
    results = {}  # Dictionary to store results keyed by variable name
    for variable in variables:
        print(f"Starting processing for variable: {variable}")
        dataset = prepare_cmip6_netcdf(start_year, end_year, variable, bounds, num_workers)
        if dataset is not None:
            results[variable] = dataset
            print(f"Data processed for variable: {variable}")
        else:
            print(f"Failed to generate data for {variable}")
            results[variable] = None  # Optionally store None or omit this line to exclude failed cases
    return results





## step 1
### get the shapefile and extract the bounds over a given area 
bounds = extract_bounds(Continent="Europe")


### step 2
## clip the netcdfs 
# List of variables to process
variables = ['pr', 'tas', 'tasmax', 'tasmin']

# Example usage
datasets = process_multiple_variables(start_year = 2025, end_year = 2026, 
                           variables = variables, bounds=bounds, 
                           num_workers=4)   

 
    

    
    


