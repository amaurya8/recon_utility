from setuptools import setup, find_packages

setup(
    name="recon_utility",
    version="1.0.0",
    description="A configurable reconciliation utility for comparing data from files and databases",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),  # Automatically finds Python packages
    install_requires=[
        "pandas",
        "datacompy",
        "cx_Oracle",
        "pyodbc",
        "openpyxl"  # For reading Excel files
    ],
    entry_points={
        "console_scripts": [
            "recon-run=recon_main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

ow to Use setup.py

1. Install Your Project Locally

Run this command in the project directory:

pip install .

This will install your project as a package.

2. Run the Recon Utility

After installation, you can run it as:

recon-run

3. Create a Distributable Package

To create a package for distribution:
    python setup.py sdist bdist_wheel

