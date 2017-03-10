#!/usr/bin/env python3
from time import time
from heapq import heappop, heappush
from read import read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan
from math import inf

'''
>>Branch and bound<<
Input: start matrix, goals matrix, walls matrix, heuristic, [bound], [cornered],
[verbose]
Output: solution path
Branch and bound can be used to find the minmal cost solution, but in the case
of Sokoban it seems better to return the shortest path.
'''
def b_bound(start, goals, walls, heuristic,bnd=inf,cornered=True, verbose=False):

    soln = []
    bound = bnd
    cnt = 0

    frontier = []
    frontier.append([start])

    while frontier:
        path = frontier.pop()
        last_matrix = path[-1]
        if is_goal(last_matrix, goals):
            cnt = 1
            if verbose:
                for matrices in path:
                    for line in matrices:
                        print(line)
                    print()
            bound = len(path)-1
            soln = path[:]
        if len(path)-1 >= bound:
            continue
        for next_matrix, _ in neighbors(last_matrix):
            if next_matrix in path:
                continue
            new_path = path + [next_matrix]
            frontier.append(new_path)
    print("length\t:", len(soln)-1)
    return soln

'''
>>Branch and bound (rank/unrank, no pruning)<<
Input: start matrix, goals matrix, walls matrix, heuristic, [bound], [cornered],
[verbose]
Output: solution path
Branch and bound can be used to find the minmal cost solution, but in the case
of Sokoban it seems better to return the shortest path.
'''
def b_bound2(start, goals, walls, heuristic, bnd=inf, cornered=True, verbose=False):

    soln = []
    bound = bnd
    cnt = 0

    start_perm = to_perm(start)
    max_pot, length, type_count = get_info(start_perm)
    start_int = rank(start_perm, max_pot, length, type_count)

    frontier = []
    frontier.append([start_int])

    while frontier:

        path = frontier.pop()
        last_int = path[-1]

        last_permut = unrank(last_int, max_pot, length, type_count)
        last_matrix = to_matrix(last_permut, walls)

        if is_goal(last_matrix, goals):
            if verbose:
                print(path)
            bound = len(path)-1
            soln = path[:]
        if len(path)-1 >= bound:
            continue
        for next_matrix, _ in neighbors(last_matrix):

            temp_perm = to_perm(next_matrix)
            int_next = rank(temp_perm, max_pot, length, type_count)

            if int_next in path:
                continue

            new_path = path + [int_next]
            frontier.append(new_path)
    print("length", len(soln)-1)
    return soln

def main():
    start_time = time()

    test, goals, walls, _, _ = read()
    b_bound(test, goals, walls, manhattan) #without pruning
    # b_bound2(test, goals, walls, manhattan) #with pruning

    print("--- %s seconds ---" % (time() - start_time))

if __name__ == "__main__":
    main()
