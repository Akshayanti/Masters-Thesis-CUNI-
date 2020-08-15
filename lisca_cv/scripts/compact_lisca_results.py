#!/usr/bin/env python3


def process_conll(conll_file):
	"""Generate a dict such that the order of sentence is the key, and the word lines therein form the value"""
	outdict = dict()
	with open(conll_file, "r", encoding="utf-8") as infile:
		i = 1   # Conll numbering starts at 1
		block = []
		for line in infile:
			if line == "\n":
				outdict[i] = block
				i += 1
				block = []
			else:
				block.append(line)
	return outdict


def process_conllu(conllu_file):
	"""Generate a dict such that sentenceID is the key, and the word lines therein form the value"""
	outdict = dict()
	with open(conllu_file, "r", encoding="utf-8") as infile:
		block = []
		sent_id = ""
		for line in infile:
			if line == "\n":
				outdict[sent_id] = block
				sent_id = ""
				block = []
			elif line.startswith("#"):
				if line.startswith("# sent_id"):
					sent_id = line.rstrip().split(" = ")[1]
			else:
				block.append(line)
	return outdict


def conllu_conllu_map(conllu_dict):
	conllu_map = dict()
	i = 1
	for sent_id in conllu_dict:
		conllu_map[i] = sent_id
		i += 1
	return conllu_map


def conll_conllu_map(conll_dict, conllu_dict):
	"""Using the two dicts generated above, create another dict that maps Sentence Order in CONLL to Sentence ID in CONLLU"""
	map = dict()
	for x in conll_dict:
		for sent_id in conllu_dict:
			if conll_dict[x] == conllu_dict[sent_id]:
				map[x] = sent_id
				break
	return map


def modify_lisca(lisca_file, mapping):
	"""Create tuples from lisca_file. Tuple format- sent_id(from conllu file), token_id, lisca_score"""
	output_tuples = []
	with open(lisca_file, "r", encoding="utf-8") as infile:
		for line in infile:
			conll_ID, token_ID, line_number, ID, FORM, LEMMA, UPOS, XPOS, FEATs, HEAD, DEPREL, score = line.rstrip().split()
			tuple1 = (mapping[int(conll_ID)], token_ID, score)
			output_tuples.append(tuple1)
	return output_tuples


def write_lisca_compact(lisca_scores, output_file):
	"""Write tuples into a TSV format. Outputs data into .tsv file"""
	with open(output_file, "w", encoding="utf-8") as outfile:
		for sent_id, token_id, score in lisca_scores:
			outfile.write("{x}\t{y}\t{z}\n".format(x=sent_id, y=token_id, z=score))
			

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--conll", type=str, help="Input Test file, in CONLL format")
	parser.add_argument("--conllu", type=str, help="Input Test file, in CONLL-U format", required=True)
	parser.add_argument("--lisca", type=str, help="Lisca generated file, .lisca extension", required=True)
	args = parser.parse_args()
	
	maps = None
	if args.conll:
		conll_IDs = process_conll(args.conll)
		conllu_IDs = process_conllu(args.conllu)
		maps = conll_conllu_map(conll_IDs, conllu_IDs)
	else:
		conllu_IDs = process_conllu(args.conllu)
		maps = conllu_conllu_map(conllu_IDs)
		
	lisca_compact_scores = modify_lisca(args.lisca, maps)
	output_file = args.lisca.strip("lisca")+"tsv"
	write_lisca_compact(lisca_compact_scores, output_file)
