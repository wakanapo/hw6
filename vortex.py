import sys
import math

from common import print_solution, read_input

def left_rightXY(city1, city2):
    if (city1[0] >=  city2[0]):
        return city1[0] - city2[0], city1[1] - city2[1]
    else:
        return city2[0] - city1[0], city2[1] - city1[1]
    
def below_aboveXY(city1, city2):
    if (city1[1] >=  city2[1]):
        return city1[0] - city2[0], city1[1] - city2[1]
    else:
        return city2[0] - city1[0], city2[1] - city1[1]

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def make_circle(cities, unvisited_cities):  
    N = len(cities)

    def get_corner(unvisited_cities):
        def get_left_below(i):
            return cities[i][0] + cities[i][1]
        left_below = min(unvisited_cities, key=get_left_below)
        def get_right_below(i):
            return cities[i][0] - cities[i][1]
        right_below = max(unvisited_cities, key=get_right_below)
        def get_left_above(i):
            return cities[i][0] - cities[i][1]
        left_above = min(unvisited_cities, key=get_left_above)
        def get_right_above(i):
            return cities[i][0] + cities[i][1]
        right_above = max(unvisited_cities, key=get_right_above)        
        return left_below, right_below, left_above, right_above

    def distance_to_next(i):
        if (i + 1 < len(cities)):
            return math.sqrt((cities[i][0] - cities[i+1][0]) ** 2
                             + (cities[i][1] - cities[i+1][1]) ** 2)
        else:
            return math.sqrt((cities[i][0] - cities[0][0]) ** 2
                             + (cities[i][1] - cities[0][1]) ** 2)
    left_b, right_b, left_a, right_a = get_corner(unvisited_cities)
    left_below = cities[left_b]
    right_below = cities[right_b]
    left_above = cities[left_a]
    right_above = cities[right_a]
    visit_cities = unvisited_cities.copy()
    route_below = []
    route_right = []
    route_above = []
    route_left = []
    x_rb_lb, y_rb_lb = left_rightXY(left_below, right_below)
    x_ra_rb, y_ra_rb = below_aboveXY(right_above, right_below)
    x_ra_la, y_ra_la = left_rightXY(left_above, right_above)
    x_la_lb, y_la_lb = below_aboveXY(left_below, left_above)
    for i in visit_cities:
        x = cities[i][0]
        y = cities[i][1]
        if (x_rb_lb * (y - left_below[1]) <= y_rb_lb * (x - left_below[1])):
            route_below.append(i)
            unvisited_cities.remove(i)
            continue
        if (x_ra_rb * (y - right_below[1]) <= y_ra_rb * (x - right_below[0])):
            route_right.append(i)
            unvisited_cities.remove(i)
            continue
        if (x_ra_la * (y - left_above[1]) >= y_ra_la * (x - left_above[1])):
            route_above.append(i)
            unvisited_cities.remove(i)
            continue
        if (x_la_lb * (y - left_below[1]) >= y_la_lb * (x - left_below[0])):
            route_left.append(i)
            unvisited_cities.remove(i)
            continue
        
    def xSort(city):
        return cities[city][0]
        
    def ySort(city):
        return cities[city][1]
        
    solution = sorted(route_below, key=xSort)
    solution.extend(sorted(route_right, key=ySort, reverse=False))
    solution.extend(sorted(route_above, key=xSort, reverse=True))
    solution.extend(sorted(route_left, key=ySort, reverse=True))
    separate_from = max(solution, key=distance_to_next)
    return solution, separate_from, unvisited_cities

def vortex(cities):
    N = len(cities)

    unvisited_cities = set(range(0, N))
    solution_first = []
    solution_end = []
    cnt = 0
    separate_before = 0
    
    def distance(i):
        return math.sqrt((cities[i][0] - cities[separate_before][0]) ** 2
                     + (cities[i][1] - cities[separate_before][1]) ** 2)

    while unvisited_cities:
        solution, separate_from, unvisited_cities = make_circle(cities, unvisited_cities)
        if (cnt % 2):
            solution.reverse()
        next = min(solution, key=distance)
        solution = solution[next:] + solution[:next]
        if (next > separate_from):
            separate_from += len(solution[:next])
        else:
            separate_from -= next
        solution_f = solution[:separate_from]
        solution_e = solution[separate_from:]
        solution_e.reverse()
        solution_first.extend(solution_f)
        solution_end.extend(solution_e)
        cnt += 1
        separate_before = separate_from
    solution_end.reverse()
    solution_first.extend(solution_end)
    return solution_first  

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution = vortex(read_input(sys.argv[1]))
    print_solution(solution)
            
