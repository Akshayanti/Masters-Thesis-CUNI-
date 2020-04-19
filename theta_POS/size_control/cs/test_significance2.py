#!/usr/bin/env python3

import sys
from scipy import stats


def test_and_write(infile, mean, outfile):
	# out = open(outfile, "w", encoding="utf-8")
	with open(infile, "r", encoding="utf-8") as infile:
		# out.write("group\t0.01\t0.05\t0.1\n")
		for lines in infile:
			group1, scores = lines.strip("\n").split("\t")
			mean1 = mean
			mean2 = float(scores.split(" ")[0])
			sd = float(scores.split(" ")[2])
			difference = mean2 - mean1
			denom = sd/10
			print(stats.wilcoxon(difference))
			# results = []
			# for confidence in [0.01, 0.05, 0.1]:
			# 	cv = t.ppf(1.0-confidence, 99)
			# 	if abs(t_val) <= cv:
			# 		results.append("Equal")
			# 	else:
			# 		results.append("Different")
			# out.write(group1 + "\t" + "\t".join(results) + "\n")
	# out.close()
	
	
def get_mean(infile):
	meanValue = 0
	with open(infile, "r", encoding="utf-8") as infile:
		for lines in infile:
			if lines != "\n":
				group, scores = lines.strip("\n").split("\t")
				meanValue = float(scores.split(" ")[0])
				yield meanValue


if __name__ == "__main__":
	usage = "Arg1: Input File\n" \
	        "Arg2: Output file\n" \
	        "Usage: python3 {x} Arg1 Arg2".format(x=sys.argv[0])
	if len(sys.argv) != 3:
		print(usage, file=sys.stderr)
		exit(1)
		
	for mean in get_mean(sys.argv[1]):
		print(mean, file=sys.stderr)
		test_and_write(sys.argv[1], mean, sys.argv[2])
		print()
