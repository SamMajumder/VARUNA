
###
install.packages("reticulate")
library(reticulate)

# Create a virtual environment for the project
virtualenv_create(envname = "VARUNA")

# Use the created virtual environment
use_virtualenv("VARUNA", required = TRUE)

# Install necessary Python packages
py_install(c("geopandas", "matplotlib", "boto3", "s3fs", "xarray", 
             "h5netcdf", "shapely", "rioxarray"), 
           envname = "VARUNA")


# Install necessary Python packages including netCDF4 for handling NetCDF files
py_install(c("netCDF4"),
           envname = "VARUNA")


# Verify installation by importing a module
py_run_string("import geopandas")


install.packages("here")
install.packages("terra")
install.packages("sf")
install.packages("leaflet")
install.packages("tidyverse")
install.packages("shiny")
install.packages("shinyWidgets")
install.packages("htmlwidgets")
install.packages("RColorBrewer")
