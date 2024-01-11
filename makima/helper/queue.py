from collections import deque


class Queue(object):
    """Queue"""

    def __init__(self):
        self.items = deque()

    def peek(self):
        """Return the front item from the queue without removing it"""
        return self.items[0] if self.items else None

    def is_empty(self):
        """Check if the queue is empty"""
        return not self.items

    def is_not_empty(self):
        """Check if the queue is not empty"""
        return bool(self.items)

    def push(self, item):
        """Enqueue item"""
        self.items.append(item)

    def pop(self):
        """Dequeue item"""
        return self.items.popleft()

    def size(self):
        """Return size of queue"""
        return len(self.items)
