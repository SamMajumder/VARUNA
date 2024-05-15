# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:48:06 2024

@author: samba
"""

import subprocess


def run_streamlit_app():
    command = ["streamlit", "run", "app.py"]
    subprocess.run(command)

run_streamlit_app()  



