# Decision Tree

### Summary of Algorithm

- Tree is constructed in a top-down recursive divide-and-conquer manner
- Tree is automatically built by training
- Each branch of tree means attribute and domain of it
- Measure of attribute selection is "Information Gain (ID3/C4.5)"
- There are 3 cases of deciding result
	- No samples left -> Majority voting by parent nodes' dataset, or choosing first one in result domains
	- No remaining attributes -> Majority voting
	- All samples for given node belong to the same class -> Returns the corresponding value

### Environments

python 3+

### How to run

```
$ python3 dt.py data/dt_train.txt data/dt_test.txt output.txt
```


### How to run test

```
$ python -m pytest tests/
```

