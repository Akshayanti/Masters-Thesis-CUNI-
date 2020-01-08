#!/usr/bin/env python3

import argparse
import os
from copy import deepcopy
from collections import defaultdict
import tqdm

ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC = range(10)
COLNAMES = 'ID,FORM,LEMMA,UPOS,XPOS,FEATS,HEAD,DEPREL,DEPS,MISC'.split(',')


def get_blocks(input_file_read):
	"""Parse each sentence from the input file in form of a block.
	Returns sentenceID, sentenceText, CONLLU-block"""
	id = ""
	text = ""
	block = []
	for lines in input_file_read:
		if lines != "\n":
			if lines.startswith("# sent_id") or lines.startswith("#sent_id"):
				id = lines.split("=")[1].strip()
			elif lines.startswith("# text") or lines.startswith("#text"):
				text = "=".join(lines.split("=")[1:]).strip()
			elif not lines.startswith("#"):
				block.append(lines.strip())
		else:
			yield id, text, block
			id = ""
			text = ""
			block.clear()


def get_directed_edges(block):
	"""Get directed edges from the CONLLU block, by reading HEAD field.
	The directed edges are in a tuple format -> (from_node, to_node)"""
	directed_edges = set()
	from_node = -1
	to_node = -1
	for lines in block:
		COLNAMES = lines.strip().split("\t")
		if "-" not in COLNAMES[ID]:
			try:
				from_node = int(COLNAMES[HEAD])
				to_node = int(COLNAMES[ID])
			except:
				continue
			directed_edges.add((from_node, to_node))
	return directed_edges


def get_trees(block):
	"""
	Get a dict that has parent and children of the nodes in dualdict format
	Get another dict that has parent and descendants of the nodes in dualdict format
	"""
	tree_relationships = defaultdict(dict)
	
	"""Collect each node's parent in the tree"""
	for lines in block:
		parent = -1
		children = set()
		COLNAMES = lines.strip().split("\t")
		try:
			parent = int(COLNAMES[HEAD])
		except:
			continue
		tree_relationships[int(COLNAMES[ID])]["parent"] = parent
		tree_relationships[int(COLNAMES[ID])]["children"] = children
	
	"""For each node, update the set of children"""
	for node in tree_relationships:
		node_parent = tree_relationships[node]["parent"]
		if node_parent != 0 and node not in tree_relationships[node_parent]["children"]:
			tree_relationships[node_parent]["children"].add(node)
	
	"""Mark leaf nodes by changing the attribute children to None"""
	for node in tree_relationships:
		if len(tree_relationships[node]["children"]) == 0:
			tree_relationships[node]["children"] = None
	
	"""Recursively get the nodes included in the subtrees for each node"""
	tree_relationships = get_nodes_in_subtree(tree_relationships)
	recursive_children_dict = dict()
	
	"""Make sure every node has itself listed in it's children, in case not a leaf node"""
	for node in tree_relationships:
		recursive_children_dict[node] = tree_relationships[node]["children"]
		if tree_relationships[node]["children"] is not None:
			recursive_children_dict[node].add(node)
			recursive_children_dict[node] = sorted(recursive_children_dict[node])
	
	return tree_relationships, recursive_children_dict


def get_nodes_in_subtree(old_relationships):
	"""For each node in tree, recursively get list of all the nodes in the subtree headed at the node.
	Called by get_trees() method above"""
	
	new_relationships = deepcopy(old_relationships)
	while True:
		for node in old_relationships:
			node_children = old_relationships[node]["children"]
			if node_children is not None:
				for node_child in node_children:
					node_grandchildren = old_relationships[node_child]["children"]
					if node_grandchildren is not None:
						for node_grandchild in node_grandchildren:
							new_relationships[node]["children"].add(node_grandchild)
		if new_relationships != old_relationships:
			old_relationships = deepcopy(new_relationships)
		else:
			return new_relationships


""" Definition of Projectivity:
i -> j & v \in (i,j) \implies v \in subtree[i]"""


def non_proj_check(recursive_children_dict, edge_set):
	"""Returns two values:
	1. Contains Non-Projective Edge(s): Boolean
	2. Non-Projective Edge(s): Set of tuples"""
	
	out = set()
	for i, j in edge_set:
		flag = 0
		if i > j:
			flag = 1
		
		if flag == 0:
			"""check for forward non-projectivities"""
			for v in range(i, j):
				if i != 0:
					if v not in recursive_children_dict[i]:
						out.add((i, j))
		elif flag == 1:
			"""check for backward non-projectivities"""
			for v in range(j, i):
				if i != 0:
					if v not in recursive_children_dict[i]:
						out.add((i, j))
	
	if len(out) != 0:
		return True, out
	else:
		return False, out


