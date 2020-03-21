<h1>Annotated Data</h1>

The data was manually annotated by the native speakers of the language. The first two characters in the
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

The second column of the file contains manually annotated data according to the following criteria. If the 
instance was found to be correctly attached to the correct head, it is marked with `1`, else it is marked with `0`.


<h3>nextConjHead.list</h3>

The file in this category corresponds to instances that were affected by nextConjHead() function call on
them. For ar data, there were no instances that were affected by nextConjHead() function call in the algorithm,
and so there is no nextConjHead.list file corresponding to the language.  

<h3>projAffected.list</h3>

<h2>Annotations for Originally Projective Data</h2>
