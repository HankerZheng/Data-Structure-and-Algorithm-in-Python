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
    lps = [0 for ch in word]
    delta = 1
    while delta < len(word):
        i = 0
        while i + delta < len(word) and word[i+delta] == word[i]:
            lps[delta+i] = i+1
            i += 1
        delta += i+1
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
        lps = [0 for ch in word]
        delta = 1
        while delta < len(word):
            i = 0
            while i + delta < len(word) and word[i+delta] == word[i]:
                lps[delta+i] = i+1
                i += 1
            delta += i+1
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
    print kmp_strstr("aaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaa","aaaaaaa")
    print normal_strstr("aaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaabaaaaaaa","aaaaaaa")
