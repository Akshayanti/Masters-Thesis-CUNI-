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
| acl4expl- | 1 |
| acl4obj- | 1 |
| acl4obl | 1 |
| advcl4advmod | 2 |
| advmod4amod | 2 |
| amod4acl | 3 |
| amod4advmod | 1 |
| amod4xcomp | 1 |
| aux4advmod- | 1 |
| Case Error (4case) | 5 |
| compound4advmod- | 1 |
| compound4obj- | 1 |
| dep4det- | 1 |
| iobj4nsubj- | 1 |
| MWE Error (4compoundORfixed) | 5 |
| Naming Error (4apposORflat) | 8 |
| nmod4acl- | 1 |
| nmod4nummod- | 1 |
| None | 109 |
| nsubj4dislocated- | 1 |
| nsubj4obl- | 1 |
| obj4acl- | 1 |
| obl4advclORacl | 1 |
| obl4advmod- | 1 |
| obl4amod- | 1 |
| obl4det- | 1 |
| obl4nsubj- | 1 |
| POS Error | 5 |
| Reported Speech Error (4parataxis) | 4 |
| Tree Error | 20 |
| Wrong Head | 38 |
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
| acl4obj- | 1 |
| advmod4amod | 1 |
| amod4xcomp | 4 |
| amod4xcomp- | 1 |
| dep4det- | 1 |
| Naming Error (4apposORflat)- | 2 |
| nmod4appos- | 1 |
| nmod4obl | 3 |
| None | 85 |
| None (Checked)- | 30 |
| nsubj4obl | 3 |
| obj4parataxis- | 1 |
| obl4advclORacl | 1 |
| obl4xcomp | 2 |
| punct4mark- | 1 |
| Random Error | 24 |
| Tree Error | 14 |
| Tree Error (Checked)- | 5 |
| Tree Error- | 1 |
| Wrong Head | 10 |
| Wrong Head (Checked)- | 8 |
| <b>Total</b> | <b>200 </b>|

<h4>Instances in K=4 not present in K=8</h4>

| Error Type | Count |
|:--------|:----|
| advmod4amod- | 1 |
| amod4xcomp | 2 |
| Case Error (4case)- | 1 |
| dep4discourse- | 1 |
| Naming Error (4apposORflat)- | 2 |
| nmod4discourse- | 1 |
| nmod4flat- | 1 |
| None | 57 |
| None (Checked)- | 15 |
| nsubj4det- | 1 |
| nsubj4obl | 2 |
| obl4advclORacl | 1 |
| obl4advmod- | 1 |
| obl4xcomp | 1 |
| Random Error | 8 |
| Tree Error | 1 |
| Tree Error (Checked)- | 2 |
| Wrong Head | 2 |
| <b>Total</b> | <b>100 </b>|

<h4>Instances in K=2 not present in K=4 or K=8</h4>

| Error Type | Count |
|:--------|:----|
| acl4amod | 2 |
| acl4obj- | 1 |
| amod4xcomp | 2 |
| amod4xcomp- | 1 |
| auxasRoot | 2 |
| compound4flat- | 1 |
| compound4obj- | 1 |
| dep4discourse- | 1 |
| dislocated4case- | 1 |
| nmod4obl | 4 |
| None | 45 |
| None (Checked)- | 17 |
| nsubj4dislocated- | 1 |
| nsubj4obl | 1 |
| nsubj4obl- | 1 |
| obl4xcomp | 4 |
| punct4case- | 1 |
| Random Error | 6 |
| Tree Error | 2 |
| Wrong Head | 3 |
| Wrong Head (Checked)- | 2 |
| xcomp4advmod | 1 |
| <b>Total</b> | <b>100 </b>|

<h2>Baseline vs Cross-Validation</h2>



<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=4  
<b>Note</b>: The 0-scored arcs in K=2 contains all the 0-scored arcs in K=8  
<b>Note</b>: The 0-scored arcs in K=4 contains all the 0-scored arcs in K=8  
<h3>Arc Flagging Statistics</h3>

| | Baseline | K=2 | K=4 | K=8 |
|:----|:----:|:-----:|:-----:|:-----:|
| | 221 | 333 | 254 | 226 |
| <b>Errors</b> | <b>112</b> | <b>166</b> | <b>130</b> | <b>117</b> |
| <b>Percentage</b>| <b>50.68 %</b> | <b>49.85 %</b> | <b>51.18 %</b> | <b>51.77 %</b> |

<b>Note:</b> Typology Counts Across different runs can be viewed [here](./Annotations/testArcs/comparisonStats.tsv)
<h3>Arcs Commonly Flagged</h3>

| | K=2 | K=4 | K=8 |
|:------:|:-----:|:-----:|:-----:|
| Baseline | 211 | 205 | 205 |
<h3>Picked by Baseline, not by Cross-Validation</h3>

| Error Type | Count |
|:--------|:----|
| Naming Error (4apposORflat) | 1 |
| None | 6 |
| Reported Speech Error (4parataxis) | 2 |
| Wrong Head | 1 |
| <b>Total</b> | <b>10 </b>|
<h3>Picked by Cross Validation, not by Baseline</h3>

| Error Type | Count |
|:--------|:----|
| advcl4det | 2 |
| advmod4discourse- | 1 |
| amod4acl | 1 |
| amod4xcomp | 1 |
| Case Error (4case) | 1 |
| case4amod- | 1 |
| compound4advmod- | 1 |
| compound4det- | 2 |
| compound4obj- | 1 |
| dep4det- | 1 |
| dep4discourse- | 1 |
| dislocated4dep- | 1 |
| iobj4nsubj- | 1 |
| mark4discourse- | 1 |
| Naming Error (4apposORflat) | 3 |
| nmod4discourse- | 1 |
| nmod4nsubj- | 1 |
| nmod4obj- | 1 |
| nmod4obl | 3 |
| nmod4xcomp- | 1 |
| None | 64 |
| nsubj4advcl- | 1 |
| obl4advmod- | 1 |
| obl4amod- | 1 |
| obl4discourse- | 2 |
| obl4mark- | 1 |
| Reported Speech Error (4parataxis) | 2 |
| Tree Error | 8 |
| Wrong Head | 16 |
| <b>Total</b> | <b>122 </b>|
