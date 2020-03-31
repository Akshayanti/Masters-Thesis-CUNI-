#!/bin/sh

if ! [ -d $HOME/ud-treebanks-v2.5 ]; then \
	wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3105/ud-treebanks-v2.5.tgz; \
	tar -xvf ud-treebanks-v2.5.tgz; \
	cp -r ud-treebanks-v2.5 $HOME/ud-treebanks-v2.5; \
	rm -rf ud-treebanks-v2.5 ud-treebanks-v2.5.tgz; \
fi;
