#!/usr/bin/sh

getdata:
	pip3 install -r requirements.txt;
	cp $(HOME)/ud-treebanks-v2.4/UD_Arabic-PADT/ar_padt*conllu ./;
	for filename in ar_padt*conllu; do \
		cat $$filename >> ar; \
		yes | rm -f $$filename; \
	done;
	cp $(HOME)/ud-treebanks-v2.4/UD_Afrikaans-AfriBooms/af_afribooms*conllu ./;
	for filename in af_afribooms*conllu; do \
		cat $$filename >> af; \
		yes | rm -f $$filename; \
	done;
	for filename in ar af; do \
		mv $$filename `echo $$filename`.conllu; \
	done;
	cp fixconjhead.py udapi-python/udapi/block/tutorial/;

direction:
	for filename in ar af; do \
		udapy util.Eval node='if node.upos == "CCONJ" and node.deprel == "cc" and node.parent.ord < node.ord and not node.parent.is_root(): print(node)' < `echo $$filename`.conllu > `echo $$filename`.direction; \
	done;

correction:
	for filename in ar af; do \
		udapy -s tutorial.fixconjhead < `echo $$filename`.conllu > `echo $$filename`2.conllu; \
		udapy util.Eval node='if node.upos == "CCONJ" and node.deprel == "cc" and node.parent.ord < node.ord and not node.parent.is_root(): print(node)' < `echo $$filename`2.conllu > `echo $$filename`2.direction; \
	done;
	
clean:
	rm -rf *conllu;
	rm -rf *direction;
