# A Fenwick tree or Binary Indexed Tree is a data structure that can efficiently update
# elements and calculate prefix sums in a table of number.
# 
# When compared with a flat array of numbers, the Fenwick tree achieves much higher
# performance for two operations: element update and prefix sum calculation. In a flat
# array of n numbers, calculating prefix sum and updating the elements both require O(n)
# time. Fenwick trees allow both operations to be performed on O(log n) time. This is
# archieved by representing the numbers as a tree, where the value of each node is the
# the sum of the numbers in that subtree. The tree structure allows operations to be 
# performed using only O(log n) node access.
# 
# Trick this data sturcture use:
#   1. n & (n-1) to eliminate the last '1' in the integer
#      parent node is array[i&(i-1)]
#   2. the value of each node is the sum of all its ##
#      node i store the sum from (i&(i-1)) to i-1 inclusively.
# 
# Methods supported:
#   1. create_tree
#   2. update_node
#   3. query
#   4. add_node

# from tree_representation import Tree

"""
For a tree_index == 0b_1100_1011_1101_0010_1000 total 10 high bits,
This node is at Level 10,
This node's parent's index is 0b_1100_1011_1101_0010_0000 - by eliminating the last 1
This node's next's index is   0b_1100_1011_1101_0011_0000 - by combining the last group of 1s
This node's value is the sum of original[0b_1100_1011_1101_0010_0000] to original[0b_1100_1011_1101_0010_0111] 
"""

class FenwickTree(object):
    def __init__(self, size):
        """
        Init a Fenwick Tree by assuming the original data are all 0s
        size is the size of original data
        """
        self._data = [0 for i in xrange(size+1)]
        self._size = size

    @classmethod
    def create_from_list(cls, nums):
        """
        Assume the original array is all 0s, then update every element to nums[i]
        """
        res = FenwickTree(len(nums))
        for i, num in enumerate(nums):
            res.update_index_by_delta(i, num)
        return res

    def _sumupto(self, i):
        """
        Sum the original array up from array[0] to array[i] inclusively
        """
        res, tree_index = 0, i+1
        while tree_index:
            res += self._data[tree_index]
            tree_index = self.get_parent(tree_index)
        return res


    def query_sum(self, i, j):
        """
        Sum the original array up from array[i] to array[j] inclusively
        If out of index, return None
        """
        if i >= self._size or j >= self._size or i < 0 or j < 0:
            return None
        if i == 0:
            return self._sumupto(j)
        return self._sumupto(j) - self._sumupto(i-1)

    def get_index(self, i):
        """
        Get the original num at index i
        """
        return self.query_sum(i,i)

    def update_index_by_delta(self, i, delta):
        """
        Add delta to num at index i in the original array
        """
        tree_index = i + 1
        while tree_index <= self._size:
            self._data[tree_index] += delta
            tree_index = self.get_next(tree_index)

    def update_index(self, i, value):
        """
        Update the num at index i in the original array a new value
        """
        delta = value - get_index(i)
        self.update_index_by_delta(i, delta)

    def get_parent(self, tree_index):
        """
        Given a tree_index, return the tree_index of its parent.
        Just eliminate the least significant 1 in that number.

        (tree_index & -tree_index)  would return the least significant bit

        >>> a = FenwickTree(2)
        >>> a.get_parent(0b1010) # return 0b1000 == 8
        8
        >>> a.get_parent(0b1101) # return 0b1100 == 12
        12
        """
        return tree_index & (tree_index - 1)

    def get_next(self, tree_index):
        """
        Given a tree_index, return the next tree_index should be updated.

        Search all siblings after this node,
        then search all parent's siblings after parent,
        then all grandparent's siblings after grandparent...
        """
        return (tree_index & -tree_index) + tree_index


def fenwickTree_test():
    fenwickTree = FenwickTree.create_from_list(range(1,1001))
    for i in xrange(1000):
        assert fenwickTree.get_index(i) == i+1
        for j in xrange(i, 1000):
            assert fenwickTree.query_sum(i, j) == ((i+j+2) * (j-i+1))/2

if __name__ == '__main__':
    # fenwickTree_test()
    a = FenwickTree.create_from_list(range(1, 16))
    print a._data

