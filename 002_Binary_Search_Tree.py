# Binary Search Tree in 'Data Structure and Algorithm Analysis' P.100
#
# Keypoint: The book implements all the BST method in recursive way. However,
#           in my implementation, I make it all presented in LOOP-way.
#
# Deletion: The general strategy is to replace the data of this node with the
#           smallest data of the right subtree and then delete that node, because
#           the smallest node in the right sub tree cannot have a left child, which
#           can be easily deleted.
#           It works the same way if we replace it with the largest node in the right
#           subtree.
#           Since the LOOP-way implementation needs to keep track on the parent node
#           of the node to be deleted, which would add complexity to the code and make
#           the code look less elegant. Therefore, delete method is implemented in
#           recursive way.
#
# Empty Tree:
#           In this implementation, we don't add the root node into this Binary Tree.
#           Therefore, we use one node with value of "EmptyNode" to represent an empty
#           tree. This reprentation would exist only when it is an empty tree. This would
#           not represent the deleted node in the tree.
#           This implementation would help when we want to delete the tree to empty and
#           then add new items into the tree. 
#
# Deletion Special Case:
#           1) delete the only root node, return None
#           2) delete the tree into empty and then insert
#

class BinaryTree(object):
    def __init__(self, content=-1):
        self.val = content
        self.left = None
        self.right = None

    def display(self):
        def print_tree(tree, depth):
            if tree:
                print "  " * depth + str(tree.val)
                if tree.left or tree.right:
                    print_tree(tree.left, depth+1)
                    print_tree(tree.right, depth+1)
            else:
                print "  " * depth + 'None'                
        # call the recursive function
        print_tree(self, 0)

class BST(BinaryTree):
    def __init__(self, content="EmptyNode"):
        super(BST,self).__init__(content)

    @classmethod
    def createFromList(cls, in_list):
        if not in_list:
            return BST()
        length, res = len(in_list), cls()
        for item in in_list:
            res.insert(item)
        return res

    def makeEmpty(self):
        self.value = 'EmptyNode'
        self.left = None
        self.right = None

    def find(self, match):
        """
        find item in the BST

        >>> import random
        >>> test = range(20)
        >>> random.shuffle(test)
        >>> bst = BST.createFromList(test)
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

    def insert(self, content):
        this_tree = self
        while 1:
            if this_tree.val == "EmptyNode":
                this_tree.val = content
                return
            if content < this_tree.val:
                if not this_tree.left:
                    # If left subtree is None
                    new_node = BST(content)
                    this_tree.left = new_node
                    break
                # Keep searching through left subtree
                this_tree = this_tree.left
            else:
                if not this_tree.right:
                    # If right subtree is None
                    new_node = BST(content)
                    this_tree.right = new_node
                    break
                # Keep searching through right subtree
                this_tree = this_tree.right

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

        >>> my_bst = BST()
        >>> item_set = range(20)
        >>> for i in xrange(4):
        ...     random.shuffle(item_set)
        ...     for item in item_set:
        ...         my_bst.insert(item)
        ...     for i in xrange(20):
        ...         my_bst = my_bst.delete(i)
        ...     my_bst.display()
        ...
        EmptyNode
        EmptyNode
        EmptyNode
        EmptyNode
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
            return BST()        

if __name__ == "__main__":
    import doctest
    import random
    doctest.testmod()
