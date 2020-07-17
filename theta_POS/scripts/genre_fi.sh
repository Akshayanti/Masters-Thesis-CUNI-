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
cp ../scripts/get_formality_scores.py ./;
cp ../scripts/average_sentence_length.py ./;

cat $HOME/ud-treebanks-v2.5/UD_Finnish-TDT/fi_tdt-ud-train.conllu > fi-tdt.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Finnish-TDT/fi_tdt-ud-dev.conllu >> fi-tdt.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Finnish-TDT/fi_tdt-ud-test.conllu >> fi-tdt.conllu;
python3 split_fi_genres.py fi-tdt.conllu;
for genre in europarl.conllu uni_art.conllu; do
  python3 average_sentence_length.py `echo $genre` >> fi/sent_lengths.tsv;
done;
rm -f split_fi_genres.py fi-tdt.conllu;

echo "Generating Scores for Finnish Data. Please be patient." > /dev/stderr;

for genre in fiction wiki grammar blog legal wiki_news uni_news fin_news; do
  python3 average_sentence_length.py `echo $genre`.conllu >> fi/sent_lengths.tsv;
done;

# Begin Variance Inter-Genre ===========================================================================================
for seedval in `seq 1 100`; do
  for filename in fiction wiki grammar blog legal; do
    python3 downsample.py -i `echo $filename`.conllu -n 1000 --seed `echo $seedval`;
  done;

  for filename1 in fiction blog grammar wiki legal; do
    for filename2 in fiction blog grammar wiki legal; do
      if ! [ $filename1 = $filename2 ]; then
        echo $filename1 $filename2 >> klcpos3.tsv;
        python3 klcpos3.py --single_source --source `echo $filename1`_1000.conllu --target `echo $filename2`_1000.conllu | cut -f2 >> klcpos3.tsv;
        python3 klcpos3.py --single_source --target `echo $filename1`_1000.conllu --source `echo $filename2`_1000.conllu | cut -f2 >> klcpos3.tsv;
        echo "" >> klcpos3.tsv;
      fi;
    done;
    echo $filename1 >> politeness_1000_`echo $seedval`;
    python3 get_formality_scores.py `echo $filename1`_1000.conllu >> politeness_1000_`echo $seedval`;
    echo "" >> politeness_1000_`echo $seedval`;
  done;

  python3 theta_POS.py klcpos3.tsv > klcpos3_scores_1000_`echo $seedval`;
	rm -f klcpos3.tsv;
done;

python3 get_scores_with_sd.py 1 klcpos3_scores_1000_* > fi/fi_scores_1000;
python3 get_scores_with_sd.py 2 politeness_1000_* > fi/formality_1000;
rm -f klcpos3_scores_1000_* politeness_1000_*;
# End Variance Inter-Genre ===========================================================================================

# Begin Variance Intra-Genre ===========================================================================================
for seedval in `seq 1 100`; do
	touch klcpos3_self.tsv;
	for filename in fiction wiki grammar blog legal wiki wiki_news uni_news fin_news europarl uni_art; do
		python3 downsample.py -i `echo $filename`.conllu -n 900 --seed `echo $seedval`;
		python3 kfold.py 2 `echo $filename`_900.conllu;
		echo $filename $filename >> klcpos3_self.tsv;
		python3 klcpos3.py --single_source --source train_1 --target test_1 | cut -f2 >> klcpos3_self.tsv;
		python3 klcpos3.py --single_source --target train_1 --source test_1 | cut -f2 >> klcpos3_self.tsv;
		echo "" >> klcpos3_self.tsv;
	done;
	python3 theta_POS.py klcpos3_self.tsv > klcpos3_self_`echo $seedval`;
	rm -f klcpos3_self.tsv train_1 test_1 train_2 test_2;
done;

python3 get_scores_with_sd.py 1 klcpos3_self* > fi/fi_self_scores_900;
rm -f *.py *.conllu klcpos3_self_*;
# End Variance Intra-Genre =============================================================================================

echo "Scores Generated. Scores Listed in \'genre_control/fi\' directory" > /dev/stderr;
