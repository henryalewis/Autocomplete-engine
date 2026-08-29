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

    def search(self, prefix, k=10): # k = number of matches 
        # walk to the node where 'prefix' ends
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # collect (frequency, word) pairs below that node
        matches = []
        self._collect(node, prefix, matches)

        # rank by frequency (highest first), keep the top k.
        matches.sort(key=lambda pair: (-pair[0], pair[1]))
        return [word for freq, word in matches[:k]]

    def fuzzySearch(self, query, maxDistance=2, k=10):
        results = [] # distance, frequency, word
        firstRow = list(range(len(query) + 1)) # the seeded top row
        for char, child in self.root.children.items():
            self._fuzzy(child, char, char, query, firstRow, maxDistance, results)
        results.sort(key=lambda r: (r[0], -r[1], r[2]))
        return [(word, distance) for distance, freq, word in results[:k]]

    def _fuzzy(self, node, char, wordSoFar, query, previousRow, maxDistance, results):
        columns = len(query) + 1
        currentRow = [previousRow[0] + 1] # left column seed for this row
        for col in range(1, columns):
            fromLeft = currentRow[col - 1] + 1
            fromAbove = previousRow[col] + 1
            fromDiagonal = previousRow[col - 1] + (0 if query[col - 1] == char else 1)
            currentRow.append(min(fromLeft, fromAbove, fromDiagonal))
        if node.frequency > 0 and currentRow[-1] <= maxDistance:
            results.append((currentRow[-1], node.frequency, wordSoFar))
        if min(currentRow) <= maxDistance:
            for nextChar, child in node.children.items():
                self._fuzzy(child, nextChar, wordSoFar + nextChar, query, currentRow, maxDistance, results)

    def _collect(self, node, wordSoFar, matches):
        if node.frequency > 0:
            matches.append((node.frequency, wordSoFar))
        for char, child in node.children.items():
            self._collect(child, wordSoFar + char, matches)
