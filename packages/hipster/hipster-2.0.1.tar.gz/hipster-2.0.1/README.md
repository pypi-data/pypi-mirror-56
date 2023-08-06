Hipster
======================


## Description
Hipster provides a thread-safe implementation of the MinHeap and MaxHeap. Each collection type provide a simple API to ```push```, ```pop```, ```peek``` and ```clear```.
The data structure is built on top of the ```heapq``` algorithm provided by Python.
#### Object Usage
For adding an object to the heap, the object needs to encapsulate it's comparison logic.
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
from hipster.heap import *

max_heap = MaxHeap()           # creates an empty max heap
max_heap.push(item)            # pushes a new item on the heap
item = max_heap.peek()         # returns the largest item from the heap without removing it
item = max_heap.pop()          # pops an item off the max heap
max_heap.clear()               # Removes all items from the heap
```

## License
MIT

## Changelog
##### 2.0.1
Updated object usage example, updated README
##### 2.0.0
Added thread safety
##### 1.0.6
Added clear, fixed README
