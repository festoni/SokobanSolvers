#!/usr/env/bin python3
from time import time
from heapq import heappush, heappop
from read import read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan

'''
>>Best First Search without pruning<<
Input: start matrix, goals matrix, walls matrix, heuristic function, boolean
whether to use corner checking, and verbose boolean whether to print solution
path
Output: Solution path, otherwise None
'''
def best_fs(start, goals, walls, heuristic, cornered=True, verbose=False):
    #frontier will look like [f(path), cost(path), [path], ...]
    frontier = []                               #initialize frontier
    heappush(frontier, (0, [start]))            #push tuple (0, start_matrix)
    while frontier:
        path_tup = heappop(frontier)            #take first tuple in frontier
        last_vertex = path_tup[1][-1]           #set equal to matrix in tuple
        if is_goal(last_vertex, goals):         #if boxes match goals, return
            if verbose:
                print(path_tup[1])
            print("length\t:", len(path_tup[1])-1)      #print soln length
            return path_tup
        for next_matrix, _ in neighbors(last_vertex):   #for each neighbor

            #calculate future cost
            next_cost = heuristic(next_matrix, goals, corn=cornered)
            if next_matrix in path_tup[1]:              #don't run into a cycle
                continue
            new_tup = (next_cost, path_tup[1] + [next_matrix])
            heappush(frontier, new_tup)       #prioritize by future cost
    return None

'''
>>Best First Search with pruning<<
Input: start matrix, goals matrix, walls matrix, heuristic function, boolean
whether to use corner checking, and verbose boolean whether to print solution
path
Output: Solution path, otherwise None
'''
def best_fs2(start, goals, walls, heuristic, cornered=True, verbose=False):

    start_perm = to_perm(start)      #find permut of start matrix
    max_pot, length, type_count = get_info(start_perm) #get level info

    start_int = rank(start_perm, max_pot, length, type_count)   #get rank index

    frontier = []                                   #initialize frontier
    heappush(frontier, (0,[start_int]))             #add (0, int) tuple

    is_visited = [False for i in range(max_pot)]    #initialize visited array
    is_visited[start_int] = True                    #mark start as visited

    while frontier:
        path_tup = heappop(frontier)        #take first path tuple from frontier
        last_vertex = path_tup[1][-1]       #take last element of path in tuple

        #unrank to multiset, and convert to matrix to check for goal and neighbs
        last_permut = unrank(last_vertex, max_pot, length, type_count)
        last_matrix = to_matrix(last_permut, walls)

        if is_goal(last_matrix, goals):     #if boxes match goals, return soln
            if verbose:                     #if asked, print solution path
                print(path_tup[1])
            print("length\t:", len(path_tup[1])-1)      #print length of soln
            return path_tup
        for next_matrix, _ in neighbors(last_matrix):   #for each neighbor

            #calculate future cost
            next_cost = heuristic(next_matrix, goals, corn=True)

            #convert from matrix to permutation, then to index
            temp_perm = to_perm(next_matrix)            #conv to permutation
            int_next = rank(temp_perm, max_pot, length, type_count) #get index

            if is_visited[int_next]:                #if already visited skip
                continue

            new_tup = (next_cost, path_tup[1] + [int_next])
            is_visited[int_next] = True
            heappush(frontier, new_tup)
    return None


def main():
    start_time = time()

    test, goals, walls, _, _ = read()
    # best_fs(test, goals, walls, manhattan, cornered=False)      #no pruning
    best_fs2(test, goals, walls, boxes)     #with pruning

    print("--- %s seconds ---" % (time() - start_time))

if __name__ == "__main__":
    main()
