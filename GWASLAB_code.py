#import the gwaslab library to be used for downstream harmonization from the GWAS summary statistics
import gwaslab as gl

#provide a certain pathway to the test data
#mysumstats provides an interpretation on each column provided in the file to be used for harmonizat>
mysumstats = gl.Sumstats("/home/nalde/GCST90568441.tsv.gz",
        snpid = "rsid",           #contains the SNPID, labeled ID from the AoU file
        chrom = "chromosome",       #contains the chromosome number, labeled #CRHOM from the AoU file
        pos = "base_pair_location",            #contains the position of the base pairs
        ea = "effect_allele",                     #effect allele
        nea = "other_allele",            #non-effect allele
        # eaf = "", #Frequency of effect allele
        beta = "beta",          #beta coefficient
        se = "standard_error",                      #standard error
        p = "p_value",           #p-value
        sep = r"\s+"
)

#this provides basica quality control checks on the current file that has been used for testing purp>
mysumstats.basic_check()

mysumstats.harmonize(ref_seq = "/home/nalde/GRCh38.fa")

mysumstats.to_csv("harmonized_sumstats.tsv", sep="\t", index = False)

#harmonize the data used for testing purposes and compare to the reference genome GRCh38.fa