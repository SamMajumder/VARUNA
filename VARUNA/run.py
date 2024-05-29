# -*- coding: utf-8 -*-
"""
Created on Wed May 15 09:48:06 2024

@author: Dr. M
"""



#import subprocess
#import os
#import sys

import subprocess
import os

def find_streamlit_executable():
    # Look for the streamlit executable in the specified path
    streamlit_path = 'C:\\Users\\samba\\anaconda3\\envs\\VARUNA-1.0\\Scripts\\streamlit.exe'
    if not os.path.isfile(streamlit_path):
        raise FileNotFoundError(f"Streamlit executable not found at {streamlit_path}")
    return streamlit_path

def get_script_path():
    try:
        # This will fail in an interactive environment
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "app.py"))
    except NameError:
        # Fallback for interactive environments
        script_path = os.path.abspath("app.py")
    
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"app.py not found at {script_path}")
    return script_path

def run_streamlit_app():
    streamlit_executable = find_streamlit_executable()
    script_path = get_script_path()
    command = [streamlit_executable, "run", script_path]
    log_file = "streamlit_app.log"
    
    with open(log_file, "w") as log:
        log.write(f"Running command: {command}\n")
        try:
            subprocess.run(command, check=True, stdout=log, stderr=log)
            log.write("Streamlit app started successfully.\n")
        except subprocess.CalledProcessError as e:
            log.write(f"Error running Streamlit: {e}\n")
            log.write(f"Command output: {e.output.decode() if e.output else 'No output'}\n")
        except Exception as e:
            log.write(f"Unexpected error: {e}\n")

if __name__ == "__main__":
    with open("streamlit_app.log", "w") as log:
        log.write("Starting Streamlit app...\n")
    try:
        run_streamlit_app()
    except Exception as e:
        with open("streamlit_app.log", "a") as log:
            log.write(f"Failed to start Streamlit app: {e}\n")
    with open("streamlit_app.log", "a") as log:
        log.write("Streamlit app has been started.\n")
