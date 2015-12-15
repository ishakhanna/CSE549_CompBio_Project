from sys import argv
from collections import defaultdict
import csv
target = open("outFinal.txt",'a');
target.truncate();
tp =0;
tn = 0;
fp = 0;
fn = 0;

with open("out.txt") as fp1:
	for line in fp1:
		#print line;
		linesplit = line.split(" ");
		#print linesplit[0];
		#print linesplit[1];
		idSplit = linesplit[0].split(':');
		#print idSplit;
		s=':';
		seq = (idSplit[2], idSplit[4], idSplit[5], idSplit[6]);
		geneId =  s.join(seq);
		#print geneId;
#		target.write(geneId);
#		target.write(" ");
#		target.write(linesplit[1]);
#		target.write("\n");
		with open("out.txt") as compFp:
			for line2 in compFp:
				linesplit2 = line2.split(" ");
                		idSplit2 = linesplit2[0].split(':');
                		s2=':';
                		seq2 = (idSplit2[2], idSplit2[4], idSplit2[5], idSplit2[6]);
              	  		geneId2 =  s2.join(seq2);				
				if geneId==geneId2 and linesplit[1]== linesplit2[1]:
					tp= tp +1;
				if geneId!=geneId2 and linesplit[1] != linesplit2[1]:
					tn= tn+1;
				if geneId==geneId2 and linesplit[1] != linesplit2[1]:
					fn = fn +1;
				if geneId!=geneId2 and linesplit[1] == linesplit2[1]:
					fp = fp +1;
print ("tp" + tp);
print ("tn" + tn);
print ("fp" + fp);
print ("fn" + fn);
target.close();
