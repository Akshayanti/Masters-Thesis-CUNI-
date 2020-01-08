#!/usr/bin/env python3

import argparse
from collections import defaultdict

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="Input files to read data from, in CONLLU format. Multiple values possible.", required=True)
	parser.add_argument("-o", "--output", help="Display the output non-projective possible trees in a CONLLU file", required=True)
	args = parser.parse_args()
	
	outdict = defaultdict(dict)
	with open(args.input, "r", encoding="utf-8") as infile:
		for lines in infile.readlines():
			try:
				vn, node = lines.strip("\n").split("\t")
			except:
				language = lines.strip("\n").split("/")[-1].split("_")[0]
				continue
			if vn not in outdict:
				outdict[vn] = dict()
				outdict[vn]["nodes"] = [node]
				outdict[vn]["lang"] = language
			else:
				outdict[vn]["nodes"].append(node)

	with open(args.output, "w", encoding="utf-8") as outfile:
		for vn in outdict.keys():
			nodeslist = outdict[vn]["nodes"]
			language = outdict[vn]["lang"]
			outfile.write(language + "\t" + vn + "\t" + ", ".join(nodeslist) + "\n")
