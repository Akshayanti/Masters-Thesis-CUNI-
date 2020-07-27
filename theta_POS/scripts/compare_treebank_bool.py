#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r", encoding="utf-8") as infile:
    content = infile.readlines()
    for lines in content:
        if lines.strip().startswith("<total>"):
            total_count = int(lines.strip().split("sentences>")[1].strip("</"))
            print(sys.argv[1].strip("/stats.xml"), str(total_count >= 1000), sep="\t")
