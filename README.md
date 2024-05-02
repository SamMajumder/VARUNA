# V.A.R.U.N.A. - Visual Analyzer for Regional Understanding of Numerical Atmospheric forecasts


<p align="center">
  <img src="https://raw.githubusercontent.com/SamMajumder/VARUNA/main/VARUNA-concept-art.webp" alt="Concept Image">
  <br>
  Created using DALL-E by OpenAI
</p>


## About V.A.R.U.N.A.

V.A.R.U.N.A., named after the Hindu deity of sky, ocean, and celestial order, is a tool designed for visualizing atmospheric forecasts derived from the Coupled Model Intercomparison Projects (CMIP6) climate models. This tool enables users to select a region of interest around a country, choose from a variety of climate models, and examine different climate variables across several Shared Socioeconomic Pathways (SSPs).

This tool can be run by downloading and clicking the VARUNA.bat executable file. 

Learn more about CMIP6 models, the climate forecasts and about the Intergovernmental Panel on Climate Change (IPCC):
1) Simple explanation on CMIP6 and IPCC: https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/
2) IPCC: https://www.ipcc.ch/
3) CMIP6: https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/


### Climate Models and Scenarios
This tool visualizes forecasts from 35 CMIP6 global climate models, helping predict how the climate could evolve based on various internal and external factors. The SSPs available in V.A.R.U.N.A. represent different pathways of socioeconomic development, affecting greenhouse gas emissions and land use in the future, including:
- **SSP 126**: A sustainable path aiming for a low greenhouse gas concentration.
- **SSP 245**: A middle-of-the-road scenario.
- **SSP 370**: High greenhouse gas emissions due to energy-intensive consumption.
- **SSP 585**: The highest greenhouse gas emissions pathway, representing a future with no policy changes to curb emissions.

A great resource to learn more about SSPs apart from the original publication: https://www.carbonbrief.org/explainer-how-shared-socioeconomic-pathways-explore-future-climate-change/

### Citation

Riahi, K., van Vuuren, D. P., Kriegler, E., Edmonds, J., O’Neill, B. C., Fujimori, S., Bauer, N., Calvin, K., Dellink, R., Fricko, O., Lutz, W., Popp, A., Crespo Cuaresma, J., KC, S., Leimbach, M., Jiang, L., Kram, T., Rao, S., Emmerling, J., ... Tavoni, M. (2017). The Shared Socioeconomic Pathways and their energy, land use, and greenhouse gas emissions implications: An overview. Global Environmental Change, 42, 153-168. https://doi.org/10.1016/j.gloenvcha.2016.05.009


### Climate Variables
The app allows exploration of various climate variables such as:
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

## Data Source

The NEX-GDDP-CMIP6 dataset, provided by NASA Earth Exchange, comprises global downscaled climate scenarios derived from the General Circulation Model (GCM) runs conducted under CMIP6. Developed in support of the IPCC's Sixth Assessment Report, these high-resolution, bias-corrected projections are distributed through the Earth System Grid Federation. The dataset spans all four 'Tier 1' SSPs, offering insights into climate change impacts on processes sensitive to climate gradients and local topography.

### Citation

NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6) was accessed on 2024-05-02 from https://registry.opendata.aws/nex-gddp-cmip6. NEX-GDDP-CMIP6 data was accessed on [date] from https://registry.opendata.aws/nex-gddp-cmip6

## Technology Stack

- **Data Retrieval and Preparation**: Python utility functions are used to retrieve and prepare the CMIP6 data from the Registry of Open Data on AWS.
- **Visualization and App Framework**: The visualization and interaction with the data are facilitated through an R Shiny application. This app leverages the robust capabilities of R for statistical analysis and the Shiny framework for creating interactive web applications.

### Citation

#### Python libraries:

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


#### R libraries:

1. **reticulate**
   - Ushey, K., Allaire, J., & Tang, Y. (2020). reticulate: Interface to Python. R package version 1.18. https://CRAN.R-project.org/package=reticulate

