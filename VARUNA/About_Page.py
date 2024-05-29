# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:28:16 2024

@author: Dr. M
"""


import os
import sys
import streamlit as st

def about_page():
    # Determine if running as a script or frozen executable
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    image_path = os.path.join(application_path, "VARUNA-concept-art.png")

    # Check if the image file exists
    if not os.path.exists(image_path):
        st.error(f"Image file not found: {image_path}")
    else:
        st.image(image_path, caption="Created using DALL-E by OpenAI.")

    st.title("About V.A.R.U.N.A.")
    st.markdown("""
    # V.A.R.U.N.A.
    **Visual Analyzer for Regional Understanding of Numerical Atmospheric data**

    Named after the Hindu deity of sky, ocean, and celestial order, VARUNA is a tool for visualizing atmospheric forecasts derived from CMIP6 models on a regional scale. This tool enables you to select a region around a country, choose from a variety of climate models, and examine different climate variables across several Shared Socioeconomic Pathways (SSPs).

    ## Learn more about CMIP6 models, climate forecasts, and the Intergovernmental Panel on Climate Change (IPCC):
    1. [Simple explanation on CMIP6 and IPCC](https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/)
    2. [IPCC](https://www.ipcc.ch/)
    3. [CMIP6](https://www.carbonbrief.org/cmip6-the-next-generation-of-climate-models-explained/)

    ## Climate Models and Scenarios
    This tool enables the user to visualize forecasts from 35 CMIP6 global climate models. These models help predict how the climate could evolve based on various internal and external factors.

    The SSPs represent different pathways of socioeconomic development, affecting greenhouse gas emissions and land use in the future. The scenarios available in VARUNA include:
    - **SSP 126**: A sustainable path aiming for a low greenhouse gas concentration.
    - **SSP 245**: A middle-of-the-road scenario.
    - **SSP 370**: A high greenhouse gas emissions due to energy-intensive consumption.
    - **SSP 585**: The highest greenhouse gas emissions pathway, representing a future with no policy changes to curb emissions.

    A great resource to learn more about SSPs apart from the original publication: [Explainer on SSPs](https://www.carbonbrief.org/explainer-how-shared-socioeconomic-pathways-explore-future-climate-change/)

    **Citation:**
    "Riahi, K., van Vuuren, D. P., Kriegler, E., Edmonds, J., O’Neill, B. C., Fujimori, S., Bauer, N., Calvin, K., Dellink, R., Fricko, O., Lutz, W., Popp, A., Crespo Cuaresma, J., KC, S., Leimbach, M., Jiang, L., Kram, T., Rao, S., Emmerling, J., ... Tavoni, M. (2017). The Shared Socioeconomic Pathways and their energy, land use, and greenhouse gas emissions implications: An overview. Global Environmental Change, 42, 153-168.(https://doi.org/10.1016/j.gloenvcha.2016.05.009).

    ## Climate Variables:
    1. **tas**: Temperature at Surface
    2. **tasmax**: Maximum Temperature at Surface
    3. **tasmin**: Minimum Temperature at Surface 
    4. **pr**: Mean Precipitation Flux 
    5. **hurs**: Near Surface Relative Humidity
    6. **huss**: Specific Humidity
    7. **rlds**: Downwelling Longwave Radiation at Surface
    8. **rsds**: Downwelling Shortwave Radiation at Surface
    9. **sfcWind**: Surface Wind Speed

    More information about these variables and how they are measured can be found [here](https://pcmdi.llnl.gov/mips/cmip3/variableList.html).

    ## Data Source:
    The NEX-GDDP-CMIP6 dataset, provided by NASA Earth Exchange, comprises global downscaled climate scenarios derived from the General Circulation Model (GCM) runs conducted under CMIP6. Developed in support of the IPCC's Sixth Assessment Report, these high-resolution, bias-corrected projections are distributed through the Earth System Grid Federation. The dataset spans all four 'Tier 1' SSPs, offering insights into climate change impacts on processes sensitive to climate gradients and local topography.

    **Citation:**
    1. NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6) was accessed on 2024-05-02 from [here](https://registry.opendata.aws/nex-gddp-cmip6). NEX-GDDP-CMIP6 data was accessed on [date] from [here](https://registry.opendata.aws/nex-gddp-cmip6).
    2. This tool was developed by Dr. Sambadi Majumder. For any questions and suggestions please feel free to email sambadimajumder@gmail.com.
    3. The source code and citations for libraries used can be found [here](https://github.com/SamMajumder/VARUNA).
    
    """)


