InputFilename = "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/10M.1.fastq"
OutputFilename = "/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/1M.fastq"

# i = 0
# lines = []
# with open("/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/small.fastq") as inputFile:
#     with open("/Users/ishakhanna/Documents/SBU/Comp Bio/proj/CSE549data/small_fixed_test.fastq", "w") as out:
#         for line in inputFile:
#             if(i % 4) == 1:
#                 lines.append(line.upper())
#             else:
#                 lines.append(line)
#
#             if (i % 4) == 3:
#                 if not(len(line.strip()) < 71 or len(line.strip()) > 81):
#                     out.write(lines[0])
#                     out.write(lines[1])
#                     out.write(lines[2])
#                     out.write(lines[3])
#                 i = 0
#                 lines = []
#             else:
#                 i += 1


i = 0
lines = []
counter = 0
with open(InputFilename) as inputFile:
    with open(OutputFilename, "w") as out:
        for line in inputFile:
            if counter >= 1000000:
                print "1000000 reads done!"
                exit(0)
            if(i % 4) == 1:
                lines.append(line.upper())
            else:
                lines.append(line)

            if (i % 4) == 3:
                if not(len(line.strip()) < 71 or len(line.strip()) > 81):
                    out.write(lines[0])
                    out.write(lines[1])
                    out.write(lines[2])
                    out.write(lines[3])
                    counter += 1
                i = 0
                lines = []
            else:
                i += 1

print "Done!", counter