2. **here**
   - Müller, K. (2017). here: A simpler way to find your files. R package version 0.1. https://CRAN.R-project.org/package=here

3. **terra**
   - Hijmans, R. J. (2021). terra: Spatial Data Analysis. R package version 1.3-22. https://CRAN.R-project.org/package=terra

4. **sf**
   - Pebesma, E. (2018). Simple Features for R: Standardized Support for Spatial Vector Data. The R Journal, 10(1), 439-446. https://doi.org/10.32614/RJ-2018-009

5. **RColorBrewer**
   - Neuwirth, E. (2014). RColorBrewer: ColorBrewer Palettes. R package version 1.1-2. https://CRAN.R-project.org/package=RColorBrewer

6. **leaflet**
   - Cheng, J., Karambelkar, B., & Xie, Y. (2021). leaflet: Create Interactive Web Maps with the JavaScript 'Leaflet' Library. R package version 2.0.4.1. https://CRAN.R-project.org/package=leaflet

7. **tidyverse**
   - Wickham, H., Averick, M., Bryan, J., Chang, W., McGowan, L., François, R., Grolemund, G., Hayes, A., Henry, L., Hester, J., Kuhn, M., Pedersen, T., Miller, E., Bache, S. M., Müller, K., Ooms, J., Robinson, D., Seidel, D., Spinu, V., ... Yutani, H. (2019). Welcome to the tidyverse. Journal of Open Source Software, 4(43), 1686. https://doi.org/10.21105/joss.01686

8. **shiny**
   - Chang, W., Cheng, J., Allaire, J., Xie, Y., & McPherson, J. (2021). shiny: Web Application Framework for R. R package version 1.6.0. https://CRAN.R-project.org/package=shiny

9. **shinyWidgets**
   - Perrier, V., Meyer, F., & Granjon, D. (2021). shinyWidgets: Custom Inputs Widgets for Shiny. R package version 0.6.0. https://CRAN.R-project.org/package=shinyWidgets

10. **htmlwidgets**
    - Vaidyanathan, R., Xie, Y., Allaire, J., Cheng, J., & Russell, K. (2020). htmlwidgets: HTML Widgets for R. R package version 1.5.3. https://CRAN.R-project.org/package=htmlwidgets

11. **leaflet.providers**
    - Rudis, B. (2020). leaflet.providers: Leaflet Providers. R package version 1.9.0. https://CRAN.R-project.org/package=leaflet.providers

### Important Scripts

#### **`app.R`**
This R script orchestrates the user interface and server logic of the Shiny application for the V.A.R.U.N.A. project. It sets up the interactive web-based dashboard which allows users to visualize atmospheric forecasts derived from CMIP6 models. The script integrates various R packages for data handling (`terra`, `sf`), visualization (`leaflet`, `RColorBrewer`), and web app development (`shiny`, `shinyWidgets`). It uses a Python virtual environment through the `reticulate` package to leverage utility functions defined in Python for data retrieval and preprocessing.

#### **`R-functions.R`**
This R script contains custom functions used within the Shiny application to handle specific tasks such as dynamic map generation and data manipulation. The `createMap` function, for instance, dynamically generates leaflet maps based on user inputs from the app interface, adjusting display properties according to the selected climate data layers. This script enhances modularity and reusability by separating function definitions from the main application logic in `app.R`.

#### **`utils.py`**
This Python script provides utility functions for data retrieval and preprocessing, essential for the backend operations of the V.A.R.U.N.A. project. It includes functions to download and process climate model data from the Registry of Open Data on AWS, using libraries such as `boto3`, `s3fs`, and `xarray` to handle data in various formats (e.g., netCDF). The script also integrates spatial analysis tools from `geopandas` and `rioxarray` to adjust and prepare the data for visualization in the Shiny application.


## Contact

Developer: Dr. Sambadi Majumder - sambadimajumder@gmail.com
