
from sys import argv
from collections import defaultdict
import csv
geneID2bin = {}; #defaultdict(list);
bin2geneID = {}; #defaultdict(list);
with open("out.txt") as fp:
	for line in fp:
		print line;
		linesplit = line.split(" ");
		print linesplit[0];
		print linesplit[1];
		idSplit = linesplit[0].split(':');
		print idSplit;
		s=':';
		seq = (idSplit[2], idSplit[4], idSplit[5], idSplit[6]);
		geneId =  s.join(seq);
		print geneId;
			
