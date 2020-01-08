#!/bin/sh

size_control:
	if ! [ -d size_control ]; then \
		mkdir size_control; \
	fi;
	cd size_control; \
		if ! [ -d models ]; then \
			mkdir models; \
		fi; \
		cp $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-train.conllu ./train.conllu; \
		cp $(HOME)/ud-treebanks-v2.4/UD_Hindi-PUD/hi_pud-ud-test.conllu ./pud.conllu; \
		cp ../scripts/split_by_parts.py ./; \
		cp ../scripts/split_pud.py ./; \
		cp train.conllu train_100.conllu; \
		python3 split_pud.py pud.conllu; \
		mv news.conllu pud_news.conllu; \
		if ! [ -f models/100.udpipe ]; then \
			udpipe --train --parse 100.udpipe < train_100.conllu; \
			mv 100.udpipe models/; \
		fi; \
		if ! [ -f models/news.udpipe ]; then \
			udpipe --train --parse news.udpipe < pud_news.conllu; \
			mv news.udpipe models/; \
		fi; \
		for percentage in 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95; do \
			python3 split_by_parts.py `echo $$percentage` train.conllu; \
			mv train.conllu_* train_`echo $$percentage`.conllu; \
			if ! [ -f models/`echo $$percentage`.udpipe ]; then \
				udpipe --train --parse `echo $$percentage`.udpipe < train_`echo $$percentage`.conllu; \
				mv `echo $$percentage`.udpipe models/; \
			fi; \
		done; \
		if [ -f split_model_on_pud ]; then \
			rm -f split_model_on_pud pud_model_on_split; \
		fi; \
		for percentage in 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100; do \
			echo `echo $$percentage` "pud_news" >> split_model_on_pud; \
			echo `echo $$percentage` "pud_news" >> pud_model_on_split; \
			udpipe --accuracy --parse models/`echo $$percentage`.udpipe < pud_news.conllu >> split_model_on_pud; \
			udpipe --accuracy --parse models/news.udpipe < train_`echo $$percentage`.conllu >> pud_model_on_split; \
			echo "" >> split_model_on_pud; \
			echo "" >> pud_model_on_split; \
		done; \
		rm -f *.py *.conllu;

genre_control:
	if ! [ -d genre_control ]; then \
		mkdir genre_control; \
	fi;
	cd genre_control; \
		if ! [ -d models ]; then \
			mkdir models; \
		fi; \
		cp ../scripts/split_pl_genres.py ./; \
		cp ../scripts/downsample.py ./; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Polish-LFG/pl_lfg-ud-train.conllu > pl.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Polish-LFG/pl_lfg-ud-dev.conllu >> pl.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Polish-LFG/pl_lfg-ud-test.conllu >> pl.conllu; \
		python3 split_pl_genres.py pl.conllu; \
		rm -f split_pl_genres.py pl.conllu spoken_media.conllu spoken_prepared.conllu academic.conllu legal.conllu; \
		for filename in fiction news nonfiction blog social spoken_conversational; do \
			python3 downsample.py -i `echo $$filename`.conllu -n 125; \
		done; \
		if [ -f las_scores ]; then \
				rm -f las_scores; \
		fi; \
		for filename1 in fiction news nonfiction blog social spoken_conversational; do \
			if ! [ -f models/`echo $$filename1`.udpipe ]; then \
				udpipe --train --parse `echo $$filename1`.udpipe < `echo $$filename1`_125.conllu; \
				mv `echo $$filename1`.udpipe models/; \
			fi; \
			for filename2 in fiction news nonfiction blog social spoken_conversational; do \
				if [ "$$filename1" != "$$filename2" ]; then \
					echo $$filename1 $$filename2 >> las_scores; \
					udpipe --accuracy --parse models/`echo $$filename1`.udpipe < `echo $$filename1`_125.conllu >> las_scores; \
					udpipe --accuracy --parse models/`echo $$filename1`.udpipe < `echo $$filename2`_125.conllu >> las_scores; \
					udpipe --accuracy --parse models/`echo $$filename2`.udpipe < `echo $$filename1`_125.conllu >> las_scores; \
					udpipe --accuracy --parse models/`echo $$filename2`.udpipe < `echo $$filename2`_125.conllu >> las_scores; \
					echo "" >> las_scores; \
				fi; \
			done; \
		done; \
		rm -f *.py;
