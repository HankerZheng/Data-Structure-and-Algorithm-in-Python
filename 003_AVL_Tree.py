# AVL Tree in 'Data Structure and Algorithm Analysis' P.110
#
# Keypoint: After insertion, roatate the tree if AVL-condition is not reached.
#           Every node keep updated with the height information.
#

class BinaryTree(object):
    def __init__(self, content=-1):
        self.val = content
        self.left = None
        self.right = None

    def display(self):
        def print_tree(tree, depth):
            if tree:
                if depth:
                    print "|  " * (depth-1) + '+--+' +str(tree.val)
                else:
                    print '+' +str(tree.val)

                if tree.left or tree.right:
                    print_tree(tree.left, depth+1)
                    print_tree(tree.right, depth+1)
            else:
                print "  " * depth + 'None'
        # call the recursive function
        print_tree(self, 0)

class AVL(BinaryTree):
    def __init__(self, content="EmptyNode"):
        self._height = 0
        super(AVL,self).__init__(content)

    @classmethod
    def createFromList(cls, in_list):
        if not in_list:
            return AVL()
        length, res = len(in_list), cls()
        for item in in_list:
            res = res.insert(item)
        return res

    @classmethod
    def getHeight(cls, node):
        if isinstance(node, cls):
            return node._height
        else:
            return -1

    def makeEmpty(self):
        self.value = 'EmptyNode'
        self._height = 0
        self.left = None
        self.right = None

    def find(self, match):
        """
        find item in the AVL

        >>> import random
        >>> test = range(20)
        >>> random.shuffle(test)
        >>> bst = AVL.createFromList(test)
        >>> for x in xrange(20):
        ...     res = bst.find(x)
        ...     if res and res.val == x:
        ...         continue
        ...     else:
        ...         print x
        ...
        >>> bst.find(20) == None
        True
        >>> bst.find(21) == None
        True
        """
        this_tree = self
        while this_tree and match != this_tree.val:
            if match < this_tree.val:
                this_tree = this_tree.left
            else:
                this_tree = this_tree.right
        return this_tree if this_tree else None

    def findMin(self):
        """
        return the node with the smallest value
        """
        this_tree = self
        while this_tree.left:
            this_tree = this_tree.left
        return this_tree

    def findMax(self):
        """
        return the node with the largest value
        """
        this_tree = self
        while this_tree.right:
            this_tree = this_tree.right
        return this_tree

    def singleRotate(self, flag):
        """
        Single rotate to handle outer unbalance.
        Paras: flag = 0 -> left node unbalanced
               flag = 1 -> right node unbalanced
        """
        # Right node unbalanced
        if flag:
            k1, k2 = self, self.right
            k1.right, k2.left = k2.left, k1
        # Left node unbalanced
        else:
            k1, k2 = self, self.left
            k1.left, k2.right = k2.right, k1

        k1._height = max(AVL.getHeight(k1.left), AVL.getHeight(k1.right)) + 1
        k2._height = max(AVL.getHeight(k2.left), AVL.getHeight(k2.right)) + 1
        return k2

    def doubleRotate(self, flag):
        """
        Single rotate to handle inner unbalance.
        Paras: flag = 0 -> left node unbalanced
               flag = 1 -> right node unbalanced
        """
        # Right node unbalanced
        if flag:
            k1, k2, k3 = self, self.right, self.right.left
            k1.right, k2.left, k3.left, k3.right = \
                    k3.left, k3.right, k1, k2
        else:
            k1, k2, k3 = self, self.left, self.left.right
            k1.left, k2.right, k3.left, k3.right = \
                    k3.right, k3.left, k2, k1       
        k1._height = max(AVL.getHeight(k1.left), AVL.getHeight(k1.right)) + 1
        k2._height = max(AVL.getHeight(k2.left), AVL.getHeight(k2.right)) + 1
        k3._height = max(AVL.getHeight(k3.left), AVL.getHeight(k3.right)) + 1
        return k3

    def insert(self, content):
        """
        Should be called as avl = avl.insert()

        >>> avl = AVL.createFromList(xrange(1,8))
        >>> print AVL.getHeight(avl)
        2
        >>> avl = avl.insert(15)
        >>> avl = avl.insert(16)
        >>> avl = avl.insert(14)
        >>> print AVL.getHeight(avl)
        3
        """
        # When input_tree is an empty tree
        if self.val == "EmptyNode":
            self.val = content
            return self
        # Left subtree operation
        elif content < self.val:
            if self.left:
                self.left = self.left.insert(content)
                if AVL.getHeight(self.left) - AVL.getHeight(self.right) == 2:
                    # Single rotate when there is an outer case
                    if content < self.left.val:
                        self = self.singleRotate(0)
                    else:
                        self = self.doubleRotate(0)
            # If left subtree is None
            else:
                new_node = AVL(content)
                self.left = new_node

        # Right subtree operation
        else:
            if self.right:
                self.right = self.right.insert(content)
                if AVL.getHeight(self.right) - AVL.getHeight(self.left) == 2:
                    if content >= self.right.val:
                        self = self.singleRotate(1)
                    else:
                        self = self.doubleRotate(1)
            # If right subtree is None
            else:
                new_node = AVL(content)
                self.right = new_node
            # Keep searching through right subtree
        # Operation on height
        self._height = max(AVL.getHeight(self.left), AVL.getHeight(self.right)) + 1
        return self

    def _deleteMin(self, p_node):
        """
        this method is to support delete method, makes it efficient
        """
        this_tree = self
        while this_tree.left:
            p_node = this_tree
            this_tree = this_tree.left
        # this_tree is the node with the Min val
        if p_node.left and p_node.left.val == this_tree.val:
            # p_node.left -> this_tree
            p_node.left = this_tree.right
        else:
            p_node.right = this_tree.right
        return this_tree.val

    def delete(self, match):
        """
        should be called as bst = bst.deletion(XX)

        >>> my_avl = AVL()
        >>> item_set = range(20)
        >>> for i in xrange(4):
        ...     random.shuffle(item_set)
        ...     for item in item_set:
        ...         my_avl = my_avl.insert(item)
        ...     for i in xrange(20):
        ...         my_avl = my_avl.delete(i)
        ...     my_avl.display()
        ...
        +EmptyNode
        +EmptyNode
        +EmptyNode
        +EmptyNode
        """
        def _delete(self, match):
            if match < self.val:
                if self.left:
                    self.left = _delete(self.left, match)
                else:
                    raise ValueError("deletion node not found!!")
            elif match > self.val:
                if self.right:
                    self.right = _delete(self.right, match)
                else:
                    raise ValueError("deletion node not found!!")
            else:
                # need to delete this root node
                if self.right and self.left:
                    # this node has 2 children
                    self.val = self.right._deleteMin(self)
                else:
                    # this node has at most 1 children
                    self = self.right if self.right else self.left
            return self
        # if all nodes of the tree have been deleted, return EmptyNode
        # There exists EmptyNode in the tree only at ROOT of the Tree
        after_deletion = _delete(self, match)
        if after_deletion:
            return after_deletion
        else:
            return AVL()        

if __name__ == "__main__":
    import doctest
    import random
    doctest.testmod()
    my_avl = AVL.createFromList(xrange(1,100))
    my_avl.display()