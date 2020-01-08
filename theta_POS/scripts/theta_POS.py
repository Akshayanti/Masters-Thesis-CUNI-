#!/usr/bin/env python3

import sys


def values(filename):
	"""
	Reads the file, and calculate a difference of the calculated klcpos3 scores in either direction
	Returns the final output score as a percentage of 1 (i.e. if actual value = 0.45, reported value = 45 (since 45 % of 1 = 0.45)
	"""
	scores_dict = dict()
	done_tbs = []
	with open(filename, "r", encoding="utf-8") as infile:
		contents = infile.readlines()
		split = ""
		val1 = 0
		val2 = 0
		for lines in contents:
			if lines != "\n":
				if split == "":
					split = lines.strip()
				else:
					if val1 == 0:
						val1 = float(lines.strip())
					else:
						val2 = float(lines.strip())
			else:
				in_val = round((val1 + val2), 3)
				if in_val >= 0 and all([x not in split for x in ["UD_French-Spoken", "UD_Swedish_Sign_Language-SSLC", "UD_French-FQB", "UD_French-FTB", "UD_English-ESL"]]):
					scores_dict[split] = in_val
				split = ""
				val1 = 0
				val2 = 0
	for treebanks in scores_dict:
		tb1, tb2 = treebanks.split()
		if {tb1, tb2} not in done_tbs:
			print(treebanks, str(scores_dict[treebanks]), sep="\t")
			done_tbs.append({tb1, tb2})


if __name__ == "__main__":
	if len(sys.argv) <= 1:
		print("Enter FileName as an argument")
	else:
		values(sys.argv[1])
