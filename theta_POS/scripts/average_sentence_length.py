#!/usr/bin/env python3

import sys


def read_blocks(file_contents):
    """Read the incoming file as a block"""
    tokens_count = 0
    outset = []
    block = []
    for lines in file_contents:
        if lines != "\n":
            block.append(lines)
        if lines == "\n":
            tokens_count += int(block[-1].split("\t")[0])
            block.append(lines)
            outset.append(block)
            block = []
    return tokens_count, len(outset)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Need exactly one input file as an argument"
    with open(sys.argv[1], "r", encoding="utf-8") as infile:
        tokens, sentences = read_blocks(infile)
    print(sys.argv[1], str(round(tokens / sentences, 3)), sep="\t")
