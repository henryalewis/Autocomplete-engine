from autocomplete import Trie, load_into

t = Trie()
count = load_into(t, "data/sample_words.txt")
print(f"loaded {count} words")

results = t.search("comp")
print(f"{len(results)} completions for 'comp':")
print(sorted(results))