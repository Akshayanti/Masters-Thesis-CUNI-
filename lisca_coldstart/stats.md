<h1>Statistics Comparing Different Runs</h1>

Table of Contents:  
1. [Baseline Results](#baseline)  
2. [Cross-Validation Results (Sampled Instances)](#cross-validation)  
3. [Baseline vs Cross-Validation](#baseline-vs-cross-validation)  

<h2>Baseline</h2>
<h3>Overall Statistics</h3>

<b>Total Arcs Processed:</b> 33739  
<b>Zero-Scored Arcs:</b> 221  
<b>Percentage:</b> 0.655 %  

<h3>Error Typology</h3>

| Error Type | Count |
|:--------|:----|
| advcl4advmod- | 1 |
| amod4acl- | 1 |
| amod4advmod- | 1 |
| amod4xcomp | 1 |
| case4compound- | 1 |
| compound4advmod- | 1 |
| compound4flat- | 1 |
| compound4obj- | 1 |
| dep4det- | 1 |
| dislocated4case- | 1 |
| mark4case- | 3 |
| Naming Error- | 1 |
| nmod4appos- | 1 |
| nmod4obl | 2 |
| None | 1 |
| None (Checked) | 57 |
| None (Checked)- | 46 |
| None- | 1 |
| nsubj4dislocated- | 1 |
| nsubj4obl- | 1 |
| obj4parataxis- | 3 |
| obl4aclORadvcl | 1 |
| obl4advcl- | 1 |
| obl4amod- | 1 |
| obl4nsubj- | 1 |
| POS Labelling Error- | 3 |
| Random Error (acl4obl) | 1 |
| Random Error (advmod4amod) | 2 |
| Random Error (amod4acl) | 1 |
| Random Error (aux4advmod) | 1 |
| Random Error (case4flat) | 1 |
| Random Error (compound4advmod) | 1 |
| Random Error (dislocated4case) | 1 |
| Random Error (dislocated4compound) | 1 |
| Random Error (nmod4nsubj) | 1 |
| Random Error (nsubj4amod) | 1 |
| Random Error (nsubj4obj) | 1 |
| Random Error (obj4aclORadvcl) | 2 |
| Random Error (obl4advmod)- | 1 |
| Random Error (POS Error) | 1 |
| Tree Error | 2 |
| Tree Error  (Checked) | 1 |
| Tree Error (Checked) | 5 |
| Tree Error (Checked)- | 8 |
| Unclassified | 27 |
| Wrong Head (Checked) | 11 |
| Wrong Head (Checked)- | 17 |
| <b>Total</b> | <b>221 </b>|

<h2>Cross-Validation</h2>
<h3>Overall Statistics</h3>

<b>Total Arcs Processed:</b> 336079  
<b>Zero-Scored Arcs:</b>

| K=2 | K=4 | K=8 |
|:------:|:-----:|:-----:|
| 3487 | 2620 | 2319 |



<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=4  
<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=8  
<b>Note</b>: The 0-scored arcs in K=4 contains all the 0-scored arcs in K=8  
<h3>Error Typology</h3>

<h4>Instances Common to K=2, K=4 and K=8</h4>

| Error Type | Count |
|:--------|:----|
| acl4amod | 1 |
| advmod4amod | 1 |
| amod4xcomp | 4 |
| nmod4obl | 3 |
| None | 110 |
| None (Checked) | 5 |
| nsubj4obl | 3 |
| obl4advclORacl | 1 |
| obl4xcomp | 3 |
| Random Error | 31 |
| Tree Error | 20 |
| Tree Error (Checked) | 1 |
| Wrong Head | 13 |
| Wrong Head (Checked) | 4 |
| <b>Total</b> | <b>200 </b>|

<h4>Instances in K=4 not present in K=8</h4>

| Error Type | Count |
|:--------|:----|
| advmod4amod | 1 |
| amod4xcomp | 2 |
| None | 78 |
| None (Checked) | 1 |
| nsubj4obl | 3 |
| obl4advclORacl | 1 |
| obl4xcomp | 1 |
| Random Error | 10 |
| Tree Error | 1 |
| Wrong Head | 2 |
| <b>Total</b> | <b>100 </b>|

<h4>Instances in K=2 not present in K=4 or K=8</h4>

| Error Type | Count |
|:--------|:----|
| acl4amod | 2 |
| amod4xcomp | 2 |
| auxasRoot | 2 |
| nmod4obl | 5 |
| None | 60 |
| None (Checked) | 4 |
| nsubj4obl | 1 |
| obl4aclORadvcl | 1 |
| obl4xcomp | 4 |
| Random Error | 9 |
| Random Error (compound4flat) | 1 |
| Random Error (dislocated4case) | 1 |
| Tree Error | 3 |
| Wrong Head | 4 |
| xcomp4advmod | 1 |
| <b>Total</b> | <b>100 </b>|

<h2>Baseline vs Cross-Validation</h2>



<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=4  
<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=8  
<b>Note</b>: The 0-scored arcs in K=4 contains all the 0-scored arcs in K=8  
<h3>Arc Flagging Statistics</h3>

| | Baseline | K=2 | K=4 | K=8 |
|:----|:----:|:-----:|:-----:|:-----:|
| | 221 | 344 | 254 | 226 |
| <b>Errors</b> | <b>87</b> | <b>119</b> | <b>96</b> | <b>85</b> |
| <b>Percentage</b>| <b>39.37 %</b> | <b>34.59 %</b> | <b>37.8 %</b> | <b>37.61 %</b> |
<h3>Arcs Commonly Flagged</h3>

| | K=2 | K=4 | K=8 |
|:------:|:-----:|:-----:|:-----:|
| Baseline | 211 | 205 | 205 |
<h3>Picked by Baseline, not by Cross-Validation</h3>

| Error Type | Count |
|:--------|:----|
| compound4flat- | 1 |
| None (Checked)- | 6 |
| obj4parataxis- | 2 |
| Wrong Head (Checked)- | 1 |
| <b>Total</b> | <b>10 </b>|
<h3>Picked by Cross Validation, not by Baseline</h3>

| Error Type | Count |
|:--------|:----|
| advmod4discourse- | 1 |
| amod4acl- | 1 |
| amod4xcomp- | 1 |
| case4amod- | 1 |
| compound4advmod- | 1 |
| conj4parataxis- | 1 |
| dislocated4case- | 1 |
| nmod4discourse- | 1 |
| nmod4obj- | 1 |
| nmod4obl | 1 |
| nmod4obl- | 1 |
| None | 3 |
| None (Checked) | 38 |
| None (Checked)- | 23 |
| nsubj4advcl- | 1 |
| obl4discourse- | 1 |
| Random Error (advcl4nmodORdet) | 1 |
| Random Error (case4flat) | 1 |
| Random Error (compound4flat) | 1 |
| Random Error (det4amod) | 1 |
| Random Error (nmod4advmod) | 1 |
| Random Error (nmod4flat) | 1 |
| Random Error (obl4advmod) | 1 |
| Random Error (obl4amod) | 1 |
| Random Error (obl4mark) | 1 |
| Random Error (obl4nmod) | 1 |
| Tree error (Checked) | 1 |
| Tree Error (Checked) | 3 |
| Tree Error (Checked)- | 1 |
| Unclassified | 22 |
| Wrong Head (Checked) | 3 |
| Wrong Head (Checked)- | 5 |
| <b>Total</b> | <b>122 </b>|
