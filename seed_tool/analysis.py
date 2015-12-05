InputFilename = "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/1M.fastq"
OutputFilename = "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_mismatch2.txt"
Filenames = ["/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_shift0.txt",
             "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_shift1.txt",
             "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_shift2.txt",
             "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_shift3.txt",
             "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_shift4.txt",
             "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_shift5.txt",
             "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/seed_tool/SEED/1M_output_shift6.txt"]

reads = []
genes = []
i = 0
with open(InputFilename) as inputFile:
        for line in inputFile:
            if(i % 4) == 1:
                reads.append(line)
            elif (i % 4) == 0:
                genes.append(line.split(':')[2])

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

for filename in Filenames:
    count = 0
    clusterId = -1
    clusters = []
    fp = 0
    seqNum = []
    geneID = []
    with open(filename) as inputFile:
            for line in inputFile:
                if(count == 0):
                    count += 1
                    continue
                # count += 1
                # if(count > 5):
                #     break

                if not(line[0].isdigit()):
                    # print "This is the start line", line
                    clusterId += 1
                    if len(seqNum) != 0:
                        clusters.append(seqNum)
                    seqNum = []
                else:
                    seqNum.append(line.split('\t')[1].split('\n')[0])


    clusters.append(seqNum)

    clusterGenes = []
    geneCount = []
    experimentCenterNum = {}
    for seqNums in clusters:
        clusterCenter = genes[int(seqNums[0])]
        if not(experimentCenterNum.has_key(clusterCenter)):
            experimentCenterNum[clusterCenter] = 0
        clusterGenes.append(genes[int(seqNums[0])])
        geneCount.append(0)
        for sn in seqNums:
            # if any(genes[sn] in s for s in clusterGenes):
            if genes[int(sn)] in clusterCenter:
                geneCount[clusterGenes.index(genes[int(sn)])] = geneCount[clusterGenes.index(genes[int(sn)])] + 1
                experimentCenterNum[clusterCenter] = experimentCenterNum[clusterCenter] + 1
            else:
                fp += 1


    print "------------\t", filename , "\t----------"
    fn = 0
    for geneCode in correctGeneCounts.keys():
        if not(experimentCenterNum.has_key(geneCode)):
            experimentCenterNum[geneCode] = 0
        fn = fn + (correctGeneCounts[geneCode] - experimentCenterNum[geneCode])

    # In percentage
    print "false positives: ", fp, float(fp/10000.0)
    print "false negatives: ", fn , float(fn/10000.0)

# print len(clusters), clusters[900], clusters[899]#, seqNum
# clusterGenes = []
# geneCount = []
# for seqNums in clusters:
#     clusterGenes.append(genes[int(seqNums[0])])
#     geneCount.append(0)
#     for sn in seqNums:
#         # if any(genes[sn] in s for s in clusterGenes):
#         if genes[int(sn)] in clusterGenes:
#             geneCount[clusterGenes.index(genes[int(sn)])] = geneCount[clusterGenes.index(genes[int(sn)])] + 1
#         else:
#             fp += 1
#             # clusterGenes.append(genes[int(sn)])
#             # geneCount.append(1)


