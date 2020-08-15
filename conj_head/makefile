#!/usr/bin/sh

get_data:
	pip3 install -r requirements.txt;
	@if ! [ -d $(HOME)/ud-treebanks-v2.4 ]; then \
		wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2988/ud-treebanks-v2.4.tgz; \
		tar -xvf ud-treebanks-v2.4.tgz; \
		cp -r ud-treebanks-v2.4 $(HOME)/ud-treebanks-v2.4; \
		rm -rf ud-treebanks-v2.4 ud-treebanks-v2.4.tgz; \
	fi;
	@cp $(HOME)/ud-treebanks-v2.4/UD_Arabic-PADT/ar_padt*conllu ./;
	@for filename in ar_padt*conllu; do \
		cat $$filename >> ar; \
		yes | rm -f $$filename; \
	done;
	@cp $(HOME)/ud-treebanks-v2.4/UD_Afrikaans-AfriBooms/af_afribooms*conllu ./;
	@for filename in af_afribooms*conllu; do \
		cat $$filename >> af; \
		yes | rm -f $$filename; \
	done;
	@for filename in ar af; do \
		mv $$filename `echo $$filename`.conllu; \
	done;

stats:
	@if ! [ -d $(HOME)/ud-treebanks-v2.4 ]; then \
		wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2988/ud-treebanks-v2.4.tgz; \
		tar -xvf ud-treebanks-v2.4.tgz; \
		cp -r ud-treebanks-v2.4 $(HOME)/ud-treebanks-v2.4; \
		rm -rf ud-treebanks-v2.4 ud-treebanks-v2.4.tgz; \
	fi;
	@rm -f *.stats;
	@for treebank in $(HOME)/ud-treebanks-v2.4/UD_*; do \
		rm -f dummy*; \
		echo $$treebank >> all_misdirected.stats; \
		echo $$treebank >> all_misdirected_nonproj.stats; \
		for filename in $$treebank/*-ud-*.conllu; do \
			udapy util.Eval node='if node.upos == "CCONJ" and node.udeprel == "cc" and node.parent.ord < node.ord : print(node)' < `echo $$filename` >> dummy_misdirected; \
			udapy util.Eval node='if node.upos == "CCONJ" and node.udeprel == "cc" and node.parent.ord < node.ord and node.is_nonprojective(): print(node)' < `echo $$filename` >> dummy_misdirected_nonproj; \
		done; \
		wc -l dummy_misdirected >> all_misdirected.stats; \
		wc -l dummy_misdirected_nonproj >> all_misdirected_nonproj.stats; \
		echo >> all_misdirected.stats; \
		echo >> all_misdirected_nonproj.stats; \
	done;
	@rm -f dummy*;

correction:
	@make get_data;
	@cp scripts/fixconjhead.py $(HOME)/udapi-python/udapi/block/tutorial/;
	@for filename in ar af; do \
		udapy util.Eval node='if node.upos == "CCONJ" and node.udeprel == "cc" and node.parent.ord < node.ord: print(node)' < `echo $$filename`.conllu > `echo $$filename`.all_misdirected; \
		udapy util.Eval node='if node.upos == "CCONJ" and node.udeprel == "cc" and node.parent.ord < node.ord and node.is_nonprojective(): print(node)' < `echo $$filename`.conllu > `echo $$filename`.nonproj_misdirected; \
		udapy -s tutorial.fixconjhead < `echo $$filename`.conllu > `echo $$filename`_corrected.conllu; \
		udapy util.Eval node='if node.upos == "CCONJ" and node.udeprel == "cc" and node.parent.ord < node.ord: print(node)' < `echo $$filename`_corrected.conllu > `echo $$filename`.all_misdirected_unfixed; \
		udapy util.Eval node='if node.upos == "CCONJ" and node.udeprel == "cc" and node.parent.ord < node.ord and node.is_nonprojective(): print(node)' < `echo $$filename`_corrected.conllu > `echo $$filename`.nonproj_misdirected_unfixed; \
		wc -l `echo $$filename`.all_misdirected*; \
		wc -l `echo $$filename`.nonproj_misdirected*; \
	done;
	
clean:
	@rm -rf *conllu;
	@rm -rf *misdirected*;
