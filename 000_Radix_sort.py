# Radix Sort in 'Data Structure and Algorithm Analysis' P.54
#
# Condition: All number needed to be sorted should be within 0 to M^P - 1 inclusively
#
# Radix Sort:   There are N numbers needs to be sorted. In general,
#               these numbers are in range 0 to M^P - 1 for Constant P.
#               We could sort them by Bucket Sort with M buckets for p
#               times.
#               Actually, if we set M = 16, P = 8, we could sort all number
#               within range of INT type.
#               Time complexity is O(NP) = O(N)
#
# Comment: Constrain on the range of number to be sorted, would help decrease
#          time complexity. This algorithm in this circumstance would have O(n)
#          time complexity, but probably still not as efficient as some of the
#          normal sorting algorithm in Chaper 7, because of the high constant
#          cost involved.
#
# RadixSort_acc show sorted result in accendent order. This algorithm use
# insert_last function while inserting element into a linked list, whose
# time complexity is O(n), that is kinda expensive.
#
# RadixSort_dec show sorted result in decedent order. This algorithm use
# insert_first function which is much cheaper than insert_last.
# However, finally it shows that this function won't work, becuase insert_first
# function would reverse the order in the unfinished list. For example, (m=10)
# original: 8 -> 0 -> 2
# 1-st round: 8 -> 2 -> 0
# 2-nd round: 0 -> 2 -> 8
# 3-rd round: 8 -> 2 -> 0
# if numbers are mixed, we would not get the right result.


def RadixSort_acc(unsorted, m=16, p=8):
    """
    : type unsorted: ListNode, header node
    : rtype: ListNode
    """
    # initialize m linked lists in linkedlists array
    linkedlists = [ListNode(-1) for i in xrange(m)]
    unfinished = ListNode(-1)
    unfinished.next = unsorted.next

    for i in xrange(p):
    # sort the list in the least i-th significant 'digit'
        terverse = unfinished.next
        while terverse:
            # fit in value into linkedlists
            tmp = terverse.next
            digit = terverse.val / (m**i)
            linkedlists[digit%m].insert_last(terverse)
            terverse = tmp
        # combine linkedlists into unfinished and empty linkedlists
        unfinished_tmp = unfinished
        for j in xrange(m):
            if linkedlists[j].next is None:
                continue
            tmp = linkedlists[j].next
            unfinished_tmp.next = tmp
            while tmp.next:
                tmp = tmp.next
            unfinished_tmp = tmp

            linkedlists[j].next = None
    return unfinished.next


# this method is cracked!
def RadixSort_dec(unsorted, m=16, p=8):
    """
    : type unsorted: ListNode, header node
    : rtype: ListNode
    """
    # initialize m linked lists in linkedlists array
    linkedlists = [ListNode(-1) for i in xrange(m)]
    unfinished = ListNode(-1)
    unfinished.next = unsorted.next

    for i in xrange(p):
    # sort the list in the least i-th significant 'digit'
        terverse = unfinished.next
        while terverse:
            # fit in value into linkedlists
            tmp = terverse.next
            digit = terverse.val / (m**i)
            linkedlists[digit%m].insert_first(terverse)
            terverse = tmp
        # combine linkedlists into unfinished and empty linkedlists
        unfinished.next = None
        for j in xrange(m):
            if linkedlists[j].next is None:
                continue
            end_node = unfinished.next
            unfinished.next = linkedlists[j].next
            tmp = linkedlists[j].next
            # find the last node in this linked list
            while tmp.next:
                tmp = tmp.next
            tmp.next = end_node
            linkedlists[j].next = None
        unfinished.display_list()
    return unfinished.next

class ListNode(object):
    """
    all linked list implemented should have header!!
    """
    def __init__(self, x):
        self.val = x
        self.next = None

    @classmethod
    def create_from_array(cls, array):
    # return the header node
        res = ListNode(-1)
        res_tmp = res
        for num in array:
            res_tmp.next = ListNode(num)
            res_tmp = res_tmp.next
        return res

    def insert_first(self, node):
        tmp = self.next
        self.next = node
        node.next = tmp

    def insert_last(self, node):
        tmp = self
        while tmp.next:
            tmp = tmp.next
        tmp.next = node
        node.next = None

    def empty_list(self):
        terverse = self
        while terverse:
            tmp = terverse.next
            del terverse
            terverse = tmp

    def display_list(self):
    # this function would make the head node visiable
        tmp = self
        while tmp.next is not None:
            print tmp.val, 
            tmp = tmp.next
        print tmp.val


if __name__ == "__main__":
    head = ListNode.create_from_array([64,8,216,512,27,729,0,1,343,125,143,643,25,634,12,535,474])
    final = RadixSort_acc(head,16,8)
    final.display_list()