# Recommender

- Finding neighbors whose preference are similar to user c.
  - Use cosine similarity to find neighbors.
- Estimating rating of item s for user c based on neighbors.
  - Use average rating value of neighbors.
- Recommending data which is in test set.

### Environments

python 3+

### How to run

```
$ python3 recommender.py data/u1.base data/u1.test
```