"""Definition of non-planar trees:
there exist edges i1<->j1 and i2<->j2 and one of these can be built over another entirely"""


def get_non_planar(edge_set):
	out = []
	for i1, j1 in edge_set:
		
		if i1 > j1:
			i1, j1 = j1, i1
		
		for v in range(i1 + 1, j1):
			for i2, j2 in edge_set:
				if i2 == v:
					if j2 > j1 or j2 < i1:
						if {(i1, j1), (i2, j2)} not in out:
							out.append({(i1, j1), (i2, j2)})
				
				elif j2 == v:
					if i2 < i1 or i2 > j1:
						if {(i1, j1), (i2, j2)} not in out:
							out.append({(i1, j1), (i2, j2)})
	
	if len(out) != 0:
		return True, out
	else:
		return False, out


"""Condition for Ill-nestedness:
i1 <-> j1, i2 <-> j2 | i1 \in Gap(i2, j2) AND i2 \in Gap(i1, j1)"""


def get_ill_nested(edges, subtree):
	out = []
	for i1, j1 in edges:
		for i2, j2 in edges:
			
			val1 = False
			val2 = False
			
			if {i1, j1} != {i2, j2} and ((i1 != i2) and (i1 != j2) and (j1 != i2) and (j1 != j2)):
				
				# Condition1: i1 \in Gap(i2, j2)
				if (i1 in range(i2 + 1, j2) or i1 in range(j2 + 1, i2)) and i1 not in subtree[i2]:
					val1 = True
				# Condition2: i2 \in Gap(i1, j1)
				if (i2 in range(i1 + 1, j1) or i2 in range(j1 + 1, i1)) and i2 not in subtree[i1]:
					val2 = True
				
				if val1 and val2:
					pass
				else:
					val1 = False
					val2 = False
					
					# Condition1 defined for non-directed edges between nodes
					if (j1 in range(i2 + 1, j2) or j1 in range(j2 + 1, i2)) and j1 not in subtree[i2]:
						val1 = True  # {(i1, j1), (i2, j2)}
					# Condition2 also defined for non-directed edges between nodes
					if (j2 in range(i1 + 1, j1) or j2 in range(j1 + 1, i1)) and j2 not in subtree[i1]:
						val2 = True
			
			# Condition1 AND Condition2 both hold
			if val1 and val2:
				if {(i1, j1), (i2, j2)} not in out:
					out.append({(i1, j1), (i2, j2)})
	
	if len(out) != 0:
		return True, out
	else:
		return False, out


# Checks the different relaxations of non-projectivities.
# calls get_ill_nested() and get_non_planar()
def check_relaxations():
	global non_planar_trees
	global ill_nested_trees
	global i
	global id
	global output2
	global recursive_children
	global non_proj
	global yes_POS
	
	if args.non_planar:
		isNonPlanar, non_planar = get_non_planar(non_proj)
		if isNonPlanar:
			non_planar_trees += 1
			for k in non_planar:
				string = ""
				for edge1 in k:
					if string != "":
						string += "\t" + str(edge1)
					else:
						string = str(edge1)
				output2.append(i.split("/")[-1] + "\t" + id + "\t" + string + "\n")
	
	elif args.ill_nested:
		isIllNested, ill_nested = get_ill_nested(non_proj, recursive_children)
		if isIllNested:
			ill_nested_trees += 1
			for k in ill_nested:
				string = ""
				for edge1 in k:
					if string != "":
						string += "\t" + str(edge1)
					else:
						string = str(edge1)
				output2.append(i.split("/")[-1] + "\t" + id + "\t" + string + "\n")
	return output2


def get_edge_degree(recursive_children_dict, given_edges):
	"""Edge Degree = Number of nodes that are in the gap."""
	
	max_degree = 0
	
	for i, j in given_edges:
		
		degree = 0
		flag = 0
		
		if i > j:
			flag = 1
		
		if flag == 0:
			"""Forward non-projectivities"""
			for v in range(i, j):
				if i != 0:
					if v not in recursive_children_dict[i]:
						degree += 1
		elif flag == 1:
			"""Backward non-projectivities"""
			for v in range(j, i):
				if i != 0:
					if v not in recursive_children_dict[i]:
						degree += 1
		
		"""Select the maximal value, and return it"""
		max_degree = max(degree, max_degree)
	return max_degree


