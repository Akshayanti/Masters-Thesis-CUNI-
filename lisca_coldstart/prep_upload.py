#!/usr/bin/env python3

import sys

arcsAnnotated = dict()
arcsNotAnnotated = dict()

with open(sys.argv[1], "r", encoding="utf-8") as infile:
    for lines in infile:
        mod_line = lines.strip("\n")
        if mod_line != "":
            tree = mod_line.split("\t")[0]
            arc = mod_line.split("\t")[1]
            annotation = mod_line.split("\t")[2:]
            arcsAnnotated[tree+"+"+arc] = annotation

with open(sys.argv[2], "r", encoding="utf-8") as readfile:
    for lines in readfile:
        if lines != "\n":
            tree = lines.strip("\n").split("\t")[0]
            arc = lines.strip("\n").split("\t")[1]
            annotation = lines.strip("\n").split("\t")[2:]
            key = tree+"+"+arc
            if key in arcsAnnotated:
                arcsNotAnnotated[key] = arcsAnnotated[key]
            else:
                arcsNotAnnotated[key] = annotation

with open(sys.argv[2]+"_new", "w", encoding="utf-8") as outfile:
    for keys in arcsNotAnnotated:
        tree, arc = keys.split("+")
        outstring = tree + "\t" + arc + "\t" + "\t".join(arcsNotAnnotated[keys]) + "\n"
        outfile.write(outstring)