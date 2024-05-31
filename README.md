# V.A.R.U.N.A. - Visual Analyzer for Regional Understanding of Numerical Atmospheric data


<p align="center">
  <img src="https://raw.githubusercontent.com/SamMajumder/VARUNA/main/VARUNA-concept-art.webp" alt="Concept Image">
  <br>
  Created using DALL-E by OpenAI
</p>


## About V.A.R.U.N.A.

V.A.R.U.N.A., named after the Hindu deity of sky, ocean, and celestial order, is a tool designed for retrieving  and visualizing atmospheric data derived from the Coupled Model Intercomparison Projects (CMIP6) climate models. This tool enables users to select a region of interest around a country or continent, choose from a variety of climate models, and examine different climate variables across several Shared Socioeconomic Pathways (SSPs).

This tool can be run by downloading and clicking the VARUNA-GUI.exe executable file within the folder VARUNA


## Features

### Data Retrieval

The Data Retrieval page allows users to retrieve climate data based on their selection of CMIP6 models, climate variables, location, and target year. Key features include:

- **Model Selection**: Choose from up to 35 CMIP6 models. The full list of available models includes:
  1. ACCESS-CM2
  2. ACCESS-ESM1-5
  3. BCC-CSM2-MR
  4. CanESM5
  5. CESM2-WACCM
  6. CESM2
  7. CMCC-CM2-SR5
  8. CMCC-ESM2
  9. CNRM-CM6-1
  10. CNRM-ESM2-1
  11. EC-Earth3-Veg-LR
  12. EC-Earth3
  13. FGOALS-g3
  14. GFDL-CM4
  15. GFDL-CM4_gr1
  16. GFDL-ESM4
  17. GISS-E2-1-G
  18. HadGEM3-GC31-LL
  19. HadGEM3-GC31-MM
  20. IITM-ESM
  21. INM-CM4-8
  22. INM-CM5-0
  23. IPSL-CM6A-LR
  24. KACE-1-0-G
  25. KIOST-ESM
  26. MIROC-ES2L
  27. MIROC6
  28. MPI-ESM1-2-HR
  29. MPI-ESM1-2-LR
  30. MRI-ESM2-0
  31. NESM3
  32. NorESM2-LM
  33. NorESM2-MM
  34. TaiESM1
  35. UKESM1-0-LL

  Learn more about CMIP6 models and about the Intergovernmental Panel on Climate Change (IPCC):
  1) Simple explanation on CMIP6 and IPCC: https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/
  2) IPCC: https://www.ipcc.ch/
  3) CMIP6: https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/


- **Variable Selection**: Select from 9 climate variables:
  - **tas**: Temperature at Surface (units: Kelvin)
  - **tasmax**: Maximum Temperature at Surface (units: Kelvin)
  - **tasmin**: Minimum Temperature at Surface (units: Kelvin)
  - **pr**: Precipitation flux (units: kg m-2 s-1)
  - **hurs**: Relative Humidity (units: percent)
  - **huss**: Specific Humidity (units: dimensionless fraction)
  - **rlds**: Downwelling Longwave Radiation at Surface (units: W m-2)
  - **rsds**: Downwelling Shortwave Radiation at Surface (units: W m-2)
  - **sfcWind**: Mean Surface Wind Speed (units: meters per second)


  More information about these variables and how they are measured can be found here: https://pcmdi.llnl.gov/mips/cmip3/variableList.html


- **Location Input**: Enter the name of the place for which you want to retrieve data (preferably, a country or continent). Map data used is courtesy of copyrighted OpenStreetMap contributors and is available from https://www.openstreetmap.org. The Python library OSMnx provides an easy interface to this data.
- **Year Selection**: Specify the target year for the data retrieval. The data is fetched for a time range spanning 20 years around the target year (9 years before and 10 years after the target year) and then it is averaged across all years for a given month. This means a rolling monthly average is calculated around the target year.
- **Output Folder**: Define the folder where the retrieved data will be saved.


### Data Visualization

The Data Visualization page enables users to upload NetCDF files for different climate scenarios and visualize the data over basemap. Key features include:

