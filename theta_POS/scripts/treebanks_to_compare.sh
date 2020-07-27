#!/usr/bin/env bash

prefix="$HOME/ud-treebanks-v2.5/"
for languages in UD_Arabic UD_Czech UD_German UD_English UD_Spanish; do
	for treebank in `echo $prefix``echo $languages`-*; do
		if ! [[ ${treebank:${#treebank}-3} == "PUD" ]]; then
			if ! [[ ${treebank:${#treebank}-7} == "GSDSimp" ]]; then
				python3 scripts/compare_treebank_bool.py `echo $treebank`/stats.xml >> treebanks_to_compare;
			fi;
		fi;
	done;
	echo "" >> treebanks_to_compare;
done;

for languages in UD_Estonian UD_Finnish UD_French UD_Galician UD_Ancient_Greek; do
	for treebank in `echo $prefix``echo $languages`-*; do
		if ! [[ ${treebank:${#treebank}-3} == "PUD" ]]; then
			if ! [[ ${treebank:${#treebank}-7} == "GSDSimp" ]]; then
				python3 scripts/compare_treebank_bool.py `echo $treebank`/stats.xml >> treebanks_to_compare;
			fi;
		fi;
	done;
  echo "" >> treebanks_to_compare;
done;

for languages in UD_Mbya_Guarani UD_Italian UD_Japanese UD_Korean UD_Komi_Zyrian UD_Latin UD_Lithuanian; do
	for treebank in `echo $prefix``echo $languages`-*; do
		if ! [[ ${treebank:${#treebank}-3} == "PUD" ]]; then
			if ! [[ ${treebank:${#treebank}-7} == "GSDSimp" ]]; then
				python3 scripts/compare_treebank_bool.py `echo $treebank`/stats.xml >> treebanks_to_compare;
			fi;
		fi;
	done;
  echo "" >> treebanks_to_compare;
done;

for languages in UD_Dutch UD_Norwegian UD_Old_Russian UD_Polish UD_Portuguese; do
	for treebank in `echo $prefix``echo $languages`-*; do
		if ! [[ ${treebank:${#treebank}-3} == "PUD" ]]; then
			if ! [[ ${treebank:${#treebank}-7} == "GSDSimp" ]]; then
				python3 scripts/compare_treebank_bool.py `echo $treebank`/stats.xml >> treebanks_to_compare;
			fi;
		fi;
	done;
	echo "" >> treebanks_to_compare;
done;

for languages in UD_Romanian UD_Russian UD_Slovenian UD_Swedish UD_Turkish UD_Chinese; do
	for treebank in `echo $prefix``echo $languages`-*; do
		if ! [[ ${treebank:${#treebank}-3} == "PUD" ]]; then
			if ! [[ ${treebank:${#treebank}-7} == "GSDSimp" ]]; then
				python3 scripts/compare_treebank_bool.py `echo $treebank`/stats.xml >> treebanks_to_compare;
			fi;
		fi;
	done;
	echo "" >> treebanks_to_compare;
done;