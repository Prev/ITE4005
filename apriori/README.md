# Apriori

### Summary of Algorithm

1. Build sparse tree
2. Run apriori algorithm
   1. Set itemsets to all possible subset whose length is1
   2. Calculate supports of itemsets
   3. Append itemsets to result which is satisfyingminimum support
   4. Generate candidates by self-joining frequent itemson previous step
   5. If there are no candidates, go to step 3
   6. Set itemsets to candidates and repeat step 3.2
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

