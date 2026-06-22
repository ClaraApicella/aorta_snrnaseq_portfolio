# Aortic Aneurysm snRNA-seq Reanalysis

This repository contains a bioinformatics portfolio project reanalyzing human single-nuclei RNA-seq (snRNA-seq) data from the aneurysmal aorta. 

The project uses the Python scientific stack (`Scanpy`, `AnnData`) and is orchestrated using a Snakemake pipeline.

## Dataset
We are utilizing dataset **[GSE207784](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE207784)**.
- **Title:** Aortic Cellular Diversity and Quantitative GWAS Trait Prioritization through Single Nuclear RNA Sequencing (snRNA-Seq) of the Aneurysmal Human Aorta.
- **Size:** ~71,689 nuclei from 13 human thoracic aorta samples.

## Workflow

This repository is built step-by-step to ensure reproducibility:
1. Data downloading
2. Quality Control & Preprocessing
3. Downstream Analysis & Clustering
4. Snakemake Pipeline Integration
