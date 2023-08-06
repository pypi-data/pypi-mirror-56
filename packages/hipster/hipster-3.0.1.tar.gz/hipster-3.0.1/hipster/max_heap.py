import heapq
from hipster.error import HeapError
from hipster.heap import Heap


class MaxHeap(Heap):
    def __init__(self):
        super().__init__()

    def peek(self):
        if len(self.heap) == 0:
            raise HeapError("Peeking into an empty heap")
        with self.read_lock:
            return heapq.nlargest(1, self.heap)[0]

    def pop(self):
        if len(self.heap) == 0:
            raise HeapError("Popping off an empty heap")
        with self.write_lock:
            return self.heap.pop()
