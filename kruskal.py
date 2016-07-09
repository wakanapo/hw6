import sys
import math
import queue

from unionfind import *
from common import print_solution, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

# 辺の定義
class Edge:
    def __init__(self, p1, p2, weight):
        self.p1 = p1
        self.p2 = p2
        self.weight = weight

    def __cmp__(x, y):
        return x.weight - y.weight

# 辺のデータを作成
def make_edge(cities):
    size = len(cities)
    dist = [[0] * size for i in range(size)]
    for i in range(size):
        for j in range(size):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    edges = queue.Queue()
    for i in range(0, size - 1):
        for j in range(i + 1, size):
            e = Edge(i, j, dist[i][j])
            edges.put(e)
    return edges

# 辺から経路へ
def edge_to_path(edges, size):
    def search_edge(x):
        r = []
        for i in range(size):
            if edges[i].p1 == x:
                r.append(edges[i].p2)
            elif edges[i].p2 == x:
                r.append(edges[i].p1)
        return r

    path = [0] * size
    for i in range(size - 1):
        x, y = search_edge(path[i])
        if i == 0:
            path[i + 1] = x
            path[-1] = y
        elif path[i - 1] == x:
            path[i + 1] = y
        else:
            path[i + 1] = x
    return path

# 探索
def kruskal_greedy(cities):
    size = len(cities)
    edges = make_edge(cities)
    edge_count = [0] * size
    u = unionfind(size)
    i = 0
    select_edge = []
    while i < size:
        e = edges.get()
        if (edge_count[e.p1] < 2 and edge_count[e.p2] < 2
        and (u.find(e.p1) != u.find(e.p2) or i == size - 1)):
            u.unite(e.p1, e.p2)
            edge_count[e.p1] += 1
            edge_count[e.p2] += 1
            select_edge.append(e)
            i += 1
    return edge_to_path(select_edge, size)

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = kruskal_greedy(read_input(sys.argv[1]))
    print_solution(solution)

