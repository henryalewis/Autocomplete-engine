from autocomplete import Trie, load_into

t = Trie()
load_into(t, "data/sample_words.txt")

print(t.search("comp", k=5))
print(t.search("te", k=5))
print(t.search("auto"))