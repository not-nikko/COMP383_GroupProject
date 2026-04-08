#First, individuals should use wget to access the reference genome required for individual usage. For the purposes of this test, we are using the GRCh38 human genome.

wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.fna.gz

#Once file has been uploaded to the terminal, users will unzip the folder using gunzip
gunzip GCF_000001405.40_GRCh38.p14_genomic.fna.gz

#A virtual environment was then used within the terminal to run gwaslab within the class server and was then named .venv
python3 -m venv .venv
#this will then show users that they are in the virtual terminal with (.venv) and the user's name

#The virtual environment was then opened to be used for future usage with gwaslab
pip install gwaslab

#From here, the code under the gwaslab folder may be used with information

#wget was used to access a separate summary statistic
wget http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90568001-GCST90569000/GCST90568441/GCST90568441.tsv.gz

#a filed called GCST90568441.tsv.gz will be created, which
#the user will have to unzip

#wget was used to access a separate summary statistic
wget http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/GCST90568001-GCST90569000/GCST90568441/GCST90568441.tsv.gz

#a filed called GCST90568441.tsv.gz will be created, which
#the user will have to unzip

gunzip GCST90568441.tsv.gz

#users will then use the updated code labeled GWASLAB_code.py

python GWASLAB_code.py


#the output will create a file called harmonized_sumstats.tsv and a new 
#code was then provided to run S-PrediXcan with the output title being gwaslab_spredixcan_results.csv

#to get the final output for the percentage of SNPs, the following line was used:
awk -F, 'NR>1 {used+=$10; total+=$12} END {print (used/total)*100}' ~/gwaslab_spredixcan_results.csv
