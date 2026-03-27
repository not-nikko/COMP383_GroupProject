#import the gwaslab library to be used for downstream harmonization from the GWAS summary statistics
import gwaslab as gl

#provide a certain pathway to the test data
#mysumstats provides an interpretation on each column provided in the file to be used for harmonization
mysumstats = gl.Sumstats("/home/data/Project3/AoU_AFR_phenotype_836850_ACAF_sumstats_for_S-PrediXcan.txt.gz",
	snpid = "ID",		#contains the SNPID, labeled ID from the AoU file
	chrom = "#CHROM",	#contains the chromosome number, labeled #CRHOM from the AoU file
	pos = "POS",		#contains the position of the base pairs
	ea = "ALT",			#effect allele
	nea = "REF",		#non-effect allele
	eaf = "AF_Allele2", #Frequency of effect allele
	beta = "BETA",		#beta coefficient
	se = "SE",			#standard error
	p = "Pvalue",		#p-value
	sep = r"\s+"
)

#this provides basica quality control checks on the current file that has been used for testing purposes
mysumstats.basic_check()

#harmonize the data used for testing purposes and compare to the reference genome GRCh38.fa
mysumstats.harmonize(ref_seq = "/home/nalde/GRCh38.fa")

#export the harmonized summary statistics to an output file, which can be used to look at the data
#which will be used downstream in comparison
mysumstats.to_csv("gwaslab_harmonized_output.txt", sep = "\t")
