# Bellman-Ford Algorithm - single source shortest paths algorithm
# step 1: init the cost of path as `init` and src to src dist as 0
# step 2: loop for N - 1 times, where N is the number of vertices
#             for each edge in the graph, update the shortest distance
# step 3: check for the negative weighted cycle in the graph



class GraphNode(object):
    def __init__(self, nodeName, distDict):
        self.nodeName = nodeName
        self.children = distDict

class Graph(object):
    def __init__(self, numNodes):
        self.vertices = numNodes
        self.edges = []

    def addEdge(self, src, dest, weight):
        if src >= self.vertices or dest >= self.vertices:
            raise ValueError("src or dest node doesn't exist")
        self.edges.append((src, dest, weight))


def bellmanFord_GraphVersion(graph, source):
    """
    :type graph: Graph
    :type source: str - the name of the source node
    :rtype: dict <nodeName, distance> - the distance from src to all other nodes 
    """
    numNodes = graph.vertices
    # step 1
    dist = [float("inf") for i in xrange(numNodes)]
    dist[source] = 0
    # step 2
    for i in xrange(numNodes-1):
        for src, dest, weight in graph.edges:
            dist[dest] = min(dist[dest], dist[src] + weight)
    # step 3
    for src, dest, weight in graph.edges:
        if dist[dest] != min(dist[dest], dist[src] + weight):
            raise ValueError("Negative Weighted Cycle detected!!")
    return dist



def bellmanFord_GraphNodeVersion(graph, source):
    """
    :type graph: list[GraphNode]
    :type source: str - the name of the source node
    :rtype: dict <nodeName, distance> - the distance from src to all other nodes 
    """
    def getEdge(graph):
        for node in graph:
            for dest, weight in node.children.items():
                yield node.nodeName, dest, weight

    numNodes = len(graph)
    dist = {node.nodeName: float("inf") for node in graph}
    dist[source] = 0
    # loop for N times
    for i in xrange(numNodes):
        for src, dest, weight in getEdge(graph):
            dist[dest] = min(dist[dest], dist[src] + weight)

    for src, dest, weight in getEdge(graph):
        if dist[dest] != min(dist[dest], dist[src] + weight):
            return dict()
    return dist

if __name__ == '__main__':
    # the graphNode version of Bellman-Ford Algorithm
    nodeA = GraphNode("A", {"B": 1})
    nodeB = GraphNode("B", {"C": 5})
    nodeC = GraphNode("C", {"D": 7})
    nodeD = GraphNode("D", {"E": 3})
    nodeE = GraphNode("E", {"C": 6})
    print bellmanFord_GraphNodeVersion([nodeE, nodeC,nodeA, nodeD,nodeB], "A")
    # the Graph version of Bellman-Ford Algorithm
    graph = Graph(5)
    graph.addEdge(3,1,-2)
    graph.addEdge(2,3,5)
    graph.addEdge(4,1,2)
    graph.addEdge(2,4,1)
    graph.addEdge(3,0,2)
    graph.addEdge(1,0,3)
    graph.addEdge(0,1,-1)
    graph.addEdge(4,3,2)
    graph.addEdge(1,2,3)
    print bellmanFord_GraphVersion(graph, 0)
