# Prefix Autocomplete

A prefix-search autocomplete engine in Python. Give it a list of words with
frequencies, then ask for the completions of any prefix — it returns the most
common matches first, the way a search box or IDE suggestion list does. It also
tolerates typos. It's built around a **trie** (prefix tree).

```
$ python main.py --prefix comp
  completions for 'comp': computer, complete, complex, computing, complexity, ...

$ python main.py --fuzzy pyton
  did you mean (<= 2 edits from 'pyton'): python (d=1)
```

## What it does right now

- **Loads a word-frequency list**, a plain `word<TAB>frequency` file, skipping
  blank lines and comments.
- **Inserts words into a trie**, accumulating frequency when a word appears more
  than once.
- **Ranked prefix search**, given a prefix, returns up to *k* completions
  ordered by frequency (most common first), so `comp` surfaces `computer`
  before `complexity`.
- **Typo-tolerant (fuzzy) search**, finds words within a small number of edits
  of the query, so a search for `pyton` still suggests `python`. It walks the
  trie while maintaining one row of the edit-distance table, so words that share
  a prefix share that computation, and branches that exceed the edit budget are
  pruned.

That's the whole of what's implemented so far. The compressed-tree variant
described under [Planned](#planned) is **not built yet**.

## Quick start

No third-party dependencies and the engine is pure Python standard library.

```bash
# one-shot: print completions for a prefix and exit
python main.py --prefix comp
python main.py --prefix te

# one-shot: fuzzy (typo-tolerant) search
python main.py --fuzzy pyton
python main.py --fuzzy progam --max-distance 1

# interactive: type a prefix, or prefix with ~ for fuzzy search
python main.py
```

By default it loads `data/sample_words.txt` (a small hand-built sample set with
lots of shared prefixes). Point it at a different file with `--data`.

## How it works

A trie stores words as a tree of single characters: each path from the root
spells out a prefix, and words that begin the same way share the same nodes near
the top.

- **Insert** walks down from the root one character at a time, creating any nodes
  that don't exist yet, and records the word's frequency on the final node. A
  node is marked as the end of a word by having a non-zero frequency, which means
  a word can also be a prefix of a longer one (`car` and `card` coexist cleanly).
- **Search** walks to the node where the prefix ends, then gathers every word in
  the subtree beneath it, rebuilding each word from the path taken. It sorts
  those matches by frequency and returns the top *k*.
- **Fuzzy search** computes edit (Levenshtein) distance between the query and
  the words in the trie, but shares work across common prefixes: it walks the
  trie carrying a single row of the dynamic-programming table, computing one new
  row per character. A branch is abandoned as soon as its best possible distance
  exceeds the allowed budget.

## Planned

These are the directions I'm taking the project next. **None of them are
implemented yet** as they're a roadmap, not a feature list:

- **Compressed radix tree**, a variant that collapses long single-child chains
  into one edge to use less memory on large datasets, plus a benchmark comparing
  it against the plain trie.
- **A larger, real-world dataset**, load a proper word-frequency corpus of
  hundreds of thousands of words and measure lookup performance at that scale.
- **A small web demo**, suggestions updating live as you type.
- **An automated test suite** covering the above.

## Project layout

```
autocomplete/
  __init__.py
  trie.py      # trie: insert, ranked prefix search, fuzzy search
  loader.py    # load "word<TAB>frequency" files
data/
  sample_words.txt   # small sample word-frequency dataset
main.py        # command-line demo
```