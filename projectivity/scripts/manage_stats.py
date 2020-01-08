#!/usr/bin/env python3

import argparse
import os
from collections import defaultdict
import tqdm
from copy import deepcopy

UNKNOWN, ALL_STATS, RELAXATION_STATS, DEGREE_STATS = range(4)


def get_stats_file_type(input_file):
	"""Start with Unknown file type, and then after analyzing the header
	contents, associate a file type that will be used for further analysis.
	Returns an integer associated with the file types."""
	
	filetype = UNKNOWN
	with open(input_file, "r", encoding="utf-8") as infile:
		header = ""
		for line in infile:
			if header == "":
				header = line
				column_count = len(header.strip("\n").split("\t"))
				column1 = header.split("\t")[0]
				if column1.startswith("--") and column_count == 4:
					filetype = RELAXATION_STATS
				elif not column1.startswith("--") and column_count == 4:
					filetype = DEGREE_STATS
				elif column1.startswith("--") and column_count > 4:
					if column_count == 6:
						filetype = ALL_STATS
					else:
						filetype = UNKNOWN
	return filetype


def combine_dicts(dict1, dict2):
	"""Combine two dictionaries. Adds the values in case of common keys, adds key otherwise"""
	
	for key in dict2:
		if key not in dict1:
			dict1[key] = dict2[key]
		else:
			dict1[key] += dict2[key]
	return dict1

	
def get_dict_as_str(dict1, total):
	"""Express a given dict as a string that can be written out.
	Concatenates values for keys > 4"""
	final_outstring = ""
	val_4 = 0
	for key in dict1:
		if key <= 4:
			value = round(dict1[key]*100/total, 4)
			final_outstring += "({x1}, {y1}), ".format(x1=key, y1=value)
		else:
			val_4 += dict1[key]
	final_outstring += "(4+, {y1})".format(y1=round(val_4*100/total, 4))
	return final_outstring


def process_relaxation_stats(input_file):
	"""Process stats files containing data on
	1. Ill-nested Structures
	2. Non-Planar Structures"""
	
	counts_dict = defaultdict(dict)
	header = ""
	placeholder = ""
	
	"""Process the Input File, and combine data from different splits of a file"""
	with open(input_file, "r", encoding="utf-8") as infile:
		for line in infile:
			if header == "":
				header = line
			else:
				placeholder, filesplit, file_count, file_total = line.strip("\n").split("\t")
				filecode = filesplit.split("-")[0]
				if filecode not in counts_dict:
					counts_dict[filecode]["count"] = int(file_count)
					counts_dict[filecode]["total"] = int(file_total)
				else:
					counts_dict[filecode]["count"] += int(file_count)
					counts_dict[filecode]["total"] += int(file_total)
	
	"""Start Writing Outputs, with an additional field of \'Percentage\'"""
	outfile = input_file + "2"
	with open(outfile, "w", encoding="utf-8") as out:
		out.write(header.strip("\n")+"\tPercentage\n")
		for filecode in sorted(counts_dict):
			percentage = round(counts_dict[filecode]["count"]*100/counts_dict[filecode]["total"], 4)
			out.write(placeholder + "\t" + filecode + "\t" + str(counts_dict[filecode]["count"]) + "\t" + str(counts_dict[filecode]["total"]) + "\t" + str(percentage) + "\n")


