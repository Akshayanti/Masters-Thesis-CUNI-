SHELL=/bin/bash

.PHONY: basecheck getdata baseline CV analyse_baseline analyse_CV analyse_CV1 analyse_CV2 process_baseline process_CV

basecheck:
	@pip3 install -r requirements.txt;
	@if ! [ -d $(HOME)/ud-treebanks-v2.4 ]; then \
		wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2988/ud-treebanks-v2.4.tgz; \
		tar -xvf ud-treebanks-v2.4.tgz; \
		cp -r ud-treebanks-v2.4 $(HOME)/ud-treebanks-v2.4; \
			rm -rf ud-treebanks-v2.4 ud-treebanks-v2.4.tgz; \
	fi;

getdata: basecheck
	@if ! [ -f hi.conllu ]; then \
		cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-train.conllu > hi.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-dev.conllu >> hi.conllu; \
		cat $(HOME)/ud-treebanks-v2.4/UD_Hindi-HDTB/hi_hdtb-ud-test.conllu >> hi.conllu;	\
	fi;
	@python3 scripts/downsample.py --input hi.conllu --number 16000;
	@mv hi.conllu_16000 hi_16000.conllu;
	@rm -f hi.conllu;
	@echo "Downsampled file created" > /dev/stderr;

# ======================= BEGIN BASELINE PIPELINE =====================================
process_baseline: getdata
	@make analyse_baseline;

analyse_baseline:
	@echo "Checking if dataset is present." > /dev/stderr;
	@if ! [ -d baseline ]; then \
		echo "Dataset Files not found. Fetching" > /dev/stderr; \
		make baseline; \
	fi;
	@make zip_baseline_check;
	@for files in baseline/baseline_test_lisca*; do \
		yes | rm $$files; \
	done;
	@yes | rm -f baseline/baseline_train.conllu;
	@echo "Unpacking Complete. Comparing the results with dataset now" > /dev/stderr;
	@python3 scripts/compact_lisca_results.py --conllu baseline/baseline_test.conllu --lisca baseline/baseline_test.lisca;
	@echo "Comparison with dataset complete." > /dev/stderr;
	@mv baseline/baseline_test.tsv baseline/baseline_all.tsv;
	@grep -h "0\.0" baseline/baseline_all.tsv | sort > baseline/baseline_zero.tsv;

baseline:
	@if ! [ -f hi_16000.conllu ]; then \
		echo "Downsampled file not found. Getting Downsampled file" > /dev/stderr; \
		make getdata; \
	fi;
	@if ! [ -d baseline ]; then \
		mkdir baseline; \
	fi;
	@echo "Creating Dataset for baseline" > /dev/stderr;
	@python3 scripts/baseline_split.py hi_16000.conllu;
	@mv baseline_test.conllu baseline/;
	@mv baseline_train.conllu baseline/;
	@echo "Baseline Dataset Stored in \'baseline\' directory" > /dev/stderr;

zip_baseline_check:
	@echo "Checking Required Files" > /dev/stderr;
	@if [ ! -f TARs/base_conll.tar ]; then \
		echo "Required File 'base_conll.tar' in 'TARs' directory not found. Could not continue." > /dev/stderr; \
		exit 1; \
	else \
		echo "File 1 of 2 found successfully." > /dev/stderr; \
	fi;
	@if [ ! -f TARs/base_lisca.tar ]; then \
		echo "Required File 'base_lisca.tar' in 'TARs' directory not found. Could not continue." > /dev/stderr; \
		exit 1; \
	else \
		echo "File 2 of 2 found successfully." > /dev/stderr; \
	fi;
	@echo "Unpacking Files" > /dev/stderr;
	@tar -xf TARs/base_conll.tar;
	@tar -xf TARS/base_lisca.tar;

# ==================== END BASELINE PIPELINE ==========================================
# ======================== BEGIN CV PIPELINE ==========================================
process_CV: getdata
	@make analyse_CV1;
	@make analyse_CV2;

