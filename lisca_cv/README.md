<h1>Mining Errors in Low-Resource Languages by Combining LISCA And
Cross-Validation</h1>

<h2>Contents</h2>

1. [Documentation](#documentation)
2. [Problem Statement](#problem-statement)
3. [Included Files](#included-files)
4. [Using This Module](#using-this-module)
5. [Conclusion](#conclusion)
6. [References](#references)

<h3>Documentation</h3>

All the details related to the experiment, from the problems related to the error type, to the final evaluation can be 
read about in Chapter 6 of the thesis document. 

[//]: # "[thesis document](../docs/thesis.pdf)."

<h3>Problem Statement</h3>

For the low-resource languages, when there is no reference corpus, 
LISCA cannot be used directly. A common approach used in the case 
of low-resource languages, k-fold cross-validation is explored in 
this experiment. However, just using cross-validation is not enough, 
as the choice of the number of folds can affect the results significantly.
 
In this experiment, we therefore 

1.  evaluate if k-fold cross-validation is an optimal strategy 
against the approach of keeping the test and train data separated, and 

2.  try to map the behaviour of the algorithm to the choice of the 
number of folds in k-fold cross-validation approach.

<h3>Included Files</h3>

1. [Annotations/*](./Annotations): Refer to documentation
[here](Annotations/README.md).

2. [baseline/*](./baseline): Contains results ([baseline_all.tsv](./baseline/baseline_all.tsv)) and the identified 0-scored arcs ([baseline_zero.tsv](./baseline/baseline_zero.tsv))
 in the baseline run of LISCA. The scores are reported on `test` set of UDv2.4 hi-HDTB treebank data.

3. [CV/*](./CV): Contains the identified instances used for the manual evaluation from the CV run of LISCA. While [allArcs](./CV/allArcs) directory
contains the 0-scored arcs from the entire dataset, the [testArcs](./CV/testArcs) directory contains the list of 0-scored arcs
from the `test` set of UDv2.4 hi-HDTB treebank.

4. [scripts/*](./scripts): Directory of `*.py` files used in the experiment.

5. [TARs](./TARs): Directory containing result files generated when LISCA algorithm is run on the dataset for CV run, and for the baseline run in 
`*_lisca.tar` files. Also contains the dataset being used for each run in `*_conll.tar` files.  

6. [shuffleKey](./.shuffleKey): The key used as seed for shuffling in `shuf` commands. Excerpt from `/dev/zero` in Linux system. 
Works without any problems in Linux, but a bit buggy in MacOS. 

7. [stats.md](./stats.md): Uses data from different files in [Annotations](./Annotations) directory to generate a `.md` file 
that summarises the results of the manual evaluation.

<h3>Using This Module</h3>

To start with the module, clone this repository in your system, and then run the commands in the given order:

    make getdata
 Downloads the required dependencies using `requirements.txt` file, UDv2.4 data using the link
 [here](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-2988) and then prepares working 
 copies of the treebanks in the current directory.
 
    make process_baseline
 Using the stored `.tar` files in [TARs](TARs), generates [baseline](./baseline) directory containing results and identified 0-scored arcs
 in the baseline run of LISCA.
 
    make process_CV
Using the stored `.tar` files in [TARs](./TARs), generates [CV](./CV) directory containing identified 0-scored arcs in the 
CV run of LISCA.
 
    make stats
  Runs `process_baseline` and `process_CV` targets as mentioned above, and analyses the manually evaluated data in
  [Annotations](./Annotations) directory to report the comparative statistics in 
  [stats.md](./stats.md) file.

<h3>Conclusion</h3>

In the experiment, we narrowed the search scope from the bins as used by [2] to focus on the arcs that were considered as improbable by the algorithm.
Additionally, we found that using cross-validation to train the algorithm
has no significant performance gain.

For low-resource languages with little to no reference corpus data, we tried
cross-validation approach for finding the errors. We discovered that the choice of
folds in cross-validation strategy is determined by the size of the reference corpus;
and in case of unavailability of one, the strategy can be used on the data itself
without a significant loss in the error-detection rate.

<h3>References</h3>

1. Felice Dell’Orletta, Giulia Venturi, and Simonetta Montemagni. Linguistically-driven
Selection of Correct Arcs for Dependency Parsing. <i>Computación y Sistemas</i>,
17(2):125–136, 2013.

2. Chiara Alzetta, Felice Dell’Orletta, Simonetta Montemagni, and Giulia Venturi.
Dangerous Relations in Dependency Treebanks. In <i>Proceedings of the 16th
International Workshop on Treebanks and Linguistic Theories</i>, pages 201–210,
Prague, Czech Republic, 2017. URL 
https://www.aclweb.org/anthology/W17-7624.

3. Nivre, Joakim; Abrams, Mitchell; Agić, Željko; et al., 2019, 
  Universal Dependencies 2.4, LINDAT/CLARIAH-CZ digital library at the Institute of Formal and Applied Linguistics (ÚFAL), Faculty of Mathematics and Physics, Charles University, 
  http://hdl.handle.net/11234/1-2988.