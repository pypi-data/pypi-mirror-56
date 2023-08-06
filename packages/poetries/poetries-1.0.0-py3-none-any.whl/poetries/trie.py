from poetries.node import TrieNode
from readerwriterlock import rwlock


class Trie:
    def __init__(self):
        self.root = TrieNode()
        lock = rwlock.RWLockFair()
        self.read_lock = lock.gen_rlock()
        self.write_lock = lock.gen_wlock()

    def add(self, word):
        with self.write_lock:
            curr = self.root
            for letter in word:
                node = curr.children.get(letter)
                if not node:
                    node = TrieNode()
                    curr.children[letter] = node
                curr = node
            curr.end_of_word = True

    def find(self, word):
        with self.read_lock:
            curr = self.root
            for w in word:
                node = curr.children.get(w)
                if not node:
                    return False
                curr = node
            return curr.end_of_word

    def all_words_with_prefix(self, prefix):
        with self.read_lock:
            cur = self.root
            for c in prefix:
                cur = cur.children.get(c)
                if cur is None:
                    return  # No words with given prefix
            yield from cur.all_words(prefix)


