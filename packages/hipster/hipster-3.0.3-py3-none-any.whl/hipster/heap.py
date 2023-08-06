import abc
import heapq
from readerwriterlock import rwlock

from hipster.error import HeapError


class Heap(abc.ABC):
    def __init__(self):
        self.heap = []
        lock = rwlock.RWLockFair()
        self.read_lock = lock.gen_rlock()
        self.write_lock = lock.gen_wlock()

    def push(self, item):
        with self.write_lock:
            heapq.heappush(self.heap, item)

    @abc.abstractmethod
    def pop(self):
        pass

    @abc.abstractmethod
    def peek(self):
        pass

    def remove(self, item):
        store = []
        found = False
        with self.write_lock:
            while len(self.heap) > 0:
                curr = self.heap.pop()
                if curr == item:
                    found = True
                    break
                else:
                    store.append(curr)
            if not found:
                raise HeapError("Item not in Heap")
            while len(store) > 0:
                heapq.heappush(self.heap, store.pop())

    def clear(self):
        with self.write_lock:
            del self.heap[:]

    def __copy__(self):
        with self.write_lock:
            self.heap.copy()

    def __len__(self):
        with self.read_lock:
            return len(self.heap)
