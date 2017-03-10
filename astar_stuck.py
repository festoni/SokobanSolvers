#!/usr/bin/env python3
from time import time
from heapq import heappop, heappush
from read import read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan
from refinements import is_stuck
from math import inf


'''
>>A* search without pruning and with is_stuck check<<
Input: start matrix, goals matrix, walls matrix, heuristic function, list of
number of boxes in each border [top, left, bottom, right], list of number of
goals in each border, and verbose boolean whether to print solution path
Output: Solution path, otherwise None
The way is_stuck works is, the lists of goals and boxes in each border are
taken from the read function, and for every neighbor, if a box is pushed into
one of the borders then is_stuck updates the boxes in border list for that
neighbor. It then check if the number of boxes in border passes the number of
goals in that same border, and returns True, which is followed by assigning
infinity as the heuristic to that state.
'''
def Astar_stuck(start, goals, walls, heuristic, box_ls, goal_ls, verbose=False):
    frontier = []
    heappush(frontier, (0, 0,[start], box_ls))

    while frontier:
        path_tup = heappop(frontier)
        last_matrix = path_tup[2][-1]

        if is_goal(last_matrix, goals):
            if verbose:
                for matrices in path_tup[2]:
                    for line in matrices:
                        print(line)
                    print()
            print("cost\t:", path_tup[1])
            print("length\t:", len(path_tup[2])-1)
            return path_tup[2]
        for next_tup in neighbors(last_matrix, with_cost=True):
            ls = path_tup[3]
            check, ls = is_stuck(goal_ls, ls[:], next_tup[-1])
            if check:                       #if in a stuck state
                future_cost = inf
            else:                           #if not in a stuck state
                future_cost = heuristic(next_tup[1], goals, corn=False)

            if next_tup[1] in path_tup[2]:
                continue
            new_cost = path_tup[1] + next_tup[0]
            combined_cost = new_cost + future_cost
            new_tup = (combined_cost, new_cost, path_tup[2] + [next_tup[1]], ls)
            heappush(frontier, new_tup)
    return None

'''
>>A* search with pruning and with is_stuck check<<
Input: start matrix, goals matrix, walls matrix, heuristic function, list of
number of boxes in each border [top, left, bottom, right], list of number of
goals in each border, and verbose boolean whether to print solution path
Output: Solution path, otherwise None
The way is_stuck works is, the lists of goals and boxes in each border are
taken from the read function, and for every neighbor, if a box is pushed into
one of the borders then is_stuck updates the boxes in border list for that
neighbor. It then check if the number of boxes in border passes the number of
goals in that same border, and returns True, which is followed by assigning
infinity as the heuristic to that state.
'''
def Astar_stuck2(start, goals, walls, heuristic, box_ls, goal_ls, verbose=False):

    start_perm = to_perm(start)                      #find perm of start matrix
    max_pot, length, type_count = get_info(start_perm)  #get level info

    start_int = rank(start_perm, max_pot, length, type_count)   #get rank index

    #frontier will look like [f(path), cost(path), [path], [# boxes in borders]]
    frontier = []                                   #initiliaze frontier
    heappush(frontier, (0, 0,[start_int], box_ls))  #add (0, cost, index) tuple

    is_visited = [False for i in range(max_pot)]    #initiliaze visited array
    is_visited[start_int] = True                    #mark start as visited

    while frontier:
        path_tup = heappop(frontier)                #take first path tuple
        last_vertex = path_tup[2][-1]               #take last element of path

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

            ls = path_tup[3]                #list of number of boxes in border
            check, ls = is_stuck(goal_ls, ls[:], next_tup[-1])
            if check:                       #if in a stuck state
                future_cost = inf
            else:                           #if not in a stuck state
                future_cost = heuristic(next_tup[1], goals, corn=False)

            #convert from matrix to permutation, then to index
            temp_perm = to_perm(next_tup[1])
            int_next = rank(temp_perm, max_pot, length, type_count)

            if is_visited[int_next]:            #if already visited skip
                continue

            new_cost = path_tup[1] + next_tup[0]    #add cost of new vertex
            combined_cost = new_cost + future_cost   #calculate f()
            new_tup = (combined_cost, new_cost, path_tup[2] + [int_next], ls)
            is_visited[int_next] = True                 #set new int to visited
            heappush(frontier, new_tup)                 #prioritize by f()
    return None


def main():
    start_time = time()

    test, goals, walls, ls1, ls2  = read()
    # Astar_stuck(test, goals, walls, manhattan, ls1, ls2)       #without pruning
    Astar_stuck2(test, goals, walls, manhattan, ls1, ls2)       #with pruning

    print("--- %s seconds ---" % (time() - start_time))

if __name__ == "__main__":
    main()
