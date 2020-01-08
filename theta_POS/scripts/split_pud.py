#!/usr/bin/env python3

import sys

news = []
wiki = []


def process_pud(file_contents):
	"""Split on the basis of the starting character in the sentence ID"""
	global news
	global wiki
	flag = 0
	for lines in file_contents:
		if lines == "\n":
			if flag == 1:
				news.append(lines)
			if flag == 2:
				wiki.append(lines)
			flag = 0
		elif lines.startswith("# sent_id = n"):
			news.append(lines)
			flag = 1
		elif lines.startswith("# sent_id = w"):
			wiki.append(lines)
			flag = 2
		else:
			if flag == 1:
				news.append(lines)
			if flag == 2:
				wiki.append(lines)


if __name__ == "__main__":
	help_txt = "Arg1: Input file in CONLL-U format\n" \
	           "Usage: python3 {x} Arg1".format(x=sys.argv[0])
	if len(sys.argv) != 2:
		print(help_txt)
		exit(0)
	
	with open(sys.argv[1], "r", encoding="utf-8") as infile:
		contents = infile.readlines()
		process_pud(contents)
	
	with open("news.conllu", "w", encoding="utf-8") as outfile:
		for x in news:
			outfile.write(x)
	
	with open("wiki.conllu", "w", encoding="utf-8") as outfile:
		for x in wiki:
			outfile.write(x)
