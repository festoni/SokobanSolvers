#!/usr/bin/env python3
from time import time
from heapq import heappop, heappush
from read import read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan

def b_bound0(start, goals, walls, depth,heuristic,cornered=True, verbose=False):
    frontier = []
    frontier.append([start])

    while frontier:
        path = frontier.pop()
        last_matrix = path[-1]
        if is_goal(last_matrix, goals):
            if verbose:
                for matrices in path:
                    for line in matrices:
                        print(line)
                    print()
            print("length\t:", len(path)-1)
            return path
        for next_matrix, _ in neighbors(last_matrix):
            next_cost = heuristic(next_matrix, goals, corn=cornered)
            if next_matrix in path:
                continue
            new_path = path + [next_matrix]
            frontier.append(new_path)
    return None

def b_bound(start, goals, walls, depth,heuristic, cornered=True, verbose=False):

    start_perm = to_perm(start)
    max_pot, length, type_count = get_info(start_perm)
    start_int = rank(start_perm, max_pot, length, type_count)

    frontier = []
    frontier.append([start_int])

    is_visited = [False for i in range(max_pot)]    #initialize visited array
    is_visited[start_int] = True                    #mark start as visited

    while frontier:
        path = frontier.pop()
        last_int = path[-1]

        last_permut = unrank(last_int, max_pot, length, type_count)
        last_matrix = to_matrix(last_permut, walls)

        if is_goal(last_matrix, goals):
            if verbose:
                print(path)
            # print("length\t:", len(path)-1)
            depth = len(path)-1
            soln = path[:]
            # return path
        if len(path)-1 >= depth:
            continue
        for next_matrix, _ in neighbors(last_matrix):

            next_cost = heuristic(next_matrix, goals, corn=cornered)

            temp_perm = to_perm(next_matrix)
            int_next = rank(temp_perm, max_pot, length, type_count)

            if last_int == 3080:
                print(int_next)

            if is_visited[int_next]:
                continue

            new_path = path + [int_next]
            is_visited[int_next] = True
            frontier.append(new_path)
    print(len(soln))
    return None

def main():
    start_time = time()

    test, goals, walls, _, _ = read()
    b_bound0(test, goals, walls, 40, manhattan) #without pruning
    # b_bound(test, goals, walls, 40, manhattan, verbose=True) #with pruning

    print("--- %s seconds ---" % (time() - start_time))

if __name__ == "__main__":
    main()
