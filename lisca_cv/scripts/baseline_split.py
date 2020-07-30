#!/usr/bin/env python3

import sys
import kfold

train = []
test = []


def read_input(input_file):
	with open(input_file, "r", encoding="utf-8") as infile:
		data = kfold.organise_as_block(infile)
		for block in data:
			if block[0].startswith("# sent_id = test-s"):
				test.append(block)
			else:
				train.append(block)
			

def write_output(out_file, out_list):
	with open(out_file, "w", encoding="utf-8") as outfile:
		for block in out_list:
			for lines in block:
				outfile.write(lines)


if __name__ == "__main__":
	read_input(sys.argv[1])
	write_output("baseline_test.conllu", test)
	write_output("baseline_train.conllu", train)
