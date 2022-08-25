# Disjoint Set Union
class DSU:
    def __init__(self):
        self.sizes = []
        self.parents = []

    def init(self, size):
        self.sizes = [-1] * size
        self.parents = [0] * size
        for i in range(size):
            self.parents[i] = i

    def find(self, node):
        # finds the root of the set
        while node != self.parents[node]:
            node = self.parents[node]
        return node

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    def size(self, node):
        return -self.sizes[self.find(node)]

    def merge(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.sizes[x] > self.sizes[y]:
            x, y = y, x
        self.parents[y] = x
        self.sizes[x] += self.sizes[y]
        return True
