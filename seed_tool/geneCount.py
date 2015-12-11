import sys

reads = []
genes = []
i = 0

InputFilename = sys.argv[1]

with open(InputFilename) as inputFile:
        for line in inputFile:
            if(i % 4) == 1:
                reads.append(line)
            elif (i % 4) == 0:
                genes.append(line.split(':')[2])
                # testGene.append(':'.join(line.split(':')[2:]))

            if (i % 4) == 3:
                i = 0
            else:
                i += 1

correctGeneCounts = {}

for g in genes:
    if (correctGeneCounts.has_key(g)):
        correctGeneCounts[g] = correctGeneCounts[g] + 1
    else:
        correctGeneCounts[g] = 1

f = open("geneCount", "w")
for key in correctGeneCounts.keys():
    f.write(str(key)+":"+str(correctGeneCounts[key])+"\n")
f.close()

