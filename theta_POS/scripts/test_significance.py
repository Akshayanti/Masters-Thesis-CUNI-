#!/usr/bin/env python3

import sys
from scipy.stats import t


def test_and_write(infile, mean, outfile):
	out = open(outfile, "w", encoding="utf-8")
	with open(infile, "r", encoding="utf-8") as infile:
		out.write("group\t0.01\t0.05\t0.1\n")
		for lines in infile:
			group1, scores = lines.strip("\n").split("\t")
			mean1 = mean
			mean2 = float(scores.split(" ")[0])
			sd = float(scores.split(" ")[2])
			denom = sd/10
			num = mean2 - mean1
			if abs(num) < 0.001 or sd < 0.001:
				results = ["Equal", "Equal", "Equal"]
				out.write(group1 + "\t" + "\t".join(results) + "\n")
				continue
			t_val = num/denom
			results = []
			for confidence in [0.01, 0.05, 0.1]:
				cv = t.ppf(1.0-confidence, 99)
				if abs(t_val) <= cv:
					results.append("Equal")
				else:
					results.append("Different")
			out.write(group1 + "\t" + "\t".join(results) + "\n")
	out.close()
	
	
def get_mean(infile):
	with open(infile, "r", encoding="utf-8") as infile:
		for lines in infile:
			group, scores = lines.strip("\n").split("\t")
			if "train_100" in group:
				meanValue = float(scores.split(" ")[0])
				return meanValue


if __name__ == "__main__":
	usage = "Arg1: Input File\n" \
	        "Arg2: Output file\n" \
	        "Usage: python3 {x} Arg1 Arg2".format(x=sys.argv[0])
	if len(sys.argv) != 3:
		print(usage, file=sys.stderr)
		exit(1)
		
	mean = get_mean(sys.argv[1])
	test_and_write(sys.argv[1], mean, sys.argv[2])
