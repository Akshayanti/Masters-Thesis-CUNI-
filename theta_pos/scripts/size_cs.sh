#!/usr/bin/env bash

mkdir cs;
cp ../scripts/split_PDT_genres.py ./;
cp ../scripts/downsample.py ./;
cp ../scripts/klcpos3.py ./;
cp ../scripts/theta_POS.py ./;
cp ../scripts/kfold.py ./;
cp ../scripts/get_scores_with_sd.py ./;
cp ../scripts/get_coverage_scores.py ./;

cat $HOME/ud-treebanks-v2.5/UD_Czech-PDT/cs_pdt-ud-train.conllu > PDT.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Czech-PDT/cs_pdt-ud-dev.conllu >> PDT.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Czech-PDT/cs_pdt-ud-test.conllu >> PDT.conllu;
python3 split_PDT_genres.py PDT.conllu;
mkdir temp;
mv *.conllu temp;
cp temp/l.conllu news.conllu;
rm -rf temp split_PDT_genres.py;

for seedval in `seq 1 100`; do
	python3 downsample.py --input news.conllu --number 50000 --output PDT.conllu --seed $seedval;
	for foldsize in 5 10 20 50 100 250 500; do
		echo "Seed = " $seedval " Fold = " $foldsize > /dev/stderr;
		python3 kfold.py $foldsize PDT.conllu;
		for filecount in `seq 1 $foldsize`; do
			echo "train_"$filecount "test_"$filecount >> cs/klcpos3_`echo $foldsize`.tsv;
			echo "train_"$filecount "test_"$filecount >> cs/coverage_`echo $foldsize`_`echo $seedval`;
			python3 klcpos3.py --single_source --source train_`echo $filecount` --target test_`echo $filecount` | cut -f2 >> cs/klcpos3_`echo $foldsize`.tsv;
			python3 klcpos3.py --single_source --target train_`echo $filecount` --source test_`echo $filecount` | cut -f2 >> cs/klcpos3_`echo $foldsize`.tsv;
			python3 get_coverage_scores.py train_`echo $filecount` test_`echo $filecount` >> cs/coverage_`echo $foldsize`_`echo $seedval`;
			echo "" >> cs/klcpos3_`echo $foldsize`.tsv;
			echo "" >> cs/coverage_`echo $foldsize`_`echo $seedval`;
		done;
		rm -f train_* test_*;
		python3 theta_POS.py cs/klcpos3_`echo $foldsize`.tsv > cs/klcpos3_`echo $foldsize`_`echo $seedval`;
		rm -f cs/klcpos3_`echo $foldsize`.tsv;
	done;
done;

cp ../scripts/test_significance.py ./;

for foldsize in 5 10 20 50 100 250 500; do
	python3 get_scores_with_sd.py 1 cs/klcpos3_`echo $foldsize`_* > cs/cs_`echo $foldsize`_scores;
	python3 get_scores_with_sd.py 2 cs/coverage_`echo $foldsize`_* > cs/cs_`echo $foldsize`_coverage;
	python3 test_significance.py cs/cs_`echo $foldsize`_scores cs/cs_`echo $foldsize`_scores_significance;
	python3 test_significance.py cs/cs_`echo $foldsize`_coverage cs/cs_`echo $foldsize`_coverage_significance;
done;
rm -f *.conllu *.py cs/klcpos* cs/coverage*;

echo "Scores Generated. Scores Listed in \'size_control/cs\' directory" > /dev/stderr;
