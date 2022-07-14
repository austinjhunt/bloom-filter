""" 
Bloom filter implementation 
Austin Hunt
7/14/2022
"""
import hashlib
import math

num_hash_functions = 3
num_bits_in_bitset = 5


def hash1(value):
    return ord(value)


def hash2(value):
    return ord(value) + 2


def hash3(value):
    return ord(value) + 4


hashes = {
    'h1': hash1,
    'h2': hash2,
    'h3': hash3
}


elems_to_insert = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

bit_set = [False for i in range(num_bits_in_bitset)]


def get_insertion_indices_of_elem(elem, hashes):
    return [func(elem) % len(bit_set) for h, func in hashes.items()]


for elem in elems_to_insert:
    insertion_indices = get_insertion_indices_of_elem(elem, hashes)
    print(f'Insertion indices for {elem}: {insertion_indices}')
    num_already_true = 0
    for i in insertion_indices:
        if not bit_set[i]:
            print(f'{elem} definitely not stored in bloom filter yet')
        else:
            num_already_true += 1
        bit_set[i] = True

    if len(insertion_indices) == num_already_true:
        # can have false positives. K hash functions together may have
        # produced the same insertion indices for two distinct elements,
        # e.g. B (66) and L (76). meaning all insertion indices already stored
        # true values for second insertion.
        print(f'{elem} MIGHT be stored in bloom filter already')
