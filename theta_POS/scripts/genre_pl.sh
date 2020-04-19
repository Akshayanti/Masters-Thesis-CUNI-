#!/usr/bin/env bash

if ! [ -d pl ]; then
	mkdir pl;
fi;

cp ../scripts/downsample.py ./;
cp ../scripts/klcpos3.py ./;
cp ../scripts/theta_POS.py ./;
cp ../scripts/kfold.py ./;
cp ../scripts/get_scores_with_sd.py ./;
cp ../scripts/split_pl_genres.py ./;

cat $HOME/ud-treebanks-v2.5/UD_Polish-LFG/pl_lfg-ud-train.conllu > pl.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Polish-LFG/pl_lfg-ud-dev.conllu >> pl.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Polish-LFG/pl_lfg-ud-test.conllu >> pl.conllu;
python3 split_pl_genres.py pl.conllu;
rm -f split_pl_genres.py pl.conllu spoken_media.conllu spoken_prepared.conllu academic.conllu legal.conllu;

echo "Generating Scores For Polish Data. Please be patient." > /dev/stderr;

for seedval in `seq 1 100`; do
	for filename in fiction news nonfiction blog social spoken_conversational; do
		python3 downsample.py -i `echo $filename`.conllu -n 100 --seed `echo $seedval`;
	done;

	for filename1 in fiction news nonfiction blog social spoken_conversational; do
		for filename2 in fiction news nonfiction blog social spoken_conversational; do
			if ! [ $filename1 = $filename2 ]; then
				echo $filename1 $filename2 >> klcpos3.tsv;
				python3 klcpos3.py --single_source --source `echo $filename1`_100.conllu --target `echo $filename2`_100.conllu | cut -f2 >> klcpos3.tsv;
				python3 klcpos3.py --single_source --target `echo $filename1`_100.conllu --source `echo $filename2`_100.conllu | cut -f2 >> klcpos3.tsv;
				echo "" >> klcpos3.tsv;
			fi;
		done;
	done;

	python3 theta_POS.py klcpos3.tsv > klcpos3_scores_`echo $seedval`;
	rm -f klcpos3.tsv;
done;

python3 get_scores_with_sd.py 1 klcpos3_scores* > pl/pl_scores;
rm -f klcpos3_scores*;

for seedval in `seq 1 100`; do
	touch klcpos3_self.tsv;
	for filename in fiction news nonfiction social spoken_conversational; do
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

python3 get_scores_with_sd.py 1 klcpos3_self* > pl/pl_self_scores;
rm -f *.py *.conllu klcpos3_self_*;

echo "Scores Generated. Scores Listed in \'genre_control/pl\' directory" > /dev/stderr;
