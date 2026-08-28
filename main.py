"""Command-line demo for the autocomplete engine.

Interactive:
    python main.py

One-shot (non-interactive):
    python main.py --prefix comp

Loads data/sample_words.txt by default; pass --data to use another file.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from autocomplete import Trie, load_into

DEFAULT_DATA = Path(__file__).parent / "data" / "sample_words.txt"


def show(trie: Trie, prefix: str) -> None:
    results = trie.search(prefix, k=10)
    if results:
        print(f"  completions for '{prefix}': " + ", ".join(results))
    else:
        print(f"  no completions for '{prefix}'")


def interactive(trie: Trie) -> None:
    print("Autocomplete demo. Type a prefix and press Enter. Ctrl-C to quit.\n")
    try:
        while True:
            text = input("> ").strip()
            if not text:
                continue
            show(trie, text.lower())
    except (KeyboardInterrupt, EOFError):
        print("\nbye")


def main() -> None:
    parser = argparse.ArgumentParser(description="Autocomplete engine demo")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--prefix", help="print completions and exit")
    args = parser.parse_args()

    trie = Trie()
    count = load_into(trie, args.data)

    if args.prefix is not None:
        show(trie, args.prefix.lower())
    else:
        print(f"Loaded {count} words from {args.data.name}.\n")
        interactive(trie)


if __name__ == "__main__":
    main()