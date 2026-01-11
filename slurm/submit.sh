#!/bin/bash
#SBATCH --job-name=phewas_gwas
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

module load nextflow
module load python

nextflow run workflows/nextflow/main.nf \
  -profile slurm \
  --genotypes data/genotypes_demo.csv \
  --phenotypes data/phenotypes_demo.csv \
  --outdir results
