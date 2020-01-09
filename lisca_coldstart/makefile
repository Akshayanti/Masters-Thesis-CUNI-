SHELL=/bin/bash

getdata:
	# Get Cross Validation Data first
	if ! [ -d CV ]; then \
		mkdir CV; \
	fi;
	if ! [ -f CV/hi.conllu ]; then \
		cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-train.conllu > CV/hi.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-dev.conllu >> CV/hi.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-test.conllu >> CV/hi.conllu;	\
	fi;
	python3 scripts/downsample.py --input CV/hi.conllu --number 16000;
	mv CV/hi.conllu_16000 CV/hi_16000.conllu;
	# K-fold with k=2
	python3 scripts/kfold.py 2 CV/hi_16000.conllu;
	if ! [ -d CV/k2 ]; then \
		mkdir CV/k2; \
	fi;
	for filename in train*; do \
		yes | mv $$filename CV/k2/`echo $$filename`.conllu; \
	done;
	for filename in test*; do \
		yes | mv $$filename CV/k2/`echo $$filename`.conllu; \
	done;
	# K-fold with k=4
	python3 scripts/kfold.py 4 CV/hi_16000.conllu;
	if ! [ -d CV/k4 ]; then \
		mkdir CV/k4; \
	fi;
	for filename in train*; do \
		yes | mv $$filename CV/k4/`echo $$filename`.conllu; \
	done;
	for filename in test*; do \
		yes | mv $$filename CV/k4/`echo $$filename`.conllu; \
	done;
	# K-fold with k=8
	python3 scripts/kfold.py 8 CV/hi_16000.conllu;
	if ! [ -d CV/k8 ]; then \
		mkdir CV/k8; \
	fi;
	for filename in train*; do \
		yes | mv $$filename CV/k8/`echo $$filename`.conllu; \
	done;
	for filename in test*; do \
		yes | mv $$filename CV/k8/`echo $$filename`.conllu; \
	done;
	# Remove extra files
	yes | rm CV/hi_16000.conllu;

cross:
	# Unzip data related to CV, CONLL files, and .lisca files
	tar -xf CV_conll.tar;
	tar -xf CV_lisca.tar;
	yes | rm CV/*/*.liscaextra;
	for trainfiles in CV/{k2,k4,k8}/train*.{conll,conllu}; do \
		rm -f $$trainfiles; \
	done;
	# Process the individual lisca file, and get values
	for id in {1..2}; do \
		python3 scripts/compact_lisca_results.py --conll CV/k2/test_`echo $$id`.conll --conllu CV/k2/test_`echo $$id`.conllu --lisca CV/k2/train_`echo $$id`.lisca; \
	done;
	for id in {1..4}; do \
		python3 scripts/compact_lisca_results.py --conll CV/k4/test_`echo $$id`.conll --conllu CV/k4/test_`echo $$id`.conllu --lisca CV/k4/train_`echo $$id`.lisca; \
	done;
	for id in {1..8}; do \
		python3 scripts/compact_lisca_results.py --conll CV/k8/test_`echo $$id`.conll --conllu CV/k8/test_`echo $$id`.conllu --lisca CV/k8/train_`echo $$id`.lisca; \
	done;
	for id in {2,4,8}; do \
		yes | rm CV/k`echo $$id`/*.{conll,conllu,lisca}; \
		if [ -f CV/k`echo $$id`.tsv ]; then \
			yes | rm CV/k`echo $$id`.tsv; \
		fi; \
		grep -Ph "\t0.0" CV/k`echo $$id`/train*.tsv >> CV/k`echo $$id`/train.tsv; \
		sort CV/k`echo $$id`/train.tsv >> CV/k`echo $$id`.tsv; \
		yes | rm -r CV/k`echo $$id`; \
	done;
	comm -12 CV/k2.tsv CV/k8.tsv > CV/k_all.tsv;
	comm -3 CV/k2.tsv CV/k4.tsv > CV/k_2-4.tsv;
	comm -3 CV/k4.tsv CV/k8.tsv > CV/k_4-8.tsv;
	sort -R --random-source=/dev/zero CV/k_all.tsv | head -n200 > CV/k_all_200.tsv1;
	sort -R --random-source=/dev/zero CV/k_2-4.tsv | head -n100 > CV/k_2not4_100.tsv1;
	sort -R --random-source=/dev/zero CV/k_4-8.tsv | head -n100 > CV/k_4not8_100.tsv1;
	rm -f CV/k*.tsv;
