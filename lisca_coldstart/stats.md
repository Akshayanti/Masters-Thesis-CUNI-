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
| Unclassified | 221 |
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



<b>Note</b>: The 0-scored arcs in K=4 contains all the 0-scored arcs in K=8  
<h3>Arc Flagging Statistics</h3>

| | Baseline | K=2 | K=4 | K=8 |
|:----|:----:|:-----:|:-----:|:-----:|
| | 221 | 380 | 254 | 226 |
| <b>Errors</b> | <b>0</b> | <b>50</b> | <b>0</b> | <b>0</b> |
| <b>Percentage</b>| <b>0.0 %</b> | <b>13.16 %</b> | <b>0.0 %</b> | <b>0.0 %</b> |
<h3>Arcs Commonly Flagged</h3>

| | K=2 | K=4 | K=8 |
|:------:|:-----:|:-----:|:-----:|
| Baseline | 211 | 205 | 205 |
<h3>Picked by Baseline, not by Cross-Validation</h3>

| Error Type | Count |
|:--------|:----|
| None | 2 |
| None (Checked) | 7 |
| Random Error (Naming, Ask Dan) | 1 |
| <b>Total</b> | <b>10 </b>|
<h3>Picked by Cross Validation, not by Baseline</h3>

| Error Type | Count |
|:--------|:----|
| None (Checked) | 17 |
| Random Error (case4flat) | 1 |
| Random Error (compound4advmod) | 1 |
| Random Error (conj4parataxis) | 1 |
| Tree Error (Checked) | 1 |
| Unclassified | 101 |
| <b>Total</b> | <b>122 </b>|
