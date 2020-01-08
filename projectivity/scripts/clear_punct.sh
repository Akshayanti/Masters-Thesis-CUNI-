#!/usr/bin/env bash

for filename in $HOME/ud-treebanks-v2.5/*/*.conllu; do
	WC1=$(wc -l ${filename} | grep -oE -m1 "[0-9][0-9]+")
	udapy -s ud.FixPunct < "$filename" > "$HOME/ud_cleaned/$(basename "$filename" .conllu)$i.conllu"
	WC2=$(wc -l "$HOME/ud_cleaned/$(basename ${filename} .conllu)$i.conllu" | grep -Eo "[0-9]+")
	WC1=$(($WC1+0))
	WC2=$(($WC2+0))
	if (($WC2 != $WC1)); then
		 cp "$filename" "$HOME/ud_cleaned/$(basename "$filename" .conllu)$i.conllu"
	fi
done
