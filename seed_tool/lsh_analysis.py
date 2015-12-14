import sys
from itertools import groupby as g

# InputFilename = sys.argv[1]
# InputFilename = "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/small.fastq"
clusteringOutputFile = sys.argv[1]
# clusteringOutputFile = "outFinal.txt"

i = 0

# correctGeneCounts = {}
# clusterCounts = {}
geneClusterMap = {}
clusterGeneMap = {}
finalGeneClusterMap = {}
finalClusterGeneMap = {}

# with open(InputFilename) as inputFile:
#     for line in inputFile:
#         if(i % 4) == 0:
#             arr = line.split(':')
#             geneStr = arr[2]+":"+arr[4]+":"+arr[5]+":"+arr[6]
#             if (correctGeneCounts.has_key(geneStr)):
#                 correctGeneCounts[geneStr] = correctGeneCounts[geneStr] + 1
#             else:
#                 correctGeneCounts[geneStr] = 1
#         if (i % 4) == 3:
#             i = 0
#         else:
#             i += 1

with open(clusteringOutputFile) as f:
    for line in f:
        if(line[0] == '\n' ):
            continue
        clusterId = line.split(' ')[1].split('\n')[0]
        geneId = line.split(' ')[0]
        # if (clusterCounts.has_key(clusterId)):
        #     clusterCounts[clusterId] = clusterCounts[clusterId] + 1
        # else:
        #     clusterCounts[clusterId] = 1

        if (geneClusterMap.has_key(geneId)):
            geneClusterMap[geneId].append(clusterId)
        else:
            geneClusterMap[geneId] = []
            geneClusterMap[geneId].append(clusterId)

        if (clusterGeneMap.has_key(clusterId)):
            clusterGeneMap[clusterId].append(geneId)
        else:
            clusterGeneMap[clusterId] = []
            clusterGeneMap[clusterId].append(geneId)

for k in geneClusterMap.keys():
    L = geneClusterMap[k]
    finalGeneClusterMap[k] = max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]

for k in clusterGeneMap.keys():
    L = clusterGeneMap[k]
    finalClusterGeneMap[k] = max(g(sorted(L)), key=lambda(x, v):(len(list(v)),-L.index(x)))[0]

fpTotal = 0
fnTotal = 0

with open(clusteringOutputFile) as f:
    for line in f:
        if(line[0] == '\n' ):
            continue
        clusterId = line.split(' ')[1].split('\n')[0]
        geneId = line.split(' ')[0]
        if(finalGeneClusterMap[geneId] != clusterId):
            fnTotal = fnTotal+1

        if(finalClusterGeneMap[clusterId] != geneId):
            fpTotal = fpTotal+1

print fnTotal
print fpTotal
