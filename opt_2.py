import sys
import math

from common import print_solution, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def opt_2(cities):
    N = len(cities)
    
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    path = [i for i in range(N)]
    while True:
        count = 0
        for i in range(N - 2):
            i1 = i + 1
            for j in range(i + 2, N):
                if j == N - 1:
                    j1 = 0
                else:
                    j1 = j + 1
                if i != 0 or j1 != 0:
                    l1 = dist[path[i]][path[i1]]
                    l2 = dist[path[j]][path[j1]]
                    l3 = dist[path[i]][path[j]]
                    l4 = dist[path[i1]][path[j1]]
                    if l1 + l2 > l3 + l4:
                        # つなぎかえる
                        new_path = path[i1:j+1]
                        path[i1:j+1] = new_path[::-1]
                        count += 1
        if count == 0: break
    return path

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = opt_2(read_input(sys.argv[1]))
    print_solution(solution)
