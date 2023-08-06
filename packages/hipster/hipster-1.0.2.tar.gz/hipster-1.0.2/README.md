# Hipster

Hipster provides a simple implementation of the MinHeap and MaxHeap. The object being added to the respective heaps need to implement the comparator logic. The APIs are identical for MinHeap and MaxHeap

## Usage
- ```pip install hipster```
- ```from hipster.heap import MaxHeap```
- ```max_heap = MaxHeap()```
- ```max_heap.push(item)```
- ```r = max_heap.peek()``` # Returns the item without popping it off the heap
- ```r = max_heap.pop()``` # Returns the item and pops it off the heap


