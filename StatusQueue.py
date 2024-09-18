from collections import deque
from dataclasses import dataclass

@dataclass
class P_info:
    hw_ratio: float
    status: str


class StatusQueue:
    def __init__(self, maxlen=None):
        self.queue = deque(maxlen=maxlen)

    def enqueue(self, hw_ratio, status):
        self.queue.append(P_info(hw_ratio, status))

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def peek(self):
        if self.queue:
            return self.queue[0]
        return None

    def size(self):
        return len(self.queue)

    def is_full(self):
        if self.queue.maxlen is not None:
            return len(self.queue) == self.queue.maxlen
        return False

    def is_empty(self):
        return len(self.queue) == 0
    
    def get_by_index(self, index):
        if 0 <= index < len(self.queue):
            return self.queue[index]
        raise IndexError("Index out of range")


"""
sq = StatusQueue(maxlen=6)
sq.enqueue(0.5, 'standing')
sq.enqueue(0.8, 'standing')
sq.enqueue(0.75, 'standing')
sq.enqueue(0.4, 'lying')
sq.enqueue(0.3, 'lying')
sq.enqueue(0.2, 'lying')


s0 = sq.get_by_index(0)
s1 = sq.get_by_index(1)
s2 = sq.get_by_index(2)
s3 = sq.get_by_index(3)
s4 = sq.get_by_index(4)
s5 = sq.get_by_index(5)
"""