Poe[Trie]s
======================


## Description
Poetries provides a thread-safe implementation of a Trie. While not limited, but the most common use case of a Trie is in implementing  auto-completion. The collection type exposes APIs to perform the following operations```add```, ```find``` and ```get_all_words_with_prefix```.

## Dependencies
Python 3

## Installation
```
pip install --upgrade poetries
```

## Usage

```
from poetries.trie import Trie


trie = Trie()
trie.add('foobar')              # Adds 'foobar' to the trie
trie.find('foo')                # Returns False since the word is not present.
trie.add('bar')                 # Adds 'bar' to the trie
trie.find('bar')                # Returns True
trie.add('foob')                # Adds 'foob' to the trie
trie.add('foof')                # Adds 'foof' to the trie
arr = list(trie.prefix('foo'))  # Returns the list of words beginning with foo in a list form, ['foobar', 'foo', 'foob', 'foof']

```

## License
MIT

## Changelog



