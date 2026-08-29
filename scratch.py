from autocomplete import Trie, load_into

t = Trie()
load_into(t, "data/sample_words.txt")

print(t.fuzzySearch("pyton", maxDistance=2))   # wider budget -> more, nearest first
print(t.fuzzySearch("serch", maxDistance=1))    # missing 'a' -> search
print(t.fuzzySearch("zzz", maxDistance=1))       # nothing close -> []