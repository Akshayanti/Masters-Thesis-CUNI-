#!/usr/bin/env python3


scores = dict()
k8_score = dict()
k4_score = dict()
k2_score = dict()
error_mappings = {"Case Error (4case)": "Case Error",
                  "None": "No Error",
                  "Reported Speech Error (4parataxis)": "Reported Speech",
                  "MWE Error (4compound|fixed)": "MWE Error",
                  "Naming Error (4appos|flat)": "Naming Error"}


def read_stats(input_file, position):
    with open(input_file, "r", encoding="utf-8") as infile:
        for lines in infile:
            error = lines.strip("\n").split("\t")[3]
            if error not in scores:
                scores[error] = [0, 0, 0, 0]
            scores[error][position] += 1


def scores_k8():
    for error in scores:
        k8_score[error] = scores[error][0] * 5


def scores_k4():
    for error in scores:
        c1 = scores[error][0] * 2319 / 200
        c2 = scores[error][1] * 301 / 100
        k4_score[error] = round((c1 + c2) * 1000 / 2620, 1)


def scores_k2():
    for error in scores:
        c1 = scores[error][0] * 2319 / 200
        c2 = scores[error][1] * 301 / 100
        c3 = scores[error][2] * 867 / 100
        k2_score[error] = round((c1 + c2 + c3) * 1000 / 3487, 1)


def get_normalised_scores():
    read_stats("Annotations/allArcs/k_all_200.tsv", 0)
    read_stats("Annotations/allArcs/k_4not8_100.tsv", 1)
    read_stats("Annotations/allArcs/k_2not4_100.tsv", 2)
    scores_k2()
    scores_k4()
    scores_k8()
    random_error = [0, 0, 0]
    with open("Annotations/allArcs/normalizedScores.tsv", "w", encoding="utf-8") as outfile:
        outfile.write("Type\tk2\tk4\tk8\n")
        for error in sorted(scores):
            outstring = ""
            if error in error_mappings:
                outstring = error_mappings[error] + "\t"
            else:
                outstring = error + "\t"
            if (k2_score[error] > 5) and (k4_score[error] > 5 or k8_score[error] > 5):
                outstring += str(k2_score[error]) + "\t" \
                             + str(k4_score[error]) + "\t" \
                             + str(k8_score[error]) + "\n"
                outfile.write(outstring)
            else:
                random_error[0] += k2_score[error]
                random_error[1] += k4_score[error]
                random_error[2] += k8_score[error]
        outfile.write("Random Errors\t" +
                      str(round(random_error[0], 1)) + "\t" +
                      str(round(random_error[1], 1)) + "\t" +
                      str(round(random_error[2], 1)) + "\n")


def get_test_scores():
    scores.clear()
    read_stats("Annotations/testArcs/base_allZero.tsv", 0)
    read_stats("Annotations/testArcs/test_k2.tsv", 1)
    read_stats("Annotations/testArcs/test_k4.tsv", 2)
    read_stats("Annotations/testArcs/test_k8.tsv", 3)
    random_errors = [0, 0, 0, 0]
    with open("Annotations/testArcs/comparisonStats.tsv", "w", encoding="utf-8") as outfile:
        outfile.write("Type\tBaseline\tk2\tk4\tk8\n")
        for error in sorted(scores):
            outstring = ""
            if (scores[error][0] != scores[error][1]) and (scores[error][0] * 100 / 221 - 0.5 > 0) or (
                    scores[error][1] * 100 / 333 - 0.5 > 0):
                if error in error_mappings:
                    outstring = error_mappings[error] + "\t"
                else:
                    outstring = error + "\t"
                outstring += str(scores[error][0]) + " (" + str(round(scores[error][0] * 100 / 221, 1)) \
                             + "%)\t" \
                             + str(scores[error][1]) + " (" + str(round(scores[error][1] * 100 / 333, 1)) \
                             + "%)\t" \
                             + str(scores[error][2]) + " (" + str(round(scores[error][2] * 100 / 254, 1)) \
                             + "%)\t" \
                             + str(scores[error][3]) + " (" + str(round(scores[error][3] * 100 / 226, 1)) \
                             + "%)\n"
                outfile.write(outstring)
            else:
                random_errors[0] += scores[error][0]
                random_errors[1] += scores[error][1]
                random_errors[2] += scores[error][2]
                random_errors[3] += scores[error][3]
        outfile.write("Random Errors\t"
                      + str(random_errors[0]) + " (" + str(round(random_errors[0] * 100 / 221, 1)) \
                      + "%)\t" \
                      + str(random_errors[1]) + " (" + str(round(random_errors[1] * 100 / 333, 1)) \
                      + "%)\t" \
                      + str(random_errors[2]) + " (" + str(round(random_errors[2] * 100 / 254, 1)) \
                      + "%)\t" \
                      + str(random_errors[3]) + " (" + str(round(random_errors[3] * 100 / 226, 1)) \
                      + "%)\n")


if __name__ == "__main__":
    get_normalised_scores()
    get_test_scores()
