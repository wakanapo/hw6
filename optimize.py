import sys
import math

from common import print_solution, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def distance_table(cities):
    size = len(cities)
    dist = [[0] * size for i in range(size)]
    for i in range(size):
        for j in range(size):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist
            
def opt_2(size, path, dist):
    total = 0
    while True:
        count = 0
        for i in range(size - 2):
            i1 = i + 1
            for j in range(i + 2, size):
                if j == size - 1:
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
        total += count
        if count == 0: break
    return path, total

def or_opt(size, path, dist):
    total = 0
    while True:
        count = 0
        for i in range(size):
            # i 番目の都市を (j) - (j1) の経路に挿入する
            i0 = i - 1
            i1 = i + 1
            if i0 < 0: i0 = size - 1
            if i1 == size: i1 = 0
            for j in range(size):
                j1 = j + 1
                if j1 == size: j1 = 0
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
        total += count
        if count == 0: break
    return path, total


def optimize(cities):
    N = len(cities)
    path = [i for i in range(N)]
    dist = distance_table(cities)
    while True:
        path, _ = opt_2(N, path, dist)
        path, flag = or_opt(N, path, dist)
        if flag == 0: return path

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = optimize(read_input(sys.argv[1]))
    print_solution(solution)
