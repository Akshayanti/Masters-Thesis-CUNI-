SHELL := /bin/bash

get_data:
	pip3 install -r requirements.txt;
	# Split into k-fold splits
	cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-*.conllu >> hi.conllu;
	python3 scripts/kfold.py 10 hi.conllu;
	for i in 1 2 3 4 5 6 7 8 9 10; do mkdir iter`echo $$i`; mv train_`echo $$i` iter`echo $$i`/train; mv test_`echo $$i` iter`echo $$i`/test; done;
	# Convert into IOBES format
	mkdir data;
	for filename in dev test train; do cp $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-`echo $$filename`.conllu data/`echo $$filename`; done;;
	python3 scripts/convert_to_iobes.py data/train data/test data/dev;
	for iteration in iter1 iter2 iter3 iter4 iter5 iter6 iter7 iter8 iter9 iter10; do python3 scripts/convert_to_iobes.py $$iteration/test $$iteration/train; done;

train:
	echo "Depending on the GPU, each iteration can take upto 8 hours to be trained" > /dev/stderr;
	for iteration in iter1 iter2 iter3 iter4 iter5 iter6 iter7 iter8 iter9 iter10; do python3 scripts/train.py $$iteration; done;

stats:
	rm -f mismatched.tsv matched.tsv *.list;
	for iteration in iter1 iter2 iter3 iter4 iter5 iter6 iter7 iter8 iter9 iter10; do python3 scripts/categorise_predictions.py $$iteration/test `echo $$iteration`_trained/test.tsv; done;
	grep -P "S-aux\tS-verb" mismatched.tsv > temp;
	grep -P "S-verb\tS-aux" mismatched.tsv >> temp;
	sort -k6 temp > aux-verb.tsv;
	grep -P "S-aux\tO" mismatched.tsv > temp;
	grep -P "O\tS-aux" mismatched.tsv >> temp;
	sort -k6 temp > aux-o.tsv;
	grep -P "S-verb\tO" mismatched.tsv > temp;
	grep -P "O\tS-verb" mismatched.tsv >> temp;
	sort -k6 temp > verb-o.tsv;
	grep -P "\tS-verb\t" matched.tsv | sort -k5 > verb-tp.tsv;
	grep -P "\tS-aux\t" matched.tsv | sort -k5 > aux-tp.tsv;
	grep -P "\tO\t" matched.tsv | sort -k5 > o-tp.tsv;
	cut -f4,5 matched.tsv > plot_points.tsv;
	rm -f mismatched.tsv temp matched.tsv;
	python3 scripts/scout_patterns.py --below --confidence=0.67 --input aux-tp.tsv verb-tp.tsv o-tp.tsv;
	python3 scripts/scout_patterns.py --above --confidence=0.995 --input aux-verb.tsv verb-o.tsv aux-o.tsv;

plot:
	python3 scripts/scout_patterns.py --plot --confidence=0.80 --input plot_points.tsv;

clean:
	rm -f *.tsv;
	rm -f *.list;
	rm -f hi.conllu;
