import random

class HeapNode(object):
    def __init__(self, val, cnt):
        self.val = val
        self.cnt = cnt

    def __cmp__(self, other):
        return self.val - other.val

    def __str__(self):
        return "[%s, %d]" % (self.val, self.cnt)
    __repr__ = __str__

class HashHeap(object):
    def __init__(self, arr):
        elemCnt = self._preProcess(arr)
        self._cap = len(arr)
        self._maxIdx = len(elemCnt) - 1
        self._data = [HeapNode(key, value) for key, value in elemCnt.items()]
        self._hashMap = {node.val: idx for idx, node in enumerate(self._data)}
        self._heapify()

    def _preProcess(self, arr):
        elemCnt = {}
        for elem in arr:
            elemCnt[elem] = elemCnt.get(elem, 0) + 1
        return elemCnt

    def _swap(self, idx1, idx2):
        elem1, elem2 = self._data[idx1], self._data[idx2]
        self._hashMap[elem1.val] = idx2
        self._hashMap[elem2.val] = idx1
        self._data[idx1], self._data[idx2] = elem2, elem1

    def _heapify(self):
        idx = self._maxIdx
        while idx > 0:
            parentIdx = (idx - 1) / 2
            if self._data[parentIdx] > self._data[idx]:
                self._swap(parentIdx, idx)
                self._siftDown(idx)
            idx -= 1

    def _siftDown(self, idx):
        def heapValid(idx):
            left, right = idx * 2 + 1, idx * 2 + 2
            if left > self._maxIdx: return True
            if right > self._maxIdx: return self._data[idx] <= self._data[left]
            return self._data[idx] <= self._data[left] and self._data[idx] <= self._data[right]
        def smallerChild(idx):
            left, right = idx * 2 + 1, idx * 2 + 2
            if left > self._maxIdx: return None
            if right > self._maxIdx: return left
            return left if self._data[left] < self._data[right] else right

        current = idx
        while not heapValid(current):
            child = smallerChild(current)
            self._swap(current, child)
            current = child

    def _siftUp(self, idx):
        current = idx
        parent = (current - 1) / 2
        while current > 0 and self._data[parent] > self._data[current]:
            self._swap(parent, current)
            current = parent
            parent = (current - 1) / 2

    def _removeLastNode(self):
        rmNode = self._data.pop(-1)
        self._cap -= 1
        self._maxIdx -= 1
        self._hashMap.pop(rmNode.val)

    def _removeByIdx(self, idx):
        thisNode = self._data[idx]
        retVal = thisNode.val
        if thisNode.cnt > 1:
            thisNode.cnt -= 1
            self._cap -= 1
        else:
            self._swap(idx, self._maxIdx)
            self._removeLastNode()
            self._siftDown(idx)
        return retVal

    def heapPeep(self):
        if not self._data:
            return float("inf")
        return self._data[0].val

    def heapPop(self):
        return self._removeByIdx(0)

    def heapPush(self, elem):
        self._cap += 1
        if elem not in self._hashMap:
            self._maxIdx += 1
            self._data.append(HeapNode(elem, 1))
            self._hashMap[elem] = self._maxIdx
            self._siftUp(self._maxIdx)
        else:
            idx = self._hashMap[elem]
            self._data[idx].cnt += 1
        
    def heapRemove(self, elem):
        if elem not in self._hashMap:
            raise ValueError("Element to be removed is not in HashHeap!!!")
        idx = self._hashMap[elem]
        self._removeByIdx(idx)

    def __contains__(self, value):
        return value in self._hashMap
    def __str__(self):
        return "%s" % [elem.val for elem in self._data]


def pushpopTest():
    """
    Randomly generate a list, and push each element into the heap.
    Test HeapPush by comparing the first element in the heap with the 
    smallest element in the List.
    Test HeapPop by comparing the popped element from the heap with the
    sorted list one by one. 
    """
    for _ in xrange(100):
        thisHeap = HashHeap([0])
        testList = [0]
        for i in xrange(1000):
            thisRandom = random.randrange(-100, 100000)
            thisHeap.heapPush(thisRandom)
            testList.append(thisRandom)
            assert min(testList) == thisHeap.heapPeep()
            assert len(testList) == thisHeap._cap
            assert len(thisHeap._hashMap) == thisHeap._maxIdx + 1
        testList.sort()
        assert len(testList) == thisHeap._cap
        for idx, num in enumerate(testList):
            assert num == thisHeap.heapPop()
            assert len(testList) - 1 - idx == thisHeap._cap
            assert len(thisHeap._hashMap) == thisHeap._maxIdx + 1

def removeTest():
    """
    Randomly generate a list, and push each element into the heap.
    Test HeapRemove by randomly delete one element from the heap by the probability
    of 0.2, and then check whether the first element in the heap is the same as the
    smallest element in the list.
    """
    for _ in xrange(100):
        thisHeap = HashHeap([0])
        testList = [0]
        for i in xrange(1000):
            thisRandom = random.randrange(-100, 100000)
            thisHeap.heapPush(thisRandom)
            if random.random() < 0.2:
                thisHeap.heapRemove(thisRandom)
            else:
                testList.append(thisRandom)
            assert min(testList) == thisHeap.heapPeep()
            assert len(testList) == thisHeap._cap
            assert len(thisHeap._hashMap) == thisHeap._maxIdx + 1
        testList.sort()
        assert len(testList) == thisHeap._cap
        for idx, num in enumerate(testList):
            assert num == thisHeap.heapPop()
            assert len(testList) - 1 - idx == thisHeap._cap
            assert len(thisHeap._hashMap) == thisHeap._maxIdx + 1

if __name__ == '__main__':
    pushpopTest()
    removeTest()

