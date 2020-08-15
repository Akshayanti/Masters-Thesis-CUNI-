#!/usr/bin/env python3

import sys
import kfold

train = []
test = []


def read_input(input_file):
	"""
	Split incoming CoNLL-U file into test and training set
	"""
	with open(input_file, "r", encoding="utf-8") as infile:
		data = kfold.organise_as_block(infile)
		for block in data:
			if block[0].startswith("# sent_id = test-s"):
				test.append(block)
			else:
				train.append(block)


def write_output(out_file, out_list):
	"""
	out_list: list of lists. Innermost list contains lines from the conllu file
	out_file: target file name where the contents of out_list need to be written
	Writes the contents of out_list to out_file, one line at a time.
	"""
	with open(out_file, "w", encoding="utf-8") as outfile:
		for block in out_list:
			for lines in block:
				outfile.write(lines)


if __name__ == "__main__":
	# Arg1: CoNLL-U file that needs to be split
	if len(sys.argv) != 2:
		print("Usage:\n"
			  "python3 {x} <Input CoNLL-U File>"
			  .format(x=sys.argv[0])
			  )
		exit(1)
	read_input(sys.argv[1])
	write_output("baseline_test.conllu", test)
	write_output("baseline_train.conllu", train)
