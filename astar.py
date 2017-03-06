#!/usr/bin/env python3
from time import time
from heapq import heappop, heappush
from read import read
from rank_unrank import rank, unrank, to_perm, to_matrix, get_info
from mechanics import neighbors, is_goal
from heuristics import boxes, manhattan

#A* search without pruning
#takes in start matrix, goals matrix, walls matrix, heuristic function, and the
#verbose boolean wether to print solution path or not
#returns the solution path or None if no solution found
def Astar(start, goals, walls, heuristic, verbose=False):

    #frontier will look like [(f(path), [path]), (f(path), [path]), ...]
    frontier = []
    heappush(frontier, (0, [start]))    #heap prioritized by f()

    while frontier:
        path_tup = heappop(frontier)    #select first tuple from frontier

        # last_vertex is last elem in path from current path tuple
        last_vertex = path_tup[1][-1]
        if is_goal(last_vertex, goals):
            if verbose:                 #if asked by user, print solution path
                for matrices in path_tup[1]:
                    for line in matrices:
                        print(line)
                    print()
            print("cost\t:", path_tup[0])   #print cost for convinience
            print("length\t:", len(path_tup[1])) #print length for convinience
            return path_tup
        for next_tup in neighbors(last_vertex, with_cost=True): #for each neighb
            future_cost = heuristic(next_tup[1], goals) #calculate future cost
            if next_tup[1] in path_tup[1]:              #avoid cycles
                continue
            combined_cost = next_tup[0] + future_cost   #calculate f()
            new_tup = (path_tup[0] + combined_cost, path_tup[1] + [next_tup[1]])
            heappush(frontier, new_tup)                 #prioritize by f()
    return None


def main():
    start_time = time()

    test, goals, walls = read()
    Astar(test, goals, walls, manhattan)      #no pruning

    print("--- %s seconds ---" % (time() - start_time))

if __name__ == "__main__":
    main()
