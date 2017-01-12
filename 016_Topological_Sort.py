from collections import defaultdict
import random, time


class Graph(object):
    def __init__(self, vertexNum):
        self.vertices = vertexNum
        self.edges = set()
    def addEdge(self, src, dest):
        if src < self.vertices and dest < self.vertices:
            self.edges.add((src, dest))
            return
        raise ValueError("dest or src is out of range!!")

    def __str__(self):
        graph = defaultdict(set)
        for src, dest in self.edges:
            graph[src].add(dest)
            graph[dest] = graph.get(dest, set())
        return "%s" % graph


def topologicalSort_Naive(graph):
    """
    Naive Solution to sort the graph topologically.
    Time Complexity: O(E + V^2)
    """
    def getNoIncomming(graphMap):
        ans = []      
        for node, edgeSet in graphMap.items():
            if not edgeSet:
                ans.append(node)
                graphMap.pop(node)
        return ans

    # O(E) time to construct the graphMap
    graphMap = {i: set() for i in xrange(graph.vertices)}
    for src, dest in graph.edges:
        graphMap[dest].add(src)
    # O(V^2) time to form the topological sort
    ans = []
    while graphMap:
        # find the node with no outcomming edges, this operation take O(V) time
        noIncomming = getNoIncomming(graphMap)
        # add the node with no outcomming edges to the right of Ans
        if not noIncomming:
            raise ValueError("Cycle Detected in the Graph!!!")
        ans += noIncomming
        # update the graphMap, kick out all the nodes already in the ans
        # this operation takes O(V) time
        for poppedNode in noIncomming:
            for node in graphMap:
                if poppedNode in graphMap[node]:
                    graphMap[node].remove(poppedNode)
    return ans


def topologicalSort_Better(graph):
    """
    Topological Srot Algorithm according to the pseudo-code in DSAA
    Time Complexity: O(V + E)
    """
    # O(E) time to construct the indegree and adjacent
    indegree = [0] * graph.vertices
    adjacent = [set()] * graph.vertices
    for src, dest in graph.edges:
        indegree[dest] += 1
        adjacent[src].add(dest)
    ans = []
    # O(V) time to find the zeroIncomming nodes
    zeroIncomming = [node for node, num in enumerate(indegree) if num == 0]
    # O(E) time in total to form the topological sort
    while zeroIncomming:
        thisNode = zeroIncomming.pop(0)
        ans.append(thisNode)
        # for each node currently has no incomming nodes
        # decrease the in-degree of all their children
        # the new zeroIncomming node could only from their chilren
        for decremntNode in adjacent[thisNode]:
            # for each child of current zeroIncomming nodes
            indegree[decremntNode] -= 1
            if indegree[decremntNode] == 0:
                zeroIncomming.append(decremntNode)
    return ans
    


def randomCreateDAG(nodeNum, edgeNum):
    thisGraph = Graph(nodeNum)
    for _ in xrange(edgeNum):
        src = random.randrange(0, nodeNum)
        while src == nodeNum - 1:
            src = random.randrange(0, nodeNum)
        dest = random.randrange(src+1, nodeNum)
        thisGraph.addEdge(src, dest)
    return thisGraph



if __name__ == '__main__':
    # greate the test graph
    # graph1 = Graph(5)
    # graph1.addEdge(0, 1)
    # graph1.addEdge(0, 3)
    # graph1.addEdge(0, 4)
    # graph1.addEdge(0, 2)
    # graph1.addEdge(1, 2)
    # graph1.addEdge(1, 4)
    # graph1.addEdge(1, 3)
    # graph1.addEdge(3, 4)
    # print topologicalSort_Naive(graph1)
    # print topologicalSort_Better(graph1)
    # random test cases
    for i in xrange(1):
        testGraph = randomCreateDAG(10, 50)
        topologicalSort_Naive(testGraph)
        topologicalSort_Better(testGraph)
        # if naive != better:
        #     print naive
        #     print better
        #     raise ValueError("different Topological Sort Result!!")