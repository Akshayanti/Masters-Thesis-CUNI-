#!/usr/bin/env python3

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def find_with_more_than(filename, cutoff):
    """"Given the filename, and the cutoff value, find instances that have been annotated with
    confidence score >= cutoff value, and write them out in a file"""
    out_lines = []
    with open(filename, "r", encoding="utf-8") as infile:
        for line in infile:
            if float(line.split("\t")[5]) >= cutoff:
                out_lines.append(line)
    outfilename = "{x}_{y}.tsv".format(x=filename.split('.tsv')[0], y=cutoff)
    with open(outfilename, "w", encoding="utf-8") as outfile:
        for line in out_lines:
            outfile.write(line)


def find_with_less_than(filename, cutoff):
    """"Given the filename, and the cutoff value, find instances that have been annotated with
    confidence score <= cutoff value, and write them out in a file"""
    out_lines = []
    with open(filename, "r", encoding="utf-8") as infile:
        for line in infile:
            if float(line.split("\t")[4]) <= cutoff:
                out_lines.append(line)
    outfilename = "{x}_{y}.tsv".format(x=filename.split('.tsv')[0], y=cutoff)
    with open(outfilename, "w", encoding="utf-8") as outfile:
        for line in out_lines:
            outfile.write(line)


def generate_plots(files, confidence):
    """Generate a Density Rug Plot for True Positive Labelled Data, with confidence of prediction less than the
    specified confidence value."""
    a = {"O": [], "S-verb": [], "S-aux": []}
    filename = files[0]
    with open(filename, "r", encoding="utf-8") as infile:
        for line in infile:
            label, value = line.rstrip().split()
            if float(value) <= confidence:
                a[label].append(float(value))
    kwargs = dict(hist_kws={'stacked': True, 'density': True}, kde_kws={'linewidth': 2})
    colors = {'O': 'red', 'S-verb': 'blue', 'S-aux': 'green'}
    for vals in a:
        arr = np.array(a[vals])
        sns.distplot(arr, hist=False, color=colors[vals], rug=True, label=vals, **kwargs)
    plt.legend()
    plt.title("Rug Plot with Distribution of Predictions with confidence <= {x}".format(x=confidence))
    plt.xlabel("Confidence Score")
    plt.ylabel("Probability Density")
    plt.savefig('docs/Distribution_{x}.png'.format(x=confidence))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('--above', action='store_true', help="Filter values with prediction confidence score "
                                                             "ABOVE \'--confidence\' value")
    group1.add_argument('--below', action='store_true', help="Filter values with prediction confidence score "
                                                             "BELOW \'--confidence\' value")
    group1.add_argument('--plot', action='store_true', help="Do not filter values, but generate rug-plot of "
                                                            "distribution of confidence scores, with "
                                                            "maximum cutoff value as specified in \'--confidence\'"
                                                            " argument")
    parser.add_argument('-c', '--confidence', type=float, help="Float value of confidence score to compare against.",
                        required=True)
    parser.add_argument('-i', '--input', type=str, nargs='+', help="Input file(s) to work with", required=True)
    args = parser.parse_args()

    if args.above:
        for x in args.input:
            find_with_more_than(x, args.confidence)
    elif args.below:
        for x in args.input:
            find_with_less_than(x, args.confidence)
    elif args.plot:
        generate_plots(args.input, args.confidence)
