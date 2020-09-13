#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print("Splits Given pl-lfg conllu file into constituent genres\n"
	      "Usage:\n"
	      "python3 " + sys.argv[0] + " <pl-lfg conllu file>")
	exit(1)


def process_data(file_contents):
	"""Processes contents of the file, and returns a dict such that the keys are different genres present"""
	a = dict()
	sent_id = "blah"
	current_genre = "blah"
	genredata = []
	for lines in file_contents:
		if lines != "\n":
			if lines.startswith("# sent_id"):
				sent_id = lines.strip("\n").split(" = ")[1]
				genredata.append(lines)
			elif lines.startswith("# text"):
				genredata.append(lines)
			elif lines.startswith("# genre = "):
				current_genre = lines.strip("\n").split(" = ")[1].strip(")")
				if "(" in current_genre:
					current_genre = current_genre.split(" (")
					current_genre = "_".join(current_genre)
			else:
				if current_genre != "blah" and sent_id != "blah":
					genredata.append(lines)
		else:
			genredata.append("\n")
			if current_genre in a:
				a[current_genre] += [x for x in genredata]
			else:
				a[current_genre] = [x for x in genredata]
			genredata.clear()
			current_genre = "blah"
			sent_id = "blah"
	return a


with open(sys.argv[1], "r", encoding="utf-8") as infile:
	contents = infile.readlines()
	genre_split = process_data(contents)
	for genre in genre_split:
		with open(genre + ".conllu", "w", encoding="utf-8") as outfile:
			for x in genre_split[genre]:
				outfile.write(x)
