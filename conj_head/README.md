<h1>conj_head - Conjunction as Head of Dependency in UD </h1>

<h2>Problem Statement</h2>

In the changed guidelines for UDv2, there were two changes with respect to conjunction tags <b>CCONJ</b> and 
<b>SCONJ</b>; and the dependency relations, <b>cc</b> and <b>conj</b>. The changes are listed as follows:

1. The PoS tag <b>CONJ</b> in UDv1 was changed to <b>CCONJ</b> in UDv2, to make it more parallel to <b>SCONJ</b>.
2. The coordinated structures are attached to the immediately succeeding conjunct in UDv2, as opposed to UDv1 where 
they were attached to the first conjunct.

Of the two changes in guidelines, the first one (renaming of tag) can be applied deterministically, and automatically 
throughout the treebank(s). The second change, however, can be classified as head identification error. The pattern in 
question was also identified by Alzetta et. al [2017] in their paper, where they note that it contributes to 24.65 \% 
of total discovered error instances. This implies that this is indeed a major error category, and needs to be handled 
well. We do take a look at this error type in our experiments.

<h2>Further Details on Experiment</h2>

All the details related to the experiment, from the problems related to the error type, to the dataset definition, 
algorithm used, and finally the evaluation can be accessed through [PDF](./conj_head.pdf) document in this folder.

<h2>How to Use</h2>

To start with the module, clone this repository in your system, and download UDv2.4 from [here](https://universaldependencies.org/#download) to your $HOME 
directory.

Next, you can run the commands in order to achieve the tasks as needed:

    make getdata
 Downloads the required dependencies, and prepares working copies of the treebanks in the current directory.
 
    make direction
 Report all the instances of mis-directed dependencies of <b>CCONJ</b> in a `*.direction` file
 
    make correction
 Corrects the instances detected in `*.direction` file, creates a `*2.conllu` file with all the corrections, and 
 `*2.direction` file with the instances not handled by the algorithm.
 
    make clean
  Removes all `.conllu` and `.direction` files
  
<h2>Results</h2>

Manually checked on 100 randomly sampled instances of corrected data for `ar` and `af` data.

|Language|Total|Correct|
|:------:|:----|:------|
| ar | 100 | 97 |
| af | 100 | 95 |

The algorithm fixes around 90\%+ instances in a deterministic manner, even if we consider a 5\% error rate in reported scores.

<h2>Citations</h2>

1. Chiara Alzetta, Felice Dell’Orletta, Simonetta Montemagni, and Giulia Venturi. Dangerous relations in dependency 
treebanks. In <i>Proceedings of the 16th International Workshop on Treebanks and Linguistic Theories</i>, pages 201–210, 2017.


