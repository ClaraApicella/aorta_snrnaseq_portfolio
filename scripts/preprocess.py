#!/usr/bin/env python3
"""
preprocess.py
Performs Quality Control (QC), normalization, and highly variable gene (HVG) 
selection on a raw AnnData object. Designed to be called via Snakemake.
"""

import argparse
import scanpy as sc
import numpy as np

def preprocess_data(input_file, output_file):
    print(f"Loading data from {input_file}...")
    adata = sc.read_h5ad(input_file)
    
    # 1. Ensure we are working with raw counts
    # If the authors saved raw counts in adata.raw, we swap it to adata.X
    if adata.raw is not None:
        print("Extracting raw counts from adata.raw...")
        adata = adata.raw.to_adata()
    
    # Check if counts are integers (raw). If not, print a warning.
    # Note: Some sparse matrices don't support simple type checking, so we check a small sample
    sample_val = adata.X[0, 0] if hasattr(adata.X, "toarray") else adata.X[0, 0]
    if not float(sample_val).is_integer():
        print("WARNING: adata.X does not appear to contain raw integer counts. Proceeding anyway.")
    
    # 2. Quality Control (QC)
    print("Performing Quality Control...")
    # Basic filtering: 
    # - Cells must have at least 200 genes expressed
    # - Genes must be expressed in at least 3 cells
    sc.pp.filter_cells(adata, min_genes=200)
    sc.pp.filter_genes(adata, min_cells=3)
    
    # Mitochondrial percentage
    # Note: For single-*nuclei* RNA-seq, MT reads are typically very low (<1%) 
    # because the cytoplasm (containing mitochondria) is stripped away.
    adata.var['mt'] = adata.var_names.str.startswith('MT-') 
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    
    # Filter cells with unusually high mitochondrial content (e.g., > 5%)
    # and unusually high/low total counts (indicative of doublets or empty droplets)
    # We use very permissive thresholds here as a baseline for the portfolio.
    adata = adata[adata.obs.n_genes_by_counts < 4000, :]
    adata = adata[adata.obs.pct_counts_mt < 5, :]
    
    # 3. Normalization and Log-Transformation
    print("Normalizing and log-transforming data...")
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    
    # 4. Feature Selection (Highly Variable Genes)
    print("Identifying highly variable genes...")
    sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
    
    # Set the .raw attribute to the normalized and log-transformed data
    # so we can use it later for differential expression
    adata.raw = adata
    
    # Filter down to just the highly variable genes for downstream PCA/UMAP
    adata = adata[:, adata.var.highly_variable]
    
    # 5. Save the preprocessed object
    print(f"Saving preprocessed data to {output_file}...")
    adata.write(output_file)
    print("Preprocessing complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess snRNA-seq data.")
    parser.add_argument("-i", "--input", required=True, help="Path to input h5ad file")
    parser.add_argument("-o", "--output", required=True, help="Path to output preprocessed h5ad file")
    
    args = parser.parse_args()
    preprocess_data(args.input, args.output)
