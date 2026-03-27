import gwaslab as gl

mysumstats = gl.Sumstats("/home/data/Project3/AoU_AFR_phenotype_836850_ACAF_sumstats_for_S-PrediXcan.txt.gz",
	snpid = "ID",
	chrom = "#CHROM",
	pos = "POS",
	ea = "ALT",
	nea = "REF",
	eaf = "AF_Allele2",
	beta = "BETA",
	se = "SE",
	p = "Pvalue",
	sep = r"\s+"
)

mysumstats.basic_check()
mysumstats.harmonize(ref_seq = "/home/nalde/GRCh38.fa")

mysumstats.to_csv("gwaslab_harmonized_output.txt", sep = "\t")
