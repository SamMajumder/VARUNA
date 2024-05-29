# -*- coding: utf-8 -*-
"""
Created on Wed May 15 00:43:33 2024

@author: Dr. M
"""
# hook-rasterio.py

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('rasterio')