![Example Image](https://raw.githubusercontent.com/SamMajumder/VARUNA/main/app-screenshot.png "This is an example image")


- **File Upload**: Upload NetCDF files for various SSP scenarios.
- **Variable Selection**: Choose the climate variable to visualize.
- **Maps**: Generate and display the data on basemaps using Folium Python library.
- **Monthly Data Navigation**: Use a slider to navigate through the data for different months.


## SSP Scenarios

The SSPs available, represent different pathways of socioeconomic development, affecting greenhouse gas emissions and land use in the future, including:
- **SSP 126**: A sustainable path aiming for a low greenhouse gas concentration.
- **SSP 245**: A middle-of-the-road scenario.
- **SSP 370**: High greenhouse gas emissions due to energy-intensive consumption.
- **SSP 585**: The highest greenhouse gas emissions pathway, representing a future with no policy changes to curb emissions.

A great resource to learn more about SSPs apart from the original publication: https://www.carbonbrief.org/explainer-how-shared-socioeconomic-pathways-explore-future-climate-change/

### Citation

Riahi, K., van Vuuren, D. P., Kriegler, E., Edmonds, J., O’Neill, B. C., Fujimori, S., Bauer, N., Calvin, K., Dellink, R., Fricko, O., Lutz, W., Popp, A., Crespo Cuaresma, J., KC, S., Leimbach, M., Jiang, L., Kram, T., Rao, S., Emmerling, J., ... Tavoni, M. (2017). The Shared Socioeconomic Pathways and their energy, land use, and greenhouse gas emissions implications: An overview. Global Environmental Change, 42, 153-168. https://doi.org/10.1016/j.gloenvcha.2016.05.009


## Data Source

The NEX-GDDP-CMIP6 dataset, provided by NASA Earth Exchange, comprises global downscaled climate scenarios derived from the General Circulation Model (GCM) runs conducted under CMIP6. Developed in support of the IPCC's Sixth Assessment Report, these high-resolution, bias-corrected projections are distributed through the Earth System Grid Federation. The dataset spans all four 'Tier 1' SSPs, offering insights into climate change impacts on processes sensitive to climate gradients and local topography.

### Citation

NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6) was accessed on 2024-05-02 from https://registry.opendata.aws/nex-gddp-cmip6. NEX-GDDP-CMIP6 data was accessed on [date] from https://registry.opendata.aws/nex-gddp-cmip6


## Libraries used in this project

This work would not have been possible without the following Python libraries. A big thanks to all the incredible developers and maintainers for these libraries.

1. **GeoPandas**
   - Joris Van den Bossche, et al. GeoPandas: Python tools for geographic data, (2014), GitHub repository, https://github.com/geopandas/geopandas

2. **matplotlib**
   - Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95. doi:10.1109/MCSE.2007.55

3. **boto3**
   - Amazon Web Services, Inc. Boto3: The AWS SDK for Python, (2021), GitHub repository, https://github.com/boto/boto3

4. **botocore**
   - Amazon Web Services, Inc. Botocore: Low-level interface to a growing number of Amazon Web Services, (2021), GitHub repository, https://github.com/boto/botocore

5. **s3fs**
   - Martin Durant, et al. S3Fs: A Pythonic file interface to S3, (2021), GitHub repository, https://github.com/dask/s3fs

6. **xarray**
   - Hoyer, S. & Hamman, J., (2017). xarray: N-D labeled arrays and datasets in Python. Journal of Open Research Software, 5(1), p.10. DOI: http://doi.org/10.5334/jors.148

7. **h5netcdf**
   - The h5netcdf developers. h5netcdf: Pythonic interface to the netCDF4 file format that doesn’t use the netCDF4 library, (2021), GitHub repository, https://github.com/h5netcdf/h5netcdf

8. **Shapely**
   - Sean Gillies, et al. Shapely: manipulation and analysis of geometric objects, (2021), GitHub repository, https://github.com/Toblerity/Shapely

9. **rioxarray**
   - Alan D. Snow, et al. rioxarray: geospatial xarray extension powered by rasterio, (2021), GitHub repository, https://github.com/corteva/rioxarray

10. **netCDF4**
    - Unidata. netCDF4: Python/numpy interface to the netCDF C library, (2021), GitHub repository, https://github.com/Unidata/netcdf4-python

11. **folium**
    - python-visualization. (2020). Folium. Retrieved from https://python-visualization.github.io/folium/

12. **osmnx**
    - Boeing, G. (2024). Modeling and Analyzing Urban Networks and Amenities with OSMnx. Working paper. https://geoffboeing.com/publications/osmnx-paper/

13. **streamlit**
    - https://docs.streamlit.io/

14. **streamlit_folium**
    - https://folium.streamlit.app/

15. **numpy**
    - Harris, C.R., Millman, K.J., van der Walt, S.J. et al. Array programming with NumPy. Nature 585, 357–362 (2020). https://doi.org/10.1038/s41586-020-2649-2


## Acknowledgement to OpenStreetMap and OSMnx

As mentioned earlier, this application uses OpenStreetMap data to enable the user to select the location during data retrieval process. Map data copyrighted OpenStreetMap contributors and available from https://www.openstreetmap.org . The awesome OSMnx Python library makes it possible to seamlessly interact with the OpenStreetMap data.


## Contact

Developer: Dr. Sambadi Majumder - sambadimajumder@gmail.com
