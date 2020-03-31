#!/bin/sh

get_data:
	chmod +x scripts/get_data.sh;
	sh scripts/get_data.sh;

all_scores:
	@echo "Generating Scores. Might take a while. Please be patient";
	@cp scripts/klcpos3.py $(HOME)/ud-treebanks*2.5/;
	@cd $(HOME)/ud-treebank*2.5; \
		if [ -f klcpos3_scores ]; then \
			rm -f klcpos3_scores; \
		fi; \
		if ! [ -d temp ]; then \
			mkdir temp; \
		fi; \
		for languages in UD_Spanish UD_Czech UD_German UD_English UD_Estonian UD_Finnish UD_French UD_Galician UD_Ancient_Greek UD_Italian UD_Korean UD_Latin UD_Lithuanian UD_Dutch UD_Norwegian UD_Polish UD_Portuguese UD_Romanian UD_Russian UD_Swedish UD_Slovenian; do \
			rm -rf temp; \
			mkdir temp; \
			for treebank in `echo $$languages`*; do \
				if ! [ $$treebank = "`echo $$languages`-PUD" ]; then \
					if [ -f `echo $$treebank`/*train.conllu ]; then \
						cat `echo $$treebank`/*-ud-*.conllu >> temp/`echo $$treebank`.conllu; \
					fi; \
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
	@echo "Done generating scores. Results available in UDv2.5_scores.tsv file";

size_control:
	if ! [ -d size_control ]; then \
		mkdir size_control; \
	fi;
	cd size_control; \
		cp $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-train.conllu ./train.conllu; \
		cp $(HOME)/ud-treebanks-v2.4/UD_Hindi-PUD/hi_pud-ud-test.conllu ./pud.conllu; \
		cp ../scripts/split_by_parts.py ./; \
		cp ../scripts/split_pud.py ./; \
		cp ../scripts/klcpos3.py ./; \
		cp ../scripts/theta_POS.py ./; \
		cp ../scripts/get_coverage_scores.py ./; \
		cp train.conllu train_100.conllu; \
		python3 split_pud.py pud.conllu; \
		mv news.conllu pud_news.conllu; \
		for percentage in 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95; do \
			python3 split_by_parts.py `echo $$percentage` train.conllu; \
			mv train.conllu_* train_`echo $$percentage`.conllu; \
		done; \
		rm -f klc_scores_* results_tag_*; \
		for percentage in 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100; do \
			echo "train_`echo $$percentage` pud_news" >> klc_scores_pud.tsv; \
			echo "train_`echo $$percentage` pud_news" >> coverage; \
			python3 klcpos3.py --single_source --source train_`echo $$percentage`.conllu --target pud_news.conllu | cut -f2 >> klc_scores_pud.tsv; \
			python3 klcpos3.py --single_source --target train_`echo $$percentage`.conllu --source pud_news.conllu | cut -f2 >> klc_scores_pud.tsv; \
			python3 get_coverage_scores.py --source train_`echo $$percentage`.conllu --target pud_news.conllu >> coverage; \
			echo "" >> klc_scores_pud.tsv; \
			echo "" >> coverage; \
		done; \
		python3 theta_POS.py klc_scores_pud.tsv > klc_scores_hdtb_vs_pud; \
		rm -f *.py *.conllu *.tsv *.udpipe;

genre_control:
	@if ! [ -d genre_control ]; then \
		mkdir genre_control; \
	fi;
	@if ! [ -d genre_control/test ]; then \
		mkdir genre_control/test; \
		cp scripts/test_fi.sh genre_control/test/test_fi.sh; \
	fi;
	@cd genre_control; \
		cp ../scripts/split_pl_genres.py ./; \
		cp ../scripts/downsample.py ./; \
		cp ../scripts/klcpos3.py ./; \
		cp ../scripts/theta_POS.py ./; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Polish-LFG/pl_lfg-ud-train.conllu > pl.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Polish-LFG/pl_lfg-ud-dev.conllu >> pl.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Polish-LFG/pl_lfg-ud-test.conllu >> pl.conllu; \
		python3 split_pl_genres.py pl.conllu; \
		rm -f split_pl_genres.py pl.conllu spoken_media.conllu spoken_prepared.conllu academic.conllu legal.conllu; \
		for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100; do \
			for filename in fiction news nonfiction blog social spoken_conversational; do \
				python3 downsample.py -i `echo $$filename`.conllu -n 125; \
			done; \
			for filename1 in fiction news nonfiction blog social spoken_conversational; do \
				for filename2 in fiction news nonfiction blog social spoken_conversational; do \
					if ! [ $$filename1 = $$filename2 ]; then \
						echo $$filename1 $$filename2 >> klcpos3.tsv; \
						python3 klcpos3.py --single_source --source `echo $$filename1`_125.conllu --target `echo $$filename2`_125.conllu | cut -f2 >> klcpos3.tsv; \
						echo "" >> klcpos3.tsv; \
					fi; \
				done; \
			done; \
			python3 theta_POS.py klcpos3.tsv > klcpos3_scores_`echo $$i`; \
			rm -f klcpos3.tsv *_125.conllu; \
		done; \
		rm -f *.py *.tsv; \
		echo "Polish Data"; \
		python3 ../scripts/get_scores_with_sd.py klcpos3_scores*; \
		echo ""; \
		cd test; \
			chmod +x test_fi.sh; \
			sh test_fi.sh; \

clean:
	rm -rf size_control *.tsv;
