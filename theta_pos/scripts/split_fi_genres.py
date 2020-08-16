#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print("Splits Given fi-tdt conllu file into constituent genres\n"
		  "Usage:\n"
		  "python3 " + sys.argv[0] + " <pl-lfg conllu file>")
	exit(1)

genres = {"grammar": [], "wiki": [], "wiki_news": [], "uni_news": [], "blog": [], "uni_art": [], "europarl": [], "legal": [], "fin_news": [], "fiction": []}


def get_genre(given_id):
	if given_id.startswith("h"):
		return "grammar"
	elif given_id.startswith("wn"):
		return "wiki_news"
	elif given_id.startswith("w"):
		return "wiki"
	elif given_id.startswith("u"):
		return "uni_news"
	elif given_id.startswith("b"):
		return "blog"
	elif given_id.startswith("s"):
		return "uni_art"
	elif given_id.startswith("e"):
		return "europarl"
	elif given_id.startswith("j"):
		return "legal"
	elif given_id.startswith("f"):
		return "fiction"
	elif given_id.startswith("t"):
		return "fin_news"


def process_data(file_contents):
	"""Processes contents of the file, and returns a dict such that the keys are different genres present"""
	sent_id = "blah"
	current_genre = "blah"
	genredata = []
	for lines in file_contents:
		if lines != "\n":
			if lines.startswith("# sent_id"):
				sent_id = lines.strip("\n").split(" = ")[1]
				genredata.append(lines)
				current_genre = get_genre(sent_id)
			elif lines.startswith("# text"):
				genredata.append(lines)
			else:
				if current_genre != "blah" and sent_id != "blah":
					genredata.append(lines)
		else:
			genredata.append("\n")
			genres[current_genre] += [x for x in genredata]
			genredata.clear()
			current_genre = "blah"
			sent_id = "blah"


with open(sys.argv[1], "r", encoding="utf-8") as infile:
	contents = infile.readlines()
	process_data(contents)
	for genre in genres:
		with open(genre + ".conllu", "w", encoding="utf-8") as outfile:
			for x in genres[genre]:
				outfile.write(x)
