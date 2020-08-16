#!/usr/bin/env bash

mkdir et;
cp ../scripts/split_EDT_genres.py ./;
cp ../scripts/downsample.py ./;
cp ../scripts/klcpos3.py ./;
cp ../scripts/theta_POS.py ./;
cp ../scripts/kfold.py ./;
cp ../scripts/get_scores_with_sd.py ./;
cp ../scripts/get_coverage_scores.py ./;

cat $HOME/ud-treebanks-v2.5/UD_Estonian-EDT/*edt-ud-train.conllu > EDT.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Estonian-EDT/*edt-ud-dev.conllu >> EDT.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Estonian-EDT/*edt-ud-test.conllu >> EDT.conllu;
python3 split_EDT_genres.py EDT.conllu;
mkdir temp;
mv *.conllu temp;
cp temp/news.conllu news.conllu;
rm -rf temp split_EDT_genres.py;

for seedval in `seq 1 100`; do
	python3 downsample.py --input news.conllu --number 12000 --output EDT.conllu --seed $seedval;
	for foldsize in 4 6 8 12 16 24 48 120; do
		echo "Seed = " $seedval " Fold = " $foldsize > /dev/stderr;
		python3 kfold.py $foldsize EDT.conllu;
		for filecount in `seq 1 $foldsize`; do
			echo "train_"$filecount "test_"$filecount >> et/klcpos3_`echo $foldsize`.tsv;
			echo "train_"$filecount "test_"$filecount >> et/coverage_`echo $foldsize`_`echo $seedval`;
			python3 klcpos3.py --single_source --source train_`echo $filecount` --target test_`echo $filecount` | cut -f2 >> et/klcpos3_`echo $foldsize`.tsv;
			python3 klcpos3.py --single_source --target train_`echo $filecount` --source test_`echo $filecount` | cut -f2 >> et/klcpos3_`echo $foldsize`.tsv;
			python3 get_coverage_scores.py train_`echo $filecount` test_`echo $filecount` >> et/coverage_`echo $foldsize`_`echo $seedval`;
			echo "" >> et/klcpos3_`echo $foldsize`.tsv;
			echo "" >> et/coverage_`echo $foldsize`_`echo $seedval`;
		done;
		rm -f train_* test_*;
		python3 theta_POS.py et/klcpos3_`echo $foldsize`.tsv > et/klcpos3_`echo $foldsize`_`echo $seedval`;
		rm -f et/klcpos3_`echo $foldsize`.tsv;
	done;
done;

cp ../scripts/test_significance.py ./;

for foldsize in 4 6 8 12 16 24 48 120; do
	python3 get_scores_with_sd.py 1 et/klcpos3_`echo $foldsize`_* > et/et_`echo $foldsize`_scores;
	python3 get_scores_with_sd.py 2 et/coverage_`echo $foldsize`_* > et/et_`echo $foldsize`_coverage;
	python3 test_significance.py et/et_`echo $foldsize`_scores et/et_`echo $foldsize`_scores_significance;
	python3 test_significance.py et/et_`echo $foldsize`_coverage et/et_`echo $foldsize`_coverage_significance;
done;
rm -f *.conllu *.py et/klcpos* et/coverage*;

echo "Scores Generated. Scores Listed in \'size_control/et\' directory" > /dev/stderr;