"""Definition of gap_degree:
No of times a non-projective edge's gap is broken + 1
Eg- if in (15, 23) nodes 18, 20 are in subtree of 15, but the rest are not.
thus, the gap is broken twice, once at 18, and once at 20. So, gd = 2+1 = 3"""


def get_gap_degree(relationships_dict, recursive_children_dict):
	gap_deg = 0
	
	for node in recursive_children_dict:
		gap_count = 0
		add_gap_flag = True

		if recursive_children_dict[node] is not None:

			# start from the first member of the recursive_subtrees, and end at the last element
			for check_node in range(recursive_children_dict[node][0], recursive_children_dict[node][-1]):  # we can always be sure that i, j will be in get_nodes_in_subtree for sure
				
				if check_node not in recursive_children_dict[node]:
					
					if relationships_dict[node]["parent"] == check_node:
						"""Case 1: it can be a parent, and so check from relationships"""
						pass
					else:
						"""Case 2: not a parent. Check if gap needs to be added"""
						if not add_gap_flag:
							pass
						else:
							gap_count += 1
							add_gap_flag = False

				else:
					"""check_node present in the subtree. Update the flag"""
					add_gap_flag = True

		"""After every iteration, make sure the maximal of the computed and stored value is the returnable gap-degree"""
		gap_deg = max(gap_count, gap_deg)

	return gap_deg


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	group0 = parser.add_mutually_exclusive_group(required=True)
	group0.add_argument("-i", "--input", nargs="+", help="Input files to read data from, in CONLL-U format. Multiple values possible.")
	group0.add_argument("-id", "--input_directory", type=str, help="Parent directory to read Conll-U files from. Reads .conllu files recursively.")
	group2 = parser.add_mutually_exclusive_group(required=False)
	group2.add_argument("--non_planar", action="store_true", help="Display the filename,SentID and edges which contribute to NON-PLANAR STRUCTURES in a non-projective tree")
	group2.add_argument("--ill_nested", action="store_true", help="Display the filename,SentID and edges which contribute to ILL-NESTED STRUCTURES in a non-projective tree")
	parser.add_argument("--gap_degree", action="store_true", help="Get the GAP_DEGREES for the trees")
	parser.add_argument("--edge_degree", action="store_true", help="Get the EDGE_DEGREES for the trees")
	parser.add_argument("--output", action="store_true", help="Write outputs in a file")
	args = parser.parse_args()
	
	# Display print formats
	if not (args.non_planar or args.ill_nested):
		print("--all\tfile_name\tnp_edges\tedges\tnp_trees\ttrees")
	else:
		if args.non_planar:
			print("--non_planar\tfile_name\tnon-planar_trees\ttrees")
		elif args.ill_nested:
			print("--ill_nested\tfile_name\till_trees\ttrees")
	
	trees_dict = defaultdict(int)  # (key, value) = (filename, total_trees)
	edge_degree_outputs = defaultdict(dict)  # (key, value) = (file_name, edge_degree)
	gap_degree_outputs = defaultdict(dict)  # (key, value) = (file_name, gap_degree)
	output_gap = []  # store ids of sentences with abnormal gap degrees
	
	# Define the input files
	input_files = []
	if args.input:
		for i in args.input:
			input_files.append(i)
	elif args.input_directory:
		for root, dirs, files in os.walk(args.input_directory):
			for filename in files:
				if filename.endswith(".conllu"):
					input_files.append(os.path.join(root, filename))
	
	# Start processing input files
	for i in tqdm.tqdm(input_files):
		with open(i, "r", encoding="utf-8") as infile:
			
			# Counters
			total_edges = 0  # Total edges in all trees
			non_proj_edges = 0  # Count of non-projective edges
			POS_proj_edges = 0  # Count of edges non-projective because of a PUNCT attachment
			total_trees = 0  # Total number of trees (1 per sentence)
			non_planar_trees = 0  # Count of non-planar trees
			non_proj_trees = 0  # Count of non-projective trees
			pos_non_proj_trees = 0  # Count of trees non-projective because of a PUNCT attachment
			ill_nested_trees = 0  # Count of ill-nested trees
			
			# Placeholder variables
			non_proj = set()  # set of non-projective edges, directed
			yes_POS = set()  # set of edges non-projective because of a PUNCT attachment
			edge_degree = defaultdict(int)  # (key, value) = (edge_degree, number_of_trees_with_edge_degree)
			gap_degree = defaultdict(int)  # (key, value) = (edge_degree, number_of_trees_with_gap_degree)
			output = []
			output2 = []
			
			contents = infile.readlines()
			for id, text, block in get_blocks(contents):
				
				total_trees += 1
				edges = get_directed_edges(block)
				p_and_c, recursive_children = get_trees(block)
				_, non_proj = non_proj_check(recursive_children, edges)
				
				# Update counters for total edges, and recursive_children non-projective edges
				total_edges += len(edges)
				non_proj_edges += len(non_proj)
				if _:
					non_proj_trees += 1
					for k in non_proj:
						output.append(i.split("/")[-1] + "\t" + id + "\t" + str(k) + "\n")
					output2 = check_relaxations()
			
				# Get edge-degrees for all edges, projective or non-projective
				if args.edge_degree:
					given_edge_degree = get_edge_degree(recursive_children, edges)
					edge_degree[given_edge_degree] += 1
				
				# Get gap-degrees for all trees
				if args.gap_degree:
					given_gap_degree = get_gap_degree(p_and_c, recursive_children)
					gap_degree[given_gap_degree] += 1
					if given_gap_degree > 1:
						output_gap.append(i.split("/")[-1] + "\t" + id + "\t" + str(given_gap_degree) + "\n")
			
			# Finished processing the contents of the file
			
			# update the total number of trees dict for each file
			trees_dict[i.split("/")[-1]] = total_trees
			
			# Update edge_degree_outputs
			if args.edge_degree:
				edge_degree_outputs[i.split("/")[-1]] = edge_degree
			
			if args.gap_degree:
				gap_degree_outputs[i.split("/")[-1]] = gap_degree
			
			# Outputs section
			mainfile = ""
			relaxed = ""
			
			mainfile = "non_proj_edges.tsv"
			if not (args.non_planar or args.ill_nested):
				print("--all", i.split("/")[-1], str(non_proj_edges), str(total_edges), str(non_proj_trees), str(total_trees), sep="\t")
			
			if args.non_planar:
				relaxed = "non_planar_edges.tsv"
				print("--non_planar", i.split("/")[-1], str(non_planar_trees), str(total_trees), sep="\t")
			
			elif args.ill_nested:
				relaxed = "ill_nested_edges.tsv"
				print("--ill_nested", i.split("/")[-1], str(ill_nested_trees), str(total_trees), sep="\t")
			
			if args.output:
				if not (args.non_planar or args.ill_nested):
					with open(mainfile, "a+", encoding="utf-8") as outfile:
						for k in output:
							outfile.write(k)
				if args.non_planar or args.ill_nested:
					with open(relaxed, "a+", encoding="utf-8") as outfile:
						for k in output2:
							outfile.write(k)
					output2.clear()
			output.clear()
	
	# Finished processing all the input files
	
	# Write the outputs of edge_degree in a file with format in the header
	if args.edge_degree:
		with open("edge_degrees.stats", "w", encoding="utf-8") as outfile:
			
			# write header
			outfile.write("filename\tmax_edge_degree\ttotal_trees\tedge_degrees\n")
			
			# print values
			for k in edge_degree_outputs:
				# for each item, make sure the value is sorted by the key
				# and all the (key, value) pairs are output in form of tuples
				edge_degrees = edge_degree_outputs[k]
				out = set()
				for degree in edge_degrees:
					out.add((degree, edge_degrees[degree]))
				out = sorted(out)
				outfile.write(k + "\t" + str(out[-1][0]) + "\t" + str(trees_dict[k]) + "\t" + str(sorted(out)) + "\n")
	
	# Write the outputs of gap_degree in a file with format in the header
	if args.gap_degree:
		
		# write all the cases where the gap_degree is greater than 1 and most probably erroneous
		with open("gap_degrees.tsv", "w", encoding="utf-8") as outfile:
			for v in output_gap:
				outfile.write(v)
		
		# print values
		with open("gap_degrees.stats", "w", encoding="utf-8") as outfile:
			outfile.write("filename\tmax_gap_degree\ttotal_trees\tgap_degrees\n")
			
			for k in gap_degree_outputs:
				# for each item, make sure the value is sorted by the key
				# and all the (key, value) pairs are output in form of tuples
				gap_degrees = gap_degree_outputs[k]
				out = set()
				for gap in gap_degrees:
					out.add((gap, gap_degrees[gap]))
				out = sorted(out)
				outfile.write(k + "\t" + str(out[-1][0]) + "\t" + str(trees_dict[k]) + "\t" + str(sorted(out)) + "\n")
