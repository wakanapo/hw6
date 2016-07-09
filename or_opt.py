import sys
import math

from common import print_solution, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def or_opt(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    path = [i for i in range(N)]
    while True:
        count = 0
        for i in range(N):
            # i 番目の都市を (j) - (j1) の経路に挿入する
            i0 = i - 1
            i1 = i + 1
            if i0 < 0: i0 = N - 1
            if i1 == N: i1 = 0
            for j in range(N):
                j1 = j + 1
                if j1 == N: j1 = 0
                if j != i and j1 != i:
                    l1 = dist[path[i0]][path[i]]  # i0 - i - i1
                    l2 = dist[path[i]][path[i1]]
                    l3 = dist[path[j]][path[j1]]  # j - j1
                    l4 = dist[path[i0]][path[i1]] # i0 - i1
                    l5 = dist[path[j]][path[i]]   # j - i - j1
                    l6 = dist[path[i]][path[j1]] 
                    if l1 + l2 + l3 > l4 + l5 + l6:
                        # つなぎかえる
                        p = path[i]
                        path[i:i + 1] = []
                        if i < j:
                            path[j:j] = [p]
                        else:
                            path[j1:j1] = [p]
                        count += 1
        if count == 0: break
    return path

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = or_opt(read_input(sys.argv[1]))
    print_solution(solution)
