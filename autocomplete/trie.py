"""A prefix tree (trie) for autocomplete."""

class TrieNode:
    def __init__(self):
        self.children = {} # character -> the TrieNode reached by that character
        self.frequency = 0 # 0 = no word ends here; a positive number = the word's frequency

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=1):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.frequency += frequency

    def search(self, prefix):
        # walk to the node where 'prefix' ends
        node = self.root
        for char in prefix:
            if char not in node.children:
                return[] # prefix not in the tree -> no completions
            node = node.children[char]

        # collect every word in the subtree below that ndoe
        results = []
        self._collect(node, prefix, results)
        return results

    def _collect(self, node, wordSoFar, results): #_collect is a private helper
        if node.frequency > 0:
            results.append(wordSoFar)
        for char, child in node.children.items():
            self._collect(child, wordSoFar + char, results)