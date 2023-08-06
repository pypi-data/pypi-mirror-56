import sys
from discere.preprocessing import process_fasta
from discere.features import feature_extraction
system = sys.platform

# def feat_ext():
# 	print("Extracting features....")
# 	if system == 'linux':
# 		subprocess.run(['python3','feature_extraction.py'])
# 	else:
# 		subprocess.run(['python.exe','process_fasta.py'])

def extract_feature(positive, negative, outdir):
	code = process_fasta.process_fasta(positive, negative, outdir)
	if code is True:
		feature_extraction.feature_extraction(outdir)
	else:print('Error processing the fasta files !')

if __name__ == '__main__':
	extract_feature(positive, negative)
	import os
	print("Have a great day ",os.getlogin(), "!")
