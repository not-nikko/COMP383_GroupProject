
import os
from snakemake.io import glob_wildcards

# 1. Path to your raw GWAS files
INPUT_DIR = "/path/to/file" 

# 2. Path where you want harmonized results to go
OUTPUT_DIR = "sample_outputs"

# 3. Path to the lab's script that needs patching
GWAS_SCRIPT = "summary-gwas-imputation/src/gwas_parsing.py"

# Load column overrides from your config.yaml
configfile: "config.yaml"


# This scans the INPUT_DIR and finds all files ending in .tsv.gz
SAMPLES, = glob_wildcards(os.path.join(INPUT_DIR, "{sample}.tsv.gz"))

rule all:
    input:
        ".patched",
        expand(os.path.join(OUTPUT_DIR, "{sample}_harmonized.txt.gz"), sample=SAMPLES)

rule patch_gwas_parsing:
    """
    Applies the sed fix to gwas_parsing.py. 
    The 'touch' command creates a hidden file so this only runs once.
    """
    input:
        GWAS_SCRIPT
    output:
        touch(".patched")
    shell:
        r"""
        sed -i 's/\[int(x) if not math.isnan(x) else "NA" for x in d.sample_size\]/[int(x) if (not isinstance(x, str) and not math.isnan(x)) else "NA" for x in d.sample_size]/' {input}
        """

rule harmonize_gwas:
    """
    The main processing rule. It links the input data, 
    the patched script, and the output destination.
    """
    input:
        script = GWAS_SCRIPT,
        data = os.path.join(INPUT_DIR, "{sample}.tsv.gz"),
        patch_check = ".patched" # This ensures the patch runs BEFORE harmonization
    output:
        os.path.join(OUTPUT_DIR, "{sample}_harmonized.txt.gz")
    params:
        # Dynamically adds --snp_col, --beta_col, etc., if defined in config.yaml
        extra = lambda wildcards: " ".join([
            f"--{k} {v}" for k, v in config.get("overrides", {}).get(wildcards.sample, {}).items()
        ])
    shell:
        "python3 run_gwas_harmonization.py "
        "-i {input.data} "
        "-o {output} "
        "{params.extra}"
