from Bio import SeqIO
import os
import shutil

def process_fasta(positive, negative, outdir=os.getcwd()):
	print("Processing fasta files....")
	path_ = outdir
	print('Cleaning existing data...')
	if os.path.isdir(path_+"/data") is True:
		shutil.rmtree(path_+"/data")
	os.mkdir(path_+"/data")

	_=(os.path.join(path_,"data/data.txt"))
	if os.path.isfile(_):
		try:os.remove("data.txt")		# Remove the data.txt file from previous run
		except Exception:pass
	print('Generating intermediate files...')
	o_put = open(_,"a+")		# create and open a new data.txt file
	o_put.write("sequence"+"\t"+"class"+"\n")
	for record in SeqIO.parse(positive, "fasta"):		# Code to parse multiple sequences using Bio Python
		o_put.write(str(record.seq)+"\t"+"1"+"\n")								# Positive sequence output

	for record in SeqIO.parse(negative, "fasta"):		# Code to parse multiple sequences using Bio Python
		o_put.write(str(record.seq)+"\t"+"0"+"\n")								# Negative sequence output
	o_put.close()
	return True

#process_fasta('positive_training.fasta', 'negative_training.fasta')
