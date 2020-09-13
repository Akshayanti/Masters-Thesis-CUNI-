<h1>Details of Scripts</h1>

<h3>Contents</h3>

1. [Python Files (*.py)](#python-files)
2. [Shell Files (*.sh)](#shell-files)

<b>Note:</b> Unless mentioned otherwise, input files are in CoNLL-U format.

<h3>Python Files</h3>

1. [all_genres_list.py](./all_genres_list.py)
    Takes input `README.md` file for a treebank, and returns the list of unique values listed
    in `Genre` category in machine-readable metadata. Multiple inputs supported.
    
    Defaults output to stdout, which can then be piped into a file, if desired.
    
    ```bash
   python3 all_genres_list.py <input_file(s)>
    ```

2. [average_sentence_length.py](./average_sentence_length.py)  
    Calculates the average sentence length in a given CoNLL-U file, given by the total number of [syntactic words](https://universaldependencies.org/u/overview/tokenization.html)
    divided by the total number of sentences.  
    
    Usage:
    
        python3 average_sentence_length.py <input_file>
3. [compare_treebank_bool.py](./compare_treebank_bool.py)  
    Determines if the total number of sentences in a given input file is more than 1000, or not. Returning `True` if the number of sentences
    is more than 1000, and `False` otherwise.
    
    Usage:
        
        python3 compare_treebank_bool.py <input_file> 
4. [downsample.py](./downsample.py)  
    Downsamples a given CoNLL-U file to a given number of sentences, or according to number of sentences in another
     CoNLL-U formatted file  
    
    Arguments:
    ```bash
   -i --input         Input File that needs to be downsampled
   -n --number        Number of Sentences to downsample to
   -f --file          The file whose number of instances the input file should be downsampled to
   -o --output        Output file to write the downsampled data in. If the argument is not provided, 
                       defaults to <input_file>_<downsampled_instances_count>.CoNLLu
   -h --help          Display Help Message and Exit
    ```
   Usage:
   ```bash
   python3 downsample.py [-h] -i <input_file> (-n NUMBER | -f FILE) [-o <output_file>]
    ```

5. [get_coverage_scores.py](./get_coverage_scores.py)  
    Calculates the coverage statistics for trigrams, as a percentage of trigrams 
    in target file. The file with greater number of trigrams is selected as the source, while
    the other is selected as source. Reports score as a percentage of trigrams common to source
    and target, over number of trigrams in target.
    
    Arguments:
    
    ```bash
   Arg1: File 1 in CoNLL-U format
   Arg2: File 2 in CoNLL-U format
   ```
   Usage:  
   
       python3 get_coverage_scores.py <input_file1> <input_file2>

6. [get_formality_scores.py](./get_formality_scores.py)  
    NOT USED IN THE PIPELINE.
    
    The script reads input CoNLL-U file to calculate the F-score (as given by [Heylighen and Dewaele, 1999]), but using normalised frequencies.
    Similarly, can be used to calculate I-measure (as given by [Mosquera and Pozo, 2011]), by commenting out line\#51 and including line\#52.
    
    Usage:
    
        python3 get_formality_scores.py <input_CoNLL-U_file>
    
7. [get_scores_with_sd.py](./get_scores_with_sd.py)  
    Calculates mean and standard deviation values when [theta_POS.py](./theta_POS.py) file is run multiple times
    for the similar data (example- 100 runs on slightly changing data). The first argument is the
    mode of the input file(s) followed by the different input files from second argument onwards.
    Can take multiple inputs. Defaults printing the output to stdout, from where it can be piped
    to the desired output file.
    
    Mode Values Description:
    ```bash
    Mode   File_Type
     1     TSV File with column1=fieldname, column2=values
     2     File such that fieldname and values are each in new lines. 
           Empty line separates fieldname entries
    ```
   
   Usage:
   ```bash
   python3 get_scores_with_sd.py <mode> <input_file(s)>
   ```

8. [get_unique_trigrams.py](./get_unique_trigrams.py)  
    Calculates for a given input file
    - the total number of POS trigrams
    - the total number of unique POS trigrams
    
    If only one `input_file` with a `.tsv` extension is given as an argument, the script reads the file to plot the first
    column as an x-value, while the subsequent columns are used to plot lines in the graph.
    
    For all other cases, the input file is read as a CoNLL-U file, and the values as indicated earlier are
    computed for the input files. 
   
   Usage:
   
        python3  get_unique_trigrams.py <input_file(s)>
   
9. [kfold.py](./kfold.py)  
    Creates `test` and `training` folds for the given data, based on the number of folds given as argument.
    Arguments:
    
    ```bash
   Arg1: The number of folds (integer)
   Arg2: Input File in CoNLL-U format
   ```
   Usage:  
   
       python3 kfold.py <folds_count> <input_file>

10. [klcpos3.py](./klcpos3.py)  
    File for calculating KL<sub>cpos<sup>3<sup></sub> measure of source and target treebanks for single-source and 
    multi-source-weighted delexicalised parsing.
    
    Arguments:
    ```bash
    --source:           Source Candidate File(s), in CoNLL-U format
    --target:           Target Candidate File, in CoNLL-U format
    --single_source:    Used for selection of a single source, the sources would be displayed in
                         decreasing order of similarity measure
    --multi_source:     Used for computing klcpos3 ^ -4 as a similarity measure for weighted 
                         multiple-source parsing. The output values are not normalised.
    ```
    Usage:
   
       ```bash
       python3 klcpos3.py [-h] -t <target_file> -s <source_file(s)> [--single_source | --multi_source]
       ```

11. [split_EDT_genres.py](./split_EDT_genres.py), [split_fi_genres.py](./split_fi_genres.py), [split_PDT_genres.py](./split_PDT_genres.py) and [split_pl_genres.py](./split_pl_genres.py)  
    Split the given `input_file` into its constituent genres. Takes CoNLL-U file as a singular input.
    ```bash
    python3 <python_file> <input_file>
    ``` 
    
12. [test_significance.py](./test_significance.py)  
    For each given mean, tests how many other means it is significantly same with, 
    at 95% confidence value.
    ```bash
    python3 test_significance.py <input_file> <output_file>
    ```
   
13. [theta_POS.py](./theta_POS.py)  
    Reads the file, and calculate the symmetric metric θ<sub>pos</sub>, which is a sum of 
    calculated KL<sub>cpos<sup>3<sup></sub> scores in either direction. Defaults output to stdout, from 
    where it can be piped into a file. 
    
    Input File Format:
    ```bash
       file1 file2
       klcpos3(file1, file2) score
       klcpos3(file2, file1) score
       
       file1 file3
       klcpos3(file1, file3) score
       klcpos3(file3, file1) score
       
       file2 file3
       klcpos3(file2, file3) score
       klcpos3(file3, file2) score
       
    ```
    Output Format (tsv, columns mark individual values):
    ```bash
       file1<space>file2  theta_pos_score
       file1<space>file3  theta_pos_score
       file2<space>file3  theta_pos_score
       ...
    ```
    Usage:
    ```bash
    python3 theta_POS.py <input_file>
    ```
	
<h3>Shell Files</h3>

1. [additive_genres_pl.sh](./additive_genres_pl.sh)  
    Batch File to check how multiple genres at the same time affect θ<sub>pos</sub> scores. 
2. [genre_fi.sh](./genre_fi.sh) and [genre_pl.sh](./genre_pl.sh)  
    Batch Files to check the variance of θ<sub>pos</sub> scores on inter-genre basis in Finnish-TDT and Polish-LFG treebanks respectively.
    In case of Finnish data, the intra-genre variance is also calculated.
3. [size_cs.sh](./size_cs.sh) and [size_et.sh](./size_et.sh)  
    Batch Files to check the variance of θ<sub>pos</sub> scores with the change in dataset size in Czech-PDT and Estonian-EDT data respectively.
4. [treebanks_to_compare.sh](./treebanks_to_compare.sh)  
    Runs [compare_treebank_bool.py](compare_treebank_bool.py) on all the different treebanks to indicate which treebanks should be compared with other
    treebanks of the same language. Stores result in [TSV file](../treebanks_to_compare.tsv). The different treebanks of a language are separated from other 
    treebanks of other language by an empty line in between.
5. [unique_trigrams_cs1.sh](./unique_trigrams_cs1.sh), [unique_trigrams_cs2.sh](./unique_trigrams_cs2.sh) and [unique_trigrams_et.sh](./unique_trigrams_et.sh)  
    Calculate the variance of count of POS trigrams Czech-PDT and Estonian-EDT data with change in dataset size.
    [unique_trigrams_cs1.sh](./unique_trigrams_cs1.sh) and [unique_trigrams_cs2.sh](./unique_trigrams_cs2.sh) calculate the statistics for Czech-PDT treebanks,
    and are split to allow parallel computation. Generates [unique_trigrams](../unique_trigrams) directory. 