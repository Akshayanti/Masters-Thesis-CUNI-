#!/usr/bin/env bash

if ! [ -f EDT-stats.tsv ]; then \
  cat $HOME/ud-treebanks-v2.5/UD_Estonian-EDT/*edt-ud-train.conllu > EDT.conllu; \
  cat $HOME/ud-treebanks-v2.5/UD_Estonian-EDT/*edt-ud-dev.conllu >> EDT.conllu; \
  cat $HOME/ud-treebanks-v2.5/UD_Estonian-EDT/*edt-ud-test.conllu >> EDT.conllu; \

  for iteration in `seq 1 100`; do \
    echo $iteration "EDT" > /dev/stderr; \
    for i in `seq 100 100 900`; do \
      python3 downsample.py --input EDT.conllu --number `echo $i` --seed $iteration; \
      python3 get_unique_trigrams.py EDT_`echo $i`.conllu >> EDT_`echo $i`; \
      rm -f EDT_`echo $i`.conllu; \
    done; \
    for i in `seq 1000 500 12000`; do \
      python3 downsample.py --input EDT.conllu --number `echo $i` --seed $iteration; \
      python3 get_unique_trigrams.py EDT_`echo $i`.conllu >> EDT_`echo $i`; \
      rm -f EDT_`echo $i`.conllu; \
    done; \
  done; \
  python3 get_unique_trigrams.py EDT_*; \
fi;

rm -f EDT.conllu EDT_*;
