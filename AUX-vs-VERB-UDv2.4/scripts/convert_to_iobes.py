#!/usr/bin/env python3

import sys


def processBlock(block):
    """Process the read block, and assign IOBES tags"""
    tokens = []
    tags = []
    for lines in block:
        if not lines.startswith("#"):
            if "-" not in lines.split()[0]:
                tokens.append(lines.split("\t")[1])
                upos = lines.split("\t")[3]
                if upos == "AUX":
                    tags.append("S-aux")
                elif upos == "VERB":
                    tags.append("S-verb")
                else:
                    tags.append("O")
    return tokens, tags


def getBlocks(filename):
    """Read the document in a block format"""
    blocks_list = []
    with open(filename, "r", encoding="utf-8") as infile:
        block = []
        for lines in infile:
            if lines != "\n":
                block.append(lines)
            else:
                blocks_list.append(block)
                block = []
    return blocks_list


def fileStructures(filename2, tokens, tags):
    """ .txt format->       token, and tag seperated with a tab
        Write the structures by appending them into a file"""
    with open(filename2+".txt", "a", encoding="utf-8") as outfile:
        for x in zip(tokens[:-1],tags[:-1]):
            outfile.write(x[0] + "\t" + x[1] + "\n")
        outfile.write(tokens[-1] + "\t" + tags[-1] + "\n\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Args: FileName(s) (in CONLL-U format) to convert into IOBES format\n"
              "Usage: python {x} <Input Args>".format(x=sys.argv[0]))
    for files in sys.argv[1:]:
        blocks = getBlocks(files)
        for block in blocks:
            tokens, tags = processBlock(block)
            fileStructures(files, tokens, tags)
