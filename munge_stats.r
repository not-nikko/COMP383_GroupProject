library(MungeSumstats)

# our summary stats file relates to GRch38, so we need to install SNPlocs.Hsapiens.dbSNP144.GRCh38 and BSgenome.Hsapiens.NCBI.GRCh38 from Bioconductor as follows: 

options(timeout=2000)
BiocManager::install("SNPlocs.Hsapiens.dbSNP155.GRCh38")
BiocManager::install("BSgenome.Hsapiens.NCBI.GRCh38")

library(SNPlocs.Hsapiens.dbSNP155.GRCh38)
library(BSgenome.Hsapiens.NCBI.GRCh38)
# doewnload the one below if the reference genoomes of the GWAS is ch37
#BiocManager::install("SNPlocs.Hsapiens.dbSNP155.GRCh37")
#BiocManager::install("BSgenome.Hsapiens.1000genomes.hs37d5")
# these are big downloads of 800kb


# required inputs to run Munge sumstats are path, ref_genome, and save_path)

format_sumstats(path="/home/data/Project3/AoU_AFR_phenotype_836850_ACAF_sumstats_for_S-PrediXcan.txt.gz", 
ref_genome="GRCh38", save_path = "/home/csebastian/COMP383_GroupProject/harmonized_summary_stats/AoU_formatted1.txt.gz")

# 
