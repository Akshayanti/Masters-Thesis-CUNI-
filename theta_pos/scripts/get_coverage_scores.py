#!/usr/bin/env python3

import sys
import klcpos3

if __name__ == "__main__":
	source = dict()
	target = dict()
	common_trigrams = 0
	coverage = 0
	
	usage = "Program to calculate the coverage statistics for UPOS trigrams, as a percentage of trigrams in target file\n" \
	        "Arg1: File 1 in CONLL-U format\n" \
	        "Arg2: File 2 in CONLL-U format\n\n" \
	        "Usage: python3 {x} Arg1 Arg2".format(x=sys.argv[0])
	
	if len(sys.argv) != 3:
		print(usage, file=sys.stderr)
		exit(1)
	
	with open(sys.argv[1], "r", encoding="utf-8") as tgt_file:
		target_data = tgt_file.readlines()
		tgt_list = klcpos3.get_pos_list(target_data)
		target, tgt_total = klcpos3.trigram_from_list(tgt_list)
	
	values_list = dict()
	with open(sys.argv[2], "r", encoding="utf-8") as source_file:
		source.clear()
		source_data = source_file.readlines()
		src_list = klcpos3.get_pos_list(source_data)
		source, src_total = klcpos3.trigram_from_list(src_list)
	
	if len(target) < len(source):
		target, source = source, target
	
	common_trigrams = len([x for x in target.keys() if x in source.keys()])
	coverage = common_trigrams / len(target.keys())
	print(round(coverage*100, 3))
