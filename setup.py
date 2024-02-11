import sys
from cx_Freeze import setup, Executable
import subprocess

# Comando para instalar os drivers do Playwright
install_playwright_drivers_cmd = "python -m playwright install"

# Executar o comando para instalar os drivers do Playwright
subprocess.run(install_playwright_drivers_cmd, shell=True, check=True)

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pickle"], 
    "includes": ["tkinter"],
    "include_files": ["./venv/lib/site-packages/playwright"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="BomControle Bot",
    version="2.1",
    description="Robotic Automation Process to extract DRE files from Bom Controle",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)