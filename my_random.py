import math
import sys

from random import random, shuffle
from common import print_solution, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def random_solve(cities):
    l = [x for x in range(len(cities))]
    shuffle(l)
    return l


if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = solve(read_input(sys.argv[1]))
    print_solution(solution)
