#coding=utf-8
# Knuth-Morris-Pratt string searching algorithm
# is a string matching algorithm wants to find the starting index `m`
# in string `S[]` that matches the search word `W[]`.
# 
# Reference:
#   https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm
#   http://www.ruanyifeng.com/blog/2013/05/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm.html
# 
# It search for a "word" W within a main "text string" S by employling the observation that
# when a mismatch occurs, the word itself embodies sufficient information to determine
# where the next match could begin, thus bypassing re-examination of previously matched characters.
# 
# Time Complexity: O(n) where n is the size of text string
# Space Complexity: O(k) where k is the size of search string
# 

def _LPSArray(word):
    """
    Build the longest prefix suffix table.
    `delta += i+1` makes it O(n) time complexity.

    e.g. word = 'abababcabc'
        1) delta = 1
            a b a b a b c a b c
              a b a b a b c a b c
              X
           The first character doesn't match, word[i+delta] != word[i] when i == 0
           Increment `delta` by 1

        2) delta = 2
            a b a b a b c a b c
                a b a b a b c a b c
                m m m m X
           The first 4 characters match, word[i+delta] == word[i] holds for i belongs to {0,1,2,3}
           Then update lps to [0, 0, 1, 2, 3, 4, ...]
           When these 4 characters is matched, no need to recheck it, increment `delta` by (i+1) where i == 3

        3) delta = 6, there is no match, increment `delta` by 1

        4) delta = 7
            a b a b a b c a b c
                          a b a b a b c a b c
                          m m X
           The first 2 characteres match, word[i+delta] == word[i] holds for i belongs to {0,1}
           Then update lps to [0, 0, 1, 2, 3, 4, 0, 1, 2, 0]            
    """
    lps = [0] * len(word)
    wordIdx = 0
    delta = 1
    while delta < len(word):
        while delta < len(word) and word[delta] == word[wordIdx]:
            lps[delta] = wordIdx + 1
            wordIdx += 1
            delta += 1
        if wordIdx != 0:
            wordIdx = lps[wordIdx-1]
        else:
            delta += 1
    return lps


def kmp_strstr(haystack, needle):
    """
    Calculate the prefix suffix table first, which stores the information
    of previous mathing.

    e.g. haystack = 'abababcabababcabcdeab', needle = 'abababcabcd', lps = [0,0,1,2,3,4,0,1,2,0,0]
        1)  Start with `i_haystack = 0` and `i_needle = 0`,
            The first 9 characters match.
                a b a b a b c a b a b a b c a b c d e a b
                a b a b a b c a b c d
                m m m m m m m m m X
            Since `i_needle` != 0, update `i_needle` to `lps[i_needle-1]`, that is lps[8] = 2

        2)  Now, `i_haystack = 9`, `i_needle = 2`
            All characters match.
                a b a b a b c a b a b a b c a b c d e a b
                              a b a b a b c a b c d
                              m m s m m m m m m m m
            Add `i_haystack = 7` to ans, and reset `i_needle` to 0

        3)  Now, `i_haystack = 9`, `i_needle = 0`
            No character match.
                a b a b a b c a b a b a b c a b c d e a b
                                                    a b a b a b c a b c d
                                                    X
            Since `i_needle = 0`, increment `i_haystack` by 1

        4)  Now, Now, `i_haystack = 10`, `i_needle = 0`
            First 2 characters match.
                a b a b a b c a b a b a b c a b c d e a b
                                                      a b a b a b c a b c d
                                                      m m
            since `i_haystack` reaches `len(haystack)`, main loop ends, return `ans`
    """
    def computeLPSArray(word):
        # The explaination of this function is in _LPSArray()
        lps = [0] * len(word)
        wordIdx = 0
        delta = 1
        while delta < len(word):
            while delta < len(word) and word[delta] == word[wordIdx]:
                lps[delta] = wordIdx + 1
                wordIdx += 1
                delta += 1
            if wordIdx != 0:
                wordIdx = lps[wordIdx-1]
            else:
                delta += 1
        return lps

    # handle special cases
    if haystack == needle:
        return [0]
    elif not needle:
        return [0]
    elif not haystack:
        return []
    # init lps table
    lps = computeLPSArray(needle)
    ans = []
    # main loop
    i_haystack = 0
    i_needle = 0
    while i_haystack < len(haystack):
        if haystack[i_haystack] == needle[i_needle]:
            i_haystack += 1
            i_needle += 1
            # print i_needle, i_haystack
            if i_needle == len(needle):
                ans.append(i_haystack - i_needle)
                i_needle = lps[i_needle-1]
        elif i_needle != 0:
            i_needle = lps[i_needle-1]
        else:
            i_haystack += 1

    return ans


