# Apriori

### Summary of Algorithm

1. Build sparse tree

2. Run apriori algorithm

   i. Set itemsets to all possible subset whose length is1
   ii. Calculate supports of itemsets
   iii. Append itemsets to result which is satisfyingminimum support
   iv. Generate candidates by self-joining frequent itemson previous step
   v. If there are no candidates, go to step 3
   vi. Set itemsets to candidates and repeat step 3-ii

3. Create association rules from frequent patterns

4. Print rules

### Environments

python 3+

### How to run

```
$ python apriori.py 5 input.txt output.txt
```


### How to run test

```
$ python -m pytest tests/
```

