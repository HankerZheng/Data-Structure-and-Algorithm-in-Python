"""
    N            1000        10000        100000       1000000
Insert_sort    0.048360    3.7469999     369.38299        -
Shell_sort     0.002749    0.0378999     0.3759999    6.20499992
Heap_sort      0.003490    0.0467000     0.4519999    5.64000010
Merge_sort     0.004260    0.0523999     0.4529998    5.17300009
quick_sort     0.002230    0.0279001     0.2699999    3.22999978
"""


LENGTH_SET = [10,20,50,100,200, 500,1000,2000,5000,10000] # length = 10

# =================
# Sort Algorithms
# =================

def insertion_sort(nums):
    """
    Assume the first i elements are in sorted order.
    Then, compare the (i+1)th element with the first i-th elements. 
    If nums[i+1]>nums[i], then the first (i+1)th
    elements are in sorted order.
    Else, swap this two elements and compare nums[i] and nums[i-1]
    until all elements are in order.

    The average number of inversions in an array of N distinct numbers
    is N(N-1)/4

    Any Algorithm that sorts by exchanging adjacent elements requires
    Omiga(N^2) Each swap removes only one inversion, so Omiga(N^2) swaps are
    required.
    """
    for i in xrange(1, len(nums)):
        this, j = nums[i], i
        while this<nums[j-1] and j>0:
            nums[j], j = nums[j-1], j-1
        nums[j] = this

def shell_sort(nums):
    """
    One of the first algorithm that breaks the quadratic barrier.
    An important property of Shellsort is that an h(k)-sorted file that
    is then h(k-1)-sorted remains h(k)-sorted.

    Use insertion sort to make every h elements in the list in order.
    The sequence h1,h2,h3,... will work as long as h1==1
    """
    def increment_generator(length):
        h = length
        while h>1:
            h = h/2
            h = max(1, h if h&1 else h-1)
            yield h
    for h in increment_generator(len(nums)):
        i = 0
        for i in xrange(h,len(nums), 1):
            this,j = nums[i],i
            while nums[j-h]>this and j>h-1:
                nums[j],j = nums[j-h],j-h
            nums[j] = this

def heap_sort(nums):
    """
    Make use of maxheap. Every time delete max, move the max element
    to the last slot of the array.

    The average number of comparisons used to heapsort a random permutation
    of N distinct items is 2N*logN - O(NloglogN).
    """
    def percolate_down(index, length):
        """
        Basic heap operation, percolate nums[index] down until this
        list satisfies heap property.
        """
        this = nums[index]
        child, slot = index*2+1, index
        while child<length:
            if child<length-1 and nums[child+1]>nums[child]:
                child +=1
            if this < nums[child]:
                nums[slot] = nums[child]
            else:
                break
            slot = child
            child = child*2+1
        nums[slot] = this
    # First, maxheapify the input nums
    # nums[(len(nums)-1)/2] is the last element with child
    for i in xrange((len(nums)-1)/2, -1, -1):
        percolate_down(i, len(nums))
    # Then, delete the first element and move it to the last
    for i in xrange(len(nums)-1, 0, -1):
        nums[0], nums[i] = nums[i], nums[0]
        percolate_down(0, i)

def merge_sort(nums):
    """
    Recursively mergesort the first half and the second half of the list.
    This algorithm is a class of divide and conquer strategy.
    Time complexity is O(N+NlogN)

    Although mergesort's running time is O(NlogN), it is hardly ever used for
    main memory sorts. The main problem is that merging two sorted lists requires
    linear extra memory and the additional work spent copying to the temporary
    array and back, throughout the algorithm, has the effect of slowing down the
    sort considerably.
    """
    def part_sort(start,end):
        """
        Basic sort-operation for mergesort. END is not included.
        """
        if end - start <= 1:
            return
        else:
            mid = start+(end-start)/2
            part_sort(start, mid)
            part_sort(mid, end)
            merge(start,mid, mid, end)
    def merge(start1, end1, start2, end2):
        """
        Merge two sorted list together
        """
        i, j, ans = start1, start2, []
        while i<end1 and j<end2:
            if nums[i] < nums[j]:
                ans.append(nums[i])
                i+=1
            else:
                ans.append(nums[j])
                j+=1
        for i in xrange(i, end1):
            ans.append(nums[i])
        for j in xrange(j,end2):
            ans.append(nums[j])
        nums[start1:end2] = ans
    # Start the mergesort
    part_sort(0, len(nums))

