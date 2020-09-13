#!/usr/bin/env python3

import sys
from sklearn.model_selection import KFold
from numpy import array


def organise_as_block(file_contents):
    """Read the incoming file as a block"""
    outset = []
    block = []
    for lines in file_contents:
        if lines != "\n":
            block.append(lines)
        if lines == "\n":
            block.append(lines)
            outset.append(block)
            block = []
    return outset


def cross_validate(data, k):
    """create k-folds of data, non-intersecting with each other"""
    kfold = KFold(k, True, 1)
    i = 1
    for train, test in kfold.split(data):
        with open("train_" + str(i), "w", encoding = "utf-8") as out_train:
            for values in data[train]:
                for lines in values:
                    out_train.write(lines)
        with open("test_" + str(i), "w", encoding="utf-8") as outfile:
            for values in data[test]:
                for lines in values:
                    outfile.write(lines)
        i += 1


if __name__ == "__main__":
    help_txt = "Arg1: k-value in k-fold cross validation\n" \
               "Arg2: Input file in CONLL-U format\n" \
               "Usage: python3 {x} Arg1 Arg2".format(x=sys.argv[0])

    if len(sys.argv) != 3:
        print(help_txt)
        exit(1)

    if not int(sys.argv[1]):
        print(help_txt)
        exit(1)

    with open(sys.argv[2], "r", encoding="utf-8") as infile:
        contents = infile.readlines()
        blocks = organise_as_block(contents)
        data = array(blocks)
        cross_validate(data, k=int(sys.argv[1]))
   

