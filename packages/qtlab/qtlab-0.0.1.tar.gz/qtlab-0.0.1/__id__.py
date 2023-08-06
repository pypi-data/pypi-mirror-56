VERSION = "0.0.1"

ID = "qtlab"
APP_NAME = "QtLab Utilities"
DEPENDANCIES = ["openpyxl", "pandas", "scipy"]
DESCRIPTION = ""
KEYWORDS = "csv chart excel science uv-vis raman cary winuv omnic"
AUTHOR = "William Belanger"
URL = f"https://gitlab.com/william.belanger/{ID}"

CLASSIFIERS = [
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3.6",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows :: Windows 7",
]

SHORTCUTS = [
    ("", "QtLab"), ##tmp
    ("calc", "Solutions Calculator"),
    ("hsp", "Solvent Designer (HSP Calculator)"),
    ("peak", "CSV to Chart Converter"),
]

HELP = [
    "--help, -h: Show this help message",
    "--hsp: Open the HSP utility",
    "--calc: Open the solution calculator",
    "   --toggle: Toggle the calculator on or off",
    "--peak: Open the csv to chart conversion utility",
    "--quit: Close the application",
]

