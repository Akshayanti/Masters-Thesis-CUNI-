#!/usr/bin/env python3

import sys
from scipy.stats import t


def test_and_write(infile, mean):
	results = 0
	with open(infile, "r", encoding="utf-8") as infile:
		for lines in infile:
			group1, scores = lines.strip("\n").split("\t")
			mean1 = mean
			mean2 = float(scores.split(" ")[0])
			sd = float(scores.split(" ")[2])
			denom = sd/10
			num = mean2 - mean1
			if abs(num) < 0.001:
				results += 1
				continue
			t_val = num/denom
			cv = t.ppf(0.95, 99)
			if abs(t_val) <= cv:
				results += 1
	return results
	
	
def get_mean(infile):
	meanValue = 0
	with open(infile, "r", encoding="utf-8") as infile:
		for lines in infile:
			if lines != "\n":
				group, scores = lines.strip("\n").split("\t")
				meanValue = float(scores.split(" ")[0])
				yield meanValue, scores


if __name__ == "__main__":
	usage = "Arg1: Input File\n" \
	        "Arg2: Output file\n" \
	        "Usage: python3 {x} Arg1 Arg2".format(x=sys.argv[0])
	if len(sys.argv) != 3:
		print(usage, file=sys.stderr)
		exit(1)
	
	with open(sys.argv[2], "w", encoding="utf-8") as outfile:
		outfile.write("Mean " + u"\u00B1" + " SD\tequalWith\n")
		for mean, scores in get_mean(sys.argv[1]):
			result = test_and_write(sys.argv[1], mean)
			outfile.write(str(scores) + "\t" + str(result) + "\n")

