#!/bin/sh

projectivities:
	python3 find_non_projectivities.py -id $(HOME)/ud-treebanks-v2.5 --edge_degree --gap_degree --output > all.stats & \
	python3 find_non_projectivities.py -id $(HOME)/ud-treebanks-v2.5 --non_planar --output > all_non_planar.stats & \
	python3 find_non_projectivities.py -id $(HOME)/ud-treebanks-v2.5 --ill_nested --output > all_ill_nested.stats;
	python3 manage_stats.py -id ./;
	rm -f *.stats;
	rm -f *.tsv;

punct_fix:
	chmod +x clear_punct.sh
	if [ ! -d "$(HOME)/ud_cleaned" ]; then \
		mkdir $(HOME)/ud_cleaned; \
	fi;
	./clear_punct.sh

after_fix:
	if [ ! -d "after_correction" ]; then \
		mkdir after_correction; \
	fi;
	cd after_correction; \
		cp ../find_non_projectivities.py ./find_non_projectivities.py; \
		python3 find_non_projectivities.py -id $(HOME)/ud_cleaned --edge_degree --gap_degree --output > all.stats; \
		python3 find_non_projectivities.py -id $(HOME)/ud_cleaned --non_planar --output > all_non_planar.stats; \
		python3 find_non_projectivities.py -id $(HOME)/ud_cleaned --ill_nested --output > all_ill_nested.stats; \
		rm -f ./find_non_projectivities.py; \
		python3 ../scripts/manage_stats.py -id ./; \
		rm -f *.stats; \
		cat non_proj_edges.tsv | uniq > all_non_proj_edges.tsv; \
		rm -f non_proj_edges.tsv;

possible_nonproj:
	for filename in $(HOME)/ud_cleaned_working/*.conllu; do \
		echo $$filename >> temp; \
		udapy tutorial.findnuclei < $$filename >> temp; \
	done;
	python3 scripts/clear_vn.py -i temp -o tail.tsv;
	rm -f temp;
	if [ -f tail.tsv ]; then \
		python3 scripts/nonproj_possibilities.py -pf tail.tsv -id $(HOME)/ud_cleaned_working -sd $(HOME)/ud_cleaned_support > dependent_intact.tsv; \
		python3 scripts/split_by_instances.py dependent_intact.tsv; \
	fi;
