"""Compare the plain trie and the compressed radix tree.

Loads the sample dataset into both structures and reports node counts (a proxy
for memory) and average lookup latency. Run with:

    python benchmark.py
    python benchmark.py path/to/bigger_wordlist.txt
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from autocomplete import Trie, RadixTree, load_into

DEFAULT_DATA = Path(__file__).parent / "data" / "sample_words.txt"


def time_lookups(structure, prefixes, repeats: int = 2000) -> float:
    """Average seconds per `search` call, in microseconds."""
    start = time.perf_counter()
    for _ in range(repeats):
        for prefix in prefixes:
            structure.search(prefix, k=10)
    elapsed = time.perf_counter() - start
    calls = repeats * len(prefixes)
    return (elapsed / calls) * 1_000_000  # microseconds per call


def main() -> None:
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DATA

    trie, radix = Trie(), RadixTree()
    n = load_into(trie, data_path)
    load_into(radix, data_path)

    trie_nodes = trie.count_nodes()
    radix_nodes = radix.count_nodes()
    reduction = (1 - radix_nodes / trie_nodes) * 100

    prefixes = ["te", "comp", "pro", "auto", "dev", "a", "co", "se"]
    trie_us = time_lookups(trie, prefixes)
    radix_us = time_lookups(radix, prefixes)

    print(f"Dataset: {data_path.name}  ({n} words)\n")
    print(f"{'':16}{'Trie':>12}{'RadixTree':>12}")
    print(f"{'nodes':16}{trie_nodes:>12,}{radix_nodes:>12,}")
    print(f"{'lookup (us)':16}{trie_us:>12.2f}{radix_us:>12.2f}")
    print(f"\nRadix tree uses {reduction:.1f}% fewer nodes than the plain trie.")


if __name__ == "__main__":
    main()
