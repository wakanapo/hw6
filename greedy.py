import sys
import math

from common import print_solution, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def greedy(cities):
    N = len(cities)
    
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    path = [i for i in range(N)]
    for i in range(N - 1):
        min_len = 1000000
        min_pos = 0
        for j in range(i + 1, N):
            l = dist[path[i]][path[j]]
            if l < min_len:
                min_len = l
                min_pos = j
        path[i + 1], path[min_pos] = path[min_pos], path[i + 1]
    return path

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = greedy(read_input(sys.argv[1]))
    print_solution(solution)
