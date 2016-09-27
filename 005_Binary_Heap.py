# Priority Queue(Heap) in 'Data Structure and Algorithm Analysis' P.182
#
# Instance variable:
#       _size:      The max number of elements that the heap could contain
#       _capacity:  The current number of elements in the heap
#       _elements:  The list that contains all the elements, and
#                   len(_elements) should be equal to _size + 1 for index 0
#                   is a dummy slot. (Initialized as `None`)
#
# Import Operations(methods):
#       Insert:     Insert a new element into the priority queue.
#                   Start from the last slot in the heap, percolating up to
#                   the node whose value is smaller than the inserted element.
#                   Continue swap the new slot's value with its parent's value.
#
#       DelMin:     Return the min value of the heap and delete it from the heap.
#                   Start from the root of the heap, percolating down to the
#                   node whose child node doesn't exist. Continue swap the slot's
#                   value with the smaller child's value.
#
#       DelMin is harder to be implemented than Insert. Because when percolating
#       down, we have to judge whether there exists a child and which child to swap,
#       while when percolating up, we need only concern about its unique parent.
#
#
# Tips: Any integer compare with None in Python would always return False
#           >>> 0 < None
#           False
#
# Binary Search Tree is much stricter than Binary Heap.
# Because left and right child of one node in the tree should
# obey different rule of binary search tree. While, in the binary
# heap, both children obey the same rule (larger than parents).
#
# Binary Heap is always a complete binary tree. No need to worry about
# balance problem.
#

class BinaryHeap(object):
    def __init__(self, maxsize):
        self._size = maxsize
        self._capacity = 0
        self._elements = [None for i in xrange(self._size+1)]

    @classmethod
    def creat_from_list(cls, in_list):
        """
        This is a classmethod, which creat a heap from input list.
        For convenience.

        >>> import random
        >>> test_list = range(100)
        >>> for i in xrange(5):
        ...     random.shuffle(test_list)
        ...     res = BinaryHeap.creat_from_list(test_list)
        ...     print res.findMin()
        ...
        0
        0
        0
        0
        0
        """
        this_heap = cls(int(len(in_list)*1.5))
        for element in in_list:
            this_heap.insert(element)
        return this_heap

    @property 
    def maxsize(self):
        """
        >>> test = BinaryHeap(12)
        >>> test.insertElements(range(12))
        >>> test.maxsize
        12
        >>> test = BinaryHeap(5)
        >>> test.maxsize
        5
        """
        return self._size

    @property 
    def length(self):
        """
        >>> test = BinaryHeap(12)
        >>> test.insertElements(range(12))
        >>> test.length
        12
        >>> test = BinaryHeap(5)
        >>> test.length
        0
        >>> test.insertElements([5,2,4])
        >>> test.length
        3
        """
        return self._capacity

    @property 
    def isEmpty(self):
        """
        >>> test = BinaryHeap(12)
        >>> test.isEmpty
        True
        >>> test.insertElements([4])
        >>> test.isEmpty
        False
        """
        return self._capacity == 0

    @property 
    def isFull(self):
        """
        >>> test = BinaryHeap(12)
        >>> test.isFull
        False
        >>> test.insertElements(range(12))
        >>> test.isFull
        True
        """
        return self._capacity == self._size

    def makeEmpty(self):
        """
        >>> test = BinaryHeap(12)
        >>> test.isFull
        False
        >>> test.insertElements(range(12))
        >>> test.isFull
        True
        >>> test.makeEmpty()
        >>> test.isEmpty
        True
        """
        self._elements = [None for i in xrange(self._size+1)]
        self._capacity = 0

    def insert(self, element):
        if self.isFull:
            raise ValueError('Heap is already full!')
        slot_index = self._capacity + 1
        # when slot_index == 1, then slot_index/2 == 0
        # at this time, self._elements[slot_index/2] == None
        # However, integetr < None would always return False
        while element < self._elements[slot_index/2]:
            self._elements[slot_index] = self._elements[slot_index/2]
            slot_index /= 2
        self._elements[slot_index] = element
        # update current capacity
        self._capacity += 1

    def insertElements(self, elements):
        if self._capacity + len(elements) > self._size:
            raise ValueError("Too many elements to be inserted")
        for element in elements:
            self.insert(element)

    def delMin(self):
        """
        Binary heap must be a complete binary tree.
        That is, all node except leaf must have left child.

        >>> import random
        >>> test_list = range(50)
        >>> test_heap = BinaryHeap(len(test_list))
        >>> for x in range(10):
        ...     random.shuffle(test_list)
        ...     test_heap.insertElements(test_list)
        ...     for i in xrange(test_heap.length):
        ...         if test_heap.delMin() != i:
        ...             print i, test_list
        ...         if test_heap.length != len(test_list)-i-1:
        ...             print i, test_list
        ...
        """
        if self.isEmpty:
            raise ValueError("Can't delete element from empty heap.")
        # get the first and the last elements
        # as well as empty the last slot
        min = self._elements[1]
        last = self._elements[self._capacity]
        self._elements[self._capacity] = None
        # update current capacity
        self._capacity -= 1

        # start percolating down
        # put the smaller child's value into parent's slot
        slot_index = 1
        while slot_index*2 <= self._capacity:
            # find the smaller child
            child = slot_index * 2
            if child != self._capacity and self._elements[child+1] < self._elements[child]:
                child += 1
            if last > self._elements[child]:
                self._elements[slot_index] = self._elements[child]
            else:
                break
            slot_index = child
        # put the last's value into the smaller child's slot
        self._elements[slot_index] = last
        return min

    def findMin(self):
        if self.isEmpty:
            raise ValueError("This is an empty Heap!! No min found!")
        return self._elements[1]

    def __str__(self):
        return self._elements.__str__()
    __repr__ = __str__


if __name__ == "__main__":
    import doctest, random
    doctest.testmod()