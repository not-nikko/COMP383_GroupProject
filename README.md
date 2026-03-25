# COMP383_GroupProject
Project 3 - Harmonize GWAS Summary Statistics for S-PrediXcan


Move data from class server into our current folder:

cp /home/data/Project3/AoU_AFR_phenotype_836850_ACAF_sumstats_for_S-PrediXcan.txt.gz .

Downloading GWAS Inspector:

R

install.packages("GWASinspector")

Getting template configuration file format for GWAS Inspector:

get_config(".")

outputs config.ini

Run demo:

#Runs a demo and outputs it in sample_outputs directory
demo_inspector("sample_outputs")

Output:
GWASinspector_demo folder in sample_outputs

Ran a test QC using demo_inspector()
Output files were saved in the specified directory (sample_outputs)
Reviewed generated outputs including:
	QC report (Excel file)
	plots (QQ plot, Manhattan plot, etc.)
    log and summary files
