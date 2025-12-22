import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

projectName = "ApparelSalesClassification"

# List of folders to create
foldersList = [
    ".github/workflows",
    f"{projectName}/src",
    f"{projectName}/data",
    f"{projectName}/models",
    f"{projectName}/visuals",
    f"{projectName}/logging",
    f"{projectName}/output",
    f"{projectName}/pipeline",
]

# List of files to create in root directory
filesList = [
    "app.py",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
]

# Create folders
for folderPath in foldersList:
    os.makedirs(folderPath, exist_ok=True)
    logging.info(f"Creating Directory: {folderPath}")

# Create root-level files
for fileName in filesList:
    if not os.path.exists(fileName) or os.path.getsize(fileName) == 0:
        with open(fileName, "w") as f:
            pass
        logging.info(f"Creating empty file: {fileName}")
    else:
        logging.info(f"{fileName} already exists.")