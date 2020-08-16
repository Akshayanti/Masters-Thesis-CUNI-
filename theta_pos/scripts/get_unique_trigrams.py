#!/usr/bin/env python3

import matplotlib.pyplot as plt
import sys
import klcpos3
import statistics as stats


def get_trigrams_stats(input_file):
    """Print trigrams_count and total_trigrams in TSV format"""
    with open(input_file, "r", encoding="utf-8") as source_file:
        source_data = source_file.readlines()
        src_list = klcpos3.get_pos_list(source_data)
        source, src_total = klcpos3.trigram_from_list(src_list)
        print(len(source), src_total, sep="\t")


def process_scores(input_files):
    all_stats = dict()
    POS_count = []
    POS_total = []
    for input_file in input_files:
        with open(input_file, "r", encoding="utf-8") as infile:
            for lines in infile:
                pos_count, total_pos = lines.strip("\n").split("\t")
                POS_count.append(int(pos_count))
                POS_total.append(int(total_pos))
        mean_count = stats.mean(POS_count)
        mean_total = stats.mean(POS_total)
        POS_count.clear()
        POS_total.clear()
        all_stats[input_file.split("_")[1]] = [mean_count, mean_total]

    with open(input_files[2].split("_")[0]+"-stats.tsv", "w", encoding="utf-8") as outputfile:
        for x in sorted(all_stats):
            outstring = x + "\t" + str(round(all_stats[x][0], 2)) + "\t" + str(round(all_stats[x][1], 2)) + "\n"
            outputfile.write(outstring)


def read_scores(infile):
    scores_1 = dict()
    with open(infile, "r", encoding="utf-8") as filedata:
        for lines in filedata:
            if lines != "":
                instances, count, total = lines.strip("\n").split("\t")
                scores_1[int(instances)] = [float(count), float(total)]
    return scores_1


def plot_and_save(indict1, infile):
    x_list = [x for x in sorted(indict1)]
    counts_list = [indict1[x][0] for x in sorted(indict1)]
    totals_list = [indict1[x][1] for x in sorted(indict1)]

    zoomed_x_list = [x for x in sorted(indict1) if x<=2000]
    zoomed_counts = [indict1[x][0] for x in zoomed_x_list]
    zoomed_totals = [indict1[x][1] for x in zoomed_x_list]

    treebank_name = infile.split("/")[-1].strip("-stats.tsv")

    fig, (ax1, ax3) = plt.subplots(nrows=2, ncols=1, sharey=True, constrained_layout=True)
    ax1.set(xlabel="Number of Sentences", title="Over " + str(max([x for x in indict1])) + " Sentences")
    ax1.plot(x_list, [round(x * 100 / max(counts_list), 2) for x in counts_list], "r-")
    ax1.plot(x_list, [round(x * 100 / max(totals_list), 2) for x in totals_list], "b-")
    ax1.grid(True)
    ax1.set_ylabel("Percentage")
    ax1.legend(["Unique POS Trigrams", "All POS Trigrams"])

    ax3.set(xlabel="Number of Sentences", title="Over 2000 Sentences")
    ax3.plot(zoomed_x_list, [round(x * 100 / max(counts_list), 2) for x in zoomed_counts], "r-")
    ax3.plot(zoomed_x_list, [round(x * 100 / max(totals_list), 2) for x in zoomed_totals], "b-")
    ax3.grid(True)
    ax3.set_ylabel("Percentage")
    ax3.legend(["Unique POS Trigrams", "All POS Trigrams"])

    fig.suptitle("Growth of POS trigrams in " + treebank_name + " with Increase in Dataset Size")
    plt.savefig("../docs/trigram-stats-" + treebank_name + ".png")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if ".tsv" not in sys.argv[1]:
            get_trigrams_stats(sys.argv[1])
        else:
            scores = read_scores(sys.argv[1])
            plot_and_save(scores, sys.argv[1])
    else:
        process_scores(sys.argv[1:])