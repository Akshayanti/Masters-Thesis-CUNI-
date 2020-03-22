<h1>Annotated Data</h1>

The data was manually annotated, based on whether the new head is correct or not. The first two characters in the
filename corresponds to the language the file corresponds to. The annotations are principally divided into
2 main categories, viz. for data instances that were originally projective, and for data instances that were
originally non-projective. The relevant details can be studied in the following sections.

<h2>Important Note</h2>



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

<h3>nextConjHead.list</h3>


In this file, the annotation was done keeping in mind if the attachment was made to the correct node
marked as `conj`. In case the deprel is marked wrong, but the association to this node was made regardless
of the presence of a better candidate, it was still marked with `1`. 

The file in this category corresponds to instances that were affected by nextConjHead() function call on
them. For ar data, there were no instances that were affected by nextConjHead() function call in the algorithm,
and so there is no nextConjHead.list file corresponding to the language.  

<h3>projAffected.list</h3>

<h3>unhandledNonProj.list</h3>

This category contains the files in `Extra Data (Not Annotated)` folder. The files contains instances that were originally
non-projective, and were not affected by the pipeline dealing with the forced projectivisation.

<h2>Annotations for Originally Projective Data</h2>

<h3>unhandledFinal.list</h3>

This category contains the files in `Extra Data (Not Annotated)` folder. The files contains instances that 
 were not affected by the algorithm at all.

