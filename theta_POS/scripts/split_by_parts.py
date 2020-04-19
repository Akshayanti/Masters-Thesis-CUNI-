#!/usr/bin/python3

import sys
import math
import random
from collections import defaultdict

a = defaultdict(dict)


def get_blocks(input_file_read):
	id = ""
	text = ""
	block = []
	for lines in input_file_read:
		if lines != "\n":
			if lines.startswith("# sent_id") or lines.startswith("#sent_id"):
				id = lines.split("=")[1].strip()
			elif lines.startswith("# text") or lines.startswith("#text"):
				text = "=".join(lines.split("=")[1:]).strip()
			elif not lines.startswith("#"):
				block.append(lines.strip())
		else:
			yield id, text, block
			id = ""
			text = ""
			block.clear()


def write_data(id, outfilename):
	"""Write the outputs in the outfilename"""
	outfile = outfilename
	with open(outfile, "a", encoding="utf-8") as zfile:
		zfile.write("# sent_id = " + id + "\n")
		text = a[id]["text"]
		zfile.write("# text = " + text + "\n")
		blocks = a[id]["block"]
		for lines in blocks:
			zfile.write(lines.strip("\n") + "\n")
		zfile.write("\n")


if __name__ == "__main__":
	help_txt = "Arg1: Percentage of data to split to\n" \
	           "Arg2: Input file in CONLL-U format\n" \
	           "Arg3: Optional Argument. Seed Value (int)\n" \
	           "Usage: python3 {x} Arg1 Arg2 Arg3".format(x=sys.argv[0])
	
	if len(sys.argv) != 3 and len(sys.argv) != 4:
		print(help_txt)
		exit(0)
	
	try:
		percentage = int(sys.argv[1])
		assert 0 <= percentage <= 100, "Percentage not within valid range"
	except:
		raise ValueError('First argument should be a percentage <= 100')
	
	try:
		seedvalue = int(sys.argv[3])
	except IndexError:
		seedvalue = 1618
	except ValueError:
		print("Invalid Seed Value. Will use default seed of 1618")
		seedvalue = 1618
	
	with open(sys.argv[2], "r", encoding="utf-8") as infile:
		contents = infile.readlines()
		for id, text, block in get_blocks(contents):
			a[id]["text"] = text
			a[id]["block"] = [x for x in block]
		counts = math.ceil(len(a)*percentage/100)
		done_ids = []
		while counts > 0:
			id, data = random.choice(list(a.items()))
			if id not in done_ids:
				write_data(id, sys.argv[2] + "_" + str(percentage))
				done_ids.append(id)
				counts -= 1
		if percentage == 50:
			exit(0)
		for id, data in list(a.items()):
			if id not in done_ids:
				write_data(id, sys.argv[2] + "_" + str(100-percentage))
