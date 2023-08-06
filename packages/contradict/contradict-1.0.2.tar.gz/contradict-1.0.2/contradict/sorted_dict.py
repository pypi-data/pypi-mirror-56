from hipster.min_heap import MinHeap
from hipster.max_heap import MaxHeap
from contradict.hashmap import Hashmap


class SortedDict(Hashmap):
    def __init__(self):
        super().__init__()
        self.min_heap = MinHeap()
        self.max_heap = MaxHeap()
        self.dict = {}

    def get(self, key):
        if key in self.dict:
            return self.dict[key]
        return None

    def set(self, key, value):
        self.dict[key] = value
        self.min_heap.push(key)
        self.min_heap.push(key)

    def contains(self, key):
        return key in self.dict

    def items(self, reverse=False):
        res = []
        temp = []
        if not reverse:
            while len(self.min_heap) > 0:
                curr = self.min_heap.pop()
                res.append((curr, self.dict[curr]))
                temp.append(curr)
            for t in temp:
                self.min_heap.push(t)
        else:
            while len(self.max_heap) > 0:
                curr = self.max_heap.pop()
                res.append((curr, self.dict[curr]))
                temp.append(curr)
            for t in temp:
                self.max_heap.push(t)
        return res

    def keys(self, reverse=False):
        res = []
        temp = []
        if not reverse:
            while len(self.min_heap) > 0:
                curr = self.min_heap.pop()
                res.append(curr,)
                temp.append(curr)
            for t in temp:
                self.min_heap.push(t)
        else:
            while len(self.max_heap) > 0:
                curr = self.max_heap.pop()
                res.append(curr)
                temp.append(curr)
            for t in temp:
                self.max_heap.push(t)
        return res

    def values(self, reverse=False):
        res = []
        temp = []
        if not reverse:
            while len(self.min_heap) > 0:
                curr = self.min_heap.pop()
                res.append(self.dict[curr])
                temp.append(curr)
            for t in temp:
                self.min_heap.push(t)
        else:
            while len(self.max_heap) > 0:
                curr = self.max_heap.pop()
                res.append(self.dict[curr])
                temp.append(curr)
            for t in temp:
                self.max_heap.push(t)
        return res


