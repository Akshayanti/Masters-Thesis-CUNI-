#!/usr/bin/env python3

STATS_FILE = open("stats.md", "w", encoding="utf-8")


def get_line_count(infile):
    with open(infile, "r", encoding="utf-8") as inputfile:
        lines = len(inputfile.readlines())
    return lines


def error_typology(infile):
    error_typology = dict()
    with open(infile, "r", encoding="utf-8") as typology_file:
        for lines in typology_file:
            try:
                sent_id, arc_id, errorBool, errorType = lines.strip("\n").split("\t")
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
    for key in sorted(typology_dict.keys(), key=lambda x: x.lower()):
        key1 = key
        if "|" in key:
            key1 = key.split("|")[0] + "OR" + key.split("|")[1]
        print("| " + key1 + " | " + str(typology_dict[key]) + " |", file=STATS_FILE)
    print("| <b>Total</b> | <b>" + str(sum(typology_dict.values())) + " </b>|", file=STATS_FILE)


# ====================== BASELINE ONLY ===============================================
def baseline_total_stats():
    BASELINE_ZERO = "baseline/baseline_zero.tsv"
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
        outprint.append("<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=4  ")
    if check_inclusion(infile1, infile3):
        outprint.append("<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=8  ")
    if check_inclusion(infile2, infile3):
        outprint.append("<b>Note</b>: The 0-scored arcs in K=4 contains all the 0-scored arcs in K=8  ")

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
    return all(check_dict.values())


def CV_total_stats():
    K2 = "CV/allArcs/k2.tsv"
    K4 = "CV/allArcs/k4.tsv"
    K8 = "CV/allArcs/k8.tsv"
    all_count = 336079
    print("<b>Total Arcs Processed:</b> " + str(all_count) + "  ", file=STATS_FILE)
    print("<b>Zero-Scored Arcs:</b>\n", file=STATS_FILE)
    print("| K=2 | K=4 | K=8 |\n|:------:|:-----:|:-----:|", file=STATS_FILE)
    print("| " + str(get_line_count(K2)) + " | " + str(get_line_count(K4)) + " | " + str(get_line_count(K8)) + " |",
          file=STATS_FILE)
    check_all_inclusion(K2, K4, K8)


def CV_typologies():
    K2not4 = "Annotations/allArcs/k_2not4_100.tsv"
    K4not8 = "Annotations/allArcs/k_4not8_100.tsv"
    Kall = "Annotations/allArcs/k_all_200.tsv"
    print("<h4>Instances Common to K=2, K=4 and K=8</h4>\n", file=STATS_FILE)
    write_typology(error_typology(Kall))
    print("\n<h4>Instances in K=4 not present in K=8</h4>\n", file=STATS_FILE)
    write_typology(error_typology(K4not8))
    print("\n<h4>Instances in K=2 not present in K=4 or K=8</h4>\n", file=STATS_FILE)
    write_typology(error_typology(K2not4))


def analyse_CV_only():
    print("<h2>Cross-Validation</h2>", file=STATS_FILE)
    print("<h3>Overall Statistics</h3>\n", file=STATS_FILE)
    CV_total_stats()
    print("<h3>Error Typology</h3>\n", file=STATS_FILE)
    CV_typologies()
    print("", file=STATS_FILE)


# ======================= BASELINE vs CV ===============================================
def get_error_count(inputfile):
    error_count = 0
    with open(inputfile, "r", encoding="utf-8") as infile:
        for lines in infile:
            if lines == "\n":
                continue
            fields = lines.strip("\n").split("\t")
            if len(fields) == 4:
                if fields[2] == "0":
                    error_count += 1
    return error_count


