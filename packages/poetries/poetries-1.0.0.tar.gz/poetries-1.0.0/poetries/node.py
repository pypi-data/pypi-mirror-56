class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

    def all_words(self, prefix):
        if self.end_of_word:
            yield prefix

        for letter, child in self.children.items():
            yield from child.all_words(prefix + letter)
