# Manacher's Algorithm - Linear Time Longest Palindromic Substring Algorithm
# 
# For string "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" (length = 65)
# there will only be 129 comparasions in Manacher algorithm,
# while in `normal_LongestPalindromeSubstring()` function, there will be 2144 comparasions!
# Even more time and space for the DP solution!!
# 
# Reference:
#   http://www.geeksforgeeks.org/manachers-algorithm-linear-time-longest-palindromic-substring-part-1/
#   https://en.wikipedia.org/wiki/Longest_palindromic_substring

def manacher(string):
    """
    Key points of Manacher's algorithm:
        1)  Insert special character into the original string, such as "#"
            This string may not be acually inserted, but virtually inserted
            by converting virtual_index to physical_index.
            This improvement could combine odd palindrome and even palindrome
            into one situation.

        2)  Maintain a longest palindrome substring table `lps`, in which
            `lps[i]` contian the half length of palindrome which center at 
            virtual index `i`. By half, we mean round up.
            Then the actual palindrome length could be get as `lps[i] - 1`

        3)  Using the information in the table to find longest palindrome in
            linear time complexity.

    Time Complexity: O(n)
    Space Complexity: O(n)

    Example for "abaaba":
                    #  a  #  b  #  a  #  a  #  b  #  a  #
    physical        -  0  -  1  -  2  -  3  -  4  -  5
    virtual         0  1  2  3  4  5  6  7  8  9  10 11 12
    LPS table       1  2  1  4  1  2  7  2  1  4  1  2  1
    right_border    0  2  -  6  -  -  12 -  -  -  -  -  -   , `-` means not updated
    center_index    0  1  -  3  -  -  6  -  -  -  -  -  -   , `-` means not updated

    Therefore, virtual_index = physical_index * 2 + 1
              physical_index = (virtual_index - 1)/2 if virtual_index&1 else -1
    Alos, the longest palindrome substring is "aba"   
    """
    # def virtual2physical(virtual_index):
    #     # convert virtual index to physical index
    #     # if virtual_index is even, just return -1
    #     return (virtual_index-1) / 2 if virtual_index & 1 else -1

    # def physical2virtual(physical_index):
    #     # convert physical_index to virtual_index
    #     return physical_index * 2 + 1

    def get_actual_char(virtual_index):
        if virtual_index & 1:
            return string[(virtual_index - 1) / 2]
        else:
            return "#"

    if not string:
        return set([])
    # init LPS table
    length = len(string)
    lps = [1 for i in xrange(length * 2 + 1)]
    # main loop to calculate the lps table
    max_length = 0
    right_border = 0
    center_index = 0
    # compare_count = 0
    for i, _ in enumerate(lps):
        # This IF-STATEMENT is the key of MANACHER'S Algorithm
        # If this character is within the range of a longer palindrome,
        # then update lps with the symmetric value
        if right_border > i:
            lps[i] = min(lps[2 * center_index - i], right_border - i + 1)
        # expand this palindrome
        while 0 <= i - lps[i] and i + lps[i] < len(lps) and get_actual_char(i + lps[i]) == get_actual_char(i - lps[i]):
            # compare_count += 1
            lps[i] += 1
        max_length = max(max_length, lps[i])
        # update right_border and center if current right_border is larger than the previous one
        if lps[i] + i - 1 > right_border:
            right_border = lps[i] + i - 1
            center_index = i
    # At here, the length of longest palindrome substring is `max_length - 1`
    # print lps
    # print compare_count
    ans = []
    for i, num in enumerate(lps):
        if num == max_length:
            ans.append((i-num+1, i+num-1))
    return set(map(lambda x: string[x[0]/2:x[1]/2], ans))


