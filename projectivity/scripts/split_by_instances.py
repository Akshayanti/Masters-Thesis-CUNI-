#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print("Python File to split the results of \'nonproj_possibilities.py\' result files in 3 groups, based on total found instances across different files\n"
	      "Group1 (discarded): Total Counts < 50\n"
	      "Group2 (Perfect): Either of non-projective or projective structures is 0. Ideal case.\n"
	      "Group3 (Keep): Total count >= 50; Majority by at least 90\% \n"
	      "Usage:\n"
	      "python3 " + sys.argv[0] + " <File Containing Results of \'nonproj_possibilities.py\' file>")
	exit(1)

with open(sys.argv[1], "r", encoding="utf-8") as infile:
	discarded = []
	kept = []
	perfect = []
	for line in infile.readlines():
		lang_code, vn, count_nonproj, count_proj, occurrences1, occurrences2 = line.strip("\n").split("\t")
		count = int(count_proj) + int(count_nonproj)
		count_proj = int(count_proj)
		count_nonproj = int(count_nonproj)
		if count < 50:
			discarded.append(line)
		else:
			if count_nonproj == 0 or count_proj == 0:
				perfect.append(line)
			elif count_proj >= 9 * count_nonproj or count_nonproj >= count_proj * 9:
				kept.append(line)
			else:
				discarded.append(line)

outfile_base = sys.argv[1].split(".tsv")[0]

with open(outfile_base+"_discard.tsv", "w", encoding="utf-8") as outfile:
	for line in discarded:
		outfile.write(line)

with open(outfile_base+"_keep.tsv", "w", encoding="utf-8") as outfile:
	for line in kept:
		outfile.write(line)

with open(outfile_base+"_perfect.tsv", "w", encoding="utf-8") as outfile:
	for line in perfect:
		outfile.write(line)
