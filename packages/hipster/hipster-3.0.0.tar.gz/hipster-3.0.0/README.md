Hipster
======================


## Description
Hipster provides a thread-safe implementation of the MinHeap and MaxHeap. Each collection type exposes a simple API to ```push```, ```pop```, ```peek``` , ```remove``` and ```clear```.
The data structure is built on top of the ```heapq``` algorithm.
#### Object Usage
For adding an object to the heap, the object needs to implement it's comparator logic.
```
class GitRepo:
    def __init__(self, url, stars, forks):
        self.url = url
        self.stars = stars
        self.forks = forks
    
    # The object needs to implement the following methods
    def __eq__(self, other):
        return self.name == other.name and self.stars == other.stars and self.forks == other.forks

    def __ne__(self, other):
        return self.name != other.name or self.stars != other.stars or self.forks != other.forks
    
    def __lt__(self, other):
        # The two repos are first compared based on stars then forks and then sorted lexically based on url
        if self.stars == other.stars and self.forks == other.forks return self.url < other.url

    def __le__(self, other):
        if self.stars == other.stars and self.forks == other.forks return self.url <= other.url

    def __gt__(self, other):
        if self.stars == other.stars and self.forks == other.forks return self.url > other.url

    def __ge__(self, other):
        if self.stars == other.stars and self.forks == other.forks return self.url >= other.url


```

## Dependencies
Python 3

## Installation
```
pip install --upgrade hipster
```

## Usage

```
from hipster.max_heap import MaxHeap
from hipster.min_heap import MinHeap

max_heap = MaxHeap()           # Creates an empty MaxHeap
max_heap.push(item)            # Pushes a new item on the MaxHeap
item = max_heap.peek()         # Returns the largest item from the heap without removing it, throws HeapError when called on an empty Heap
item = max_heap.pop()          # Pops an item off the MaxHeap, throws HeapError when called on an empty Heap
max_heap.remove(item)          # Removes the item from the heap if its present, or throws HeapError if the item is not present
max_heap.clear()               # Removes all items from the heap


min_heap = MinHeap()           # Creates an empty MinHeap
min_heap.push(item)            # Pushes a new item on the MinHeap
item = min_heap.peek()         # Returns the samllest item from the heap without removing it, throws HeapError when called on an empty Heap
item = min_heap.pop()          # Pops an item off the MinHeap, throws HeapError when called on an empty Heap
min_heap.remove(item)          # Removes the item from the heap if its present, or throws HeapError if the item is not present
min_heap.clear()               # Removes all items from the heap
```

## License
MIT

## Changelog
##### 3.0.0
Added remove, refactored duplicated code to base class, added more tests, updated README
##### 2.0.2
fixed README
##### 2.0.1
Updated object usage example, updated README
##### 2.0.0
Added thread safety, added more tests

