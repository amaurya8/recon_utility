# %fs cp dbfs:/FileStore/my_project.zip /tmp/my_project.zip

import zipfile
import os

local_zip_path = "/dbfs/FileStore/my_project.zip"
extract_path = "/dbfs/tmp/my_project"

with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

import sys
sys.path.append("/dbfs/tmp/my_project/my_project")  # Add to module search path

# Now you can import and run your code
from main import main_func
main_func()

# Run the recon_main.py module directly
runpy.run_path("/dbfs/tmp/my_project/my_project/recon_main.py", run_name="__main__")


import os

path = "/dbfs/tmp/my_project/my_project/"
files = os.listdir(path)
print("Files in path:", files)

import os
import sys

print("Current working directory:", os.getcwd())
print("sys.path:", sys.path)
print("Files in directory:", os.listdir("/dbfs/tmp/my_project/my_project"))

os.chdir("/dbfs/tmp/my_project/my_project")

# If your requirements.txt is at /dbfs/tmp/my_project/requirements.txt
%pip install -r /dbfs/tmp/my_project/requirements.txt

import subprocess

requirements_path = "/dbfs/tmp/my_project/requirements.txt"
subprocess.check_call(["pip", "install", "-r", requirements_path])

#Creating requirement.txt:
windows:

.\venv\Scripts\activate

pip freeze > requirements.txt

OR

pip install pipreqs
pipreqs /path/to/your/project


