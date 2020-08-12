<h1>AUX vs. VERB: Attempt at
Separation of Verbs and
Auxiliary Verbs</h1>

<h2>Contents</h2>

1. [Documentation](#documentation)
2. [Problem Statement](#problem-statement)
3. [Included Files](#included-files)
4. [Using This Module](#using-this-module)
5. [Results](#results)
6. [Discussion and Conclusion](#discussion-and-conclusion)
7. [References](#references)

<h3>Documentation</h3>

All the details related to the experiment, from the problems related to the error type, to the final evaluation can be 
read about in Chapter 7 of the thesis document. 

[//]: # "[thesis document](../docs/thesis.pdf)."

<h3>Problem Statement</h3>

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

<h3>Included Files</h3>
 
 1. [orig_splits](./orig_splits): The original splits generated for the data which have annotated values.
 2. [orig_splits_trained](./orig_splits_trained): The generated test files with predictions for models trained on [orig_splits](./orig_splits) data.
 2. [Annotated Data](./Annotated%20Data): The annotated data over the data in [orig_splits](./orig_splits) data.
 4. [optimisation_evals](./optimisation_evals): Optimized parameters for the entire treebank.
 
<h3>Using This Module</h3>

To start with the module, clone this repository in your system.

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
 
<h3>Results</h3>

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

<h3>Discussion and Conclusion</h3>

Of the total number of tags listed in either category, 
we are able to focus on just 225 instances where we might be 
able to identify the problems. Even out of those 225 identified 
instances, just a bit over 25\% are actually erroneous. 

While hypertuning the best configuration of the classifier, 
the parameters correspond to the F1 score on how well it fits 
to the original data. Essentially, the best performing model 
is biased in the way that it would always try to find a 
prediction that matches the original annotation. While there 
is no other way on how to hypertune the model, the experimental 
results are therefore liable to find comparatively less 
instances where the confidence score is within the bounds as 
considered in the experiment. 

While certain patterns are more reliable than others 
(the case where predicted output doesn't match the original 
annotation), the overall performance for the experiment 
is low as can be attributed to different factors mentioned 
above. Given the low scout-ability of the error cases in the 
experiment, the approach used in the experiment is not reliable 
enough for the process to be automated.

<h3>References</h3>

1. Timothy Shopen. <i>Language Typology and Syntactic Description</i>, volume 1, pages
40–59. Cambridge University Press, 2 edition, 2007. ISBN 0-511-36671-
X. doi: https://doi.org/10.1017/CBO9780511619427. URL https://doi.org/10.1017/CBO9780511619427.

2. Joseph H Greenberg. Some Universals of Grammar with Particular Reference to
the Order of Meaningful Elements. <i>Universals of Language</i>, 2:73–113, 1963.
URL http://hdl.handle.net/11707/78.

3. Alan Akbik, Duncan Blythe, and Roland Vollgraf. Contextual String Embeddings
for Sequence Labeling. In <i>Proceedings of the 27th International Conference on
Computational Linguistics</i>, pages 1638–1649, Santa Fe, New Mexico, USA,
August 2018. Association for Computational Linguistics. URL 
https://www.aclweb.org/anthology/C18-1139.

4. Nivre, Joakim; Abrams, Mitchell; Agić, Željko; et al., 2019, 
  Universal Dependencies 2.4, LINDAT/CLARIAH-CZ digital library at the Institute of Formal and Applied Linguistics (ÚFAL), Faculty of Mathematics and Physics, Charles University, 
  http://hdl.handle.net/11234/1-2988.
