class TrieNode(object):
    def __init__(self, char):
        self.val = char
        self.isWord = False
        self.diction = {}
    def __getitem__(self, key):
        return self.diction.get(key, None)
    def __setitem__(self, key, val):
        self.diction[key] = val
    def child_list(self):
        return self.diction.keys()

class TrieTree(object):
    def __init__(self):
        self.root = TrieNode('dummy')
    def insert(self, word):
        def insert_char(node, char, end):
            if node[char]:
                this_node = node[char]
            else:
                node[char] = TrieNode(char)
                this_node = node[char]
            if end:
                this_node.isWord = True
            return this_node
        this_node = self.root
        for i,ch in enumerate(word):
            this_node = insert_char(this_node, ch, i==(len(word)-1))
        
    def find_prefix(self, prefix):
        this_node = self.root
        for ch in prefix:
            this_node = this_node[ch]
            if this_node is None:
                return False
        return True

    def find_word(self, word):
        this_node = self.root
        for ch in word:
            this_node = this_node[ch]
            if this_node is None:
                return False
        return this_node.isWord

    def display_tree(self):
        this_node = self.root


def permutation(test, length):
    def helper(ans, index):
        if index == length:
            res.append(ans)
            return
        for ch in test:
            helper(ans+ch, index+1)
    res = []
    helper("", 0)
    return res

def my_test(dictionary, testchar, length):
    mytree = TrieTree()
    for word in dictionary:
        mytree.insert(word)
    for test in permutation(testchar, length):
        assert mytree.find_word(test) == (test in dictionary)
    # for test in permutation(testchar, length-1):
    #     print test, mytree.find_prefix(test)


if __name__ == '__main__':
    dictionary = ['qwre','qwrw','qqrq','eere','qqrw','eerw','wwrq','wwww','qweq']
    test_char = 'qwer'
    my_test(dictionary, test_char, 3)