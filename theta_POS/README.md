<h1>Estimating POS Annotation Consistency of Different Treebanks in a Language: A Language-Independent Approach Based on KLcpos3 Measure</h1>

For documentation, please refer [here](docs/)


<h2>Contents</h2>

1. [Makefile Targets](#makefile-targets)
2. [Included Scripts](#included-scripts)
    1. [Files Used Throughout the Experiment](#files-used-throughout-the-experiment)
    2. [Files Specific to "size control" target](#files-specific-to-size_control-target)
    3. [Files Specific to "genre_control" target](#files-specific-to-genre_control-target) 
3. [References](#references)

<h2>makefile targets</h2>

1. `get_data`: Downloads and unzips the UDv2.5 data to `$HOME` directory.

2. `all_scores`: Get theta_POS scores for all the treebank combinations in UDv2.5. Results stored
in `UDv2.5_scores.tsv` file.

3. `size_control`: Get theta_POS scores and coverage scores for 100 different seeds. Results stored in `size_control/klc_scores_hdtb_vs_pud`
 and `size_control/coverage` respectively.
 
<h3>Included Scripts</h3>

<b>Note:</b> Unless mentioned otherwise, input files are in CONLL-U format.

<h4>Files Used Throughout the Experiment</h4>

1. <b>all_genres_list.py</b>
    Takes input `README.md` file for a treebank, and returns the list of unique values listed
    in 'Genre' category in machine-readable metadata. Multiple inputs supported.
    
    Defaults output to stdout, which can then be piped into a file, if desired.
    
    ```bash
   python3 all_genres_list.py <input_file(s)>
    ```

2. <b>get_data.sh</b>  
    Downloads and unpacks UDv2.5 Treebank Files to `HOME` directory, if not already present.
    ```bash
   sh get_data.sh
    ```
   
3. <b>get_scores_with_sd.py</b>  
    Calculates mean and standard deviation values when `theta_POS.py` file is run multiple times
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
    
4. <b>klcpos3.py</b>  
    File for calculating klcpos3 measure of source and target treebanks for single-source and 
    multi-source-weighted delexicalised parsing.
    
    Arguments:
    ```bash
   --source:           Source Candidate File(s), in CONLL-U format
   --target:           Target Candidate File, in CONLL-U format
   --single_source:    Used for selection of a single source, the sources would be displayed in
                         decreasing order of similarity measure
   --multi_source:     Used for computing klcpos3 ^ -4 as a similarity measure for weighted 
                         multiple-source parsing. The output values are not normalised.
    ```
   
   Usage:
   
   ```bash
   python3 klcpos3.py [-h] -t <target_file> -s <source_file(s)> [--single_source | --multi_source]
   ```

5. <b>test_significance.py</b>  
    Test if the scores generated from `get_scores_with_sd.py` are significantly different
    at 1%, 5%, 10% confidence value.
    ```bash
    python3 test_significance.py <input_file> <output_file>
    ```
   
6. <b>theta_POS.py</b>  
    Reads the file, and calculate the symmetric metric theta_pos, which is a sum of 
    calculated klcpos3 scores in either direction. Defaults output to stdout, from 
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
	
<h4>Files Specific to "size_control" target</h4>

1. <b>get_coverage_scores.py</b>  
    Program to calculate the coverage statistics for trigrams, as a percentage of trigrams 
    in target file. The file with greater number of trigrams is selected as the source, while
    the other is selected as source. Reports score as a percentage of trigrams common to source
    and target, over number of trigrams in target.
    
    Arguments:
    
    ```bash
   Arg1: File 1 in CONLL-U format
   Arg2: File 2 in CONLL-U format
   ```
   
   Usage:
   
        python3 get_coverage_scores.py <input_file1> <input_file2>
    
2. <b>split_by_parts.py</b>  
    Splits a given input file into two. The percentage of the split is specified by the first
    argument. An argument value of 30 (as an example) would split the file into one file containing
    30% sentences, and the other file containing 100 - 30 = 70% sentences. The output files retain
    the same name as input file, with "_PERCENT" appended to the end, where PERCENT is the percentage
    of sentences contained within the file.
    
    If needed, the third argument can be used to specify the seed value for the randomness of the
    split. If not provided, default seed is 1618. 
    
    Arguments:
    ```bash
    Arg1:  Percentage of data to split to
    Arg2:  Input file in CONLL-U format
    Arg3:  Integral Seed Value
	```
   Usage: 
   ```bash
   python3 split_by_parts.py <percentage_to_split> <input_file> [<seed_value>]
   ``` 
   
3. <b>split_pud.py</b>  
    Splits a given PUD file into `news.conllu` and `wiki.conllu` files.  
    
   ```bash
    python3 split_pud.py <input_pud_file> 
    ```

<h4>Files Specific to "genre_control" target</h4>

1. <b>downsample.py</b>  
    Downsamples a given CONLL-U file to a given number of sentences, or according to number of sentences in another
     CONLL-U formatted file  
    
    Arguments:
    ```bash
   -i --input         Input File that needs to be downsampled
   -n --number        Number of Sentences to downsample to
   -f --file          The file whose number of instances the input file should be downsampled to
   -o --output        Output file to write the downsampled data in. If the argument is not provided, 
                       defaults to <input_file>_<downsampled_instances_count>.conllu
   -h --help          Display Help Message and Exit
    ```
   Usage:
   ```bash
   python3 downsample.py [-h] -i <input_file> (-n NUMBER | -f FILE) [-o <output_file>]
    ```
   
Coming Soon.. 

<h3>References</h3>

1. Zeman, Daniel; Nivre, Joakim; Abrams, Mitchell; et al., 2019, 
  Universal Dependencies 2.5, LINDAT/CLARIAH-CZ digital library at the Institute of Formal and Applied Linguistics (ÚFAL), Faculty of Mathematics and Physics, Charles University, 
  http://hdl.handle.net/11234/1-3105.

2. Rosa, R. and Žabokrtský, Z. (2015). KLcpos3 - a language
similarity measure for delexicalized parser transfer. In
<i>Proceedings of the 53rd Annual Meeting of the Association
for Computational Linguistics and the 7th International Joint 
Conference on Natural Language Processing (Volume 2: Short Papers)</i>, 
pages 243–249, Beijing, China, July. Association for Computational Linguistics.
