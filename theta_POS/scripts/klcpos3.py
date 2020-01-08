#!/usr/bin/env python3

import argparse
import math
import operator

div_by = 0


def klcpos3(tgt_dict, src_dict, tgt_total, src_total):
	"""
	Calculate the final Klc_pos^3 scores from calculated metrics
	"""
	final_result = 0
	for trigram in tgt_dict:
		src_val = src_dict[trigram] / src_total
		tgt_val = tgt_dict[trigram] / tgt_total
		result = tgt_val * (math.log(tgt_val/src_val))
		final_result += result
	return final_result


def get_pos_list(file_contents):
	"""
	Given the contents of the input file, include all the PoS tags in form of a list
	"""
	out_list = ["_"]
	for lines in file_contents:
		if lines != "\n":
			if lines[0] != "#":
				Id, form, lemma, upos, xpos, feats, head, deprel, deps, misc = lines.split("\t")
				if upos != "_":
					"""multi word tokens"""
					out_list.append(upos)
		else:
			out_list.append("_")
	return out_list


def get_ngrams(input_list, n=2, i=0):
	"""Gets n-grams from a given list"""
	while len(input_list[i:i+n]) == n:
		yield input_list[i:i+n]
		i += 1


def trigram_from_list(pos_list):
	"""
	Generate the trigrams from the generated list
	Since _ is the sentence boundary, do not include anything that has form -> +_+
	"""
	a = dict()
	total = 0
	trigrams = get_ngrams(pos_list, n=3)
	for trigram in trigrams:
		trigram_string = trigram[0] + "+" + trigram[1] + "+" + trigram[2]
		if "+_+" not in trigram_string:
			total += 1
			if trigram_string in a:
				a[trigram_string] += 1
			else:
				a[trigram_string] = 1
	return a, total


def mod_source_list(orig_source, orig_tgt, orig_source_count):
	"""
	account for the unseen counts of trigrams seen in target, not in source
	"""
	new_source = dict()
	new_source_count = orig_source_count + 1 - 1
	for i in orig_tgt:
		if i not in orig_source:
			new_source[i] = 1
			new_source_count += 1
		else:
			new_source[i] = orig_source[i]
	return new_source, new_source_count


if __name__ == "__main__":
	source = dict()
	target = dict()
	tgt_total = 0
	
	parser = argparse.ArgumentParser("Program to calculate klcpos3 measure for single, and multi-sourced delexicalised parsing algorithms")
	parser.add_argument("-t", "--target", type=str, required=True, help="Target candidate file, in CONLLU format")
	parser.add_argument("-s", "--source", nargs="+", type=str, required=True, help="Source candidate file(s), in CONLLU format")
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument("--single_source", action='store_true', help="Used for selection of single source, the values would be displayed in decreasing order of similarity measure")
	group.add_argument("--multi_source", action='store_true', help="Used for computing klcpos3 ^ -4 as a similarity measure for weighted multiple source parsing")
	args = parser.parse_args()
	
	with open(args.target, "r", encoding="utf-8") as tgt_file:
		target_data = tgt_file.readlines()
		tgt_list = get_pos_list(target_data)
		target, tgt_total = trigram_from_list(tgt_list)
	
	values_list = dict()
	for i in args.source:
		with open(i, "r", encoding="utf-8") as source_file:
			source.clear()
			src_total = 0
			source_data = source_file.readlines()
			src_list = get_pos_list(source_data)
			source, src_total = trigram_from_list(src_list)
			""" So far, we have generated the trigrams
			We need to account for instances not seen in the source, but present in target """
			new_source, src_total2 = mod_source_list(source, target, src_total)
			values_list[i] = klcpos3(target, new_source, tgt_total, src_total2)
	
	if args.single_source:
		values_list_2 = sorted(values_list.items(), key=operator.itemgetter(1), reverse=True)
		for i, j in values_list_2:
			print(i + "\t" + str(j))
	else:
		for i in values_list:
			values_list[i] = math.pow(values_list[i], -4)
		
		values_list_2 = sorted(values_list.items(), key=operator.itemgetter(1), reverse=True)
		for i, j in values_list_2:
			print(i + "\t" + str(j))
		print("\n\nNote that the above weights are not normalised.")
