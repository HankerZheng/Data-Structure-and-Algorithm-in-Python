# Ref: http://www.geeksforgeeks.org/greedy-algorithms-set-6-dijkstras-shortest-path-algorithm/
# Algorithm
# 1) Create a set sptSet (shortest path tree set) that keeps track of vertices
#    included in shortest path tree, i.e., whose minimum distance from source is
#    calculated and finalized. Initially, this set is empty.
# 2) Assign a distance value to all vertices in the input graph. Initialize all
#    distance values as INFINITE. Assign distance value as 0 for the source vertex
#    so that it is picked first.
# 3) While sptSet doesn't include all vertices
#   a) Pick a vertex u which is not there in sptSet and has minimum distance value.
#   b) Include u to sptSet.
#   c) Update distance value of all adjacent vertices of u. To update the distance
#      values, iterate through all adjacent vertices. For every adjacent vertex v,
#      if sum of distance value of u (from source) and weight of edge u-v, is less
#      than the distance value of v, then update the distance value of v.

import heapq
class Graph(object):
    def __init__(self, vertexNum):
        self.vertices = vertexNum
        self.edges = set()
        self.graphMap = {nodeName: set() for nodeName in xrange(self.vertices)}
    def addEdge(self, src, dest, cost):
        if src < self.vertices and dest < self.vertices:
            self.edges.add((src, dest))
            self.graphMap[src].add((dest, cost))
            self.graphMap[dest].add((src, cost))
            return
        raise ValueError("dest or src is out of range!!")
    def getNeighbors(self, node):
        return self.graphMap[node]
    def __str__(self):
        graph = defaultdict(set)
        for src, dest in self.edges:
            graph[src].add(dest)
            graph[dest] = graph.get(dest, set())
        return "%s" % graph

def dijkstra(graph, src):
    visited = {src}
    distance = [float("inf")] * graph.vertices
    distance[src] = 0
    heap = [(0, src)]
    while heap:
        dist, thisNode = heapq.heappop(heap)
        for neighbor, cost in graph.getNeighbors(thisNode):
            distance[neighbor] = min(distance[neighbor], distance[thisNode] + cost)
            if neighbor not in visited:
                heapq.heappush(heap, (distance[neighbor], neighbor))
        visited.add(thisNode)
    return distance

if __name__ == '__main__':
    graph = Graph(9)
    graph.addEdge(0, 1, 4)
    graph.addEdge(1, 2, 8)
    graph.addEdge(2, 3, 7)
    graph.addEdge(3, 4, 9)
    graph.addEdge(4, 5, 10)
    graph.addEdge(5, 6, 2)
    graph.addEdge(6, 7, 1)
    graph.addEdge(7, 0, 8)
    graph.addEdge(7, 8, 7)
    graph.addEdge(1, 7, 11)
    graph.addEdge(2, 8, 2)
    graph.addEdge(6, 8, 6)
    graph.addEdge(2, 5, 4)
    graph.addEdge(3, 5, 14)
    print dijkstra(graph, 0)
