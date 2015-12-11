import sys

reads = []
genes = []
i = 0

# InputFilename = sys.argv[1]
InputFilename = "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/1M.fastq"
f = open("/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/ensemblToGeneName.csv")

geneCodeClusterMap = {}
lines = f.readlines()
for line in lines[1:]:
    geneCode = line.split(',')[0]
    clusterCode = line.split(',')[1]
    if not (geneCodeClusterMap.has_key(geneCode)):
        geneCodeClusterMap[geneCode] = clusterCode

with open(InputFilename) as inputFile:
    with open("readClusterMapping", "w") as out:
        read = ""
        geneCode = ""
        for line in inputFile:
            if(i % 4) == 1:
                read = line
                # reads.append(line)
            elif (i % 4) == 0:
                geneCode = line.split(':')[2]
                # testGene.append(':'.join(line.split(':')[2:]))
            if (i % 4) == 3:
                if geneCodeClusterMap.has_key(geneCode):
                    print geneCode
                    out.write(read+":"+geneCodeClusterMap[geneCode]+"\n")
                else:
                    out.write(read+":"+geneCode+"\n")
                i = 0
            else:
                i += 1

# correctGeneCounts = {}
#
# for g in genes:
#     if (correctGeneCounts.has_key(g)):
#         correctGeneCounts[g] = correctGeneCounts[g] + 1
#     else:
#         correctGeneCounts[g] = 1
#
# f = open("geneCount", "w")
# for key in correctGeneCounts.keys():
#     f.write(str(key)+":"+str(correctGeneCounts[key])+"\n")
# f.close()

