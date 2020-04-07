import sys
import statistics as stats

a = dict()
mode = sys.argv[1]

usage = "Arg1: Mode Value\n" \
        "\tMode\tFile Type\n" \
        "\t1\tTSV File with column1=fieldname, column2=values\n" \
        "\t2\tFile such that fieldname and values are each in new lines. Empty line separates fieldname entries\n" \
        "Arg2: Input file\n" \
        "Usage: python3 {x} Arg1 Arg2".format(x=sys.argv[0])

if len(sys.argv) < 3:
	print(usage, file=sys.stderr)
	exit(0)

if mode == "1":
	# File(s) contain splitnames and values in TSV format
	for givenfile in sys.argv[2:]:
		with open(givenfile, "r", encoding="utf-8") as infile:
			for line in infile:
				split_names, val = line.strip("\n").split("\t")
				if split_names not in a:
					a[split_names] = [float(val)]
				else:
					a[split_names].append(float(val))
elif mode == "2":
	# File(s) contain splitnames and values in successive lines, with empty line as a seperator between entries
	for givenfile in sys.argv[2:]:
		with open(givenfile, "r", encoding="utf-8") as infile:
			split_names = ""
			val = 0
			for line in infile:
				if line != "\n":
					if split_names == "":
						split_names = line.strip("\n")
					else:
						val = line.strip("\n")
				else:
					if split_names not in a:
						a[split_names] = [float(val)]
					else:
						a[split_names].append(float(val))
					split_names = ""
					val = 0
else:
	print(usage, file=sys.stderr)
	exit(1)

for split_name in a:
	sample = a[split_name]
	mean = round(stats.mean(sample), 3)
	sd = round(stats.stdev(sample), 3)
	print(split_name, str(mean) + " " + u"\u00B1" + " " + str(sd), sep="\t")
