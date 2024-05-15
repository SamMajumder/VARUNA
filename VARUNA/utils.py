# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:43:37 2024

@author: Dr. M
"""

## imports 
import os
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from branca.colormap import LinearColormap
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import ColorbarBase

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
import numpy as np 

import osmnx as ox

from concurrent.futures import ThreadPoolExecutor, as_completed


###############
#####

def extract_bounds_osmnx(place = "India"):
    
    # Get a geodataframe related to the place
    area = ox.geocode_to_gdf(place)  
    
    ### isolate the geometry
    area = area[["geometry"]] 
    
    ## project it to a epsg 4326
    area = area.to_crs("EPSG: 4326") 
    
    ### extracting the bounds
    bounds = area.total_bounds  
    
    ### create a tuple
    bounds = tuple(bounds)

    
    return(bounds)

########## 
##



#########
###
def extract_bounds(Country = "India"):  
    
    # Relative path to the shapefile
    shapefile_path = 'Data/Shapefile/World_Countries_Generalized.shp'

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
        # Create a multi-index by extracting 'month' and 'year' from 'time' dimension
        combined_nc['month'] = combined_nc['time'].dt.month
        combined_nc['year'] = combined_nc['time'].dt.year
        combined_nc = combined_nc.set_index(time=['month', 'year'])

        # Sort by the new multi-index
        combined_nc = combined_nc.unstack('time').sortby(['month', 'year']).stack()
        print(f"All datasets for variable {variable} processed successfully.")
    else:
        combined_nc = None
        print(f"No datasets were processed for variable {variable}.")
    return combined_nc

############
#### 

def process_multiple_scenarios(start_year, end_year, model, variable, scenarios, bounds=None, num_workers=4, log_func=None):
    results = {}
    for scenario in scenarios:
        key = f"{model}_{variable}_{scenario}"
        message = f"Starting processing for: {key}"
        if log_func:
            log_func(message)
        else:
            print(message)
        try:
            dataset = prepare_cmip6_netcdf(start_year, end_year, model, scenario, variable, bounds, num_workers)
            results[key] = dataset
            if dataset is not None:
                message = f"Data processed for: {key}"
                if log_func:
                    log_func(message)
                else:
                    print(message)
            else:
                message = f"No data returned for: {key}"
                if log_func:
                    log_func(message)
                else:
                    print(message)
        except Exception as e:
            message = f"Exception while processing {key}: {str(e)}"
            if log_func:
                log_func(message)
            else:
                print(message)
            results[key] = None
    return results



############ 
####
def export_datasets_to_netcdf(dataset_dict, output_folder):
    
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    for dataset_name, dataset in dataset_dict.items():
        output_path = os.path.join(output_folder, f"{dataset_name}.nc")
        dataset.to_netcdf(output_path)
        print(f"Saved dataset '{dataset_name}' to '{output_path}'")


##########
### 

#######   
def generate_maps(ds, variable):
    maps_data = []
    for year in ds.year.values:
        for month in ds.month.values:
            data = ds[variable].sel(month=month, year=year)
            data_numpy = data.values
            lat = data.lat.values
            lon = data.lon.values
            maps_data.append({
                'data': data_numpy,
                'lat_bounds': [lat.min(), lat.max()],
                'lon_bounds': [lon.min(), lon.max()],
                'month': month,
                'year': year
            })
    return maps_data

def create_folium_map(map_info):
    data_numpy = map_info['data']
    lat_bounds = map_info['lat_bounds']
    lon_bounds = map_info['lon_bounds']
    
    center_lat = np.mean(lat_bounds)
    center_lon = np.mean(lon_bounds)
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}',
        attr='Map data: National Geographic, Esri'
    )
    
    colormap = plt.get_cmap('RdYlBu_r')
    norm = plt.Normalize(vmin=data_numpy.min(), vmax=data_numpy.max())

    folium.raster_layers.ImageOverlay(
        image=data_numpy,
        bounds=[lat_bounds, lon_bounds],
        colormap=lambda x: colormap(norm(x)),
        opacity=0.6
    ).add_to(m)

    colorbar = LinearColormap(
        colors=[colormap(i) for i in np.linspace(0, 1, num=256)],
        vmin=data_numpy.min(),
        vmax=data_numpy.max(),
        caption='Temperature'
    )
    m.add_child(colorbar)
    folium.LayerControl().add_to(m)
    
    return m

def create_colorbar_file(cmap, vmin, vmax, filename='colorbar.png'):
    # Set up the figure and axis for the colorbar
    fig, ax = plt.subplots(figsize=(6, 1))
    norm = Normalize(vmin=vmin, vmax=vmax)
    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])

    # Creating the colorbar with automatic tick placement
    cbar = ColorbarBase(ax, cmap=cmap, norm=norm, orientation='horizontal')

    # Determine the number of ticks based on the data range
    num_ticks = 5  # You can adjust this number as needed
    ticks = np.linspace(vmin, vmax, num_ticks)
    cbar.set_ticks(ticks)

    # Format tick labels with precision, e.g., to two decimal places
    cbar.set_ticklabels([f"{tick:.2f}" for tick in ticks])

    # Ensure layout is tight so labels are not cut off
    plt.tight_layout()

    # Save the colorbar to a file
    plt.savefig(filename)
    plt.close()

