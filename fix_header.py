import gzip
import shutil

input_file = "data/sample_class_gwas/AoU_AFR_phenotype_836850_ACAF_sumstats_for_S-PrediXcan.txt.gz"
output_file = input_file.replace(".txt.gz", "_fixed.txt.gz")

with gzip.open(input_file, "rt") as infile, gzip.open(output_file, "wt") as outfile:
    # Fix header
    header = infile.readline().replace("#CHROM", "CHROM")
    outfile.write(header)

    # Copy rest of file unchanged
    shutil.copyfileobj(infile, outfile)

print(f"Fixed file written to: {output_file}")

