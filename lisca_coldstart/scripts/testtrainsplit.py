#!/usr/bin/env python

import sys
import random


def organise_as_block(file_contents):
    """read incoming CONLL-U file as a block"""
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


def split(data, k):
    """Do a non-intersecting split of the data as per given arguments"""
    train = random.sample(data, k)
    test = [x for x in data if x not in train]
    with open("train.conllu", "w", encoding="utf-8") as out_train:
        for values in train:
            for lines in values:
                out_train.write(lines)
    with open("test.conllu", "w", encoding="utf-8") as outfile:
        for values in test:
            for lines in values:
                outfile.write(lines)


if __name__ == "__main__":
    help_txt = "Arg1: Train File Size (in /%)\n" \
               "Arg2: Input file in conllu format\n" \
               "Usagee: python3 {x} Arg1 Arg2".format(x=sys.argv[0])
    if len(sys.argv) != 3:
        print(help_txt)
        exit(1)
    
    if not int(sys.argv[1]):
        print(help_txt)
        exit(1)
    else:
        if not 50 <= int(sys.argv[1]) < 100:
            print("Train Size should be >=50/% and <100/%")
            exit(1)
    
    data = None
    random.seed(1618)
    with open(sys.argv[2], "r", encoding="utf-8") as infile:
        contents = infile.readlines()
        data = organise_as_block(contents)
        split(data, k=int(int(sys.argv[1]) * len(data) / 100))
