#!/usr/bin/env python3

import find_non_projectivities
import argparse
import os
from collections import defaultdict
import tqdm
from itertools import combinations
import sys


ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC = range(10)
COLNAMES = 'ID,FORM,LEMMA,UPOS,XPOS,FEATS,HEAD,DEPREL,DEPS,MISC'.split(',')


def head_present(gpattern, blockset):
	"""
	Determines if the head in the variation nucleus is present in the current block.
	Returns boolean value based on if or not the head is present.
	"""
	head = gpattern.split()[0]
	for node in blockset:
		node_data = node.strip().split("\t")
		lemma_data = node_data[LEMMA] if node_data[LEMMA] != "_" else node_data[FORM].lower()
		if head == lemma_data:
			return True
	return False


def dependent_present(gpattern, blockset):
	"""
	Determines if the dependent in the variation nucleus is present in the current block.
	Additional checks:
		dependent is attached to the head
	Returns boolean value based on if or not the dependent is present.
	"""
	tail = gpattern.split()[-1]
	head = gpattern.split()[0]
	link_head = 0
	head_data = -1
	for node in blockset:
		node_data = node.strip().split("\t")
		lemma_data = node_data[LEMMA] if node_data[LEMMA] != "_" else node_data[FORM].lower()
		if tail == lemma_data:
			link_head = str(node_data[HEAD])
		elif head == lemma_data:
			head_data = str(node_data[ID])
	return link_head == head_data


def check_vn_occurrence(vn_data, blockset):
	"""
	Having checked for the head, and the dependent part of the variation nucleus, look for the remaining elements in the blockset.
	Takes in a split variation nucleus as the input.
	Returns boolean True if all the elements of the variation nucleus are present, else False
	"""
	occurs = dict()
	for x in vn_data:
		occurs[x] = False
	for node in blockset:
		node_data = node.strip().split("\t")
		lemma_data = node_data[LEMMA] if node_data[LEMMA] != "_" else node_data[FORM].lower()
		if lemma_data in occurs:
			occurs[lemma_data] = True
	return all([occurs[x] for x in occurs])
	

def combo_does_appear(gpattern, blockset):
	"""
	:param gpattern: Given Variation Nucleus
	:param blockset: Current Tree, in CONLL-U format
	:return: True if given variation nucleus is present in the current tree, else False
	Check the occurrence of the given variation nucleus in the current tree in following steps:
		1. Check if the head appears in the tree. If not, return False.
		2. Check if the dependent appears in the tree, and if it is linked to the same head. If not, return False.
		3. For each element in variation nucleus (minus the head, and the dependent):
			If the element is not present in the given tree, return False
		Else, if every element is present, return True for the variation nucleus does appear in the current tree.
	"""
	if head_present(gpattern, blockset):
		if dependent_present(gpattern, blockset):
			vn = gpattern.split()[1:-1]
			return check_vn_occurrence(vn, blockset)
	return False


def is_nonprojective(givenblock, vn):
	"""
	Borrows functions from find_non_projectivities module.
	For a given tree, we check if the association (involving head, and dependent) is non-projective:
		1. Since dependent is present as the final element of the variation nucleus:
			mark as nonprojective if the edge from head -> dependent features in list of non-projective edges in the tree.
		2. Otherwise, mark the tree as projective.
	Return boolean value if the tree being non-projective, subject to above conditions
	"""
	edges = find_non_projectivities.get_directed_edges(givenblock)
	p_and_c, recursive_subtrees = find_non_projectivities.get_trees(givenblock)
	dependent = vn.split()[-1]
	head = vn.split()[0]
	head_id = -1
	dependent_id = -1
	vn_lemmas = [x for x in vn.split()[1:]]
	vn_ids = []
	for givennode in givenblock:
		node_data = givennode.strip().split("\t")
		lemma_data = node_data[LEMMA] if node_data[LEMMA] != "_" else node_data[FORM].lower()
		if lemma_data == head:
			head_id = int(node_data[ID])
		elif lemma_data == dependent:
			dependent_id = int(node_data[ID])
	check, non_proj = find_non_projectivities.non_proj_check(recursive_subtrees, edges)
	if check:
		return any([(x[0] == head_id and x[1] == dependent_id) for x in non_proj])
	return False


