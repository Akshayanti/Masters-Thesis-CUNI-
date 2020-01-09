<h1>AUX and VERB Distinctions</h1>

<h2>Problem Statement</h2>

There is a significant overlap between <b>VERB</b> and <b>AUX</b>. The distinction between <b>AUX</b> and <b>VERB</b> is 
not always explicit, and is very liable to be affected by the agreement between the definitions of the terms in UD, and 
according to the traditional language-grammar. This is noted in part in the guidelines for UDv2 as well, where the 
following point is noted, with reference to the [definition of <b>AUX</b>](https://universaldependencies.org/u/pos/all.html#aux-auxiliary):

    [AUX] is often a verb (which may have non-auxiliary uses as 
    well) but many languages have nonverbal TAME markers and
    these should also be tagged AUX.

One of the proposed change in guidelines was to [get rid of <b>AUX</b> altogether](https://github.com/UniversalDependencies/docs/issues/275). 
However, as per findings of de Lhoneux and Nivre \[2016\], a parser is not able to learn the distinction between the
 two categories, when they are merged together. The authors observe a decrease in parsing scores when the two categories 
 are not explicitly separated. This was the principal motivation behind keeping the two separate, but there are still 
 overlaps.
 
In UDv2.4, it was proposed to limit the <b>AUX</b> by a list. The list would essentially identify all auxiliaries by a 
common definition, and thus would be able to create a better distinction between the two conflicting categories of 
<b>AUX</b> and <b>VERB</b>. This could be realized just in part though, principally because of the conflicts between 
traditional grammar-based definitions of the two categories, and the definitions as per UD. 

With respect to this particular error type, the experiment to separate the classes of <b>AUX</b> and <b>VERB</b> was 
unsuccessful with respect to UDv2.4, when we don't use the aforementioned list. This experiment here is the failed 
experiment done on UD\_Hindi-HDTB treebank in UDv2.4. 

Note that there still exist problems with respect to the differentiation between the two categories, 
as can be seen in the [list of open issues on the subject](https://github.com/universaldependencies/docs/issues?utf8=\%E2\%9C\%93&q=is\%3Aopen+aux).

<h2>Details Of the Experiment</h2>

All the details related to the experiment, from the problems related to the error type, to the final evaluation can be 
accessed through [PDF](docs/auxvsverb.pdf) document in this folder.

<h2>How to Use</h2>

To start with the module, clone this repository in your system, and download UDv2.4 from [here](https://universaldependencies.org/#download) to your $HOME 
directory.

Next, you can run the commands using [makefile](./makefile) in order to achieve the tasks as needed:

    make getdata
 Downloads the required dependencies, and prepares working copies of the treebanks in the current directory. Also, converts
 the data into IOBES format, and generates 10-fold splits for the data.
 
    make train
 Trains the model with optimized parameters on each fold of the data (as generated above). Each fold can take upto 8 hours to train,
 depending upon the GPU.
 
    make stats
 From the generated predictions on the folds of the test data, the instances with confidence scores in the bounds (>= 0.995 for 
 cases where prediction != annotation, and <= 0.667 for cases where annotated label == prediction) are isolated. 
 
    make plot
 Generate a rug-plot showing the distribution of the confidence scores in the case where the prediction is the same as the 
 annotated labels.
 
     make clean
  Removes all files created in the process of the pipeline.
 
 <h2>Other Files</h2>
 
 1. [orig_splits](./orig_splits): The original splits generated for the data which have annotated values.
 2. [orig_splits_trained](./orig_splits_trained): The generated test files with predictions for models trained on [orig_splits](./orig_splits) data.
 2. [Annotated Data](./Annotated%20Data): The annotated data over the data in [orig_splits](./orig_splits) data.
 4. [optimisation_evals](./optimisation_evals): Optimized parameters for the entire treebank.
 
<h2>Results</h2>

Defined Categories of errors:

|Category|Annotated Label|Predicted Label|
|:-------|:-------------:|:-------------:|
|aux-TP| S-aux | S-aux |
|O-TP| O | O |
|verb-TP| S-verb | S-verb|
|aux-O| S-aux | O |
| | O | S-aux |
|aux-verb| S-aux | S-verb|
| | S-verb | S-aux |
|verb-O| S-verb | O |
| | O | S-verb |

Results of Manual Annotation:


|Category|Instances|Mislabelled|Percentage|
|:------:|:--------|:----------|:---------|
| aux-TP |  83 | 3 | 03.61 |
| O-TP | 25 | 5 | 20.00 |
| verb-TP | 45 | 10 | 22.22 |
| aux-O | 10 | 9 | 90.00 |
| aux-verb | 42 | 23 | 54.76 |
| verb-O | 20 | 11 | 55.00 |
| Total | 225 | 61 | 27.11 |

The experiment failed owing to insufficiency in prediction results, or inability to detect the cases of mismatches in a reliable manner.  

<h2>Citations</h2>

1. Miryam de Lhoneux and Joakim Nivre.
Should Have, Would Have, Could Have. Investigating Verb Group Representations for Parsing with Universal Dependencies.
In <i>Proceedings of the Workshop on Multilingual and Cross-lingual Methods in NLP</i>, pages 10–19, 2016.

<h2>Acknowledgments</h2>

1. Computational resources were provided by the CESNET LM2015042 and the CERIT Scientific Cloud LM2015085, provided under the programme "Projects of Large Research, Development, and Innovations Infrastructures"
2. Computational resources were supplied by the Ministry of Education, Youth and Sports of the Czech Republic under the Projects CESNET (Project No. LM2015042) and CERIT-Scientific Cloud (Project No. LM2015085) provided within the program Projects of Large Research, Development and Innovations Infrastructures.
