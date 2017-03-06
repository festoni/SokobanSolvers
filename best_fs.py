#!/usr/env/bin python3
import time, heapq
import rank_unrank, read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan

def best_fs(start, goals, walls, heuristic, verbose=False):

    start_perm = to_perm(start)      #find permut of start matrix
    max_pot, length, type_count = get_info(start_perm) #get level info

    start_int = rank(start_perm, max_pot, length, type_count)


    frontier = []
    heapq.heappush(frontier, (0,[start_int]))

    is_visited = [False for i in range(max_pot)]
    is_visited[start_int] = True

    while frontier:
        path_tup = heapq.heappop(frontier)  #take first path tuple from frontier
        last_vertex = path_tup[1][-1]       #take last element of path in tuple

        last_permut = unrank(last_vertex, max_pot, length, type_count)
        last_matrix = to_matrix(last_permut, walls)

        if is_goal(last_matrix, goals):
            if verbose:
                print(path_tup[1])
            print("length:\t", len(path_tup[1]))
            return path_tup
        for next_matrix in neighbors(last_matrix):
            next_cost = heuristic(next_matrix, goals)       #get future cost
            temp_perm = to_perm(next_matrix)                #conv to permutation
            int_next = rank(temp_perm, max_pot, length, type_count) #get index

            if is_visited[int_next]:                    #if already visited skip
                continue

            new_tup = (next_cost, path_tup[1] + [int_next])
            is_visited[int_next] = True
            heapq.heappush(frontier, new_tup)
    return None

def main():
    start_time = time.time()

    test, goals, walls = read.read()
    for i in test:
        print(i)
    for i in goals:
        print(i)
    # test2 = to_perm(test)
    # max_pot, length, type_count = get_info(test2) #get level info
    # print(type_count)
    best_fs(test, goals, walls, manhattan, True)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