def beamSearch_OCs(given_list):
	"""
	Beam search, and split a given list of variation nuclei into OC (main chain) and duplicates (subsequences formed off combinations of gap nucleus)
	:param given_list: List containing variation nuclei as strings
	:return: Split the variation nuclei into main chain, and all the subchains
	"""
	unique_vn = []
	subunits = []
	for vn in given_list:
		vn = vn.split()
		tail = vn[-1]
		gap_nucleus = vn[1:-1]
		unique_vn.append((vn[0], gap_nucleus, tail))
	for given_vn in given_list:
		head = given_vn.split()[0]
		vn = given_vn.split()
		tail = vn[-1]
		gap_nucleus = vn[1:-1]
		for i in range(1, len(gap_nucleus)):
			for j in list(combinations(gap_nucleus, i)):
				same_gap = [x for x in unique_vn if x[1] == list(j) and x[0] == head and x[2] == tail]
				for x in same_gap:
					if x in unique_vn:
						unique_vn.remove(x)
						subunits.append((head, list(j), tail))
	return unique_vn, subunits


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	group0 = parser.add_mutually_exclusive_group(required=True)
	group0.add_argument("-i", "--input", nargs="+", help="Input files to read data from, in CONLLU format. Multiple values possible.")
	group0.add_argument("-id", "--input_directory", type=str, help="Parent directory to read Conll-U files from. Reads .conllu files recursively.")
	group1 = parser.add_mutually_exclusive_group(required=False)
	group1.add_argument("-sf", "--support_files", nargs="+", help="Support files to read data from, in CONLLU format. Multiple values possible.")
	group1.add_argument("-sd", "--support_directory", type=str, help="Parent directory to read support files from. Reads .conllu files recursively.")
	parser.add_argument("-pf", "--pattern_file", type=str, help="File containing the lang_code, variation nucleus (vn) and vn source in a tsv format", required=True)
	args = parser.parse_args()
	
	"""
	Read in the patterns file, and register all the variation nuclei and their occurrences in \'patterns\' dict.
	To reduce runtime, the variation nuclei associated with a particular language are recorded in \'patterns_by_lang\' dict, with lang code as the key.
	Reads the data from args.pattern_file file
	"""
	patterns = dict()
	patterns_by_lang = dict()
	with open(args.pattern_file, "r", encoding="utf-8") as pfile:
		for line in pfile.readlines():
			lang, vn, all_nodes = line.strip("\n").split("\t")
			nodeslist = all_nodes.split(", ")
			mod_nodeslist = []
			for nodes in nodeslist:
				mod_nodeslist.append(nodes.split("#")[0])
			if lang not in patterns_by_lang:
				patterns_by_lang[lang] = [vn]
			else:
				patterns_by_lang[lang].append(vn)
			patterns[vn] = mod_nodeslist
	
	"""
	While generating patterns, we took a look at only the working data, now we use the structures located in additional data viz. the support directory
	Read through all the input and support directories, adding all the conllu files recursively
	"""
	input_files = []
	if args.input:
		for i in args.input:
			input_files.append(i)
	elif args.input_directory:
		for root, dirs, files in os.walk(args.input_directory):
			for filename in files:
				if filename.endswith(".conllu"):
					input_files.append(os.path.join(root, filename))
	
	support_files = []
	if args.support_files:
		for i in args.support_files:
			support_files.append(i)
	elif args.support_directory:
		for root, dirs, files in os.walk(args.support_directory):
			for filename in files:
				if filename.endswith(".conllu"):
					support_files.append(os.path.join(root, filename))
	
	"""
	For each read tree in conllu file (read in terms of blockset), blast it with all instances of variation nuclei, checking if the variation nucleus occurs in the tree.
	If the variation nucleus does occur, register the filename and sentenceID of current tree, in \"in\" segment of \'pattern_occurrence_dict\'.
	Next, we check if the association is non-projective:
		1. If dependent is the final element of the variation nucleus, mark as nonprojective if the edge from head -> dependent features in list of non-projective edges in the tree.
		2. If none of the above conditions is true, mark the tree as projective.
	If the tree is projective, increase the variation nucleus' \'proj\' counter by 1.
	Else, increase the variation nucleus' \'nonproj\' counter by 1.
	"""
	pattern_occurrence_dict = defaultdict(dict)
	all_files = support_files + input_files
	for i in tqdm.tqdm(sorted(all_files)):
		with open(i, "r", encoding="utf-8") as infile:
			treebank_id = i.split("/")[-1].split("-")[0]
			filename = i.split("/")[-1].strip()
			contents = infile.readlines()
			language_code = treebank_id.split("_")[0]
			for sent_id, text, block in find_non_projectivities.get_blocks(contents):
				for given_pattern in patterns_by_lang[language_code]:
					if sent_id not in patterns[given_pattern]:
						if combo_does_appear(given_pattern, block):
							if given_pattern not in pattern_occurrence_dict:
								pattern_occurrence_dict[given_pattern] = dict()
								pattern_occurrence_dict[given_pattern]["in_proj"] = []
								pattern_occurrence_dict[given_pattern]["in_nonproj"] = []
								pattern_occurrence_dict[given_pattern]["proj"] = 0
								pattern_occurrence_dict[given_pattern]["nonproj"] = 0
							is_nonproj = is_nonprojective(block, given_pattern)
							if is_nonproj:
								pattern_occurrence_dict[given_pattern]["nonproj"] += 1
								pattern_occurrence_dict[given_pattern]["in_nonproj"].append(filename + "/" + sent_id)
							else:
								pattern_occurrence_dict[given_pattern]["proj"] += 1
								pattern_occurrence_dict[given_pattern]["in_proj"].append(filename + "/" + sent_id)
	
	"""
	Implemented beam search here, passively.
	"""
	print("Counts Generated. Implementing beam search laterally", file=sys.stderr)
	sent_id_dict = defaultdict(dict)
	for vn in pattern_occurrence_dict:
		proj = pattern_occurrence_dict[vn]["in_proj"]
		nonproj = pattern_occurrence_dict[vn]["in_nonproj"]
		for sent_id in proj:
			if sent_id not in sent_id_dict:
				sent_id_dict[sent_id]["proj"] = [vn]
				sent_id_dict[sent_id]["nonproj"] = []
			else:
				sent_id_dict[sent_id]["proj"].append(vn)
		for sent_id in nonproj:
			if sent_id not in sent_id_dict:
				sent_id_dict[sent_id]["nonproj"] = [vn]
				sent_id_dict[sent_id]["proj"] = []
			else:
				sent_id_dict[sent_id]["nonproj"].append(vn)

	for sent_id in sent_id_dict:
		proj = [x for x in sent_id_dict[sent_id]["proj"]]
		nonproj = [x for x in sent_id_dict[sent_id]["nonproj"]]
		unique_vns, duplicate_vns = beamSearch_OCs(proj + nonproj)
		for vn in duplicate_vns:
			gn_string = " ".join(vn[1])
			new_vn = [vn[0], gn_string, vn[2]]
			vn_string = " ".join(new_vn)
			if vn_string in pattern_occurrence_dict:
				if sent_id in pattern_occurrence_dict[vn_string]["in_proj"]:
					pattern_occurrence_dict[vn_string]["in_proj"].remove(sent_id)
					pattern_occurrence_dict[vn_string]["proj"] -= 1
				elif sent_id in pattern_occurrence_dict[vn_string]["in_nonproj"]:
					pattern_occurrence_dict[vn_string]["in_nonproj"].remove(sent_id)
					pattern_occurrence_dict[vn_string]["nonproj"] -= 1

	"""
	At the end of complete run, print the following in a tsv format:
		language code, variation nucleus, number of times tree was declared nonprojective, number of times tree was declared projective,
		Filename/SentenceID of trees where pattern was found nonprojectively (CSV), Filename/SentenceID of trees where pattern was found projectively (CSV)
	"""
	for language_code in sorted(patterns_by_lang.keys()):
		for vn in sorted(patterns_by_lang[language_code]):
			if vn in pattern_occurrence_dict:
				if pattern_occurrence_dict[vn]["proj"]+pattern_occurrence_dict[vn]["nonproj"] != 0:
					print(language_code, vn, str(pattern_occurrence_dict[vn]["nonproj"]), str(pattern_occurrence_dict[vn]["proj"]), ", ".join(pattern_occurrence_dict[vn]["in_nonproj"]), ", ".join(pattern_occurrence_dict[vn]["in_proj"]), sep="\t")

	"""get counts of unique variation nuclei, and display them on stderr"""
	for language in sorted(patterns_by_lang.keys()):
		unique_vns, duplicate_vns = beamSearch_OCs(patterns_by_lang[language])
		occur_count = 0
		for vn in unique_vns:
			gn_string = " ".join(vn[1])
			new_vn = [vn[0], gn_string, vn[2]]
			vn_string = " ".join(new_vn)
			if vn_string in pattern_occurrence_dict and pattern_occurrence_dict[vn_string]["proj"]+pattern_occurrence_dict[vn_string]["nonproj"] != 0:
				occur_count += 1
		print(language, len(unique_vns), occur_count, sep="\t", file=sys.stderr)
