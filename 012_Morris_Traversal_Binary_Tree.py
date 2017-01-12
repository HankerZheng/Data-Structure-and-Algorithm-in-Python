# Reference: http://www.cnblogs.com/AnnieKim/archive/2013/06/15/MorrisTraversal.html
# 
# Morris Traversal is an algorithm that can traverse a bianry traverse with
# O(n) time Complexity and O(1) space Complexity.
# The normal recursive and iterative method to traverse a bianry would use O(logn) space
# 
# Node: `preNode` of curNode in the Steps refers to the node that is adjacently before 
#       `curNode` in the output list of the inorder traversal of the given tree.
# 
# Steps for in-order-traveral:
#   0. set curNode to root
#   1. if curNode.left is None, output curNode.val and set curNode to curNode.right
#   2. if curNode.left is not None, find preNode of curNode in its left subtree
#       1) if preNode.right == None, set preNode.right to curNode
#       2) if preNode.right == curNode, set preNode.right back to None, output curNode,
#          and update curNode to curNode.right
#   3. loop step 1 and 2 until curNode == None
# 
# Steps for pre-order-traversal:
#   0. set curNode to root
#   1. if curNode.left is None, set curNode to curNode.right, output curNode.val
#   2. if curNode.left is not None, find preNode of curNode in its left subtree
#       1) if preNode.right == None, set preNode.right to curNode, output curNode.val
#       2) if preNode.right == curNode, set preNode.right back to None, and update
#          curNode to curNode.left
#   3. loop step 1 and 2 until curNode == None



class TreeNode(object):
    def __init__(self, val):
        self.val = val
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


def _findRightmost(root, parent):
    """
    Find the right most node of `root`
    `parent` is included to prevent infinite loop
    """
    tmp = root
    while tmp.right and tmp.right != parent:
        tmp = tmp.right
    return tmp

def inOrder_Morris(root):
    """
    In-Order-Traversal of Morris Algorithm
    """
    if not root:    return []
    ans = []
    curNode = root
    while curNode:
        if curNode.left:
            prevNode = _findRightmost(curNode.left, curNode)
            if prevNode.right == curNode:
                prevNode.right = None
                ans.append(curNode.val)
                curNode = curNode.right
            else:
                prevNode.right = curNode
                curNode = curNode.left
        else:
            ans.append(curNode.val)
            curNode = curNode.right
    return ans


def preOrder_Morris(root):
    """
    Pre-Order-Traversal of Morris Algorithm
    """
    if not root:    return []
    ans = []
    curNode = root
    while curNode:
        if curNode.left:
            prevNode = _findRightmost(curNode.left, curNode)
            if prevNode.right == curNode:
                prevNode.right = None
                curNode = curNode.right
            else:
                ans.append(curNode.val)
                prevNode.right = curNode
                curNode = curNode.left
        else:
            ans.append(curNode.val)
            curNode = curNode.right
    return ans


if __name__ == '__main__':
    testTree = TreeNode(1)
    testTree.left = TreeNode(2)
    testTree.left.left = TreeNode(3)
    testTree.left.right = TreeNode(4)
    testTree.right = TreeNode(5)
    testTree.right.left = TreeNode(6)
    testTree.right.right = TreeNode(7)
    testTree.right.right.left = TreeNode(8)
    testTree.right.right.left.right = TreeNode(9)

    # testTree.display()
    # print inOrder_Morris(testTree)
    print preOrder_Morris(testTree)