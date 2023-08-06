import heapq
from hipster.error import HeapError
from readerwriterlock import rwlock


class MinHeap:
    def __init__(self):
        self.heap = []
        lock = rwlock.RWLockFair()
        self.read_lock = lock.gen_rlock()
        self.write_lock = lock.gen_wlock()

    def push(self, item):
        with self.write_lock:
            heapq.heappush(self.heap, item)

    def pop(self):
        if len(self.heap) == 0:
            raise HeapError("Popping off an empty heap")
        with self.write_lock:
            return heapq.heappop(self.heap)

    def peek(self):
        if len(self.heap) == 0:
            raise HeapError("Peeking into an empty heap")
        with self.read_lock:
            return heapq.nsmallest(1, self.heap)[0]

    def clear(self):
        with self.write_lock:
            del self.heap[:]

    def __len__(self):
        with self.read_lock:
            return len(self.heap)


class MaxHeap(MinHeap):
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