analyse_CV1:
	@make analyse_CV;
	@echo "Creating data for part 1 of analysis (Comparison with Baseline)" > /dev/stderr;
	@cd CV; \
		mkdir testArcs; \
		for run in {k2,k4,k8}; do \
			for tsv_file in $$run/*.tsv; do \
				grep "test" $$tsv_file | grep -h "0\.0" >> temp; \
			done; \
			sort temp > testArcs/test_`echo $$run`.tsv; \
			rm -f temp;	\
		done;
	@echo "Finished. Data stored in 'CV/testArcs' folder";

analyse_CV2:
	@echo "Creating data for part 2 of analysis" > /dev/stderr;
	@for id in {2,4,8}; do \
		yes | rm CV/k`echo $$id`/*.{conll,conllu,lisca}; \
		if [ -f CV/k`echo $$id`.tsv ]; then \
			yes | rm CV/k`echo $$id`.tsv; \
		fi; \
		grep -h "0\.0" CV/k`echo $$id`/train*.tsv >> CV/k`echo $$id`/train.tsv; \
		sort CV/k`echo $$id`/train.tsv >> CV/k`echo $$id`.tsv; \
		yes | rm -r CV/k`echo $$id`; \
	done;
	@comm -12 CV/k2.tsv CV/k8.tsv > CV/k_all.tsv;
	@comm -3 CV/k2.tsv CV/k4.tsv > CV/k_2-4.tsv;
	@comm -3 CV/k4.tsv CV/k8.tsv > CV/k_4-8.tsv;
	@sort -R --random-source=.shuffleKey CV/k_all.tsv | head -n200 > CV/k_all_200.tsv1;
	@sort -R --random-source=.shuffleKey CV/k_2-4.tsv | head -n100 > CV/k_2not4_100.tsv1;
	@sort -R --random-source=.shuffleKey CV/k_4-8.tsv | head -n100 > CV/k_4not8_100.tsv1;
	@mkdir CV/allArcs;
	@for filename in CV/k2.tsv CV/k4.tsv CV/k8.tsv; do \
		mv $$filename CV/allArcs/; \
	done;
	@rm -f CV/k*.tsv;
	@mkdir CV/allArcs/RandomSampled;
	@for filename in k_all_200 k_2not4_100 k_4not8_100; do \
		mv CV/`echo $$filename`.tsv1 CV/allArcs/RandomSampled/`echo $$filename`.tsv; \
	done;
	@echo "The files are present in \'CV\' folder, marked as .tsv" > /dev/stderr;

analyse_CV:
	@echo "Checking if dataset is present." > /dev/stderr;
	@if ! [ -d CV ]; then \
		echo "Dataset Files not found. Fetching" > /dev/stderr; \
		make CV; \
	fi;
	@make zip_CV_check;
	@yes | rm CV/*/*.liscaextra;
	@for trainfiles in CV/{k2,k4,k8}/train*.{conll,conllu}; do \
		rm -f $$trainfiles; \
	done;
	@echo "Unpacking Complete. Comparing the results with dataset now" > /dev/stderr;
	@for id in {1..2}; do \
		python3 scripts/compact_lisca_results.py --conll CV/k2/test_`echo $$id`.conll --conllu CV/k2/test_`echo $$id`.conllu --lisca CV/k2/train_`echo $$id`.lisca; \
	done;
	@for id in {1..4}; do \
		python3 scripts/compact_lisca_results.py --conll CV/k4/test_`echo $$id`.conll --conllu CV/k4/test_`echo $$id`.conllu --lisca CV/k4/train_`echo $$id`.lisca; \
	done;
	@for id in {1..8}; do \
		python3 scripts/compact_lisca_results.py --conll CV/k8/test_`echo $$id`.conll --conllu CV/k8/test_`echo $$id`.conllu --lisca CV/k8/train_`echo $$id`.lisca; \
	done;
	@echo "Comparison with dataset complete." > /dev/stderr;

CV:
	@if ! [ -f hi_16000.conllu ]; then \
		echo "Downsampled file not found. Getting Downsampled file" > /dev/stderr; \
		make getdata; \
	fi;
	@if ! [ -d CV ]; then \
		mkdir CV; \
	fi;
	@echo "Processing K-fold with k=2" > /dev/stderr;
	@python3 scripts/kfold.py 2 hi_16000.conllu;
	@if ! [ -d CV/k2 ]; then \
		mkdir CV/k2; \
	fi;
	@echo "Processing Complete. Moving Files around" > /dev/stderr;
	@for filename in train*; do \
		yes | mv $$filename CV/k2/`echo $$filename`.conllu; \
	done;
	@for filename in test*; do \
		yes | mv $$filename CV/k2/`echo $$filename`.conllu; \
	done;
	@echo "Processing K-fold with k=4" > /dev/stderr;
	@python3 scripts/kfold.py 4 hi_16000.conllu;
	@if ! [ -d CV/k4 ]; then \
		mkdir CV/k4; \
	fi;
	@echo "Processing Complete. Moving Files around" > /dev/stderr;
	@for filename in train*; do \
		yes | mv $$filename CV/k4/`echo $$filename`.conllu; \
	done;
	@for filename in test*; do \
		yes | mv $$filename CV/k4/`echo $$filename`.conllu; \
	done;
	@echo "Processing K-fold with k=8" > /dev/stderr;
	@python3 scripts/kfold.py 8 hi_16000.conllu;
	@if ! [ -d CV/k8 ]; then \
		mkdir CV/k8; \
	fi;
	@echo "Processing Complete. Moving Files around" > /dev/stderr;
	@for filename in train*; do \
		yes | mv $$filename CV/k8/`echo $$filename`.conllu; \
	done;
	@for filename in test*; do \
		yes | mv $$filename CV/k8/`echo $$filename`.conllu; \
	done;
	@echo "Cross-Validation Dataset Stored in 'CV' directory" > /dev/stderr;

zip_CV_check:
	@echo "Checking Required Files" > /dev/stderr;
	@if [ ! -f TARs/CV_conll.tar ]; then \
		echo "Required File 'CV_conll.tar' in 'TARs' directory not found. Could not continue." > /dev/stderr; \
		exit 1; \
	else \
		echo "File 1 of 2 found successfully." > /dev/stderr; \
	fi;
	@if [ ! -f TARs/CV_lisca.tar ]; then \
		echo "Required File 'CV_lisca.tar' in 'TARs' directory not found. Could not continue." > /dev/stderr; \
		exit 1; \
	else \
		echo "File 2 of 2 found successfully." > /dev/stderr; \
	fi;
	@echo "Unpacking Files" > /dev/stderr;
	@tar -xf TARs/CV_conll.tar;
	@tar -xf TARs/CV_lisca.tar;
# ========================== END CV PIPELINE ==========================================

get_stats:
	@rm -rf baseline CV;
	@make process_baseline;
	@make process_CV;
	@python3 scripts/get_stats.py;
	@echo "Statistics Stored in stats.README file" > /dev/stderr;
	@rm -f baseline/baseline_test.lisca baseline/baseline_test.conllu;

prep_upload:
	@pip3 install -r requirements.txt;
	for filename in base_allZero base_not_k k_not_base test_k4 test_k8; do \
		python3 prep_upload.py Annotations/testArcs/`echo $$filename`.tsv; \
		mv Annotations/testArcs/`echo $$filename`.tsv_new Annotations/testArcs/`echo $$filename`.tsv; \
	done;
	make get_stats;
	git add Annotations stats.md;
	git commit -m `date`;
