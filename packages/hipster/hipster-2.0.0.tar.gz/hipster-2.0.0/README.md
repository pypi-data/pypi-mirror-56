Hipster
======================


## Description
Hipster provides a thread-safe implementation of the MinHeap and MaxHeap. For adding an object to the heap, the object needs to encapsulate it's comparison logic.
#### Object Usage
```
class CustomObject:
    def __init__(self, a, b):
        pass
    
    # The object needs to implement the following methods
    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass
    
    def __lt__(self, other):
            pass

    def __le__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass


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
##### 1.0.6
Added clear, fixed README