def normal_strstr(haystack, needle):
    """
    This is the naive solution to strstr()
    This algorithm is same as `haystack[i:i_haystack+len(needle)] == needle` solution
    The worst-case time Complexity is O(n*k)
    """
    # handle special cases
    if haystack == needle:
        return [0]
    elif not needle:
        return [0]
    elif not haystack:
        return []

    i_haystack = 0
    ans = []
    while i_haystack + len(needle) - 1 < len(haystack):
        i_needle = 0
        while haystack[i_haystack + i_needle] == needle[i_needle]:
            i_needle += 1
            if i_needle == len(needle):
                ans.append(i_haystack)
                break
        i_haystack += 1
    return ans

def strstr_test():
    test_text = \
"""
A string matching algorithm wants to find the starting index m in string S[] that matches the search word W[].
The most straightforward algorithm is to look for a character match at successive values of the index m, the position in the string being searched, i.e. S[m]. If the index m reaches the end of the string then there is no match, in which case the search is said to "fail". At each position m the algorithm first checks for equality of the first character in the word being searched, i.e. S[m] =? W[0]. If a match is found, the algorithm tests the other characters in the word being searched by checking successive values of the word position index, i. The algorithm retrieves the character W[i] in the word being searched and checks for equality of the expression S[m+i] =? W[i]. If all successive characters match in W at position m, then a match is found at that position in the search string.
Usually, the trial check will quickly reject the trial match. If the strings are uniformly distributed random letters, then the chance that characters match is 1 in 26. In most cases, the trial check will reject the match at the initial letter. The chance that the first two letters will match is 1 in 262 (1 in 676). So if the characters are random, then the expected complexity of searching string S[] of length k is on the order of k comparisons or O(k). The expected performance is very good. If S[] is 1 billion characters and W[] is 1000 characters, then the string search should complete after about one billion character comparisons.
That expected performance is not guaranteed. If the strings are not random, then checking a trial m may take many character comparisons. The worst case is if the two strings match in all but the last letter. Imagine that the string S[] consists of 1 billion characters that are all A, and that the word W[] is 999 A characters terminating in a final B character. The simple string matching algorithm will now examine 1000 characters at each trial position before rejecting the match and advancing the trial position. The simple string search example would now take about 1000 character comparisons times 1 billion positions for 1 trillion character comparisons. If the length of W[] is n, then the worst-case performance is O(kn).
The KMP algorithm has a better worst-case performance than the straightforward algorithm. KMP spends a little time precomputing a table (on the order of the size of W[], O(n)), and then it uses that table to do an efficient search of the string in O(k).
The difference is that KMP makes use of previous match information that the straightforward algorithm does not. In the example above, when KMP sees a trial match fail on the 1000th character (i = 999) because S[m+999] ≠ W[999], it will increment m by 1, but it will know that the first 998 characters at the new position already match. KMP matched 999 A characters before discovering a mismatch at the 1000th character (position 999). Advancing the trial match position m by one throws away the first A, so KMP knows there are 998 A characters that match W[] and does not retest them; that is, KMP sets i to 998. KMP maintains its knowledge in the precomputed table and two state variables. When KMP discovers a mismatch, the table determines how much KMP will increase (variable m) and where it will resume testing (variable i).
"""
    words = ['algorithm', 'equality', 'strings', 'difference', 'billion', 'random', 'letters', 'searched', 
             'The algorithm retrieves the character W[i] in the word being searched and checks for equality of the expression',
             '1000 characters, then the string search should complete', 'ormance is not guarant', 
             're all A, and that the word W[] is 999 A characters termin', 'dvancing the trial position. The simple string search example would now take ab',
             'mation that the straightforw', 'en it uses ', ' uniformly dist', 'arch is said to "fai']
    for word in words:
        assert normal_strstr(test_text, word) == kmp_strstr(test_text, word)


if __name__ == '__main__':
    test_strings = ["aaaaaaaaaaacccccccdddddc", "qwertyuiopasdfghjklxcvbnm", "abababcabababcabcdeab"
                    "jjjjjkkkkkjjjjjkkkkkkjkjjjkkl", "jkljkljkljkljkljkl", "ABABDABACDABABCABAB",
                    "", "", "emptytest",
                    "aaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaba"]
    words = ["ccccccc", "hjkl", "abababcabcd"
             "jjjjjjkkk", "ljk", "ABABCABAB",
             "", "emptytest", "",
             "aaaaaaa"]
    for i, text in enumerate(test_strings):
        assert kmp_strstr(text, words[i]) == normal_strstr(text, words[i])
    # print _LPSArray("abababcabcd")
    # print _LPSArray("aaaacaa")
    # print _LPSArray("aaaaaaaaaa")
    # print kmp_strstr("aaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaa","aaaaaaa")
    # print normal_strstr("aaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaa","aaaaaaa")
    strstr_test()
    # print _LPSArray("ababcaabc")
    # print kmp_strstr("ababcaababcaabc","ababcaabc")