def baseline_vs_CV_compare():
    base = "Annotations/testArcs/base_allZero.tsv"
    K2 = "Annotations/testArcs/test_k2.tsv"
    K4 = "Annotations/testArcs/test_k4.tsv"
    K8 = "Annotations/testArcs/test_k8.tsv"
    print("| | Baseline | K=2 | K=4 | K=8 |\n|:----|:----:|:-----:|:-----:|:-----:|", file=STATS_FILE)
    print("| | " + str(get_line_count(base)) + " | " + str(get_line_count(K2)) + " | " + str(
        get_line_count(K4)) + " | " + str(get_line_count(K8)) + " |", file=STATS_FILE)
    print("| <b>Errors</b> | <b>" + str(get_error_count(base)) + "</b> | <b>" +
          str(get_error_count(K2)) + "</b> | <b>" +
          str(get_error_count(K4)) + "</b> | <b>" +
          str(get_error_count(K8)) + "</b> |", file=STATS_FILE)
    print("| <b>Percentage</b>| <b>" + str(round(get_error_count(base) * 100 / get_line_count(base), 2)) +
          " %</b> | <b>" + str(round(get_error_count(K2) * 100 / get_line_count(K2), 2)) +
          " %</b> | <b>" + str(round(get_error_count(K4) * 100 / get_line_count(K4), 2)) +
          " %</b> | <b>" + str(round(get_error_count(K8) * 100 / get_line_count(K8), 2)) +
          " %</b> |", file=STATS_FILE)


def check_inclusion_common_elements_count(infile1, infile2):
    lines_1 = []
    lines_2 = []
    with open(infile1, "r", encoding="utf-8") as file1:
        for lines in file1:
            if lines == "\n":
                continue
            sent = lines.split("\t")[0]
            arc = lines.split("\t")[1]
            lines_1.append(sent + "#" + arc)
    with open(infile2, "r", encoding="utf-8") as file2:
        for lines in file2:
            if lines == "\n":
                continue
            sent = lines.split("\t")[0]
            arc = lines.split("\t")[1]
            lines_2.append(sent + "#" + arc)
    if len(lines_1) > len(lines_2):
        return str(len([x for x in lines_1 if x in lines_2]))
    else:
        return str(len([x for x in lines_2 if x in lines_1]))


def baseline_vs_CV_common():
    base = "Annotations/testArcs/base_allZero.tsv"
    K2 = "Annotations/testArcs/test_k2.tsv"
    K4 = "Annotations/testArcs/test_k4.tsv"
    K8 = "Annotations/testArcs/test_k8.tsv"
    print("| | K=2 | K=4 | K=8 |\n|:------:|:-----:|:-----:|:-----:|", file=STATS_FILE)
    print("| Baseline | " + check_inclusion_common_elements_count(base, K2) + " | " +
          check_inclusion_common_elements_count(base, K4) + " | " +
          check_inclusion_common_elements_count(base, K8) + " |", file=STATS_FILE)


def analyse_baseline_vs_CV():
    base_not_k = "Annotations/testArcs/base_not_k.tsv"
    k_not_base = "Annotations/testArcs/k_not_base.tsv"
    print("<h2>Baseline vs Cross-Validation</h2>", file=STATS_FILE)
    check_all_inclusion("Annotations/testArcs/test_k2.tsv",
                        "Annotations/testArcs/test_k4.tsv",
                        "Annotations/testArcs/test_k8.tsv")
    print("<h3>Arc Flagging Statistics</h3>\n", file=STATS_FILE)
    baseline_vs_CV_compare()
    print(
        "\n<b>Note:</b> Typology Counts Across different runs can be viewed "
        "[here](./Annotations/testArcs/comparisonStats.tsv)", file=STATS_FILE)
    print("<h3>Arcs Commonly Flagged</h3>\n", file=STATS_FILE)
    baseline_vs_CV_common()
    print("<h3>Picked by Baseline, not by Cross-Validation</h3>\n", file=STATS_FILE)
    write_typology(error_typology(base_not_k))
    print("<h3>Picked by Cross Validation, not by Baseline</h3>\n", file=STATS_FILE)
    write_typology(error_typology(k_not_base))


if __name__ == "__main__":
    print("<h1>Statistics Comparing Different Runs</h1>\n", file=STATS_FILE)
    print("Table of Contents:  ", file=STATS_FILE)
    print("1. [Baseline Results](#baseline)  ", file=STATS_FILE)
    print("2. [Cross-Validation Results (Sampled Instances)](#cross-validation)  ", file=STATS_FILE)
    print("3. [Baseline vs Cross-Validation](#baseline-vs-cross-validation)  \n", file=STATS_FILE)
    analyse_baseline_only()
    analyse_CV_only()
    analyse_baseline_vs_CV()
    STATS_FILE.close()
