<h1>Annotated Data</h1>

The data was manually annotated, based on whether the new head is correct or not. The first two characters in the
filename corresponds to the language the file corresponds to. The annotations are principally divided into
2 main categories, viz. for data instances that were originally projective, and for data instances that were
originally non-projective. The relevant details can be studied in the following sections.

<h2>Annotations for Originally Non-Projective Data</h2>

This category contains 2 kind of files:
  
1. nextConjHead.list  
2. projAffected.list

The files in this category contains data in tab-separated formatted in 2 columns. The first column
of the file corresponds to the affected instance, in the following format. Note that there is 
no spacing between individual fields but the format is monospaced for readability, with placeholders
marked in uppercase.

    node < SENT_ID # TOKEN_ID, TOKEN_FORM >

The second column of the file contains manually annotated data according to the following criteria. 

    00  Correction Gone Wrong Because of False Non-Projectivity
    01  Direction Corrected, introducing Conjunction Sandwich. 
        Better Candidate Available.
    1   Correction Successful Without Any Faults
    0   Correction Failed
    XX  Some Other Fault, elaborated in documentation

<h3>nextConjHead.list</h3>

The file in this category corresponds to instances that were affected by nextConjHead() function call on
them. For ar data, there were no instances that were affected by nextConjHead() function call in the algorithm,
and so there is no nextConjHead.list file corresponding to the language.  

<h3>projAffected.list</h3>

The file in this category corresponds to instances that were NOT affected by nextConjHead() function call, 
and so were forced into a projective association to the immediately preceding content word (or pronoun) in the
word-order.

<h3>unhandledNonProj.list</h3>

This category contains the files in `Extra Data (Not Annotated)` folder. The files contains instances that were originally
non-projective, and were not affected by the pipeline dealing with the forced projectivisation.

<h2>Annotations for Pipeline Independent of Projectivity Status</h2>

This section contains the annotations for the algorithms that do not differentiate based on the projectivity status
of the association, in a tab-separated format. The first column identifies the node, as in the previous section, with
the annotation in the second column as per following guidelines:

```
00  Misdirected Dependency
01  Correction Gone Wrong, Introduced Conjunction Sandwich
1   Correction Successful Without Any Faults
```

The group contains 2 kind of files:
1. .siblingsAnnotate
2. .notSiblingAnnotate

The description of individual file type follows.

<h3>.siblingsAnnotate</h3>

This category contains files that were affected by attachToSibling() algorithm. The nodes that were originally non-projective
were evaluated earlier in previous section, and are therefore removed from the consideration in this group.

Contains randomly sampled 100 nodes, all manually annotated.

<h3>.notSiblingAnnotate</h3>

This category contains files that were affected by attachToAunt() and attachToGrandparent() algorithms. The nodes 
that were originally non-projective were evaluated earlier in previous section, and are therefore removed from the 
consideration in this group.

Contains upto 100 randomly sampled nodes, all manually annotated.

<h3>unhandledFinal.list</h3>

This category contains the files in `Extra Data (Not Annotated)` folder. The files contains instances that 
 were not affected by the algorithm at all.
