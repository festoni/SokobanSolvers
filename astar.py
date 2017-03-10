#!/usr/bin/env python3
from time import time
from heapq import heappop, heappush
from read import read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan

'''
>>A* search without pruning<<
Input: start matrix, goals matrix, walls matrix, heuristic function, boolean
whether to use corner checking, and verbose boolean whether to print solution
path
Output: Solution path, otherwise None
'''
def a_star(start, goals, walls, heuristic, cornered=True, verbose=False):
    #frontier will look like [f(path), cost(path), [path], ...]
    frontier = []
    heappush(frontier, (0, 0, [start]))     #heap prioritized by f()

    while frontier:
        path_tup = heappop(frontier)        #select first tuple from frontier

        # last_vertex is last elem in path from current path tuple
        last_vertex = path_tup[2][-1]
        if is_goal(last_vertex, goals):
            if verbose:                     #if requested, print solution path
                for matrices in path_tup[2]:
                    for line in matrices:
                        print(line)
                    print()
            print("cost\t:", path_tup[1])   #print cost for convinience
            print("length\t:", len(path_tup[2])-1) #print length for convinience
            return path_tup
        for next_tup in neighbors(last_vertex, with_cost=True): #for each neighb

            #calculate future cost
            future_cost = heuristic(next_tup[1], goals, corn=cornered)
            if next_tup[1] in path_tup[2]:              #avoid cycles
                continue
            new_cost = path_tup[1] + next_tup[0]        #add cost of new node
            combined_cost = next_tup[0] + future_cost   #calculate f()
            new_tup = (combined_cost, new_cost, path_tup[2] + [next_tup[1]])
            heappush(frontier, new_tup)                 #prioritize by f()
    return None

'''
>>A* search with pruning<<
Input: start matrix, goals matrix, walls matrix, heuristic function, boolean
whether to use corner checking, and verbose boolean whether to print solution
path
Output: Solution path, otherwise None
'''
def a_star2(start, goals, walls, heuristic, cornered=True, verbose=False):

    start_perm = to_perm(start)                 #find perm of start matrix
    max_pot, length, type_count = get_info(start_perm)  #get level info

    start_int = rank(start_perm, max_pot, length, type_count)   #get rank index

    frontier = []                               #initiliaze frontier
    heappush(frontier, (0, 0,[start_int]))      #add (0, cost, index) tuple

    is_visited = [False for i in range(max_pot)]    #initiliaze visited array
    is_visited[start_int] = True                    #mark start as visited

    while frontier:
        path_tup = heappop(frontier)            #take first path tuple
        last_vertex = path_tup[2][-1]           #take last element of path

        #unrank to multiset, and convert to matrix to check for goal and neighbs
        last_permut = unrank(last_vertex, max_pot, length, type_count)
        last_matrix = to_matrix(last_permut, walls)

        if is_goal(last_matrix, goals):         #if boxes match goals, finish
            if verbose:                         #if asked print solution path
                print(path_tup[2])
            print("cost\t:", path_tup[1])       #print cost for convinience
            print("length\t:", len(path_tup[2])-1)    #print length for conv
            return path_tup

        for next_tup in neighbors(last_matrix, with_cost=True):

            #calculate future cost, and use corn(ernered refinement)
            future_cost = heuristic(next_tup[1], goals, corn=cornered)

            #convert from matrix to permutation, then to index
            temp_perm = to_perm(next_tup[1])
            int_next = rank(temp_perm, max_pot, length, type_count)

            if is_visited[int_next]:            #if already visited skip
                continue

            new_cost = path_tup[1] + next_tup[0]    #add cost of new vertex
            combined_cost = new_cost + future_cost   #calculate f()
            new_tup = (combined_cost, new_cost, path_tup[2] + [int_next])
            is_visited[int_next] = True                 #set new int to visited
            heappush(frontier, new_tup)                 #prioritize by f()
    return None


def main():
    start_time = time()

    test, goals, walls, _, _  = read()
    # a_star(test, goals, walls, manhattan)        #no pruning
    a_star2(test, goals, walls, manhattan)       #with pruning


    print("--- %s seconds ---" % (time() - start_time))

if __name__ == "__main__":
    main()
