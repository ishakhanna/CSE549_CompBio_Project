import sys
import itertools
import numpy as np

def get_kmers(infilepath, outfilepath):
	f = open(infilepath)
	kmer_counts = {}
	# read in the data and keep a count for every kmer
	for read_name,read,line3,quality in itertools.izip_longest(*[f]*4):
		for i in range(len(read)-34): #-25): #LINE A:  If you want to compare two distributions with different read length, adjust this line to only read up to length 75, for example.
			kmer = (read[i:i+33]).upper()
			if kmer in kmer_counts:
				kmer_counts[kmer] = kmer_counts[kmer] + 1
			else:
				kmer_counts[kmer] = 1
	f.close()	
	print "number of distinct kmers:"
	print len(kmer_counts)
	v=list(kmer_counts.values())
	k=list(kmer_counts.keys())
	print "the most common kmer"
	print k[v.index(max(v))]
	print "appears this number of times:"
	print max(v)
	#for value in set(v):
	#	print(value)
	unique_counts = {}
	for v in kmer_counts.values():
		if not v in unique_counts: unique_counts[v]=1
		else: unique_counts[v]+=1
	#print "printing unique counts"
	#print unique_counts	
	uv=list(unique_counts.values())
	uk=list(unique_counts.keys())
	f = open(outfilepath, 'w')
	for k, v in zip(uk, uv):
		f.write("%d, %d\n" %(k, v))
	f.close()	

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print("requires a fastq input file, and an output file name")
		exit(-1)
	print("Assumes a fastq input file. See #LINE A comment to adjust length of read to count.")
	get_kmers(sys.argv[1], sys.argv[2])
