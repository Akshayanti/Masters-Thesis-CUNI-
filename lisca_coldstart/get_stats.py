#!/usr/bin/env python3


def get_line_count(infile):
	lines = 0
	with open(infile, "r", encoding="utf-8") as inputfile:
		lines = len(inputfile.readlines())
	return lines


def error_typology(infile):
	error_typology = dict()
	with open(infile, "r", encoding="utf-8") as typology_file:
		for lines in typology_file:
			try:
				sent_id, arc_id, score, errorBool, errorType = lines.strip("\n").split("\t")
				if errorType not in error_typology:
					error_typology[errorType] = 1
				else:
					error_typology[errorType] += 1
			except ValueError:
				if lines == "\n":
					continue
				else:
					if "Unclassified" in error_typology:
						error_typology["Unclassified"] += 1
					else:
						error_typology["Unclassified"] = 1
	return error_typology


def write_typology(typology_dict):
	print("| Error Type | Count |\n|:--------|:----|", file=STATS_FILE)
	for key in typology_dict:
		print("| " + key + " | " + str(typology_dict[key]) + " |", file=STATS_FILE)

# ====================== BASELINE ONLY ===============================================
def baseline_total_stats():
	BASELINE_ZERO = "baseline/base_allZero.tsv"
	BASELINE_ALL = "baseline/baseline_test.lisca"
	all_count = get_line_count(BASELINE_ALL)
	zero_arcs = get_line_count(BASELINE_ZERO)
	print("<b>Total Arcs Processed:</b> " + str(all_count) + "  ", file=STATS_FILE)
	print("<b>Zero-Scored Arcs:</b> " + str(zero_arcs) + "  ", file=STATS_FILE)
	print("<b>Percentage:</b> " + str(round(zero_arcs * 100 / all_count, 3)) + " %  ", file=STATS_FILE)


def baseline_typology():
	BASELINE = "Annotations/testArcs/base_allZero.tsv"
	errorsType_baseline = error_typology(BASELINE)
	write_typology(errorsType_baseline)


def analyse_baseline_only():
	print("<h2>Baseline</h2>", file=STATS_FILE)
	print("<h3>Overall Statistics</h3>\n", file=STATS_FILE)
	baseline_total_stats()
	print("", file=STATS_FILE)
	print("<h3>Error Typology</h3>\n", file=STATS_FILE)
	baseline_typology()
	print("", file=STATS_FILE)

# ====================== CV ONLY ===============================================
def check_all_inclusion(infile1, infile2, infile3):
	outprint = []
	if check_inclusion(infile1, infile2):
		outprint.append("<b>Note: The 0-scored arcs in K=2 contains all the arcs in K=4  ")
	if check_inclusion(infile1, infile3):
		outprint.append("<b>Note: The 0-scored arcs in K=2 contains all the arcs in K=8  ")
	if check_inclusion(infile2, infile3):
		outprint.append("<b>Note: The 0-scored arcs in K=4 contains all the arcs in K=8  ")
	
	if len(outprint) != 0:
		print("\n\n", file=STATS_FILE)
		for x in outprint:
			print(x, file=STATS_FILE)


def check_inclusion(infile1, infile2):
	len1 = get_line_count(infile1)
	len2 = get_line_count(infile2)
	if len2 > len1:
		infile1, infile2 = infile2, infile1
	check_dict = dict()
	with open(infile2, "r", encoding="utf-8") as smaller_file:
		for lines in smaller_file:
			check_dict[lines.strip("\n")] = False
	with open(infile1, "r", encoding="utf-8") as big_file:
		for lines in big_file:
			if lines.strip("\n") in check_dict:
				check_dict[lines.strip("\n")] = True
	print(all(check_dict))
	for x in check_dict:
		if not check_dict[x]:
			return False


def CV_total_stats():
	K2 = "CV/test_k2.tsv"
	K4 = "CV/test_k4.tsv"
	K8 = "CV/test_k8.tsv"
	all_count = 336079
	print("<b>Total Arcs Processed:</b> " + str(all_count) + "  ", file=STATS_FILE)
	print("<b>Zero-Scored Arcs:</b>\n", file=STATS_FILE)
	print("| K=2 | K=4 | K=8 |\n|:------:|:-----:|:-----:|", file=STATS_FILE)
	print("| " + str(get_line_count(K2)) + " | " + str(get_line_count(K4)) + " | " + str(get_line_count(K8)) + " |", file=STATS_FILE)
	check_all_inclusion(K2, K4, K8)
	

def analyse_cv_only():
	print("<h2>Cross-Validation</h2>", file=STATS_FILE)
	print("<h3>Overall Statistics</h3>\n", file=STATS_FILE)
	CV_total_stats()


if __name__ == "__main__":
	STATS_FILE = open("stats.README", "w", encoding="utf-8")
	print("<h1>Statistics Comparing Different Runs</h1>\n", file=STATS_FILE)
	print("Table of Contents:  ", file=STATS_FILE)
	print("1. [Baseline Results](#baseline)  ", file=STATS_FILE)
	print("2. [Cross-Validation Results (Sampled Instances)](#cross-validation)  ", file=STATS_FILE)
	print("3. [Baseline vs Cross-Validation](#baseline-cross)  \n", file=STATS_FILE)
	analyse_baseline_only()
	STATS_FILE.close()
