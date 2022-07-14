# Bloom Filter Data Structure

A Bloom filter is a space-efficient probabilistic data structure, conceived by Burton Howard Bloom in 1970, that is used to test whether an element is a member of a set. It depends heavily on the use of hashing.

Unfortunately, while very space efficient (bit set can be much smaller than the number of elements you want to store), the probabilistic nature of the data structure's response to the question "is this element already a member of the set?" means there can be **false positives**. I'll explain this in more detail below.

On the other hand, there are no false negatives, meaning if the Bloom filter says "no, this element is not a member of the set", that's a guarantee and is not probabilistic.

## How Does It Work?

First off, the bloom filter data structure has some (tuneable) hyperparameters that define its architecture, namely some number of hash functions `m` and some number of bits in a bit set `m`.

Before any elements are inserted, i.e. when the cardinality of the set whose membership we are checking is still 0, we initialize all of our bits in our bit set (an array) of length `m` to `0` (False).

Now, let's say we have a username input by someone who's trying to create an account on our fancy large-scale website. We need to make sure that all usernames are unique, which means we need to make sure the username they provided does not match any usernames already stored in the system. The bloom filter can help us answer this question.

We take that username, and we pass that username through each of our `k` hash functions stored in the data structure, where each hash function is unique and outputs a different number given the input. Then, for each of those outputs, we want a corresponding index within our bit set to flip to true (which signals insertion). To map the outputs to indices within our bit set of length `m`, we mod each output by `m`.

Then, for each of those indices, we set that index in our bit set to `1` (True). If it is the case that all of those indices in our bit set were already set to `1` (True), then it is _possible_ (not a guarantee) that this username is taken. We say _might_ here because it's possible that another username may have generated the same set of indices when passed into our set of `k` hash functions. Unlikely, but possible.

However, if we encounter at least one index in our bit set where the value is still `0` (False), then this username has definitely NOT been taken and is still available, since a value of `0` means that index hasn't been used by any previous usernames.

## Caveats

After some deeper reading, it seems that both `m` (number of bits in our bit set) and `k` (number of hash functions to use for generating insertion indices) are optimizable parameters for a given bloom filter data structure.

## Optimization ideas

So we know we have two parameters, `m` and `k`, that define the behavior of the data structure. It seems obvious that the closer `k` is to `m`, the more false positives the data structure will produce. For example, if `k` equaled `m`, and if each `k` produced a different value, we'd quickly set all bits in the bit set of length `m` to 1, after which all queries would return "yes, this element is in the set". The smaller `k` is in relation to `m`, the slower we approach a "fully true" bit set, which lowers our false positive rate.

Also, regarding the hash functions themselves, ideally we'd want to minimize the number of false positives, which when broken down means minimizing the number of collisions produced by our hash functions, and this is really just a general goal associated with choosing good hash functions. Conceptually, it makes sense that collisions become harder to avoid once you begin modding the outputs of your hash to fit in a small shared window (i.e. the bit set).

## Time Complexity

Both insertion of data into a bloom filter and querying a bloom filter are both O(k) time complexity. Why?

When we insert, we need to generate k indices by passing our element-to-insert into k hash functions (each is constant time), use mod to get the indices, and we then loop over those k indices and flip the value at that index to true in the bit set. Key words: loop, k indices => O(k).

When we query, i.e. are asking whether an element is in our set, we need to do the same thing essentially: pass the query element into k hash functions, use mod to get the indices, and loop over those k indices to check whether any of the respective bits in the bit set are still `0`. Again, key words: loop, k indices => O(k).

## Example output to demonstrate probabilistic nature

```
PS C:\Users\huntaj\dev\bloom-filter> python .\main.py
Insertion indices for A: [0, 2, 4]
A definitely not stored in bloom filter yet
A definitely not stored in bloom filter yet
A definitely not stored in bloom filter yet
Insertion indices for B: [1, 3, 0]
B definitely not stored in bloom filter yet
B definitely not stored in bloom filter yet
Insertion indices for C: [2, 4, 1]
C MIGHT be stored in bloom filter already # this happens because 2,4 marked True by A insertion and 1 marked true by B insertion
Insertion indices for D: [3, 0, 2]
D MIGHT be stored in bloom filter already # this happened because 3 marked true by B insertion, 0 marked true by A insertion, 2 marked true by A insertion
Insertion indices for E: [4, 1, 3]
E MIGHT be stored in bloom filter already # and so on... least reliable once most or all indices store a 1
Insertion indices for F: [0, 2, 4]
F MIGHT be stored in bloom filter already
Insertion indices for G: [1, 3, 0]
G MIGHT be stored in bloom filter already
Insertion indices for H: [2, 4, 1]
H MIGHT be stored in bloom filter already
Insertion indices for I: [3, 0, 2]
I MIGHT be stored in bloom filter already
Insertion indices for J: [4, 1, 3]
J MIGHT be stored in bloom filter already
Insertion indices for K: [0, 2, 4]
K MIGHT be stored in bloom filter already
Insertion indices for L: [1, 3, 0]
L MIGHT be stored in bloom filter already
```
