# -*- coding: utf-8 -*-
# Python 2
"""
"""

from random import randint
class BasicDisjointSet(object):
    """
    Use a tree to represent each set, since each element
    in a tree has the same root. The name of a set is given
    by the node at the root. Since only the name of the
    parent is required, we can assume that this tree is
    stored implicitly in an array: each `P[i]` in the array
    represents the parent of element `i`. If `i` is a root,
    then `P[i]` = 0.
    """
    def __init__(self, element_num):
        self._length = element_num
        self._data = [-1 for i in xrange(self._length)]
    def find(self, identity):
        """
        With path comprehension, recursively update all the nodes
        along the way to the root.
        """
        tmp = identity
        _stack = []
        while self._data[tmp]>=0:
            _stack.append(tmp)
            tmp = self._data[tmp]
        for _ in _stack:
            self._data[_] = tmp
        return tmp
    def union(self, i0, i1):
        """
        This original implementation has a fatal error!!
        1) Error 1: infinity loop problem
            test_set = BasicDisjointSet(10)
            test_set.union(8,9)
            test_set.union(9,8)
            If `test_set.find(8)` is performed, the program
            would run into infinity loop!
        2) Error 2: transitive problem
            test_set = BasicDisjointSet(10)
            test_set.union(8,9)
            test_set.union(7,8)
            If `test_set.union(2,9)` is performed, then
            `test_set.find(9)` would not be equal to `test_set.find(8)`,
            that is the code would remove element 9 from the original set.

        In order to fix it, check the root of the two element, and union
        the root instead of union the element.
        However, this fix would make union slower than O(1).
        """
        if i0 == i1:
            raise ValueError("Must union two distinct element!")
        p0, p1 = self.find(i0), self.find(i1)
        if p0 == p1:
            return
        self._data[p1] = p0


class SmartUnionBySize(BasicDisjointSet):
    """
    When `union()`, always make the smaller tree a subtree of the larger.
    If Unions are done by size, the depth of any node is never more than logN.

    To implement this strategy, we store the size of the tree as a
    negative number in the `_data` array.
    """
    def union(self, i0, i1):
        if i0 == i1:
            raise ValueError("Must union two distinct element!")
        p0, p1 = self.find(i0), self.find(i1)
        if p0 == p1:
            return
        if self._data[p0] < self._data[p1]:
            # tree p0 got more element, append p1 to p0
            self._data[p0] += self._data[p1]
            self._data[p1] = p0
        else: # if self._data[p0] > self._data[p1]:
            self._data[p1] += self._data[p0]
            self._data[p0] = p1

class SmartUnionByHeight(BasicDisjointSet):
    def find(self, identity):
        """
        Not compatible with path comprehension.
        """
        tmp = identity
        while self._data[tmp]>=0:
            tmp = self._data[tmp]
        if identity != tmp:
            self._data[identity] = tmp
        return tmp
    def union(self, i0, i1):
        if i0 == i1:
            raise ValueError("Must union two distinct element!")
        p0, p1 = self.find(i0), self.find(i1)
        if p0 == p1:
            return
        if self._data[p0] < self._data[p1]:
            # tree p0 is higher, append p1 to p0
            self._data[p1] = p0
        else: #if self._data[p0] > self._data[p1]:
            # tree p1 is higher, append p0 to p1
            if self._data[p0] == self._data[p1]:
                self._data[p1] -= 1
            self._data[p0] = p1




def disjoint_set_test(class_name=BasicDisjointSet):
    def random_test(test_set):
        for i in xrange(5):
            try:
                test_set.union(randint(0,9), randint(0,9))
            except ValueError:
                pass
        for i in xrange(10):
            assert test_set._data[test_set.find(i)] < 0

    test_lengths = [0,1,10,100,100]
    for test_length in test_lengths:
        test_set = class_name(test_length)
        if test_length <= 1:
            print "test_length == 1 passed!"
            continue
        if test_length >= 10:
            for i in xrange(9):
                assert test_set.find(i) != test_set.find(i+1)
            test_set.union(0,9)
            assert test_set.find(0) == test_set.find(9)
            test_set.union(1,8)
            assert test_set.find(1) == test_set.find(8)
            test_set.union(2,5)
            test_set.union(0,5)
            test_set.union(5,1)
            assert test_set.find(5) == test_set.find(0)
            assert test_set.find(5) == test_set.find(9)
            assert test_set.find(1) == test_set.find(2)
            for i in xrange(9):
                assert test_set.find(i) == test_set.find(i)
            for i in xrange(10):
                random_test(test_set)
            print "test_length == 10 passed!"
        if test_length >= 100:
            test_set.union(99,98)
            test_set.union(98,97)
            assert test_set.find(99) == test_set.find(97)
            test_set.union(1,99)
            assert test_set.find(99) == test_set.find(0)
            assert test_set.find(99) == test_set.find(1)
            assert test_set.find(99) == test_set.find(2)
            assert test_set.find(99) == test_set.find(5)
            assert test_set.find(99) == test_set.find(8)
            assert test_set.find(99) == test_set.find(9)
            assert test_set.find(97) == test_set.find(0)
            assert test_set.find(97) == test_set.find(1)
            assert test_set.find(97) == test_set.find(2)
            assert test_set.find(97) == test_set.find(5)
            assert test_set.find(97) == test_set.find(8)
            assert test_set.find(97) == test_set.find(9)
            if class_name == SmartUnionBySize:
                count = 1
                for elem in test_set._data:
                    if elem >= 0:
                        count +=1
                assert count == -min(test_set._data)
            print "test_length == 100 passed!"

if __name__ == '__main__':
    test = BasicDisjointSet(10)
    for i in xrange(10):
        print test.find(i)
    print test._data
    test.union(0,1)
    test.union(1,0)
    print test.find(0), test.find(1)
    print test._data
    algorithms = [BasicDisjointSet,SmartUnionBySize,SmartUnionByHeight]
    for algor in algorithms:
        disjoint_set_test(class_name=algor)