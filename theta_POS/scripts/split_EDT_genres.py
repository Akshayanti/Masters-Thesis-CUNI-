#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print("Splits Given EDT conllu file into constituent genres\n"
		  "Usage:\n"
		  "python3 " + sys.argv[0] + " <cs-PDT conllu file>")
	exit(1)

genres = {"grammar": [], "magazine": [], "science": [], "news": [], "thesis": [], "report": [], "geophysics": [], "medical": [], "IT": [], "fiction": [], "other": []}


def get_genre(given_id):
	if given_id.startswith("arbor"):
			return "grammar"
	elif given_id.startswith("aja"):
		if given_id.startswith("aja_luup"):
			return "magazine"
		elif given_id.startswith("aja_horisont"):
			return "science"
		else:
			return "news"
	elif given_id.startswith("tea_dr"):
		return "thesis"
	elif given_id.startswith("tea_toohoive"):
		return "report"
	elif given_id.startswith("tea_geofyysika"):
		return "geophysics"
	elif given_id.startswith("tea_eesti_arst"):
		return "medical"
	elif given_id.startswith("tea_AA"):
		return "IT"
	elif given_id.startswith("ilu_"):
		return "fiction"
	else:
		return "other"


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
