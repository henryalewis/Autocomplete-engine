"""Load "word<TAB>frequency" files into a trie or radix tree."""

from __future__ import annotations

from pathlib import Path

def load_into(structure, path: Path) -> int:
    """Insert every "word<TAB>frequency" line from 'path' into 'structure'.
    
    Blank lines and lines starting with '#' are skipped. 
    Returns the number of words inserted.
    """

    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            word, frequency = line.split("\t")
            structure.insert(word, int(frequency))
            count += 1
    return count

