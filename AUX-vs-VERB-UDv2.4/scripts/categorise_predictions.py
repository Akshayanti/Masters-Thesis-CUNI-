#!/usr/bin/env python3

import sys
from collections import defaultdict


def check_inputs():
	"""The function that checks if all inputs are
	in right order, and all the files are present"""
	help_text = "Arg1: Original Test File (in CONLL-U format)\n" \
				"Arg2: Final Annotations File\n" \
				"Usage: python3 {x} Arg1 Arg2".format(x=sys.argv[0])
	if len(sys.argv) != 3:
		print(help_text)
		exit(0)


def align_sent_id(orig_file, annotated_file):
	"""The function that aligns sentences IDs from CONLL-U file to
	the annotated test data for easy debugging"""
	sent_dict = dict()
	mismatch_dict = defaultdict(dict)
	match_dict = defaultdict(dict)
	with open(orig_file, "r", encoding="utf-8") as orig_handle:
		sent_id = ""
		for line in orig_handle:
			if line.startswith("# sent_id"):
				sent_id = line.strip("\n").split(" = ")[1]
			if line.startswith("# text"):
				text = line.strip("\n").split(" = ")[1]
				sent_dict[sent_id] = text
	# time to get the data
	with open(annotated_file, "r", encoding="utf-8") as annotated_handle:
		sentence = ""
		a = []
		b = []
		token_id = 0
		for line in annotated_handle:
			if line == "\n":
				token_id = 0
				for key in sent_dict:
					if sent_dict[key] == sentence.rstrip():
						break
				if len(a) != 0:
					temp = dict()
					temp["text"] = sentence.rstrip()
					temp["values"] = a
					mismatch_dict[key] = temp
				if len(b) != 0:
					temp2 = dict()
					temp2["text"] = sentence.rstrip()
					temp2["values"] = b
					match_dict[key] = temp2
				a = []
				b = []
				sentence = ""
			else:
				token, true, predict, score = line.strip("\n").split()
				sentence += token + " "
				if true != predict:
					tup1 = (token, token_id, true, predict, round(float(score), 4))
					a.append(tup1)
				elif true == predict:
					tup2 = (token, token_id, true, round(float(score), 4))
					b.append(tup2)
				token_id += 1
	return mismatch_dict, match_dict


def generate_distribution(label, structure):
	with open("{x}.list".format(x=label), "a", encoding="utf-8") as outfile:
		for key in structure.keys():
			for vals in structure[key]["values"]:
				if vals[2] == label and vals[3] <= 0.70:
					outfile.write("{x}\n".format(x=vals[2]))


if __name__ == "__main__":
	check_inputs()
	mismatched_instances, match_instances = align_sent_id(sys.argv[1], sys.argv[2])
	
	# Implement TOKEN_ ID Universally if possible
	with open("mismatched.tsv", "a+", encoding="utf-8") as outfile:
		for key in mismatched_instances.keys():
			text = mismatched_instances[key]["text"]
			for vals in mismatched_instances[key]["values"]:
				val1, tid, val2, val3, val4 = vals
				outfile.write("{x}\t{v1}\t{ti}\t{v2}\t{v3}\t{v4}\t{t}\n".format(x=key, v1=val1, ti=tid, v2=val2, v3=val3, v4=val4, t=text))

	with open("matched.tsv", "a+", encoding="utf-8") as outfile:
		for key in match_instances.keys():
			text = match_instances[key]["text"]
			for vals in match_instances[key]["values"]:
				val1, tid, val2, val3 = vals
				outfile.write("{x}\t{v1}\t{ti}\t{v2}\t{v3}\t{t}\n".format(x=key, v1=val1, ti=tid, v2=val2, v3=val3, t=text))

	for x in ["S-verb", "S-aux", "O"]:
		generate_distribution(x, match_instances)
