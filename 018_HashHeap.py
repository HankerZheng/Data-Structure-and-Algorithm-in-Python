# !/usr/bin/python

# This is the Python implementation of Hash Heap based on the list implementation 
# of binary heap. The difference between Hash Heap and Binary Heap is that Hash
# Heap supports the `heapRemove` operation in O(log n) time and can check whether
# certain element is in the Hash Heap or not in O(1) time.
# 
# Basic automatic tests are given in `pushpopTest()` and `removeTest()`.
# Note: It may takes about 10 seconds to run both test functions.

import random

class HeapNode(object):
    """
    The node in the HashHeap to deal with duplicates.
    Each node store the value of each element and the number of duplicates
    with the same value.
    """
    def __init__(self, val, cnt):
        self.val = val
        self.cnt = cnt

    def __cmp__(self, other):
        return self.val - other.val

    def __str__(self):
        return "[%s, %d]" % (self.val, self.cnt)
    __repr__ = __str__

class HashHeap(object):
    """
    This HashHeap is the same as the list implementation of binary heap, but with
    a hashMap to map the value of one elemnt to its index in the list.
    """
    def __init__(self, arr):
        """
        `_cap` - the number of elements in the HashHeap
        `_maxIdx` - the max index of the binary heap
        `_data` - the list implementation of the binary heap
        `_hashMap` - mapping the element to its index in the binary heap
        """
        elemCnt = self._preProcess(arr)
        self._cap = len(arr)
        self._maxIdx = len(elemCnt) - 1
        self._data = [HeapNode(key, value) for key, value in elemCnt.items()]
        self._hashMap = {node.val: idx for idx, node in enumerate(self._data)}
        self._heapify()

    def _preProcess(self, arr):
        """
        Convert the input array into a dict object.
        The key to the dict is the value of the element.
        The value of the dict is the occurence of each element.
        """
        elemCnt = {}
        for elem in arr:
            elemCnt[elem] = elemCnt.get(elem, 0) + 1
        return elemCnt

    def _swap(self, idx1, idx2):
        """
        Swap the 2 elements in the heap.
        Also, change the index stored in `self._hashMap`
        """
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
            if left > self._maxIdx:
                return True
            if right > self._maxIdx:
                return self._data[idx] <= self._data[left]
            return self._data[idx] <= self._data[left] and self._data[idx] <= self._data[right]
        def smallerChild(idx):
            left, right = idx * 2 + 1, idx * 2 + 2
            if left > self._maxIdx:
                return None
            if right > self._maxIdx:
                return left
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
        elif idx == self._maxIdx:
            # the node itself is the last node
            self._removeLastNode()
        else:
            self._swap(idx, self._maxIdx)
            self._removeLastNode()
            pidx = (idx - 1) / 2
            # check to see we should sift up or sift down
            if pidx >= 0 and self._data[pidx] > self._data[idx]:
                self._siftUp(idx)
            else:
                self._siftDown(idx)
        return retVal

    @property
    def length(self):
        """
        Return the number of elements in the Hash Heap
        """
        return self._cap

    def heapPeep(self):
        """
        Return the MIN element in the Hash Heap
        """
        if not self._data:
            return float("inf")
        return self._data[0].val

    def heapPop(self):
        """
        Remove the MIN element from the Hash Heap and return its value
        """
        return self._removeByIdx(0)

    def heapPush(self, elem):
        """
        Push a new element into the Hash Heap
        """
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
        """
        Remove a existing element from the Hash Heap
        If the element to be removed is not in the Hash Heap, raise an error.
        """
        if elem not in self._hashMap:
            raise ValueError("Element to be removed is not in HashHeap!!!")
        idx = self._hashMap[elem]
        self._removeByIdx(idx)

    def __contains__(self, value):
        return value in self._hashMap

    def __str__(self):
        return "%s" % [elem.val for elem in self._data]
    __repr__ = __str__


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
            assert len(testList) == thisHeap.length
            assert len(thisHeap._hashMap) == thisHeap._maxIdx + 1
        testList.sort()
        assert len(testList) == thisHeap.length
        for idx, num in enumerate(testList):
            assert num == thisHeap.heapPop()
            assert len(testList) - 1 - idx == thisHeap.length
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
            assert len(testList) == thisHeap.length
            assert len(thisHeap._hashMap) == thisHeap._maxIdx + 1
        testList.sort()
        assert len(testList) == thisHeap.length
        for idx, num in enumerate(testList):
            assert num == thisHeap.heapPop()
            assert len(testList) - 1 - idx == thisHeap.length
            assert len(thisHeap._hashMap) == thisHeap._maxIdx + 1


if __name__ == '__main__':
    pushpopTest()
    removeTest()