# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:27:00 2024

@author: Dr. M
"""

import streamlit as st
from utils import *
from streamlit_folium import st_folium
import io


def data_visualization_page():
    # Title for the page
    st.title("Data Visualization")

    # Sidebar components
    st.sidebar.title("Settings")

    # File upload for each scenario
    uploaded_files = {
        "SSP126": st.sidebar.file_uploader("Upload SSP126 NetCDF File", type=["nc"]),
        "SSP245": st.sidebar.file_uploader("Upload SSP245 NetCDF File", type=["nc"]),
        "SSP370": st.sidebar.file_uploader("Upload SSP370 NetCDF File", type=["nc"]),
        "SSP585": st.sidebar.file_uploader("Upload SSP585 NetCDF File", type=["nc"]),
    }

    # Dropdown for Climate Variable
    climate_vars = ["tas", "tasmax", "tasmin", "pr", "hurs", "huss", "rlds", "rsds", "sfcWind"]
    selected_climate_var = st.sidebar.selectbox("Climate Variable", climate_vars)

    # Load button
    load_button = st.sidebar.button("Load Data")

    # Initialize session state if not already initialized
    if "datasets" not in st.session_state:
        st.session_state["datasets"] = {}

    if load_button:
        # Initialize dataset dictionary
        datasets = {
            "SSP126": None,
            "SSP245": None,
            "SSP370": None,
            "SSP585": None
        }

        # Load datasets from the uploaded files
        for scenario, uploaded_file in uploaded_files.items():
            if uploaded_file is not None:
                # Read the file content into a BytesIO object
                bytes_data = uploaded_file.read()
                file_obj = io.BytesIO(bytes_data)
                
                # Load the dataset from the BytesIO object
                ds = xr.open_dataset(file_obj)
                st.session_state["datasets"][scenario] = ds
                st.write(f"Loaded dataset '{uploaded_file.name}' as {scenario}")

    # Visualization
    if "datasets" in st.session_state and any(st.session_state["datasets"].values()):
        scenario_names = [key for key, value in st.session_state["datasets"].items() if value is not None]
        datasets = [st.session_state["datasets"][name] for name in scenario_names]

        # Scenario names for tabs
        tabs = st.tabs(scenario_names)
        for tab, ds, scenario in zip(tabs, datasets, scenario_names):
            with tab:
                variable = selected_climate_var  # Use the selected climate variable
                maps_data = generate_maps(ds, variable)

                month_index = st.slider('Select a Month', min_value=1, max_value=12, value=1, key=f'month_{scenario}')

                selected_map_info = next((item for item in maps_data if item['month'] == month_index), None)

                if selected_map_info:
                    min_val = selected_map_info['data'].min()
                    max_val = selected_map_info['data'].max()
                    create_colorbar_file(plt.get_cmap('RdYlBu_r'), min_val, max_val)
                    map_obj = create_folium_map(selected_map_info)
                    map_return = st_folium(map_obj, width=700, height=500)
                    st.image('colorbar.png', caption='Color Scale')
                else:
                    st.write("No data available for the selected month.")
    else:
        st.write("Welcome to VARUNA-1.0! Please upload NetCDF files for the scenarios and click 'Load Data'.")