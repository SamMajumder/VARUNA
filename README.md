# V.A.R.U.N.A. - Visual Analyzer for Regional Understanding of Numerical Atmospheric forecasts


![Alt text](https://raw.githubusercontent.com/SamMajumder/VARUNA/main/VARUNA-concept-art.webp)


## About V.A.R.U.N.A.

V.A.R.U.N.A., named after the Hindu deity of sky, ocean, and celestial order, is a tool designed for visualizing atmospheric forecasts derived from CMIP6 models on a regional scale. This tool enables users to select a region around a country, choose from a variety of climate models, and examine different climate variables across several Shared Socioeconomic Pathways (SSPs).

### Climate Models and Scenarios
This tool visualizes forecasts from 35 CMIP6 global climate models, helping predict how the climate could evolve based on various internal and external factors. The SSPs available in V.A.R.U.N.A. represent different pathways of socioeconomic development, affecting greenhouse gas emissions and land use in the future, including:
- **SSP 126**: A sustainable path aiming for a low greenhouse gas concentration.
- **SSP 245**: A middle-of-the-road scenario.
- **SSP 370**: High greenhouse gas emissions due to energy-intensive consumption.
- **SSP 585**: The highest greenhouse gas emissions pathway, representing a future with no policy changes to curb emissions.

### Climate Variables
The app allows exploration of various climate variables such as:
- **tas**: Temperature at Surface
- **tasmax**: Maximum Temperature at Surface
- **tasmin**: Minimum Temperature at Surface
- **pr**: Precipitation
- **hurs**: Relative Humidity
- **huss**: Specific Humidity
- **rlds**: Downwelling Longwave Radiation at Surface
- **rsds**: Downwelling Shortwave Radiation at Surface
- **sfcWind**: Surface Wind Speed

## Data Source

The NEX-GDDP-CMIP6 dataset, provided by NASA Earth Exchange, comprises global downscaled climate scenarios derived from the General Circulation Model (GCM) runs conducted under CMIP6. Developed in support of the IPCC's Sixth Assessment Report, these high-resolution, bias-corrected projections are distributed through the Earth System Grid Federation. The dataset spans all four 'Tier 1' SSPs, offering insights into climate change impacts on processes sensitive to climate gradients and local topography.

## Technology Stack

- **Data Retrieval and Preparation**: Python utility functions are used to retrieve and prepare the CMIP6 data from the Registry of Open Data on AWS.
- **Visualization and App Framework**: The visualization and interaction with the data are facilitated through an R Shiny application. This app leverages the robust capabilities of R for statistical analysis and the Shiny framework for creating interactive web applications.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## Contact

Developer: Dr. Sambadi Majumder - sambadimajumder@gmail.com
