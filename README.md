

https://github.com/user-attachments/assets/4b17dc2b-5182-4214-9c47-665c6fff85b2

# Digital Library System

A digital library engine that indexes books and supports fast keyword search — built two ways, using a sort-based approach and a hash table implemented from scratch, to compare the two.

## What It Does

- Extracts the set of **distinct words** in each book
- Supports **keyword search** — find every book containing a given word

## Two Approaches

**1. Sorting (Merge Sort + Binary Search)**
A custom merge sort dedupes words during the merge step. Books stay sorted by title, enabling O(log k) binary search lookups.

**2. Hashing (Custom Hash Table)**
- Hand-written **polynomial rolling hash** — no built-in hash functions used
- Each book gets its own independent hash table
- Three collision strategies implemented side by side: **chaining**, **linear probing**, **double hashing**
- **Dynamic resizing** — the table grows to the next prime size once load factor passes 0.5, keeping operations close to O(1) on average

## Complexity

| Operation | Sort-based | Hash-based (avg) |
|---|---|---|
| Build index | O(kW log W) | O(W)/book |
| Distinct words | O(D + log k) | O(D) |
| Keyword search | O(k log D) | O(k) |

Where k = books, W = words per book, D = distinct words per book.

## Files

- `hash_table.py` — HashSet and HashMap with three collision strategies
- `dynamic_hash_table.py` — dynamic resizing variants
- `library.py` — MuskLibrary (sorting) and JGBLibrary (hashing)
- `library_digitalization.cpp` — full C++ implementation
- `checker.py`, `big_tester.py` — test and verification scripts

## Limitations

- No deletion support in either implementation
- No formal benchmarks comparing the three collision strategies

## Tech Stack
Python, C++

## Usage
```bash
python main.py
# or
g++ -std=c++17 library_digitalization.cpp -o library && ./library
```