def dp_LongestPalindromeSubstring(string):
    """
    DP solution to Longest Palindromic Substring.
    dp[i][j] - whether substring start from string[i] to string[j] is palindromic

    Time Complexity:  O(n^2)
    Space Complexity: O(n^2)
    """
    # init dp matrix
    dp = [[0 for _ in string] for __ in string]
    # when count hits 2, we should break the loop
    ans, count = [], 0
    for delta in xrange(len(string)):
        i = 0
        this_ans = []
        while i + delta < len(string):
            if delta == 0:
                # every single character is a palindrome
                dp[i][i+delta] = 1
                this_ans.append((i, i+delta+1))
                count = 0
            elif delta == 1 and string[i] == string[i+delta]:
                # every 2 identical characters can form a palindrome
                dp[i][i+delta] = 1
                this_ans.append((i, i+delta+1))
                count = 0
            elif delta > 1 and dp[i+1][i+delta-1] and string[i] == string[i+delta]:
                # start matches end, and also the characters in the middle is a palindrome
                dp[i][i+delta] = 1
                this_ans.append((i, i+delta+1))
                count = 0
            i += 1
        # If this length has no palindrome, imcrement `count`
        # Otherwise, update `ans`
        if not this_ans:
            count += 1
        else:
            ans = this_ans
        # check whether to end the loop in advance
        if count == 2:
            break
    # ans are stored as `(start_index, end_index + 1)
    return set(map(lambda x: string[x[0]:x[1]], ans))


def normal_LongestPalindromeSubstring(string):
    """
    Search from the middle of the string.
    Generate all even length and odd length palindromes,
    and keep track of the longest palindrome seen so far.

    Step to generate odd length palindrome:
    Fix a centre and expand in both directions for longer palindromes.
    Step to generate even length palindrome
    Fix two centre ( low and high ) and expand in both directions for longer palindromes.

    Time Complexity:  O(n^2)
    Space Complexity: O(1), if we wants store the result string, then it will be O(n)
    """
    # compare_count = 0
    max_length = 1
    ans = []
    for i in xrange(1, len(string)):
        # find the longest even length palindrome with center position
        # at (i-1) and i
        low = i - 1
        high = i
        while 0 <= low and high < len(string) and string[low] == string[high]:
            # compare_count += 1
            if high - low + 1 > max_length:
                max_length = high - low + 1
                ans = []
                ans.append((low, high+1))
            elif high - low + 1 == max_length:
                ans.append((low, high+1))

            low -= 1
            high += 1
        # find the longest odd length palindrome with center position at i
        low = i
        high = i
        while 0 <= low and high < len(string) and string[low] == string[high]:
            # compare_count += 1
            if high - low + 1 > max_length:
                max_length = high - low + 1
                ans = []
                ans.append((low, high+1))
            elif high - low + 1 == max_length:
                ans.append((low, high+1))
            low -= 1
            high += 1
    # print compare_count
    if max_length == 1:
        return set(string.split())
    return set(map(lambda x: string[x[0]:x[1]], ans))

def longest_palindrome_substring_test():
    import random
    char_set = "qwert"
    for i in xrange(100):
        test_case = [random.choice(char_set) for _ in xrange(300)]
        test = "".join(test_case)
        # print manacher(test)
        assert manacher(test) == dp_LongestPalindromeSubstring(test)
        assert manacher(test) == normal_LongestPalindromeSubstring(test)


if __name__ == '__main__':
    # assert dp_LongestPalindromeSubstring("aaab.ba") == set(["ab.ba"])
    # assert dp_LongestPalindromeSubstring("aaaaabbbb") == set(["aaaaa"])
    # assert dp_LongestPalindromeSubstring("aaaaa") == set(["aaaaa"])
    # assert dp_LongestPalindromeSubstring(".babcbaaaaa") == set(["abcba", "aaaaa"])
    # assert normal_LongestPalindromeSubstring("aaab.ba") == set(["ab.ba"])
    # assert normal_LongestPalindromeSubstring("aaaaabbbb") == set(["aaaaa"])
    # assert normal_LongestPalindromeSubstring("aaaaa") == set(["aaaaa"])
    # assert normal_LongestPalindromeSubstring(".babcbaaaaa") == set(["abcba", "aaaaa"])
    # testcases = ["", "a", "aa", "aaa", "aaaa", "aaaaba", "ab.bab.", "asdsfsexe"]
    # for test in testcases:
    #     assert dp_LongestPalindromeSubstring(test) == normal_LongestPalindromeSubstring(test)
    #     # print manacher(test), normal_LongestPalindromeSubstring(test)
    #     assert manacher(test) == normal_LongestPalindromeSubstring(test)
    # print manacher("abaaba")
    # print manacher("")
    longest_palindrome_substring_test()
    # manacher("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    # normal_LongestPalindromeSubstring("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")