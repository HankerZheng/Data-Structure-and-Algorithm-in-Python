# Given two sequences, find the length of longest subsequence present in both of them.
# A subsequence is a sequence that appears in the same relative order, but not necessarily contiguous.
# For example, "abc", "abg", "bdf", "aeg", "acefg", .. etc are subsequences of "abcdefg". So a string of length n has 2^n different possible subsequences.

class Solution(object):
    def longestCommonSubsequence(self, a, b):
        """
        :tpye a: string
        :type b: string
        :rtype: int
        """
        lenA = len(a)
        lenB = len(b)
        dp = [[0 for j in xrange(lenB + 1)] for i in xrange(lenA + 1)]

        for i, line in enumerate(dp):
            for j, _ in enumerate(line):
                if i == 0 or j == 0:
                    dp[i][j] = 0
                else:
                    dp[i][j] = max(dp[i-1][j-1] + (a[i-1] == b[j-1]), dp[i][j-1], dp[i-1][j])
        return dp[-1][-1]

if __name__ == '__main__':
    sol = Solution()
    print sol.longestCommonSubsequence("abb", "bbc")
    print sol.longestCommonSubsequence("ABCDGH", "AEDFHR")
    print sol.longestCommonSubsequence("AGGTAB", "GXTXAYB")