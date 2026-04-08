"""
Usage:
    #Auto-detect column names
    python3 run_gwas_harmonization.py \
        -i my_gwas_file.tsv.gz \
        -o my_harmonized_output.txt.gz
 
    # Manually override specific columns if auto-detection fails
    python3 run_gwas_harmonization.py \
        -i my_gwas_file.tsv.gz \
        -o my_harmonized_output.txt.gz \
        --snp_col SNP \
        --pvalue_col P
"""
 
import sys #for reading command line arguments and exiting
import argparse #for parsing command line arguments
import subprocess #for running gwas_parsing.py as a subprocess
import os #for file path handling
import gzip #for reading gzipped input files
 
#path to gwas_parsing.py from the summary-gwas-imputation repo
GWAS_PARSING_SCRIPT = os.path.expanduser(
    "~/Final_Project/summary-gwas-imputation/src/gwas_parsing.py"
)
 
#column alias dictionary
#maps each standard column name to a list of all known alternative names
#used to auto-detect column names from any GWAS file header
COLUMN_ALIASES = {
    "snp_col": [ #all known names for the SNP/variant ID column
        "rsid", "SNP", "snp", "variant_id", "ID", "SNPID", "MarkerName",
        "rs_id", "variant", "RSID", "snpID", "SNP_ID", "snp_id"
    ],
    "effect_allele_col": [ #all known names for the effect allele column
        "effect_allele", "A1", "ALT", "alt", "EA", "Allele1", "ALLELE1",
        "EffectAllele", "effect_allele_1", "Risk_Allele"
    ],
    "other_allele_col": [ #all known names for the non-effect allele column
        "other_allele", "A2", "REF", "ref", "NEA", "Allele2", "ALLELE2",
        "OtherAllele", "non_effect_allele", "other_allele_2"
    ],
    "beta_col": [ #all known names for the beta/effect size column
        "beta", "BETA", "Effect", "effect", "effect_size", "Beta",
        "b", "EFFECT", "effect_weight"
    ],
    "se_col": [ #all known names for the standard error column
        "standard_error", "SE", "se", "StdErr", "stderr",
        "Standard_Error", "STDERR", "se_dgc"
    ],
    "pvalue_col": [ #all known names for the p-value column
        "p_value", "P", "pval", "PVALUE", "pvalue", "Pvalue",
        "p.value", "P_value", "P-value", "LOG10P"
    ],
    "freq_col": [ #all known names for the allele frequency column
        "effect_allele_frequency", "AF_Allele2", "EAF", "Freq1", "FRQ",
        "MAF", "freq", "A1FREQ", "effect_allele_freq", "AF", "FREQ"
    ],
    "chr_col": [ #all known names for the chromosome column
        "chromosome", "CHR", "chr", "#CHROM", "CHROM",
        "Chromosome", "chrom", "Chr"
    ],
    "pos_col": [ #all known names for the base pair position column
        "base_pair_location", "POS", "BP", "position", "Position",
        "pos", "BASE_PAIR", "base_pair"
    ],
}
 
#auto-detection function
#reads the first line of the input file and matches column names to standard names
def detect_columns(filepath, separator="\t"):
    if filepath.endswith(".gz"): #open as gzip if file is compressed
        with gzip.open(filepath, "rt") as f:
            header = f.readline().strip().split(separator) #read and split header line
    else: #open as plain text if file is not compressed
        with open(filepath, "r") as f:
            header = f.readline().strip().split(separator) #read and split header line
 
    detected = {} #dictionary to store detected column mappings
    for standard_name, aliases in COLUMN_ALIASES.items(): #loop through each standard column
        for alias in aliases: #check each known alias
            if alias in header: #if alias matches a column in the file
                detected[standard_name] = alias #store the match
                break #stop checking once first match is found
 
    return detected, header #return detected mappings and full header list
 
#parse command line arguments
parser = argparse.ArgumentParser(
    description="Harmonize GWAS summary statistics for S-PrediXcan using gwas_parsing.py"
)
 
parser.add_argument("-i", "--input", #required input file path
    help="Input GWAS summary stats file (.tsv.gz or .txt.gz)",
    required=True)
parser.add_argument("-o", "--output", #required output file path
    help="Output harmonized file (.txt.gz)",
    required=True)
 
#optional column overrides — auto-detected from file header if not provided
parser.add_argument("--snp_col",           default=None, help="SNP/variant ID column name (auto-detected if not set)")
parser.add_argument("--effect_allele_col", default=None, help="Effect allele column name (auto-detected if not set)")
parser.add_argument("--other_allele_col",  default=None, help="Non-effect allele column name (auto-detected if not set)")
parser.add_argument("--beta_col",          default=None, help="Beta/effect size column name (auto-detected if not set)")
parser.add_argument("--se_col",            default=None, help="Standard error column name (auto-detected if not set)")
parser.add_argument("--pvalue_col",        default=None, help="P-value column name (auto-detected if not set)")
parser.add_argument("--freq_col",          default=None, help="Allele frequency column name (auto-detected if not set)")
parser.add_argument("--chr_col",           default=None, help="Chromosome column name (auto-detected if not set)")
parser.add_argument("--pos_col",           default=None, help="Base pair position column name (auto-detected if not set)")
parser.add_argument("--separator",         default="\t", help="Column separator (default: tab)")
 
arguments = parser.parse_args(sys.argv[1:]) #parse arguments from command line
infile  = arguments.input #store input file path
outfile = arguments.output #store output file path
 
#validate that input file exists
infile = os.path.expanduser(infile) #expand ~ to full home directory path
if not os.path.isfile(infile): #check if file exists
    print(f"ERROR: Input file not found: {infile}")
    sys.exit(1) #exit if file not found
 
