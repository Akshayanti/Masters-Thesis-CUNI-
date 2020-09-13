#!/usr/bin/env bash

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

rm -f split_pl_genres.py;

for x in spoken_conversational.conllu spoken_prepared.conllu spoken_media.conllu; do
  cat $x >> spoken.conllu;
  rm -f $x;
done;

for x in *.conllu; do
  if ! [[ $x == "fiction.conllu" ]]; then
    if ! [[ $x == "news.conllu" ]]; then
      if ! [[ $x == "spoken.conllu" ]]; then
        rm -f $x;
      fi;
    fi;
  fi;
done;

for seedval in `seq 1 100`; do
  python3 downsample.py -i spoken.conllu -n 1000 --seed `echo $seedval`;
  mv spoken_1000.conllu spoken_base.conllu;

  for genre in fiction news; do
    python3 downsample.py -i `echo $genre`.conllu -n 2000 --seed `echo $seedval`;
    python3 kfold.py 2 `echo $genre`_2000.conllu;
    mv test_1 `echo $genre`_base.conllu;
    mv test_2 `echo $genre`_test.conllu;
    rm -f train_1 train_2;
  done;

  # Case 1: Filename1's genre composition is subset of Filename2's genre composition
  for filename in news_test fiction_test spoken_base; do
    cat `echo $filename`.conllu >> all_genres.conllu;
  done;
  for testfile in fiction_test news_test; do
    cat `echo $testfile`.conllu >> news_fiction_test.conllu;
  done;
  for filename in fiction_base news_base; do
    cat `echo $filename`.conllu >> news_fiction_base.conllu;
  done;
  for testfile in news_test fiction_test; do
    cat spoken_base.conllu >> spoken_`echo $testfile`.conllu;
    cat `echo $testfile`.conllu >> spoken_`echo $testfile`.conllu;
  done;
  for basefile in fiction_base news_base news_fiction_base; do
    echo $basefile "news_fiction_test" >> klcpos3_Case1.tsv;
    python3 klcpos3.py --single_source --source `echo $basefile`.conllu --target news_fiction_test.conllu | cut -f2 >> klcpos3_Case1.tsv;
    python3 klcpos3.py --single_source --target `echo $basefile`.conllu --source news_fiction_test.conllu | cut -f2 >> klcpos3_Case1.tsv;
    echo "" >> klcpos3_Case1.tsv;
    echo $basefile "all_genres" >> klcpos3_Case1.tsv;
    python3 klcpos3.py --single_source --source `echo $basefile`.conllu --target all_genres.conllu | cut -f2 >> klcpos3_Case1.tsv;
    python3 klcpos3.py --single_source --target `echo $basefile`.conllu --source all_genres.conllu | cut -f2 >> klcpos3_Case1.tsv;
    echo "" >> klcpos3_Case1.tsv;
  done;
  echo "news_fiction_base" "all_genres" >> klcpos3_Case1.tsv;
  python3 klcpos3.py --single_source --source news_fiction_base.conllu --target all_genres.conllu | cut -f2 >> klcpos3_Case1.tsv;
  python3 klcpos3.py --single_source --target news_fiction_base.conllu --source all_genres.conllu | cut -f2 >> klcpos3_Case1.tsv;
  echo "" >> klcpos3_Case1.tsv;

  echo "news_base" "spoken_news_test" >> klcpos3_Case1.tsv;
  python3 klcpos3.py --single_source --source news_base.conllu --target spoken_news_test.conllu | cut -f2 >> klcpos3_Case1.tsv;
  python3 klcpos3.py --single_source --target news_base.conllu --source spoken_news_test.conllu | cut -f2 >> klcpos3_Case1.tsv;
  echo "" >> klcpos3_Case1.tsv;

  echo "fiction_base" "spoken_fiction_test" >> klcpos3_Case1.tsv;
  python3 klcpos3.py --single_source --source fiction_base.conllu --target spoken_fiction_test.conllu | cut -f2 >> klcpos3_Case1.tsv;
  python3 klcpos3.py --single_source --target fiction_base.conllu --source spoken_fiction_test.conllu | cut -f2 >> klcpos3_Case1.tsv;
  echo "" >> klcpos3_Case1.tsv;

  python3 theta_POS.py klcpos3_Case1.tsv > klcpos3_Case1_`echo $seedval`;
  rm -f klcpos3_Case1.tsv;
  rm -f all_genres.conllu;

  # Case 2: Intersection between Filename1 and Filename2's genre composition
  for combinedfile in spoken_news_test spoken_fiction_test spoken_base news_test fiction_test; do
    echo $combinedfile "news_fiction_base" >> klcpos3_Case2.tsv;
    python3 klcpos3.py --single_source --source `echo $combinedfile`.conllu --target news_fiction_base.conllu | cut -f2 >> klcpos3_Case2.tsv;
    python3 klcpos3.py --single_source --target `echo $combinedfile`.conllu --source news_fiction_base.conllu | cut -f2 >> klcpos3_Case2.tsv;
    echo "" >> klcpos3_Case2.tsv;
  done;

  for filename1 in spoken_news_test spoken_fiction_test; do
    for filename2 in news_base fiction_base; do
      echo $filename1 $filename2 >> klcpos3_Case2.tsv;
      python3 klcpos3.py --single_source --source `echo $filename1`.conllu --target `echo $filename2`.conllu | cut -f2 >> klcpos3_Case2.tsv;
      python3 klcpos3.py --single_source --target `echo $filename1`.conllu --source `echo $filename2`.conllu | cut -f2 >> klcpos3_Case2.tsv;
      echo "" >> klcpos3_Case2.tsv;
    done;
  done;

  python3 theta_POS.py klcpos3_Case2.tsv > klcpos3_Case2_`echo $seedval`;
  rm -f klcpos3_Case2.tsv;

  # Case 3: Disjoint between Filename1 and Filename2's genre composition
  echo "fiction_base" "spoken_news_test" >> klcpos3_Case3.tsv;
  python3 klcpos3.py --single_source --source fiction_base.conllu --target spoken_news_test.conllu | cut -f2 >> klcpos3_Case3.tsv;
  python3 klcpos3.py --single_source --target fiction_base.conllu --source spoken_news_test.conllu | cut -f2 >> klcpos3_Case3.tsv;
  echo "" >> klcpos3_Case3.tsv;

  echo "news_base" "spoken_fiction_test" >> klcpos3_Case3.tsv;
  python3 klcpos3.py --single_source --source news_base.conllu --target spoken_fiction_test.conllu | cut -f2 >> klcpos3_Case3.tsv;
  python3 klcpos3.py --single_source --target news_base.conllu --source spoken_fiction_test.conllu | cut -f2 >> klcpos3_Case3.tsv;
  echo "" >> klcpos3_Case3.tsv;

  echo "spoken_base" "news_fiction_test" >> klcpos3_Case3.tsv;
  python3 klcpos3.py --single_source --source spoken_base.conllu --target news_fiction_test.conllu | cut -f2 >> klcpos3_Case3.tsv;
  python3 klcpos3.py --single_source --target spoken_base.conllu --source news_fiction_test.conllu | cut -f2 >> klcpos3_Case3.tsv;
  echo "" >> klcpos3_Case3.tsv;

  python3 theta_POS.py klcpos3_Case3.tsv > klcpos3_Case3_`echo $seedval`;
  rm -f klcpos3_Case3.tsv;

  # Calculation of theta-POS amongst different sets
	for filename1 in fiction_base fiction_test spoken_base news_base news_test; do
		for filename2 in fiction_base fiction_test spoken_base news_base news_test; do
			if ! [ $filename1 = $filename2 ]; then
				echo $filename1 $filename2 >> klcpos3.tsv;
				python3 klcpos3.py --single_source --source `echo $filename1`.conllu --target `echo $filename2`.conllu | cut -f2 >> klcpos3.tsv;
				python3 klcpos3.py --single_source --target `echo $filename1`.conllu --source `echo $filename2`.conllu | cut -f2 >> klcpos3.tsv;
				echo "" >> klcpos3.tsv;
			fi;
		done;
	done;
	python3 theta_POS.py klcpos3.tsv > theta_all_`echo $seedval`;
	rm -f klcpos3.tsv;

	rm -f *_base.conllu *_test.conllu *.tsv;
done;

python3 get_scores_with_sd.py 1 klcpos3_Case1_* > theta_Case1.tsv;
rm -f klcpos3_Case1_*;
python3 get_scores_with_sd.py 1 klcpos3_Case2_* > theta_Case2.tsv;
rm -f klcpos3_Case2_*;
python3 get_scores_with_sd.py 1 klcpos3_Case3_* > theta_Case3.tsv;
rm -f klcpos3_Case3_*;
python3 get_scores_with_sd.py 1 theta_all_* > theta_all.tsv;
rm -f theta_all_*;
rm *.py *.sh *.conllu;