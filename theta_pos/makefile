#!/bin/sh

.PHONY: get_data all_scores clean get_trigrams genre_control all_genres genres_additive dummy

get_data:
	@pip3 install -r requirements.txt;
	@if ! [ -d $(HOME)/ud-treebanks-v2.5 ]; then \
		wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3105/ud-treebanks-v2.5.tgz; \
		tar -xvf ud-treebanks-v2.5.tgz; \
		cp -r ud-treebanks-v2.5 $(HOME)/ud-treebanks-v2.5; \
		rm -rf ud-treebanks-v2.5 ud-treebanks-v2.5.tgz; \
	fi;


all_scores: get_data
	@echo "Generating Scores. Might take a while. Please be patient." > /dev/stderr;
	@cp scripts/klcpos3.py $(HOME)/ud-treebanks*2.5/;
	@cd $(HOME)/ud-treebank*2.5; \
		if [ -f klcpos3_scores ]; then \
			rm -f klcpos3_scores; \
		fi; \
		if ! [ -d temp ]; then \
			mkdir temp; \
		fi; \
		for languages in UD_Arabic UD_Czech UD_German UD_Spanish UD_English UD_Estonian UD_Finnish UD_French UD_Galician UD_Ancient_Greek UD_Italian UD_Japanese UD_Korean UD_Latin UD_Dutch UD_Norwegian UD_Polish UD_Portuguese UD_Romanian UD_Russian UD_Slovenian UD_Swedish UD_Turkish UD_Chinese; do \
			rm -rf temp; \
			mkdir temp; \
			for treebank in `echo $$languages`*; do \
				if ! [ $$treebank = "`echo $$languages`-PUD" ]; then \
					cat `echo $$treebank`/*-ud-*.conllu >> temp/`echo $$treebank`.conllu; \
				fi; \
			done; \
			cd temp; \
				for filename1 in *.conllu; do \
					for filename2 in *conllu; do \
						if ! [ $$filename1 = $$filename2 ]; then \
							echo $$filename1 $$filename2 >> klcpos3; \
							python3 ../klcpos3.py --single_source --source `echo $$filename1` --target `echo $$filename2` | cut -f2 >> klcpos3; \
							python3 ../klcpos3.py --single_source --target `echo $$filename1` --source `echo $$filename2` | cut -f2 >> klcpos3; \
							echo "" >> klcpos3; \
						fi; \
					done; \
				done; \
				cat klcpos3 >> ../klcpos3_scores; \
			cd ..; \
			rm -rf temp; \
		done; \
		rm -rf temp klcpos3.py;
	@cp $(HOME)/ud-treebanks*2.5/klcpos3_scores ./;
	@python3 scripts/theta_POS.py klcpos3_scores > UDv2.5_scores.tsv;
	@rm -f klcpos3_scores;
	@echo "Done generating scores. Results available in UDv2.5_scores.tsv file." > /dev/stderr;

size_control: get_data
	@if ! [ -d size_control ]; then \
		mkdir size_control; \
	fi;
	@cd size_control; \
		if ! [ -d cs ]; then \
			cp ../scripts/size_cs.sh ./; \
			sh size_cs.sh; \
			rm -f size_cs.sh; \
		fi; \
		if ! [ -d et ]; then \
			cp ../scripts/size_et.sh ./; \
			sh size_et.sh; \
			rm -f size_et.sh; \
		fi;

get_trigrams: get_data
	@if ! [ -d unique_trigrams ]; then \
		mkdir unique_trigrams; \
	fi;
	@cp scripts/get_unique_trigrams.py unique_trigrams/get_unique_trigrams.py;
	@cp scripts/klcpos3.py unique_trigrams/klcpos3.py;
	@cp scripts/downsample.py unique_trigrams/downsample.py;
	@cp scripts/unique_trigrams* unique_trigrams/;
	@cp scripts/split_PDT_genres.py unique_trigrams/;
	@cd unique_trigrams; \
		sh unique_trigrams_et.sh; \
		python3 get_unique_trigrams.py EDT-stats.tsv; \
		rm -f unique_trigrams_et.sh; \
		echo "EDT Stats Plotted. Can be found in 'docs' folder" > /dev/stderr; \
		cat $(HOME)/ud-treebanks-v2.5/UD_Czech-PDT/cs_pdt-ud-train.conllu > PDT.conllu; \
		cat $(HOME)/ud-treebanks-v2.5/UD_Czech-PDT/cs_pdt-ud-dev.conllu >> PDT.conllu; \
		cat $(HOME)/ud-treebanks-v2.5/UD_Czech-PDT/cs_pdt-ud-test.conllu >> PDT.conllu; \
		python3 split_PDT_genres.py PDT.conllu; \
		mkdir temp; \
		mv *.conllu temp; \
		cp temp/l.conllu PDT.conllu; \
		rm -rf temp split_PDT_genres.py; \
		sh unique_trigrams_cs1.sh & sh unique_trigrams_cs2.sh; \
		python3 get_unique_trigrams.py PDT-stats.tsv; \
		rm -f *.py *.sh; \
		rm -f PDT.conllu PDT_*; \
		echo "PDT Stats Plotted. Can be found in 'docs' folder" > /dev/stderr;

genre_control:	get_data
	@if ! [ -d genre_control ]; then \
		mkdir genre_control; \
	fi;
	@if ! [ -d genre_control/fi ]; then \
		cp scripts/genre_fi.sh genre_control/; \
		cd genre_control; \
		sh genre_fi.sh; \
		rm -f genre_fi.sh; \
	fi;
	@if ! [ -d genre_control/pl ]; then \
		cp scripts/genre_pl.sh genre_control/; \
		cd genre_control; \
			sh genre_pl.sh; \
		rm -f genre_pl.sh; \
	fi;

genres_additive:	genre_control
	@if ! [ -d genre_control/genres_additive ]; then \
		mkdir "genres_additive"; \
		mkdir genre_control/genres_additive; \
		cp scripts/additive_genres_pl.sh genres_additive/additive_genres_pl.sh; \
		cd genres_additive; \
			sh additive_genres_pl.sh; \
	fi;
	@yes | mv genres_additive/* genre_control/genres_additive/;
	@yes | rm -r genres_additive;

clean:
  @rm -rf size_control;
  @rm -rf unique_trigrams;
	@rm -rf genre_control;
	@rm -f treebanks_to_compare.tsv;
	@rm -f UDv2.5_scores.tsv;
	@rm -f docs/trigram-stats*;
