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
cp ../scripts/get_formality_scores.py ./;
cp ../scripts/average_sentence_length.py ./;

cat $HOME/ud-treebanks-v2.5/UD_Polish-LFG/pl_lfg-ud-train.conllu > pl.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Polish-LFG/pl_lfg-ud-dev.conllu >> pl.conllu;
cat $HOME/ud-treebanks-v2.5/UD_Polish-LFG/pl_lfg-ud-test.conllu >> pl.conllu;
python3 split_pl_genres.py pl.conllu;
for genre in spoken_media.conllu blog.conllu spoken_prepared.conllu academic.conllu legal.conllu; do
    python3 average_sentence_length.py `echo $genre` >> pl/sent_lengths.tsv;
done;
rm -f split_pl_genres.py pl.conllu spoken_media.conllu blog.conllu spoken_prepared.conllu academic.conllu legal.conllu;

echo "Generating Scores For Polish Data. Please be patient." > /dev/stderr;

for genre in fiction news nonfiction social spoken_conversational; do
  python3 average_sentence_length.py `echo $genre`.conllu >> pl/sent_lengths.tsv;
done;

for seedval in `seq 1 100`; do
  python3 downsample.py -i spoken_conversational.conllu -n 600 --seed `echo $seedval`;
  mv spoken_conversational_600.conllu spoken_conversational_500.conllu;
  for filename in fiction news nonfiction social; do
    python3 downsample.py -i `echo $filename`.conllu -n 500 --seed `echo $seedval`;
  done;

	for filename1 in fiction news nonfiction social spoken_conversational; do
		for filename2 in fiction news nonfiction social spoken_conversational; do
			if ! [ $filename1 = $filename2 ]; then
				echo $filename1 $filename2 >> klcpos3.tsv;
				python3 klcpos3.py --single_source --source `echo $filename1`_500.conllu --target `echo $filename2`_500.conllu | cut -f2 >> klcpos3.tsv;
				python3 klcpos3.py --single_source --target `echo $filename1`_500.conllu --source `echo $filename2`_500.conllu | cut -f2 >> klcpos3.tsv;
				echo "" >> klcpos3.tsv;
			fi;
		done;
		echo $filename1 >> politeness_`echo $seedval`;
		python3 get_formality_scores.py `echo $filename1`_500.conllu >> politeness_`echo $seedval`;
		echo "" >> politeness_`echo $seedval`;
	done;

	python3 theta_POS.py klcpos3.tsv > klcpos3_scores_`echo $seedval`;
	rm -f klcpos3.tsv;
done;

python3 get_scores_with_sd.py 1 klcpos3_scores* > pl/pl_scores_500;
python3 get_scores_with_sd.py 2 politeness_* > pl/formality_500;
rm -f klcpos3_scores* politeness_* *.py *.conllu;

echo "Scores Generated. Scores Listed in \'genre_control/pl\' directory" > /dev/stderr;
