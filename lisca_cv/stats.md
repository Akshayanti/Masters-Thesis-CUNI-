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
| acl4expl | 1 |
| acl4obj | 1 |
| acl4obl | 1 |
| advcl4advmod | 2 |
| advmod4amod | 1 |
| amod4acl | 2 |
| amod4advmod | 1 |
| amod4xcomp | 2 |
| aux4advmod | 1 |
| Case Error (4case) | 5 |
| compound4advmod | 1 |
| compound4obj | 1 |
| dep4det | 1 |
| iobj4nsubj | 1 |
| MWE Error (4compoundORfixed) | 5 |
| Naming Error (4apposORflat) | 9 |
| nmod4nummod | 1 |
| None | 112 |
| nsubj4obl | 1 |
| obj4acl | 1 |
| obl4advclORacl | 1 |
| obl4advmod | 1 |
| obl4det | 1 |
| obl4nsubj | 1 |
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
| acl4obj | 1 |
| acl4orphan | 1 |
| advcl4advmod | 1 |
| advmod4amod | 2 |
| advmod4orphan | 1 |
| amod4acl | 1 |
| amod4det | 1 |
| Case Error (4case) | 1 |
| case4det | 1 |
| compound4acl | 1 |
| conj4xcomp | 1 |
| dep4advmod | 1 |
| dep4det | 1 |
| dep4discourseORmark | 1 |
| dislocated4amod | 1 |
| iobj4nummod | 1 |
| mark4advcl | 1 |
| mark4advmod | 1 |
| mark4amod | 1 |
| MWE Error (4compoundORfixed) | 3 |
| Naming Error (4apposORflat) | 10 |
| nmod4nummod | 1 |
| nmod4obl | 1 |
| None | 103 |
| nsubj4amod | 1 |
| nsubj4nmod | 1 |
| nsubj4obj | 1 |
| nummod4amod | 1 |
| obl4advclORacl | 1 |
| obl4amod | 1 |
| POS Error | 3 |
| punct4det | 1 |
| punct4discourseORmark | 1 |
| Reported Speech Error (4parataxis) | 3 |
| Tree Error | 12 |
| Wrong Head | 36 |
| <b>Total</b> | <b>200 </b>|

<h4>Instances in K=4 not present in K=8</h4>

| Error Type | Count |
|:--------|:----|
| advcl4acl | 1 |
| Case Error (4case) | 3 |
| case4nummod | 1 |
| compound4obl | 1 |
| dep4det | 3 |
| dep4discourseORmark | 1 |
| Naming Error (4apposORflat) | 6 |
| nmod4discourseORmark | 1 |
| None | 56 |
| nsubj4advmod | 1 |
| nsubj4det | 2 |
| nsubj4obj | 2 |
| obl4advclORacl | 3 |
| obl4advmod | 1 |
| obl4det | 2 |
| obl4iobj | 2 |
| Tree Error | 7 |
| Wrong Head | 7 |
| <b>Total</b> | <b>100 </b>|

<h4>Instances in K=2 not present in K=4 or K=8</h4>

| Error Type | Count |
|:--------|:----|
| advmod4det | 3 |
| amod4det | 1 |
| amod4xcomp | 2 |
| Case Error (4case) | 4 |
| case4det | 2 |
| case4nummod | 1 |
| compound4amod | 1 |
| compound4obj | 2 |
| dep4advmod | 1 |
| dep4discourseORmark | 1 |
| MWE Error (4compoundORfixed) | 2 |
| Naming Error (4apposORflat) | 2 |
| nmod4advmod | 1 |
| nmod4dislocated | 1 |
| None | 51 |
| nsubj4dislocated | 1 |
| nsubj4nmod | 1 |
| nsubj4obj | 1 |
| nsubj4obl | 1 |
| obl4expl | 1 |
| obl4obj | 1 |
| obl4xcomp | 1 |
| Reported Speech Error (4parataxis) | 1 |
| Tree Error | 1 |
| Wrong Head | 15 |
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
| <b>Errors</b> | <b>109</b> | <b>160</b> | <b>127</b> | <b>114</b> |
| <b>Percentage</b>| <b>49.32 %</b> | <b>48.05 %</b> | <b>50.0 %</b> | <b>50.44 %</b> |

<b>Note:</b> Typology Counts Across different runs can be viewed [here](./Annotations/testArcs/comparisonStats.tsv)

<b>Note:</b> Typology counts across experimental runs (normalised per 1000) can be viewed[here](./Annotations/allArcs/normalizedScores.tsv)
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
| advmod4discourseORmark | 1 |
| amod4acl | 1 |
| amod4xcomp | 1 |
| Case Error (4case) | 1 |
| compound4advcl | 1 |
| compound4det | 2 |
| compound4obj | 1 |
| dep4discourseORmark | 1 |
| dep4nummod | 1 |
| dislocated4dep | 1 |
| Naming Error (4apposORflat) | 3 |
| nmod4discourseORmark | 1 |
| nmod4obj | 1 |
| nmod4obl | 4 |
| nmod4xcomp | 1 |
| None | 67 |
| nsubj4obj | 1 |
| obl4advclORacl | 1 |
| obl4amod | 1 |
| obl4discourseORmark | 3 |
| Tree Error | 9 |
| Wrong Head | 17 |
| <b>Total</b> | <b>122 </b>|