def process_degree_stats(input_file):
	"""Process stats files containing data on
	1. Gap-Degree Statistics
	2. Edge-Degree Statistics
	Invokes get_dict_as_str() and combine_dicts()"""
	
	degree_counts_dict = defaultdict(dict)
	degree_dicts_dict = defaultdict(dict)
	header = ""
	
	"""Process the Input File, and combine data from different splits of a file"""
	with open(input_file, "r", encoding="utf-8") as infile:
		for line in infile:
			if header == "":
				header = line
			else:
				working_line = line.strip("\n")
				filecode = working_line.split("\t")[0].split("-")[0]
				file_count = int(working_line.split("\t")[1])
				file_total = int(working_line.split("\t")[2])
				degree_list = working_line.split("\t")[3]
				dummy1 = "".join([x for x in degree_list if x not in ["(", ")", "[", "]"]])
				dummy1 = dummy1.split(", ")
				a = dict()
				for dummy_count in range(len(dummy1)):
					if dummy_count % 2 == 0:
						a[int(dummy1[dummy_count])] = int(dummy1[dummy_count+1])
				if filecode not in degree_dicts_dict:
					degree_dicts_dict[filecode] = a
				else:
					degree_dicts_dict[filecode] = combine_dicts(degree_dicts_dict[filecode], a)
				if filecode not in degree_counts_dict:
					degree_counts_dict[filecode]["count"] = file_count
					degree_counts_dict[filecode]["total"] = file_total
				else:
					degree_counts_dict[filecode]["count"] = max(file_count, degree_counts_dict[filecode]["count"])
					degree_counts_dict[filecode]["total"] += file_total
	
	"""Start Writing Outputs"""
	outfile = input_file + "2"
	with open(outfile, "w", encoding="utf-8") as out:
		out.write(header)
		for filecode in sorted(degree_counts_dict):
			out.write(filecode + "\t" + str(degree_counts_dict[filecode]["count"]) + "\t" + str(degree_counts_dict[filecode]["total"]) + "\t")
			out.write(get_dict_as_str(degree_dicts_dict[filecode], degree_counts_dict[filecode]["total"]) + "\n")


def process_all_stats(input_file):
	"""Process stats files containing data on
		All Non-Projective Structures"""
	
	counts_dict = defaultdict(dict)
	header = ""
	placeholder = ""
	
	"""Process the Input File, and combine data from different splits of a file"""
	with open(input_file, "r", encoding="utf-8") as infile:
		for line in infile:
			if header == "":
				header = line
			else:
				placeholder, filesplit, edge_count, edge_total, tree_count, tree_total = line.strip("\n").split("\t")
				filecode = filesplit.split("-")[0]
				if filecode not in counts_dict:
					counts_dict[filecode]["edge_count"] = int(edge_count)
					counts_dict[filecode]["edge_total"] = int(edge_total)
					counts_dict[filecode]["tree_count"] = int(tree_count)
					counts_dict[filecode]["tree_total"] = int(tree_total)
				else:
					counts_dict[filecode]["edge_count"] += int(edge_count)
					counts_dict[filecode]["edge_total"] += int(edge_total)
					counts_dict[filecode]["tree_count"] += int(tree_count)
					counts_dict[filecode]["tree_total"] += int(tree_total)
	
	"""Start Writing Outputs, with additional fields of \'Percentages\'"""
	outfile = input_file + "2"
	with open(outfile, "w", encoding="utf-8") as out:
		header = header.strip("\n").split("\t")
		header_out = "\t".join(header[:4]) + "\tPercentage\t"
		header_out += "\t".join(header[4:]) + "\tPercentage\n"
		out.write(header_out)
		for filecode in sorted(counts_dict):
			percentage1 = round(counts_dict[filecode]["edge_count"] * 100 / counts_dict[filecode]["edge_total"], 4)
			percentage2 = round(counts_dict[filecode]["tree_count"] * 100 / counts_dict[filecode]["tree_total"], 4)
			out.write(placeholder + "\t" + filecode + "\t" + str(counts_dict[filecode]["edge_count"]) + "\t" + str(counts_dict[filecode]["edge_total"]) + "\t" + str(percentage1) + "\t" + str(counts_dict[filecode]["tree_count"]) + "\t" + str(counts_dict[filecode]["tree_total"]) + "\t" + str(percentage2) +"\n")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	group0 = parser.add_mutually_exclusive_group(required=True)
	group0.add_argument("-i", "--input", nargs="+", help="Input files to read data from, in *.stats format. Multiple values possible.")
	group0.add_argument("-id", "--input_directory", type=str, help="Parent directory to read *.stats files from. Reads files recursively.")
	args = parser.parse_args()
	
	"""Define the input files"""
	input_files = []
	if args.input:
		for i in args.input:
			input_files.append(i)
	elif args.input_directory:
		for root, dirs, files in os.walk(args.input_directory):
			for filename in files:
				if filename.endswith(".stats"):
					input_files.append(os.path.join(root, filename))
	
	"""Process the input files sequentially"""
	for x in tqdm.tqdm(input_files):
		filetype = get_stats_file_type(x)
		if filetype == RELAXATION_STATS:
			process_relaxation_stats(x)
		elif filetype == DEGREE_STATS:
			process_degree_stats(x)
		elif filetype == ALL_STATS:
			process_all_stats(x)
