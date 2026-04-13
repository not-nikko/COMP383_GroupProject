# COMP383_GroupProject
Project 3 - Harmonize GWAS Summary Statistics for S-PrediXcan

## Project Overview
The purpose of this project was to create a pipe line 

For more information about the Introduction, Dataset, and project workflow please look at the Wiki page.


## Dependencies Used
### Sodtwares
- conda -> creates an environment for Metxcan and Predixcan to be ran on 
- Linux or macOS
- Python 
- R 
### Python Pakcages
	- numpy 
	- scipy
	- pandas
	
### external tools 
	- summary-gwas-imputation
	- GWAS Catalog datasets

### Description of scripts 
	- S-Predixcan
	- 

## Set up Instructions 

Create a folder and name it Finalproject 
move into that folder 

cloned this repo
```bash
git clone https://github.com/christina2564/COMP383_GroupProject
```
In this repo you should have, config.yaml, environment.yaml, Snakefile, all in the same directory 

create a directory called gwas_stats. This is where you will store the gwas summary statistics you want to harmonize 
```bash
gwas_stats
```
To test if this works, download this gwas summary stat into the directory 
```bash
cd gwas_stats
wget http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90568001-GCST90569000/GCST90568441/GCST90568441.tsv.gz
```




## Instructions 

STEP 1
Cloned the Metaxcan harmonization tool lab repo into my Final_Project directory:
```bash
cd ~/Final_Project
git clone https://github.com/hakyimlab/summary-gwas-imputation.git
```
Verify it downloaded correctly and that gwas_parsing.py is in the folder:
```bash
ls ~/Final_Project/summary-gwas-imputation/src/
```
gwas_parsing.py is in the output.


### Data set set up 
To download ADHD GWAS summary statistics used to test pipeline:
```bash
wget http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90568001-GCST90569000/GCST90568441/GCST90568441.tsv.gz
```

### Installing Metxcan (S-Predixcan)
STEP 2 — DOWNLOAD MetaXcan (S-PrediXcan)

Clone the MetaXcan repo into my Final_Project directory:
```bash
cd ~/Final_Project
git clone https://github.com/hakyimlab/MetaXcan.git
```

Verify SPrediXcan.py is there:
```bash
ls ~/Final_Project/MetaXcan/software/SPrediXcan.py
```

For more information/instructions on downloading Metaxcan, go to the Metaxcan Lab GitHub: https://github.com/hakyimlab/MetaXcan/blob/master/README.md 

### Installing Dependencies 
STEP 3 — INSTALL DEPENDENCIES

Check that numpy, pandas, and scipy are available:
on bash 
```bash
python3 -c "import numpy, pandas, scipy; print('OK')"
```
Install pyliftover which is required by gwas_parsing.py:

```bash
pip install pyliftover --break-system-packages
```
Check that genomic_tools_lib is accessible:

```bash
python3 -c "import sys; sys.path.insert(0, '/home/mabdulmuiz/Final_Project/summary-gwas-imputation/src'); import genomic_tools_lib; print('OK')"
```

### STEP 4 — PATCH gwas_parsing.py

There is a bug in gwas_parsing.py that causes a crash when the
input file does not have a sample_size column. Apply this fix:

```bash
sed -i 's/\[int(x) if not math.isnan(x) else "NA" for x in d.sample_size\]/[int(x) if (not isinstance(x, str) and not math.isnan(x)) else "NA" for x in d.sample_size]/' ~/Final_Project/summary-gwas-imputation/src/gwas_parsing.py
```
This only needs to be done once after cloning the repo.


### STEP 5 — HARMONIZATION SCRIPT
 
Copy run_gwas_harmonization.py into my Final_Project directory:

```bash
cp run_gwas_harmonization.py ~/Final_Project/
```
Open the script and update the GWAS_PARSING_SCRIPT path at the top
if your directory structure is different:

```python
    GWAS_PARSING_SCRIPT = os.path.expanduser(
        "~/Final_Project/summary-gwas-imputation/src/gwas_parsing.py"
    )
```


### Running harmonization tool
STEP 6 — RUN THE HARMONIZATION SCRIPT

The script automatically detects column names from the input file.
We do not need to specify column names for most standard GWAS files.

On command line (to use with your own gwas summary statistics with a different name, replace path/to/your_gwas_file.tsv.gz with path to your file: 
```bash
python3 run_gwas_harmonization.py \
        -i /path/to/your_gwas_file.tsv.gz \
        -o /path/to/your_harmonized_output.txt.gz
```

Example using the GWAS Catalog file on this repo:

```bash
    python3 run_gwas_harmonization.py \
        -i ~/Final_Project/data/GCST90568441.tsv.gz \
        -o ~/Final_Project/sample_outputs/GCST90568441_harmonized.txt.gz
```

If auto-detection fails for any column, we can override manually (example):
```bash
    python3 run_gwas_harmonization.py \
        -i ~/Final_Project/data/my_gwas.tsv.gz \
        -o ~/Final_Project/sample_outputs/my_harmonized.txt.gz \
        --snp_col SNP \
        --pvalue_col P \
        --beta_col BETA
```

Available column override flags:
```bash
    --snp_col           SNP/variant ID column
    --effect_allele_col Effect allele column
    --other_allele_col  Non-effect allele column
    --beta_col          Beta/effect size column
    --se_col            Standard error column
    --pvalue_col        P-value column
    --freq_col          Allele frequency column
    --chr_col           Chromosome column
    --pos_col           Base pair position column
```

### Running Predixcan
STEP 7 — RUN S-PREDIXCAN ON HARMONIZED OUTPUT
To run predixcan you must navigate to the software folder in the folder Metaxcan

```bash
cd Metaxcan/software
```
Activate the conda environment to run Predixcan in:

```bash
conda activate imlabtools
```

if conda is not installed, run:

```bash
conda env create -f /path/to/this/repo/software/conda_env.yaml
```

After harmonization, run S-PrediXcan using the standardized column names that the harmonization script will always output:

```bash
    python3 ~/Final_Project/MetaXcan/software/SPrediXcan.py \
        --model_db_path /home/data/Project3/elastic-net-with-phi/en_Whole_Blood.db \
        --covariance /home/data/Project3/elastic-net-with-phi/en_Whole_Blood.txt.gz \
        --gwas_folder /path/to/harmonized/output/folder \
        --gwas_file_pattern "your_harmonized_output.txt.gz" \
        --snp_column variant_id \
        --effect_allele_column effect_allele \
        --non_effect_allele_column non_effect_allele \
        --beta_column effect_size \
        --se_column standard_error \
        --pvalue_column pvalue \
        --output_file /path/to/results/spredixcan_results.csv
```
Example using the GWAS Catalog file:

```bash
    python3 ~/Final_Project/MetaXcan/software/SPrediXcan.py \
        --model_db_path /home/data/Project3/elastic-net-with-phi/en_Whole_Blood.db \
        --covariance /home/data/Project3/elastic-net-with-phi/en_Whole_Blood.txt.gz \
        --gwas_folder ~/Final_Project/sample_outputs \
        --gwas_file_pattern "GCST90568441_harmonized.txt.gz" \
        --snp_column variant_id \
        --effect_allele_column effect_allele \
        --non_effect_allele_column non_effect_allele \
        --beta_column effect_size \
        --se_column standard_error \
        --pvalue_column pvalue \
        --output_file ~/Final_Project/sample_outputs/spredixcan_results.csv
```

To access your results:
```bash
cat /Final_Project/sample_outputs/spredixcan_results.csv
```

