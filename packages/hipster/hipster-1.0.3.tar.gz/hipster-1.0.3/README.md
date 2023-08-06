# Hipster

Hipster provides a simple implementation of the MinHeap and MaxHeap. The object being added to the respective heaps need to implement the comparator logic. The APIs are identical for MinHeap and MaxHeap

## Installation
Use pip to install the module
- ```pip install hipster```

## Usage
- ```>>> from hipster.heap import MaxHeap```
- ```>>> max_heap = MaxHeap()```
- ```>>> max_heap.push(6)```
- ```>>> max_heap.push(9)```
- ```>>> max_heap.push(3)```
- ```>>> max_heap.peek()```
- ```>>> 9```
- ```>>> max_heap.pop()```
- ```>>> 9```
- ```>>> max_heap.pop()```
- ```>>> 6```



