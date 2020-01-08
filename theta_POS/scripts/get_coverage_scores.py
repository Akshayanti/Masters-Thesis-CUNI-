#!/usr/bin/env python3

import argparse
import klcpos3

if __name__ == "__main__":
	source = dict()
	target = dict()
	common_trigrams = 0
	coverage = 0
	
	parser = argparse.ArgumentParser("Program to calculate the coverage statistics for UPOS trigrams, as a percentage of trigrams in target file")
	parser.add_argument("-t", "--target", type=str, required=True, help="Target candidate file, in CONLLU format")
	parser.add_argument("-s", "--source", type=str, required=True, help="Source candidate file, in CONLLU format")
	args = parser.parse_args()
	
	with open(args.target, "r", encoding="utf-8") as tgt_file:
		target_data = tgt_file.readlines()
		tgt_list = klcpos3.get_pos_list(target_data)
		target, tgt_total = klcpos3.trigram_from_list(tgt_list)
	
	values_list = dict()
	with open(args.source, "r", encoding="utf-8") as source_file:
		source.clear()
		source_data = source_file.readlines()
		src_list = klcpos3.get_pos_list(source_data)
		source, src_total = klcpos3.trigram_from_list(src_list)
	
	common_trigrams = len([x for x in target.keys() if x in source.keys()])
	coverage = common_trigrams / len(target.keys())
	print(round(coverage*100, 3))
