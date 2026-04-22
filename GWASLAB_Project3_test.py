#import the gwaslab library to be used for downstream harmonization from the GWAS summary statistics
import gwaslab as gl

#provide a certain pathway to the test data
#mysumstats provides an interpretation on each column provided in the file to be used for harmonizat>
mysumstats = gl.Sumstats("/home/data/Project3/hg38_AoU_AFR_phenotype_836850_ACAF_sumstats.tsv.gz",
        snpid = "variant_id",           
        chrom = "chromosome",      
        pos = "position",            
        ea = "effect_allele",  
        eaf = "frequency",                   
        nea = "non_effect_allele",            
        beta = "effect_size",          
        se = "standard_error",                      
        p = "pvalue",     
        n = "sample_size",      
        sep = r"\t"
)

#this provides basica quality control checks on the current file that has been used for testing purposes
mysumstats.basic_check()

mysumstats.harmonize(
    ref_seq="/home/nalde/GRCh38.fa",
    verbose=True)

mysumstats.harmonize(
    ref_seq="/home/nalde/GRCh38_fixed.fa",
    verbose=True
)

#create a new file with the harmonized data
mysumstats.to_csv("harmonized_sumstats.tsv", sep="\t", index = False)

import csv

with open("gwaslab_spredixcan_results.csv", newline='') as f:
    reader = csv.DictReader(f)
    
    # Get column names
    columns = reader.fieldnames
    print("Detected columns:", columns)

    # Find columns automatically and try to produce expected results
    used_col = None
    total_col = None

    for col in columns:
        col_lower = col.lower()
        if "used" in col_lower:
            used_col = col
        if "total" in col_lower or "all" in col_lower:
            total_col = col

    print("Using columns:", used_col, total_col)

    used_col = "n_snps_used"
    total_col = "n_snps_in_model"

    used_sum = 0
    total_sum = 0

    for row in reader:
        try:
            used_sum += float(row[used_col])
            total_sum += float(row[total_col])
        except:
            pass

# provide output for the SNP percentage
if total_sum > 0:
    print(f"Percentage of SNPs used: {(used_sum / total_sum) * 100:.2f}%")
else:
    print("Could not calculate percentage")