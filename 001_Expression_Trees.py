# Expression Trees in 'Data Structure and Algorithm Analysis' P.97
#
# Function: Expression Tree construction with postfix input
#           Expression Tree calculation
#           Support +, -, *, /, ^, % operations only.
#           Support INT and FLOAT.
#
# Need stack to implement this.
# In the code bleow, we simulate a stack Data Structure by Linked List
#
# Construct: Store ans in stack
#
# Calculate: Use post-order traversal to calculate the result.
#

class BinaryTree(object):
    def __init__(self, content=-1):
        self.val = content
        self.left = None
        self.right = None

    def display(self):
        def print_tree(tree, depth):
            print "  " * depth + str(tree.val)
            if tree.left:
                print_tree(tree.left, depth+1)
            if tree.right:
                print_tree(tree.right, depth+1)
        # call the recursive function
        print_tree(self, 0)


class ExpressionTree(object):
    _operators = ['+', '-', '*', '/', '^', '%']

    @classmethod
    def construct(cls, in_list):
        """
        given in_list with operators and operands,
        automatically construct an Expression Tree and return its root.
        """
        if not in_list:
            return None
        if not in_list[-1] in cls._operators:
            print "Error Expression input! Input is None"
            return None

        operand_stack = Stack()
        for symbol in in_list:
            if isinstance(symbol, (int, float)):
                # if it is an operands, push it into stack
                new_node = BinaryTree(float(symbol))
                operand_stack.push(new_node)
            elif symbol in cls._operators:
                # if it is an operator, pop 2 operands from stack
                # make 2 operands 2 children of the operator
                new_node = BinaryTree(symbol)
                first_operand = operand_stack.pop()
                second_operand = operand_stack.pop()
                if first_operand and second_operand:
                    # first operand is the one popped later
                    new_node.left, new_node.right = second_operand, first_operand 
                    operand_stack.push(new_node)
                else:
                    operand_stack.pop_all()
                    print "Error Expression input! Stack already empty"
                    return None
        res = operand_stack.pop()
        # check whether stack is empty
        if operand_stack.is_empty():
            return res
        operand_stack.pop_all()
        print "Error Expression input! Stack is not empty in the end!"
        return None

    @classmethod
    def calculate(cls, in_tree):
        def cal_node(tree):
            if isinstance(tree.val, (int, float)):
                return tree.val

            if tree.left:
                left = cal_node(tree.left)
            if tree.right:
                right = cal_node(tree.right)

            if tree.val == '+':
                return left + right
            elif tree.val == '-':
                return left - right
            elif tree.val == '*':
                return left * right
            elif tree.val == '/':
                return left / right
            elif tree.val == '^':
                return left ** right
            elif tree.val == '%':
                return left % right

        return cal_node(in_tree)


class Stack(object):
    """
    Simple stack implemented by linked list.
    """
    def __init__(self):
        self._storage = ListNode(-1)

    def pop(self):
        """
        No need to care about freeing memory
        Once there is no reference to that resource,
        that resource would be freed. 
        """
        if self._storage.next:
            res, self._storage.next = \
                self._storage.next.val, self._storage.next.next
            return res
        else:
            print 'Empty Stack. Nothing to be pop!'
            return None

    def push(self, content):
        if not isinstance(content, ListNode):
            node = ListNode(content)
        else:
            node = content
        tmp = self._storage.next
        self._storage.next = node
        node.next = tmp

    def is_empty(self):
        return self._storage.next is None

    def pop_all(self):
        """
        Python would handle the memory for you :)
        """
        self._storage.next = None


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

    @classmethod
    def create_from_array(cls, array):
        res = ListNode(-1)
        res_tmp = res
        for num in array:
            res_tmp.next = ListNode(num)
            res_tmp = res_tmp.next
        return res.next

    def display(self):
        tmp = self
        while tmp.next is not None:
            print tmp.val, 
            tmp = tmp.next
        print tmp.val


if __name__ == "__main__":
    express = ExpressionTree.construct([1,2,'-',3,4,5,'/','^','%'])
    print ExpressionTree.calculate(express)