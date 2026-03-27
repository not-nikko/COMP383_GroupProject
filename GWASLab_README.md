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
