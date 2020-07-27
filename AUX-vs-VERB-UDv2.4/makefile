#!/bin/sh

.PHONY: get_data train stats clean

get_data:
	@pip3 install -r requirements.txt;
	@if ! [ -d $(HOME)/ud-treebanks-v2.4 ]; then \
		wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2988/ud-treebanks-v2.4.tgz; \
		tar -xvf ud-treebanks-v2.4.tgz; \
		cp -r ud-treebanks-v2.4 $(HOME)/ud-treebanks-v2.4; \
			rm -rf ud-treebanks-v2.4 ud-treebanks-v2.4.tgz; \
	fi;
	@cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-*.conllu >> hi.conllu;
	@python3 scripts/kfold.py 10 hi.conllu;
	@for i in `seq 1 10`; do \
	  if ! [ -d iter`echo $$i` ]; then \
	    mkdir iter`echo $$i`; \
	    mv train_`echo $$i` iter`echo $$i`/train; \
	    mv test_`echo $$i` iter`echo $$i`/test; \
	  fi; \
	done;
	@if ! [ -d data ]; then \
	  mkdir data; \
	  for filename in dev test train; do \
	    cp $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-`echo $$filename`.conllu data/`echo $$filename`; \
	    @python3 scripts/convert_to_iobes.py data/`echo $$filename`; \
  	done; \
	  for iteration in `seq 1 10`; do \
	    python3 scripts/convert_to_iobes.py iter`echo $$iteration`/test iter`echo $$iteration`/train; \
	  done; \
	fi;
	@rm -f hi.conllu;
	@rm -f test_{1..10};
	@rm -f train_{1..10};


train: get_data
	@echo "Depending on the GPU, each iteration can take upto 8 hours to be trained" > /dev/stderr;
	@for iteration in `seq 1 10`; do \
	  if ! [ -d iter`echo $$iteration`_trained ]; then \
	    python3 scripts/train.py iter`echo $$iteration`; \
	  fi; \
	done;

stats: train
	@rm -f mismatched.tsv matched.tsv *.list;
	@for iteration in `seq 1 10` ; do \
	  python3 scripts/categorise_predictions.py iter`echo $$iteration`/test iter`echo $$iteration`_trained/test.tsv; \
	done;
	@grep -h "S-aux\tS-verb" mismatched.tsv > temp1;
	@grep -h "S-verb\tS-aux" mismatched.tsv > temp2;
	@mv temp1 temp;
	@cat temp2 >> temp;
	@sort -k6 temp > aux-verb.tsv;
	@grep -h "S-aux\tO" mismatched.tsv > temp1;
	@grep -h "O\tS-aux" mismatched.tsv > temp2;
	@mv temp1 temp;
	@cat temp2 >> temp;
	@sort -k6 temp > aux-o.tsv;
	@grep -h "S-verb\tO" mismatched.tsv > temp1;
	@grep -h "O\tS-verb" mismatched.tsv > temp2;
	@mv temp1 temp;
	@cat temp2 >> temp;
	@sort -k6 temp > verb-o.tsv;
	@grep -h "\tS-verb\t" matched.tsv | sort -k5 > verb-tp.tsv;
	@grep -h "\tS-aux\t" matched.tsv | sort -k5 > aux-tp.tsv;
	@grep -h "\tO\t" matched.tsv | sort -k5 > o-tp.tsv;
	@cut -f4,5 matched.tsv > plot_points.tsv;
	@rm -f mismatched.tsv temp matched.tsv;
	@python3 scripts/scout_patterns.py --below --confidence=0.67 --input aux-tp.tsv verb-tp.tsv o-tp.tsv;
	@python3 scripts/scout_patterns.py --above --confidence=0.995 --input aux-verb.tsv verb-o.tsv aux-o.tsv;
	@rm -f temp temp1 temp2;

plot: stats
	@python3 scripts/scout_patterns.py --plot --confidence=0.80 --input plot_points.tsv;
	@echo "The Plot has been generated and saved as docs/Distribution_0.8.png";

clean:
	@rm -f *.tsv *.list;
	@rm -rf iter{1..10};
	@for x in `seq 1 10`; do \
	  rm -rf iter`echo $$x`; \
	  rm -rf iter`echo $$x`_trained; \
	done;
	@rm -rf data data_trained;
