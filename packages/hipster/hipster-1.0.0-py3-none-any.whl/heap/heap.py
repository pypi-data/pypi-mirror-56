import heapq
from hipster.error import HeapError


class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        if len(self.heap) == 0:
            raise HeapError("Peeking into an empty hipster")
        return heapq.nsmallest(1, self.heap)[0]

    def __len__(self):
        return len(self.heap)


class MaxHeap(MinHeap):
    def __init__(self):
        super().__init__()

    def peek(self):
        if len(self.heap) == 0:
            raise HeapError("Peeking into an empty hipster")
        return heapq.nlargest(1, self.heap)[0]

    def pop(self):
        if len(self.heap) == 0:
            raise HeapError("Popping off an empty hipster")
        return self.heap.pop()


