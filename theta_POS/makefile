#!/bin/sh

get_data:
	@pip3 install -r requirements.txt;
	@chmod +x scripts/get_data.sh;
	@sh scripts/get_data.sh;

all_scores:
	@echo "Generating Scores. Might take a while. Please be patient." > /dev/stderr;
	@cp scripts/klcpos3.py $(HOME)/ud-treebanks*2.5/;
	@cd $(HOME)/ud-treebank*2.5; \
		if [ -f klcpos3_scores ]; then \
			rm -f klcpos3_scores; \
		fi; \
		if ! [ -d temp ]; then \
			mkdir temp; \
		fi; \
		for languages in  UD_Czech UD_German UD_Spanish UD_English UD_Estonian UD_Finnish UD_French UD_Galician UD_Ancient_Greek UD_Italian UD_Japanese UD_Korean UD_Latin UD_Lithuanian UD_Dutch UD_Norwegian UD_Old_Russian UD_Polish UD_Portuguese UD_Romanian UD_Russian UD_Slovenian UD_Swedish UD_Turkish UD_Chinese; do \
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

size_control:
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

genre_control:
	@if ! [ -d genre_control ]; then \
		mkdir genre_control; \
	fi;
	@cd genre_control; \
		if ! [ -d fi ]; then \
			cp ../scripts/genre_fi.sh ./; \
			sh genre_fi.sh; \
			rm -f genre_fi.sh; \
		fi; \
		if ! [ -d pl ]; then \
			cp ../scripts/genre_pl.sh ./; \
			sh genre_pl.sh; \
			rm -f genre_pl.sh;
		fi;

clean:
	rm -rf size_control *.tsv genre_control;
