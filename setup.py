import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"], 
    "includes": ["tkinter"],
    "include_files": ["venv/lib/python3.10/site-packages/playwright"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="RPA_BomControle",
    version="0.1",
    description="Robotic Automation Process to extract DRE files from Bom Controle",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)