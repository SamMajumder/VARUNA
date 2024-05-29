# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:28:58 2024

@author: Dr. M
"""

import streamlit as st
from streamlit_option_menu import option_menu
from utils import * ## may not be required but doing it just to be sure that we are importing the client id and client secret

# Import page functions
from About_Page import *
from download_page import *
from visualization_page import *







def main():
    st.title('VARUNA')
    # Sidebar navigation
    #st.sidebar.title('Navigation')
    selected = option_menu("Menu", ["About", "Data Retrieval", "Data Visualization"],
                           icons=['info-circle', 'cloud-upload', 'cloud-upload'],
                           menu_icon="cast", default_index=0)

    if selected == "About":
        about_page()
    elif selected == "Data Retrieval":
        data_retrieval_page()
    elif selected == "Data Visualization":
        data_visualization_page()

if __name__ == "__main__":
    main()