#!/usr/env/bin python3
import time, heapq
import rank_unrank, read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan


#BEST FIRST SEARCH without pruning
#takes in start matrix, goals matrix, walls matrix, heuristic function, and
#verbose boolean whether to print solution path or next_cost
#return the path to the solution if any exists, otherwise None
def best_fs(start, goals, walls, heuristic, verbose=False):
    frontier = []                               #initialize frontier
    heapq.heappush(frontier, (0, [start]))      #push tuple (0, start_matrix)
    while frontier:
        path_tup = heapq.heappop(frontier)      #take first tuple in frontier
        last_vertex = path_tup[1][-1]           #set equal to matrix in tuple
        if is_goal(last_vertex, goals):         #if boxes match goals, return
            if verbose:
                print(path_tup[1])
            print("length:\t", len(path_tup[1]))    #print soln length
            return path_tup
        for next_matrix in neighbors(last_vertex):  #for all neighbors of matrix
            next_cost = heuristic(next_matrix, goals)   #calculate future cost
            if next_matrix in path_tup[1]:          #don't run into a cycle
                continue
            new_tup = (next_cost, path_tup[1] + [next_matrix])
            heapq.heappush(frontier, new_tup)       #prioritize by future cost
    return None

#BEST FIRST SEARCH with pruning
#takes in start matrix, goals matrix, walls matrix, heuristic function, and
#verbose boolean whether to print solution path or next_cost
#return the path to the solution if any exists, otherwise None
def best_fs2(start, goals, walls, heuristic, verbose=False):

    #find permutation of start matrix and get information that is used in
    #ranking and unranking
    #max_pot is the total number of permutations for this multiset
    #length is the length of the multiset
    #type_count is a list of counts for each type in the sorted multiset
    start_perm = to_perm(start)      #find permut of start matrix
    max_pot, length, type_count = get_info(start_perm) #get level info

    #get the rank of the start matrix
    start_int = rank(start_perm, max_pot, length, type_count)

    frontier = []                                   #initialize frontier
    heapq.heappush(frontier, (0,[start_int]))       #add (0, int) tuple

    is_visited = [False for i in range(max_pot)]    #initialize visited array
    is_visited[start_int] = True                    #mark start as visited

    while frontier:
        path_tup = heapq.heappop(frontier)  #take first path tuple from frontier
        last_vertex = path_tup[1][-1]       #take last element of path in tuple

        #unrank to multiset, and convert to matrix to check for goal and neighbs
        last_permut = unrank(last_vertex, max_pot, length, type_count)
        last_matrix = to_matrix(last_permut, walls)

        if is_goal(last_matrix, goals):     #if boxes match goals, return soln
            if verbose:                     #if asked, print solution path
                print(path_tup[1])
            print("length:\t", len(path_tup[1]))    #print length of solution
            return path_tup
        for next_matrix in neighbors(last_matrix):  #for each neighbor
            next_cost = heuristic(next_matrix, goals)   #calculate future cost

            #convert from matrix to permutation, then to index
            temp_perm = to_perm(next_matrix)            #conv to permutation
            int_next = rank(temp_perm, max_pot, length, type_count) #get index

            if is_visited[int_next]:                #if already visited skip
                continue

            new_tup = (next_cost, path_tup[1] + [int_next])
            is_visited[int_next] = True
            heapq.heappush(frontier, new_tup)
    return None


def main():
    start_time = time.time()

    test, goals, walls = read.read()
    best_fs(test, goals, walls, manhattan)
    best_fs2(test, goals, walls, manhattan)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
