# Autocomplete Engine

A prefix-search autocomplete engine in Python, built up from a plain trie to a compressed radix tree. It returns **frequency-ranked** completions, tolerates **typos** via bounded edit distance, and includes a **benchmark** showing the radix tree's memory savings over a naive trie.

```
> comp
  completions for 'comp': computer, complete, complex, computing, complexity, ...
> ~pyton
  did you mean (<= 2 edits from 'pyton'): python (d=1)
```

## Why this exists

Autocomplete is a great small-scale systems problem: it starts with one data structure (the trie) and naturally grows into questions about ranking, approximate matching, and memory which the same questions real search boxes, IDEs, and phone keyboards have to answer.

## Features

| Tier | Feature | Where |
|------|---------|-------|
| 0 | Core trie: insert + prefix lookup | `autocomplete/trie.py` |
| 1 | Frequency-ranked suggestions (top-k) | `Trie.search` |
| 2 | Typo-tolerant fuzzy search (bounded edit distance) | `Trie.fuzzy_search` |
| 3 | Compressed **radix tree** for lower memory | `autocomplete/radix.py` |

## Quick start

```bash
# no third-party runtime deps; pytest is only needed for the tests
pip install -r requirements.txt

# interactive demo (type a prefix; prefix with ~ for fuzzy search)
python main.py

# one-shot
python main.py --prefix comp
python main.py --fuzzy pyton --max-distance 2

# trie vs radix tree comparison
python benchmark.py

# run the tests
python -m pytest
```

## How it works

**Trie (Tiers 0–2).** Each node holds one character; a path from the root spells a prefix. `search` walks to the node ending the prefix, gathers every word in that subtree, and returns the top *k* by frequency using a heap (`O(n log k)` rather than fully sorting).

**Fuzzy search (Tier 2).** `fuzzy_search` finds every word within a set number of edits (insertions, deletions, substitutions) of the query. It walks the trie while maintaining a single row of the Levenshtein dynamic-programming table. Because words that share a prefix share the top of that table, each shared prefix is scored once instead of re-running edit distance against every word; branches are pruned as soon as their best possible distance exceeds the budget.

**Radix tree (Tier 3).** A plain trie stores `international` as a chain of 13 single-child nodes. A radix (Patricia) tree collapses any such chain into one edge carrying the whole substring, so it uses far fewer nodes. The trade-off is harder insertion: when a new word partially matches an existing edge, that edge has to be **split**. `RadixTree` exposes the same ranked `search` as `Trie`, and a test asserts the two return identical results.

## Benchmark

Loading the 84-word sample set into both structures
(`python benchmark.py`):

```
                        Trie   RadixTree
nodes                    280         119
lookup (us)            10.75        6.86

Radix tree uses 57.5% fewer nodes than the plain trie.
```

Node count is a proxy for memory footprint; the reduction grows with dataset size and with how many words share prefixes. (Numbers vary by machine; rerun locally.)

## Project layout

```
autocomplete/
  trie.py      # trie: ranked search + fuzzy search  (Tiers 0-2)
  radix.py     # compressed radix tree               (Tier 3)
  loader.py    # load "word<TAB>frequency" files
tests/         # pytest suite (trie, radix, equivalence)
data/          # sample word-frequency dataset
benchmark.py   # trie vs radix comparison
main.py        # interactive / CLI demo
```

## Future work (Tiers 4–5)

- **Tier 4 — scale & persistence.** Load a real word-frequency dataset
  (hundreds of thousands of words), save/load the structure to disk, and
  benchmark lookup latency at that scale.
- **Tier 5 — live demo.** A small REST API (Flask/FastAPI) behind a web page
  that shows suggestions as you type, so the project is clickable.
- **Precomputed top-k per node** to make hot-prefix lookups `O(k)`.
- **Fuzzy search over the radix tree** (the DP row has to advance across
  multi-character edge labels) — a nice extension for a stronger project.

## License

MIT