#validate that gwas_parsing.py exists
script_path = os.path.expanduser(GWAS_PARSING_SCRIPT) #expand ~ in script path
if not os.path.isfile(script_path): #check if script exists
    print(f"ERROR: gwas_parsing.py not found at: {script_path}")
    print("Update the GWAS_PARSING_SCRIPT variable at the top of this script.")
    sys.exit(1) #exit if script not found
 
#create output directory if it doesnt exist
outfile = os.path.expanduser(outfile) #expand ~ in output path
os.makedirs(os.path.dirname(outfile), exist_ok=True) #make output folder if missing
 
#print header and run auto-detection
print("=" * 60)
print("GWAS Harmonization — summary-gwas-imputation")
print("=" * 60)
print(f"Input file:  {infile}") #show input path
print(f"Output file: {outfile}") #show output path
print()
print("Detecting column names from file header...")
 
detected, header = detect_columns(infile, arguments.separator) #run auto-detection
print(f"Columns found in file: {header}") #print all column names found in file
print()
 
#merge auto-detected columns with any manual overrides
#manual overrides take priority over auto-detected values
final_cols = {
    "snp_col":           arguments.snp_col           or detected.get("snp_col"),           #use manual override or auto-detected
    "effect_allele_col": arguments.effect_allele_col or detected.get("effect_allele_col"), #use manual override or auto-detected
    "other_allele_col":  arguments.other_allele_col  or detected.get("other_allele_col"),  #use manual override or auto-detected
    "beta_col":          arguments.beta_col           or detected.get("beta_col"),          #use manual override or auto-detected
    "se_col":            arguments.se_col             or detected.get("se_col"),            #use manual override or auto-detected
    "pvalue_col":        arguments.pvalue_col         or detected.get("pvalue_col"),        #use manual override or auto-detected
    "freq_col":          arguments.freq_col           or detected.get("freq_col"),          #use manual override or auto-detected
    "chr_col":           arguments.chr_col            or detected.get("chr_col"),           #use manual override or auto-detected
    "pos_col":           arguments.pos_col            or detected.get("pos_col"),           #use manual override or auto-detected
}
 
#check that all required columns were found
required = ["snp_col", "effect_allele_col", "other_allele_col",
            "beta_col", "se_col", "pvalue_col"] #list of columns that must be present
missing = [col for col in required if not final_cols[col]] #find any that are missing
 
if missing: #if any required columns are missing, print error and exit
    print("WARNING: Could not auto-detect the following required columns:")
    for col in missing:
        print(f"  {col}") #print each missing column name
    print()
    print("Please re-run with manual overrides, e.g.:")
    print("  --snp_col SNP --pvalue_col P")
    sys.exit(1) #exit since we cant proceed without required columns
 
#print the final column mappings so user can verify
print("Column mappings (your file → standard name):")
print(f"  {final_cols['snp_col']:<30} → variant_id")           #show snp column mapping
print(f"  {final_cols['effect_allele_col']:<30} → effect_allele")     #show effect allele mapping
print(f"  {final_cols['other_allele_col']:<30} → non_effect_allele")  #show other allele mapping
print(f"  {final_cols['beta_col']:<30} → effect_size")          #show beta mapping
print(f"  {final_cols['se_col']:<30} → standard_error")        #show se mapping
print(f"  {final_cols['pvalue_col']:<30} → pvalue")             #show pvalue mapping
if final_cols["freq_col"]: #only print if frequency column was found
    print(f"  {final_cols['freq_col']:<30} → frequency")
else:
    print(f"  {'(not found - skipping)':<30} → frequency") #notify user if freq col missing
if final_cols["chr_col"]: #only print if chromosome column was found
    print(f"  {final_cols['chr_col']:<30} → chromosome")
if final_cols["pos_col"]: #only print if position column was found
    print(f"  {final_cols['pos_col']:<30} → position")
print("=" * 60)
 
#build the gwas_parsing.py command with all required arguments
cmd = [
    "python3", script_path,          #run gwas_parsing.py with python3
    "-gwas_file",  infile,           #input gwas file
    "-output",     outfile,          #output file path
    "-separator",  arguments.separator, #column separator (default tab)
    "--chromosome_format",           #convert chromosome to chr1 format
    "--insert_value", "sample_size", "NA", #insert NA for missing sample size column
    "-output_column_map", final_cols["snp_col"],           "variant_id",       #map snp column
    "-output_column_map", final_cols["effect_allele_col"], "effect_allele",     #map effect allele column
    "-output_column_map", final_cols["other_allele_col"],  "non_effect_allele", #map other allele column
    "-output_column_map", final_cols["beta_col"],          "effect_size",       #map beta column
    "-output_column_map", final_cols["se_col"],            "standard_error",    #map se column
    "-output_column_map", final_cols["pvalue_col"],        "pvalue",            #map pvalue column
]
 
#add optional columns to command only if they were detected
if final_cols["freq_col"]: #add frequency mapping if column exists
    cmd += ["-output_column_map", final_cols["freq_col"], "frequency"]
if final_cols["chr_col"]: #add chromosome mapping if column exists
    cmd += ["-output_column_map", final_cols["chr_col"], "chromosome"]
if final_cols["pos_col"]: #add position mapping if column exists
    cmd += ["-output_column_map", final_cols["pos_col"], "position"]
 
#run gwas_parsing.py
print("Running gwas_parsing.py...")
result = subprocess.run(cmd) #execute the command and wait for it to finish
 
if result.returncode == 0: #if command succeeded
    print()
    print("=" * 60)
    print("Harmonization complete!")
    print(f"Output saved to: {outfile}") #show where output was saved
    print()
else: #if command failed
    print()
    print("ERROR: gwas_parsing.py failed. Check the output above for details.")
    sys.exit(1) #exit with error code
 