# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, copy_metadata
import os

# Collect necessary data files
datas = collect_data_files("streamlit")
datas += copy_metadata("streamlit")
datas.append(('app.py', '.'))  # Add app.py to the datas 

# Specify the absolute path for the VARUNA-concept-art.png file
image_path = os.path.abspath('VARUNA-concept-art.png')

# Add your image file with the absolute path to the datas list
datas.append((image_path, '.'))

# Add additional Python files
datas.append(('utils.py', '.'))  # Add utils.py
datas.append(('About_Page.py', '.'))  # Add About_Page.py
datas.append(('download_page.py', '.'))  # Add download_page.py
datas.append(('visualization_page.py', '.'))  # Add visualization_page.py

# Add the streamlit executable
streamlit_executable_path = 'C:\\Users\\samba\\anaconda3\\envs\\VARUNA-1.0\\Scripts\\streamlit.exe'
datas.append((streamlit_executable_path, 'Scripts'))

a = Analysis(
    ['run.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=None,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show the console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VARUNA',
)
