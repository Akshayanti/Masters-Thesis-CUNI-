#!/usr/bin/env python3

import sys


def get_stats(filehandle):
	with open(filehandle, "r", encoding="utf-8") as readme:
		activate = False
		for lines in readme:
			if not activate:
				if "Machine-readable metadata" in lines or "Machine readable metadata" in lines:
					activate = True
				continue
			else:
				if lines.startswith("Genre") or lines.startswith("genre"):
					genres_list = lines.strip("\n").split("enre: ")[1].split()
					return genres_list


if __name__ == "__main__":
	for filename in sys.argv[1:]:
		genres = get_stats(filename)
		try:
			for x in genres:
				print(x)
		except TypeError:
			print(filename, file=sys.stderr)
