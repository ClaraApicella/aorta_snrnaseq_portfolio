#!/usr/bin/env python3
"""
download_data.py
Downloads the GSE207784 snRNA-seq dataset (h5ad format) from NCBI GEO.
"""

import os
import urllib.request
import sys

def download_file(url, dest_path):
    print(f"Downloading from {url}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Successfully downloaded to {dest_path}")
    except Exception as e:
        print(f"Failed to download: {e}")
        sys.exit(1)

if __name__ == "__main__":
    url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE207nnn/GSE207784/suppl/GSE207784_AorticAneurysm_scportal_06.29.2022.h5ad.gz"
    
    # Define destination path
    # We place it in the 'data' directory relative to the repository root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(repo_root, "data")
    dest_path = os.path.join(data_dir, "GSE207784_AorticAneurysm_scportal_06.29.2022.h5ad.gz")
    
    os.makedirs(data_dir, exist_ok=True)
    
    if os.path.exists(dest_path):
        print(f"File already exists at {dest_path}. Skipping download.")
    else:
        download_file(url, dest_path)
