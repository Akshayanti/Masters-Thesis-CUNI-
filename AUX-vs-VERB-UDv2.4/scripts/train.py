#!/usr/bin/env python3

from flair.data import Corpus
from flair.embeddings import WordEmbeddings, StackedEmbeddings
from flair.embeddings import FlairEmbeddings
from flair.datasets import ColumnCorpus
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
import sys

# Set up the Corpus
columns = {0: 'text', 1: 'ner'}

if len(sys.argv) != 2:
    print("Need to input directory name as first arg")
    exit(0)

data_folder = './' + sys.argv[1]

corpus: Corpus = ColumnCorpus(data_folder, columns, train_file="train.txt", test_file="test.txt")
tag_dictionary = corpus.make_tag_dictionary(tag_type='ner')

# Init Embeddings
embeddings: StackedEmbeddings = StackedEmbeddings([
    WordEmbeddings('hi'),
    FlairEmbeddings('hi-forward'),
    FlairEmbeddings('hi-backward'),
])

# Init Seq Tagger
tagger: SequenceTagger = SequenceTagger(
    hidden_size=256,
    embeddings=embeddings,
    tag_dictionary=tag_dictionary,
    tag_type='ner',
    use_crf=True,
    use_rnn=True,
    rnn_layers=2,
    dropout=0.25
)

# Init Trainer
trainer: ModelTrainer = ModelTrainer(tagger, corpus)

# Init Training
trainer.train(sys.argv[1] + "_trained",
              learning_rate=0.1,
              mini_batch_size=8,
              max_epochs=30)
