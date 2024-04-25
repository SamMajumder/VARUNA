# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:25:29 2024

@author: Dr. M
"""


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



## get my current working directory first 
print(os.getcwd())


#### Let's load in a shapefile which has outlines of continents. 
## prepping the shapefile 

# Relative path to the shapefile
shapefile_path = 'Data\\Shapefile\\World_Continents.shp'

# Read the shapefile
gdf = gpd.read_file(shapefile_path)

# Print column headers to see the dataframe's structure
print(gdf.columns)

## only select CONTINENT and geometry ##

gdf = gdf[["CONTINENT","geometry"]]

## removing Antarctica 

gdf = gdf[gdf["CONTINENT"] != "Antarctica"] 


##### Now extracting a the roi of a specific area 
### isolating asia

Asia = gdf[gdf["CONTINENT"] == "Asia"].to_crs("EPSG: 4326")

### extracting the bounds
bounds = Asia.total_bounds 

### 
# Configure s3fs to interact with the S3 bucket
fs = s3fs.S3FileSystem(anon=True)

# Specify the S3 file path
file_path = 's3://nex-gddp-cmip6/NEX-GDDP-CMIP6/ACCESS-CM2/ssp126/r1i1p1f1/pr/pr_day_ACCESS-CM2_ssp126_r1i1p1f1_gn_2027_v1.1.nc'

# Use xarray to open the dataset directly from S3, letting xarray manage the file system
ds = xr.open_dataset(fs.open(file_path, mode='rb'), engine='h5netcdf')

print(ds)


# Compute the monthly mean
monthly_pr = ds['pr'].groupby('time.month').mean('time').astype('float32')

## set the crs 
monthly_pr.rio.write_crs("epsg:4326", inplace=True)

print(monthly_pr)  



clipped_netcdf = monthly_pr.rio.clip_box(*bounds)

print(clipped_netcdf)


# Apply the mask
masked_data = monthly_pr.rio.clip(Asia.geometry.apply(mapping), Asia.crs, drop=False, invert=False)



import matplotlib.pyplot as plt

# Select the first layer of the DataArray
first_layer = clipped_netcdf.isel(month=0)

# Plot using Matplotlib
plt.figure(figsize=(10, 6))
plt.pcolormesh(first_layer.lon, first_layer.lat, first_layer, shading='auto')
plt.colorbar(label='Precipitation (kg m-2 s-1)')
plt.title('Monthly Precipitation for January')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()



# Select the first layer of the DataArray
first_layer = masked_data.isel(month=0)

# Plot using Matplotlib
plt.figure(figsize=(10, 6))
plt.pcolormesh(first_layer.lon, first_layer.lat, first_layer, shading='auto')
plt.colorbar(label='Precipitation (kg m-2 s-1)')
plt.title('Monthly Precipitation for January')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()



    
    


### plotting 
# Define a base map centered around a relevant location (let's approximate Asia's centroid)
m = folium.Map(location=[35, 100], zoom_start=4)

# Add the ROI GeoDataFrame to the map
folium.GeoJson(
    roi_gdf,
    name='geojson'
).add_to(m)

# Add layer control to toggle layers
folium.LayerControl().add_to(m)

# Save the map as an HTML file
m.save('Asia_outline_roi_map.html')

Asia.total_bounds







#### establishing connection to the bucket

s3 = boto3.client('s3', region_name='us-west-2', config=Config(signature_version=UNSIGNED))


#### list the objects or directories

response = s3.list_objects_v2(Bucket='nex-gddp-cmip6')
if 'Contents' in response:  # Check if the bucket is not empty
    for item in response['Contents']:
        print(item['Key'])



# Configure s3fs to interact with the S3 bucket
fs = s3fs.S3FileSystem(anon=True)

# Specify the S3 file path
file_path = 's3://nex-gddp-cmip6/NEX-GDDP-CMIP6/ACCESS-CM2/ssp126/r1i1p1f1/pr/pr_day_ACCESS-CM2_ssp126_r1i1p1f1_gn_2027_v1.1.nc'

# Use xarray to open the dataset directly from S3, letting xarray manage the file system
ds = xr.open_dataset(fs.open(file_path, mode='rb'), engine='h5netcdf')

print(ds)

# For the original dataset 'ds'
print("Min value in original data:", ds['pr'].min().values)
print("Max value in original data:", ds['pr'].max().values)


# Compute the monthly mean
monthly_pr = ds['pr'].groupby('time.month').mean('time')
print(monthly_pr)


# For the monthly averages 'monthly_pr'
print("Min value in monthly data:", monthly_pr.min().values)
print("Max value in monthly data:", monthly_pr.max().values)

monthly_pr.isnull().sum()



# Load data into memory to avoid read issues during computation
ds['pr'] = ds['pr'].load()


ds['pr'].min().values

# Now try to find min and max
print("Min value in original data:", ds['pr'].min().values)
print("Max value in original data:", ds['pr'].max().values)

# Count NaN values in the 'pr' data variable
nan_count = ds['pr'].isnull().sum()

# Print the number of NaN values
print("Number of NaN values in original data:", nan_count.values)

######################
import rasterio
from rasterio.mask import mask

# Function to clip the raster with the geometry
def clip_raster(raster_path, shapes):
    with rasterio.open(raster_path) as src:
        out_image, out_transform = mask(src, shapes, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

    return out_image, out_meta

# Assuming 'Asia.geometry' is your shape
# And 'path_to_your_netcdf' is where your raster data is stored
# Note: Ensure the CRS matches between your shapefile and raster data
clipped_image, clipped_meta = clip_raster('path_to_your_netcdf.nc', Asia.geometry)

# Now, you can write the clipped image to a new raster file
with rasterio.open('clipped_raster.tif', 'w', **clipped_meta) as dest:
    dest.write(clipped_image)



















