#!/usr/bin/env bash

if ! [ -d fi ]; then
	mkdir fi;
fi;

cp ../scripts/downsample.py ./;
cp ../scripts/klcpos3.py ./;
cp ../scripts/theta_POS.py ./;
cp ../scripts/kfold.py ./;
cp ../scripts/get_scores_with_sd.py ./;
cp ../scripts/split_fi_genres.py ./;

cat $HOME/ud-treebanks-v2.5/UD_Finnish-TDT/fi_tdt-ud-train.conllu > fi-tdt.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Finnish-TDT/fi_tdt-ud-dev.conllu >> fi-tdt.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Finnish-TDT/fi_tdt-ud-test.conllu >> fi-tdt.conllu;
python3 split_fi_genres.py fi-tdt.conllu;
rm -f split_fi_genres.py fi-tdt.conllu grammar.conllu jrc_acquis.conllu uni_art;

echo "Generating Scores for Finnish Data. Please be patient." > /dev/stderr;

for seedval in `seq 1 100`; do
	for downsize in 100 200 300 400 500 600 700 800 900; do
		for filename in blog fiction europarl wiki wiki_news uni_news fin_news; do
			python3 downsample.py -i `echo $filename`.conllu -n `echo $downsize` --seed `echo $seedval`;
		done;

		for filename1 in fiction blog wiki_news uni_news fin_news wiki europarl; do
			for filename2 in fiction blog wiki_news uni_news fin_news wiki europarl; do
				if ! [ $filename1 = $filename2 ]; then
					echo $filename1 $filename2 >> klcpos3.tsv;
					python3 klcpos3.py --single_source --source `echo $filename1`_`echo $downsize`.conllu --target `echo $filename2`_`echo $downsize`.conllu | cut -f2 >> klcpos3.tsv;
					python3 klcpos3.py --single_source --target `echo $filename1`_`echo $downsize`.conllu --source `echo $filename2`_`echo $downsize`.conllu | cut -f2 >> klcpos3.tsv;
					echo "" >> klcpos3.tsv;
				fi;
			done;
		done;

		python3 theta_POS.py klcpos3.tsv > klcpos3_scores_`echo $downsize`_`echo $seedval`;
	done;
	rm -f klcpos3.tsv;
done;

for downsize in 100 200 300 400 500 600 700 800 900; do
	python3 get_scores_with_sd.py 1 klcpos3_scores_`echo $downsize`_* > fi/fi_scores_`echo $downsize`;
done;

for seedval in `seq 1 100`; do
	touch klcpos3_self.tsv;
	for filename in fiction blog europarl wiki wiki_news uni_news fin_news; do
		python3 downsample.py -i `echo $filename`.conllu -n 200 --seed `echo $seedval`;
		python3 kfold.py 2 `echo $filename`_200.conllu;
		echo $filename $filename >> klcpos3_self.tsv;
		python3 klcpos3.py --single_source --source train_1 --target test_1 | cut -f2 >> klcpos3_self.tsv;
		python3 klcpos3.py --single_source --target train_1 --source test_1 | cut -f2 >> klcpos3_self.tsv;
		echo "" >> klcpos3_self.tsv;
	done;
	python3 theta_POS.py klcpos3_self.tsv > klcpos3_self_`echo $seedval`;
	rm -f klcpos3_self.tsv train_1 test_1 train_2 test_2;
done;

python3 get_scores_with_sd.py 1 klcpos3_self* > fi/fi_self_scores;
rm -f *.py *.conllu klcpos3_self_*;

echo "Scores Generated. Scores Listed in \'genre_control/fi\' directory" > /dev/stderr;
