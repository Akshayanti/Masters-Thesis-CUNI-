#!/usr/bin/env bash

if ! [ -f PDT-stats.tsv ]; then \
  for iteration in `seq 1 100`; do \
    for i in `seq 100 100 900`; do \
      python3 downsample.py --input PDT.conllu --number `echo $i` --seed $iteration; \
      python3 get_unique_trigrams.py PDT_`echo $i`.conllu >> PDT_`echo $i`; \
      rm -f PDT_`echo $i`.conllu; \
    done; \
    for i in `seq 1000 500 20000`; do \
      python3 downsample.py --input PDT.conllu --number `echo $i` --seed $iteration; \
      python3 get_unique_trigrams.py PDT_`echo $i`.conllu >> PDT_`echo $i`; \
      rm -f PDT_`echo $i`.conllu; \
    done; \
  done; \
fi;