def quick_sort(nums):
    """
    THe basic algorithm to sort an array S consists of the 4 steps:
    1. If the number of elements in S is 0 or 1, then return
    2. Pick any element v in S. This is called the pivot.
    3. Partition S-{v} into two disjoint groups: S1(all elements in S-{v}
        that is smaller than v), and S2(all elements in S-{v} that is larger
        or equal to v).
    4. Return {quick_sort(S1) followed by v followed by quick_sort(S2 )}

    It would take the longest time for quick_sort to sort an pre-ordered
    list among all the sort algorithm
    """
    def median3(start,end):
        """
        This is the STEP 2
        Return the value of median of [nums[start], nums[mid], nums[end]],
        and swap the median with nums[end].
        `end` is included in the list
        """
        mid = start+(end-start)/2
        if nums[start] > nums[mid]:
            nums[start], nums[mid] = nums[mid], nums[start]
        if nums[start] > nums[end]:
            nums[start], nums[end] = nums[end], nums[start]
        if nums[mid] > nums[end]:
            nums[mid], nums[end] = nums[end], nums[start]
        # Now is SM, MED, LG
        nums[mid], nums[end] = nums[end], nums[mid]
    def qsort(start, end):
        """
        This is the STEP 3&4
        Partition the list into two parts.
        And then, return {quick_sort(S1) followed by v followed by quick_sort(S2 )}
        `end` is included in the list.
        """
        if start>=end:
            return
        median3(start, end)
        pivot, i, j = nums[end], start, end
        while True:
            while nums[i]<pivot and i<j:
                i+=1
            if i<j:
                nums[j] = nums[i]
                j-=1
            while nums[j]>pivot and i<j:
                j-=1
            if i<j:
                nums[i] = nums[j]
                i+=1
            else:
                break
        nums[j] = pivot
        # This is STEP 4
        qsort(start, j-1)
        qsort(j+1, end)
    # Starts the quick sort
    qsort(0, len(nums)-1)



def quickSort(a):
    def median(start,end):  
        center=(start+end)/2  
        if a[start]>a[center]:  
            a[start],a[center]=a[center],a[start]  
        if a[start]>a[end]:  
            a[start],a[end]=a[end],a[start]  
        if a[center]>a[end]:  
            a[center],a[end]=a[end],a[center]  
        a[start],a[center]=a[center],a[start]  
    def doSwap(start,end):  
        if start>=end:  
            return  
        i,j=start,end  
        median(start,end)  
        tmp=a[start]  
        while(True):  
            while(a[j]>tmp and i<j):  
                j-=1  
            if i<j:  
                a[i]=a[j]  
                i+=1  
            while(a[i]<tmp and i<j):  
                i+=1  
            if i<j:  
                a[j]=a[i]  
                j-=1  
            else:  
                break  
        a[i]=tmp  
        doSwap(start,i-1)  
        doSwap(j+1,end)  
    doSwap(0,len(a)-1)  


# ===========================
#  TEST-concerning
# ===========================
def order_test(nums, isprint):
    old = float("-inf")
    for num in nums:
        if num < old:
            print test
            raise ValueError("This list is not sorted! %d,%d" %(old, num))
        old = num
    if isprint:
        print "%s\ntest passed!" % nums

def test_generate(times):
    from random import randint
    yield []
    yield [12]
    for i in xrange(times):
        length = LENGTH_SET[i%10]
        test_list = [randint(0,500) for i in xrange(length)]
        yield test_list

def random_generate(length, times):
    from random import randint
    for i in xrange(times):
        test_list = [randint(0,500) for i in xrange(length)]
        yield test_list

def algorithm_compare(sort_algorithms,length=1000, times=50, isprint=False):
    from time import time
    stats = {sort.__name__:0 for sort in sort_algorithms}    
    for test in random_generate(length, times):
        for my_sort in sort_algorithms:
            this = list(test)
            start = time()
            my_sort(this)
            cost_time = time()-start
            stats[my_sort.__name__]+=cost_time
            if isprint:
                print "Algorithm %s for list of %d elements finished in %f seconds." %(my_sort.__name__, len(test),cost_time)
    for sort in sort_algorithms:
        print sort.__name__, stats[sort.__name__]


if __name__=="__main__":
    # Algorithm test
    my_sort = quick_sort
    for test in test_generate(times=50):
        print "Algorithm %s for list of %d elements starts." %(my_sort.__name__, len(test))
        my_sort(test)
        order_test(test, isprint=False)

    # # Time Statistics
    # sort_algorithms = [shell_sort, heap_sort, merge_sort, quick_sort]
    # algorithm_compare([insertion_sort], length=100000, times=1, isprint=True)

    # # Pre-order test
    # preorder = range(100000)
    # for i in xrange(10):
    #     my_sort(preorder)
