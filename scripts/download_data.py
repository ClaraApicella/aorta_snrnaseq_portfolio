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

import argparse
import yaml

if __name__ == "__main__":
    # 1. Set up argparse to allow command-line execution
    parser = argparse.ArgumentParser(description="Download dataset for scRNA-seq pipeline.")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    # 2. Find the config file relative to the script location
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(repo_root, args.config)
    
    # 3. Read the YAML configuration file
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        
    url = config['dataset']['url']
    filename = config['dataset']['filename']
    
    # 4. Define destination path
    data_dir = os.path.join(repo_root, "data")
    dest_path = os.path.join(data_dir, filename)
    
    os.makedirs(data_dir, exist_ok=True)
    
    if os.path.exists(dest_path):
        print(f"File already exists at {dest_path}. Skipping download.")
    else:
        download_file(url, dest_path)
