class Stack(object):
    """Stack"""

    def __init__(self):
        self.items = []

    def is_empty(self):
        """is null"""
        return self.items == []

    def is_not_empty(self):
        """is null"""
        return self.items != []

    def push(self, item):
        """add item"""
        self.items.append(item)

    def pop(self):
        """pop item"""
        return self.items.pop()

    def peek(self):
        """pop item"""
        return self.items[len(self.items) - 1]

    def size(self):
        """return sie of stack"""
        return len(self.items)
