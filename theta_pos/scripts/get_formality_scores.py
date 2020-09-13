#!/usr/bin/env python3

import sys
import conllu


def read_data(infile):
	a = dict()
	with open(infile, "r", encoding="utf-8") as tgt_file:
		for sentences in conllu.parse_incr(tgt_file):
			for token in sentences:
				upos = token["upostag"]
				if upos not in a:
					a[upos] = 1
				else:
					a[upos] += 1
				feats = token["feats"]
				if feats is None:
					continue
				if "Typo" in feats:
					if "Typo" not in a:
						a["Typo"] = 1
					else:
						a["Typo"] += 1
	return a


def get_relative_freq(input_pos, in_dict):
	total = 0
	for x in in_dict.values():
		total += x
	if input_pos in in_dict:
		return round(in_dict[input_pos]/total, 5)
	else:
		return 0.0


def calculate_F_measure(in_dict):
	f_noun = get_relative_freq("NOUN", in_dict)
	f_adjective = get_relative_freq("ADJ", in_dict)
	f_adposition = get_relative_freq("ADP", in_dict)
	f_det = get_relative_freq("DET", in_dict)
	f_pronoun = get_relative_freq("PRON", in_dict)
	f_verb = get_relative_freq("VERB", in_dict)
	f_adverb = get_relative_freq("ADV", in_dict)
	f_inter = get_relative_freq("INTJ", in_dict)
	f_typo = get_relative_freq("Typo", in_dict)
	f_sym = get_relative_freq("SYM", in_dict)
	total = (f_noun + f_adjective + f_adposition + f_det) - (f_pronoun + f_verb + f_adverb + f_inter) + 100
	inform = (f_typo + f_sym + f_inter) * 100
	return total/2


if __name__ == "__main__":
	source = dict()
	target = dict()
	common_trigrams = 0
	coverage = 0
	
	usage = "Program to calculate the F-measure for given CONLLU file\n" \
	        "Arg1: File 1 in CONLL-U format\n" \
	        "Usage: python3 {x} Arg1".format(x=sys.argv[0])
	
	if len(sys.argv) != 2:
		print(usage, file=sys.stderr)
		exit(1)
		
	pos_dict = read_data(sys.argv[1])
	print(round(calculate_F_measure(pos_dict), 3))
