# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:25:54 2024

@author: Dr. M
"""

from utils import *

import streamlit as st

def log_message(message):
    st.write(message)
    print(message)

def data_retrieval_page():
    valid_models = [
        "ACCESS-CM2", "ACCESS-ESM1-5", "BCC-CSM2-MR", "CanESM5", "CESM2-WACCM",
        "CESM2", "CMCC-CM2-SR5", "CMCC-ESM2", "CNRM-CM6-1", "CNRM-ESM2-1",
        "EC-Earth3-Veg-LR", "EC-Earth3", "FGOALS-g3", "GFDL-CM4", "GFDL-CM4_gr1",
        "GFDL-ESM4", "GISS-E2-1-G", "HadGEM3-GC31-LL", "HadGEM3-GC31-MM",
        "IITM-ESM", "INM-CM4-8", "INM-CM5-0", "IPSL-CM6A-LR", "KACE-1-0-G",
        "KIOST-ESM", "MIROC-ES2L", "MIROC6", "MPI-ESM1-2-HR", "MPI-ESM1-2-LR",
        "MRI-ESM2-0", "NESM3", "NorESM2-LM", "NorESM2-MM", "TaiESM1",
        "UKESM1-0-LL"
    ]

    climate_variables = [
        "tas", "tasmax", "tasmin", "pr", "hurs", "huss", "rlds", "rsds", "sfcWind"
    ]

    st.title("Data Retrieval")
    st.write("Please make your selections and hit submit.")

    # Dropdowns and text input boxes
    model_choice = st.selectbox("CMIP6 Model Choice", valid_models)
    variable_choice = st.selectbox("Climate Variable", climate_variables)
    place_name = st.text_input("Place Name")
    target_year = st.number_input("Target Year", min_value=1900, max_value=2100, step=1)
    output_folder = st.text_input("Output Folder")

    # Submit button
    if st.button("Submit"):
        log_message("Starting the data retrieval process...")

        if output_folder:
            log_message(f"Output folder selected: {output_folder}")
            try:
                bounds = extract_bounds_osmnx(place_name)
                log_message(f"Bounds extracted: {bounds}")

                start_year = target_year - 9
                end_year = target_year + 10
                scenarios = ["ssp126", "ssp245", "ssp370", "ssp585"]

                results = process_multiple_scenarios(start_year=start_year,
                                                     end_year=end_year,
                                                     model=model_choice,
                                                     variable=variable_choice,
                                                     scenarios=scenarios,
                                                     bounds=bounds,
                                                     num_workers=4,
                                                     log_func=log_message)

                export_datasets_to_netcdf(results, output_folder)
                log_message("Data retrieval and export completed.")
            except Exception as e:
                log_message(f"An error occurred: {e}")
        else:
            log_message("No output folder selected")